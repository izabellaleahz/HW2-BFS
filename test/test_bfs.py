# write tests for bfs
import pytest
from search import graph
from search.graph import NodeNotFoundError, EmptyGraphError
import os


def test_bfs_traversal():
    """
    TODO: Write your unit test for a breadth-first
    traversal here. Create an instance of your Graph class 
    using the 'tiny_network.adjlist' file and assert 
    that all nodes are being traversed (ie. returns 
    the right number of nodes, in the right order, etc.)
    """
    import tempfile
    # Create a simple graph 
    #     A
    #    / \
    #   B   C
    #   |
    #   D
    # BFS from A should be: A, B, C, D (B and C at distance 1, D at distance 2)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('A;B;C\n')  # A -> B, A -> C
        f.write('B;D\n')     # B -> D
        f.write('C\n')
        f.write('D\n')
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        result = g.bfs('A')
        
        # Verify exact BFS order
        assert result[0] == 'A', "Should start with A"
        assert set(result[1:3]) == {'B', 'C'}, "B and C should be visited before D (same level)"
        assert result[3] == 'D', "D should be visited last (level 2)"
        assert len(result) == 4, "Should visit exactly 4 nodes"
        assert len(set(result)) == len(result), "No duplicates"
    finally:
        os.unlink(temp_file)

def test_bfs():
    """
    TODO: Write your unit test for your breadth-first 
    search here. You should generate an instance of a Graph
    class using the 'citation_network.adjlist' file 
    and assert that nodes that are connected return 
    a (shortest) path between them.
    
    Include an additional test for nodes that are not connected 
    which should return None. 
    """
    g = graph.Graph(os.path.join('data', 'citation_network.adjlist'))
    
    # test connected nodes - verify exact shortest path
    path = g.bfs('Luke Gilbert', 'Michael Keiser')
    expected_path = ['Luke Gilbert', '33382968', 'Nevan Krogan', '29334369', 'Michael Keiser']
    assert path == expected_path, f"Expected shortest path {expected_path}, got {path}"
    
    # test nonexistent end node raises error
    with pytest.raises(NodeNotFoundError) as exc_info:
        g.bfs('Luke Gilbert', 'some_nonexistent_node')
    assert "some_nonexistent_node" in str(exc_info.value)

def test_bfs_empty_graph():
    """test that BFS on empty graph raises EmptyGraphError"""
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('')
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        with pytest.raises(EmptyGraphError) as exc_info:
            g.bfs('any_node')
        assert "empty graph" in str(exc_info.value).lower()
    finally:
        os.unlink(temp_file)

def test_bfs_nonexistent_start():
    """test start node not in graph raises NodeNotFoundError"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    with pytest.raises(NodeNotFoundError) as exc_info:
        g.bfs('not_in_graph')
    assert "not_in_graph" in str(exc_info.value)
    assert "Start node" in str(exc_info.value)

def test_bfs_nonexistent_end():
    """test end node not in graph raises NodeNotFoundError"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    with pytest.raises(NodeNotFoundError) as exc_info:
        g.bfs('Luke Gilbert', 'not_in_graph')
    assert "not_in_graph" in str(exc_info.value)
    assert "not found in graph" in str(exc_info.value)

def test_bfs_file_not_found():
    """test that loading nonexistent file raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        graph.Graph('nonexistent_file.adjlist')

def test_bfs_same_start_end():
    """test when start and end are the same node"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert', 'Luke Gilbert')
    assert result == ['Luke Gilbert']

def test_bfs_handles_cycles():
    """test BFS doesn't infinite loop on graphs with cycles"""
    import tempfile
    
    # Create a graph with a cycle: A -> B -> C -> A
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('A;B\n')
        f.write('B;C\n')
        f.write('C;A\n')  # Cycle back to A
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        result = g.bfs('A')
        
        # Should visit each node exactly once despite cycle
        assert result == ['A', 'B', 'C'], f"Expected ['A', 'B', 'C'], got {result}"
        assert len(set(result)) == 3, "Should visit each node exactly once"
    finally:
        os.unlink(temp_file)

def test_bfs_shortest_path_tiny_network():
    """test BFS returns the exact shortest path on tiny network"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    path = g.bfs('Martin Kampmann', 'Luke Gilbert')
    
    # BFS guarantees shortest path: Martin Kampmann -> 33483487 -> Luke Gilbert
    expected_path = ['Martin Kampmann', '33483487', 'Luke Gilbert']
    assert path == expected_path, f"Expected {expected_path}, got {path}"

def test_bfs_visits_all_reachable_nodes():
    """test that BFS traversal visits ALL reachable nodes"""
    import tempfile
    
    # Create graph: A -> B -> C, and D is unreachable from A
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('A;B\n')
        f.write('B;C\n')
        f.write('C\n')
        f.write('D\n')  # D is isolated
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        result = g.bfs('A')
        
        # Should visit exactly A, B, C (all reachable from A)
        assert set(result) == {'A', 'B', 'C'}, f"Should visit all reachable nodes, got {result}"
        assert 'D' not in result, "Should NOT visit unreachable node D"
    finally:
        os.unlink(temp_file)

def test_bfs_no_path_exists():
    """test when nodes exist but no path between them returns None"""
    import tempfile
    
    # Create a disconnected graph where A->B but C is isolated
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('A;B\n')
        f.write('B\n')
        f.write('C\n')  # C is isolated, no path from A to C
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        # A can reach B
        path = g.bfs('A', 'B')
        assert path == ['A', 'B'], "Should find path from A to B"
        
        # A cannot reach C (no edges to C)
        no_path = g.bfs('A', 'C')
        assert no_path is None, "Should return None when no path exists"
    finally:
        os.unlink(temp_file)

def test_bfs_finds_shortest_not_any_path():
    """test that BFS finds SHORTEST path, not just any valid path"""
    import tempfile
    
    # Create graph where there are two paths from A to D:
    #   Short: A -> B -> D (length 2)
    #   Long:  A -> C -> E -> D (length 3)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('A;B;C\n')   # A -> B, A -> C
        f.write('B;D\n')      # B -> D (short path)
        f.write('C;E\n')      # C -> E
        f.write('E;D\n')      # E -> D (long path completes)
        f.write('D\n')
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        path = g.bfs('A', 'D')
        
        # BFS MUST return the shortest path: A -> B -> D
        assert path == ['A', 'B', 'D'], f"BFS should return shortest path ['A', 'B', 'D'], got {path}"
        assert len(path) == 3, "Shortest path has 3 nodes"
    finally:
        os.unlink(temp_file)
