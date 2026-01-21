import networkx as nx

class Graph:
    """
    Class to contain a graph and your bfs function
    
    You may add any functions you deem necessary to the class
    """
    def __init__(self, filename: str):
        """
        Initialization of graph object 
        """
        self.graph = nx.read_adjlist(filename, create_using=nx.DiGraph, delimiter=";")

    def bfs(self, start, end=None):
        """
        TODO: write a method that performs a breadth first traversal and pathfinding on graph G

        * If there's no end node input, return a list nodes with the order of BFS traversal
        * If there is an end node input and a path exists, return a list of nodes with the order of the shortest path
        * If there is an end node input and a path does not exist, return None

        """
        # ========================================
        if not self.graph.nodes():
            return []
        
        if start not in self.graph:
            return []
        
        if end is not None and end not in self.graph:
            return None
        
        visited = set()
        queue = [start]
        visited.add(start)
        result = [start]
        parent = {start: None}
        
        while queue:
            node = queue.pop(0)
            
            if end is not None and node == end:
                path = []
                curr = end
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr]
                return path[::-1]
            
            for neighbor in self.graph.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    result.append(neighbor)
                    parent[neighbor] = node
        
        if end is not None:
            return None
        
        return result
        # ========================================




