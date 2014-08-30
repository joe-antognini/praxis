#! /usr/bin/env python

class node(object):
  '''A class representing a node of a disjoint-set forest data structure.'''
  
  def __init__(self, name):
    '''Set up a node.  The node is set up to be a singleton tree.

    Parameters:
      name: string

    Returns:
      node: a node instance
    '''
    
    # Typechecking
    if type(name) is not str:
      raise TypeError('node: name must be a string!')

    self.name = name
    self.parent = name
    self.rank = 0

class disjoint_set:
  '''A class implementing the disjoint-set forest data structure.

  Methods:
    makeset: Make a disjoint set out of a single node.

    find: Find the root of the tree for a particular node.  This function
      also flattens the tree if run.

    union: Join two trees together.  The tree with the smaller rank is
      joined as a subtree to the tree with the larger rank.
  '''

  def __init__(self, name=None):
    '''Initialize the disjoint-set forest to be empty.'''
    self.ds_forest = {}

  def __getitem__(self, name):
    '''Return a node's properties as a list.'''

    # Typechecking
    if type(name) is not str:
      raise TypeError('__getitem__(): element name must be a string!')
    elif name not in self.ds_forest:
      raise ValueError('__getitem__(): element must be in forest!')

    return [self.ds_forest[name].name, self.ds_forest[name].parent,
      self.ds_forest[name].rank]

  def printstate(self):
    '''Print the state of the tree.'''
    for elem in self.ds_forest:
      print (self.ds_forest[elem].name, self.ds_forest[elem].parent, 
        self.ds_forest[elem].rank)

  def makeset(self, name):
    '''Make a singleton tree.

    Parameters:
      name: string
    '''

    # Typechecking
    if type(name) is not str:
      raise TypeError('node: name must be a string!')

    self.ds_forest[name] = node(name)

  def find(self, a):
    '''Follow a node's parents to the root of the tree.  This function
    implements path compression -- once the root of the tree has been found,
    the root of the tree becomes the node's new parent.

    Parameters:
      a: node
    '''

    # Typechecking
    if type(a) is not str: 
      raise TypeError('find(): parameter must be a node!')
    elif a not in self.ds_forest:
      raise ValueError('find(): node must be in tree!')

    if self.ds_forest[a].parent == a:
      return a
    else:
      self.ds_forest[a].parent = self.find(self.ds_forest[a].parent)
      return self.ds_forest[a].parent

  def union(self, tree1, tree2):
    '''Join two trees.  The tree with the smaller rank is joined under the
    tree with the larger rank.

    Parameters:
      tree1: node
      
      tree2: node
    '''

    # Typechecking
    if type(tree1) is not str:
      raise TypeError('union(): tree1 must be a node!')
    elif type(tree2) is not str:
      raise TypeError('union(): tree2 must be a node!')
    elif tree1 not in self.ds_forest:
      raise ValueError('union(): tree1 must be in the tree!')
    elif tree2 not in self.ds_forest:
      raise ValueError('union(): tree2 must be in the tree!')

    root1 = self.find(tree1)
    root2 = self.find(tree2)

    if root1 == root2:
      return self.ds_forest
    else:
      if self.ds_forest[root1].rank > self.ds_forest[root2].rank:
        self.ds_forest[root2].parent = root1
      else:
        self.ds_forest[root1].parent = root2
        if self.ds_forest[root1].rank == self.ds_forest[root2].rank:
          self.ds_forest[root2].rank += 1

if __name__ == '__main__':
  ds = disjoint_set()
  ds.makeset('A')
  ds.makeset('B')
  ds.makeset('C')
  ds.makeset('D')
  ds.makeset('E')
  ds.makeset('F')
  ds.makeset('G')

  ds.union('A', 'D')
  ds.union('B', 'E')
  ds.union('C', 'F')

  ds.union('C', 'G')
  ds.union('E', 'A')

  ds.union('B', 'G')

  ds.printstate()
