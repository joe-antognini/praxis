#! /usr/bin/env python

import numpy
import random
import copy
from itertools import permutations

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
      self.g = {}
    elif type(name) is dict:
      for elem in name:
        if type(name[elem]) is not dict:
          raise ValueError('graph.__init__(): cast to graph failed!')
      self.g = {}
      for elem in name:
        self.g[elem] = name[elem]
    else:
      self.g = {name : {}}

  def __getitem__(self, i):
    '''Return the edges connected to a specific node.'''
    if i not in self.g:
      raise ValueError('node not in graph!')
    return self.g[i]

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
    if name in self.g:
      raise ValueError('graph.add_node(): node already in graph!')

    if edges is None:
      self.g[name] = {}

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
        if elem not in self.g:
          raise ValueError('graph.add_node(): ' + str(elem) +
          ': edge connects to nonexistant node!')
        
      # First add the node
      self.g[name] = edges

      # Now update all the adjacent nodes
      for adj_node in edges:
        self.g[adj_node][name] = edges[adj_node]
  
  def add_edge(self, x, y, length):
    '''Add an edge between nodes x and y with given length.  If an edge
    already connects x and y, this function changes the length.

    Parameters:
      x: node
      
      y: node

      length: int, float, or long
    '''

    # First check that the nodes are in the graph.
    if x not in self.g:
      raise ValueError('graph.add_node(): ' + str(x) + ' not in graph!')
    if y not in self.g:
      raise ValueError('graph.add_node(): ' + str(y) + ' not in graph!')
    # Check that the length is a number
    if type(length) not in [int, float, long]:
      raise ValueError('graph.add_node(): length must be a number!')

    self.g[x][y] = length
    self.g[y][x] = length

  def neighbors(self, x):
    '''Returns all nodes with an edge connecting them to x.

    Parameters:
      x: node
        A node in the graph.

    Returns:
      list
        A list of all nodes connected to the given node.
    '''
    if x not in self.g:
      raise ValueError('graph.neighbors():' + str(x) + ' not in graph!')

    return self.g[x].keys()

  def delete_node(self, x):
    '''Delete a node from the graph.

    Parameters:
      x: node
        The node to be deleted
    '''

    if x not in self.g:
      raise ValueError('delete_node(): node not in graph!')

    # Delete the edges connecting the node
    for node in self.neighbors(x):
      del self.g[node][x]

    # Delete the node itself
    del self.g[x]

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
    if y not in self.g[x]:
      raise ValueError('graph.get_edge(): no edge connecting the nodes!')
    
    return self.g[x][y]

  def count_nodes(self):
    '''Return the number of nodes in the graph.'''
    return len(self.g)

  def nodes(self):
    '''Return the nodes in the graph.'''
    return self.g.keys()

def shortest_path(g, a, b):
  '''Caculate the shortest path from a to b in a graph g by brute force.

  Parameters:
    g: graph
      The graph on which to find the shortest route
    
    a: node
      Starting node

    b: node
      Ending node

  Returns:
    shortest_path_length: number
      The length of the shortest path

    shortest_path_nodes: tuple
      A tuple consisting of the nodes along the shortest path.
  '''

  if a == b:
    # Trivial case of starting and ending on the same node.
    return (0, [b])
  elif len(g.neighbors(a)) == 0:
    # In this case we've reached a dead end.
    return (numpy.inf, [])
  else:
    shortest_path_length = numpy.inf
    shortest_path_nodes = []
    for adj_node in g[a]:
      path_length = g[a][adj_node]
      h = copy.deepcopy(g)
      h.delete_node(a)
      sub_path_length, sub_path_nodes = shortest_path(h, adj_node, b)
      path_length += sub_path_length
      
      if path_length < shortest_path_length:
        shortest_path_length = path_length
        shortest_path_nodes = sub_path_nodes
        shortest_path_nodes.insert(0, a)

    return (shortest_path_length, shortest_path_nodes)

def salesman_brute(g):
  '''Calculate the shortest tour that visits every node of the graph, G, and
  returns to the starting node.

  Parameters:
    g: graph
      The graph on which to find the shortest tour

  Returns:
    shortest_tour_length: number
      The length of the shortest tour

    shortest_tour_nodes: tuple
      A tuple consisting of the nodes along the shortest tour
  '''

  # Randomly pick a node to start.
  start_node = random.choice(g.nodes())
  permute_nodes = g.nodes()
  permute_nodes.remove(start_node)

  min_length = numpy.inf
  for path in permutations(permute_nodes):
    prev_node = start_node
    path_length = 0
    for node in path:
      path_length += shortest_path(g, prev_node, node)[0]
      prev_node = node
    path_length += shortest_path(g, node, start_node)[0]
    if path_length < min_length:
      min_length = path_length
      shortest_tour = list(path)
      shortest_tour.insert(0, start_node)
      shortest_tour.append(start_node)

  return (min_length, shortest_tour)

if __name__ == '__main__':
  # Set up a default graph
  G = graph()
  G.add_node('A')
  G.add_node('B')
  G.add_node('C')
  G.add_node('D')
  G.add_node('E')
  G.add_node('F')

  G.add_edge('A', 'B', 10)
  G.add_edge('A', 'C', 20)
  G.add_edge('A', 'E', 50)
  G.add_edge('B', 'D', 24)
  G.add_edge('B', 'C', 15)
  G.add_edge('B', 'E', 30)
  G.add_edge('C', 'E', 6)
  G.add_edge('C', 'F', 12)
  G.add_edge('D', 'E', 15)
  G.add_edge('D', 'F', 40)
  G.add_edge('E', 'F', 18)

  TOUR = salesman_brute(G)
  print "Optimum tour:", TOUR[1]
  print "Tour length:", TOUR[0]
