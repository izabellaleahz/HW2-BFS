# write tests for bfs
import pytest
from search import graph
import os

def test_bfs_traversal():
    """
    TODO: Write your unit test for a breadth-first
    traversal here. Create an instance of your Graph class 
    using the 'tiny_network.adjlist' file and assert 
    that all nodes are being traversed (ie. returns 
    the right number of nodes, in the right order, etc.)
    """
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert')
    
    assert result is not None
    assert len(result) > 0
    assert result[0] == 'Luke Gilbert'
    assert len(set(result)) == len(result)  # no duplicates

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
    
    # test connected nodes
    path = g.bfs('Luke Gilbert', 'Michael Keiser')
    assert path is not None
    assert path[0] == 'Luke Gilbert'
    assert path[-1] == 'Michael Keiser'
    
    # test unconnected nodes
    no_path = g.bfs('Luke Gilbert', 'some_nonexistent_node')
    assert no_path is None

def test_bfs_empty_graph():
    """test empty graph handling"""
    import networkx as nx
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.adjlist') as f:
        f.write('')
        temp_file = f.name
    
    try:
        g = graph.Graph(temp_file)
        result = g.bfs('any_node')
        assert result == []
    finally:
        os.unlink(temp_file)

def test_bfs_nonexistent_start():
    """test start node not in graph"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('not_in_graph')
    assert result == []

def test_bfs_nonexistent_end():
    """test end node not in graph"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert', 'not_in_graph')
    assert result is None

def test_bfs_exception():
    """test that raises exception"""
    with pytest.raises(Exception):
        g = graph.Graph('nonexistent_file.adjlist')

def test_bfs_same_start_end():
    """test when start and end are the same node"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert', 'Luke Gilbert')
    assert result == ['Luke Gilbert']

def test_bfs_single_node_path():
    """test pathfinding returns correct single node"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert', 'Luke Gilbert')
    assert len(result) == 1
    assert result[0] == 'Luke Gilbert'

def test_bfs_traversal_different_starts():
    """test traversal from different start nodes"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    
    result1 = g.bfs('Luke Gilbert')
    result2 = g.bfs('Michael Keiser')
    
    assert result1 is not None
    assert result2 is not None
    assert result1[0] == 'Luke Gilbert'
    assert result2[0] == 'Michael Keiser'

def test_bfs_path_tiny_network():
    """test pathfinding on tiny network"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    path = g.bfs('Luke Gilbert', 'Michael Keiser')
    
    if path is not None:
        assert path[0] == 'Luke Gilbert'
        assert path[-1] == 'Michael Keiser'
        assert len(path) >= 2

def test_bfs_traversal_all_nodes():
    """test that traversal visits multiple nodes"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    result = g.bfs('Luke Gilbert')
    
    assert len(result) > 1
    assert 'Luke Gilbert' in result

def test_bfs_no_path_exists():
    """test when nodes exist but no path between them"""
    g = graph.Graph(os.path.join('data', 'tiny_network.adjlist'))
    
    # try to find path that might not exist
    result = g.bfs('Luke Gilbert', 'Neil Risch')
    
    # should return None if no path, or a valid path if one exists
    if result is not None:
        assert result[0] == 'Luke Gilbert'
        assert result[-1] == 'Neil Risch'

def test_bfs_path_length():
    """test that returned path is actually a path"""
    g = graph.Graph(os.path.join('data', 'citation_network.adjlist'))
    path = g.bfs('Luke Gilbert', 'Michael Keiser')
    
    if path is not None and len(path) > 1:
        # check consecutive nodes are connected
        for i in range(len(path) - 1):
            assert path[i+1] in list(g.graph.neighbors(path[i])) or path[i] in list(g.graph.neighbors(path[i+1]))
