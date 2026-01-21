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
