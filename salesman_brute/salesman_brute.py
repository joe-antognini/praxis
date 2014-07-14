#! /usr/bin/env python

class graph:
  '''A graph data structure.  
  
  The data structure consists of a dictionary for which each element is a
  node.  Each node stores a list of all other nodes to which the node is
  connected along with the length of the edge.
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
    else:
      self.G = {name : []}

  def __getitem__(self, i):
    '''Return the edges connected to a specific node.'''
    return self.G[i]

  def add_node(self, name, edges):
    '''Add a node to the graph.

    Parameters:
      name: any type
        The name of the node.  This should usually be a short string or an
        integer.

      edges: iterable
        A list of nodes this new node connects to.  Each element should
        consist of a two-element iterable, the first of which is the node to
        which the edge connects and the second of which is the length of the
        edge.
    '''
   
    #
    # First perform some checks on the received data types.
    #

    # Make sure that the node is not already in the graph
    if name in self.G:
      raise ValueError('graph.add_node(): node already in graph!')

    # Make sure that the edges are iterable
    if not hasattr(edges, '__iter__'):
      raise TypeError('graph.add_node(): edges are not iterable!')
    for elem in edges:
      if not hasattr(elem, '__iter__'):
        raise TypeError('graph.add_node(): ' + str(elem) + 
        ': edge is not iterable!')
      if len(elem) < 2:
        raise TypeError('graph.add_node(): ' + str(elem) +
        ': edge is missing name or length data!')
      if not isinstance(elem[1], (int, long, float)):
        raise TypeError('graph.add_node(): ' + str(elem) + 
        ': edge length is not a number!')
      # Check that the edges are to nodes already in the graph
      if elem[0] not in self.G:
        raise ValueError('graph.add_node(): ' + str(elem) +
        ': edge connects to nonexistant node!')
        
    # First add the node
    self.G[name] = edges

    # Now update all the adjacent nodes
    for node in edges:
      adj_name = node[0]
      length = node[1]
      adj_node = self.G[adj_name][:]
      adj_node.append((name, length))
      self.G[adj_name] = adj_node

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

    return [y[0] for y in self.G[x]]

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
    if y not in self.neighbors(x):
      raise ValueError('graph.get_edge(): no edge connecting the nodes!')
    
    for elem in self.G[x]:
      if elem[0] == y:
        return elem[1]
