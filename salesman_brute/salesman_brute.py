#! /usr/bin/env python

class graph:
  '''A graph data structure.  
  
  The data structure consists of a dictionary for which each element is a
  node.  Each node stores a dictionary of all other nodes to which the node
  is connected along with the length of the edge.  
  '''

  def __init__(self, name=None):
    '''Initialize the graph.

    Parameters:
      name: any type
        The name of the node.  This should usually be a short string or an
        integer.
    '''
    if name is None:
      self.G = {}
    elif type(name) is dict:
      for elem in name:
        if type(name[elem]) is not dict:
          raise ValueError('graph.__init__(): cast to graph failed!')
      self.G = {}
      for elem in name:
        self.G[elem] = name[elem]
    else:
      self.G = {name : {}}

  def __getitem__(self, i):
    '''Return the edges connected to a specific node.'''
    if i not in self.G:
      raise ValueError('node not in graph!')
    return self.G[i]

  def copy(self):
    '''Return a deep copy of the graph.'''
    H = {}
    for elem in self.G:
      H[elem] = self.G[elem]
    return graph(H)

  def add_node(self, name, edges=None):
    '''Add a node to the graph.

    Parameters:
      name: any type
        The name of the node.  This should usually be a short string or an
        integer.

      edges: dict, optional
        The nodes this new node connects to.  The key for each element of
        this dictionary is the name of an adjacent node and the associated
        value is the length of the corresponding edge.
        '''
   
    #
    # First perform some checks on the received data types.
    #

    # Make sure that the node is not already in the graph
    if name in self.G:
      raise ValueError('graph.add_node(): node already in graph!')

    if edges is None:
      self.G[name] = {}

    else:
      # Make sure that the edges are a dictionary
      if type(edges) is not dict:
        raise TypeError('graph.add_node(): edges must be a dictionary!')
      for elem in edges:
        # Make sure the length is some kind of number
        if not isinstance(edges[elem], (int, long, float)):
          raise TypeError('graph.add_node(): ' + str(elem) + 
          ': edge length is not a number!')
        # Check that the edges are to nodes already in the graph
        if elem not in self.G:
          raise ValueError('graph.add_node(): ' + str(elem) +
          ': edge connects to nonexistant node!')
        
      # First add the node
      self.G[name] = edges

      # Now update all the adjacent nodes
      for adj_node in edges:
        self.G[adj_node][name] = edges[adj_node]
  
  def add_edge(self, x, y, length):
    '''Add an edge between nodes x and y with given length.  If an edge
    already connects x and y, this function changes the length.

    Parameters:
      x: node
      
      y: node

      length: int, float, or long
    '''

    # First check that the nodes are in the graph.
    if x not in self.G:
      raise ValueError('graph.add_node(): ' + str(x) + ' not in graph!')
    if y not in self.G:
      raise ValueError('graph.add_node(): ' + str(y) + ' not in graph!')
    # Check that the length is a number
    if type(length) not in [int, float, long]:
      raise ValueError('graph.add_node(): length must be a number!')

    self.G[x][y] = length
    self.G[y][x] = length

  def neighbors(self, x):
    '''Returns all nodes with an edge connecting them to x.

    Parameters:
      x: node
        A node in the graph.

    Returns:
      list
        A list of all nodes connected to the given node.
    '''
    if x not in self.G:
      raise ValueError('graph.neighbors():' + str(x) + ' not in graph!')

    return self.G[x].keys()

  def delete_node(self, x):
    '''Delete a node from the graph.

    Parameters:
      x: node
        The node to be deleted
    '''

    if x not in self.G:
      raise ValueError('delete_node(): node not in graph!')

    # Delete the edges connecting the node
    for node in self.neighbors(x):
      del self.G[node][x]

    # Delete the node itself
    del self.G[x]

  def get_edge(self, x, y):
    '''Returns the value of the edge connecting x and y.

    Parameters:
      x: node
        A node in the graph

      y: node
        Another node in the graph
    
    Returns:
      number
        The length of the edge connecting x and y
    '''
    # First check that there exists an edge connecting x and y.
    if y not in self.G[x]:
      raise ValueError('graph.get_edge(): no edge connecting the nodes!')
    
    return self.G[x][y]

  def count_nodes(self):
    '''Return the number of nodes in the graph.'''
    return len(self.G)

def salesman_brute(G, A, B):
  '''Caculate the shortest path from A to B in a graph G by brute force.

  Parameters:
    G: graph
      The graph on which to find the shortest route
    
    A: node
      Starting node

    B: node
      Ending node

  Returns:
    path: tuple
      A tuple consisting of the nodes along the shortest path
  '''

  from numpy import inf

  shortest_path_length = inf
  shortest_path_nodes = []
  for adj_node in G[A]:
    path_length = G[A][adj_node]
    
    H = G.copy()
    H.delete_node(A)
    sub_path_length, sub_path_nodes = salesman_brute(H, node, B)
    path_length += sub_path_length
    path_nodes = sub_path_nodes.insert(0, A)
    
    if path_length < shortest_path:
      shortest_path_length = path_length
      shortest_path_nodes = path_nodes

  return (shortest_path_length, shortest_path_nodes)
