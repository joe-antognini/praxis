#! /usr/bin/env python

class disjoint_set:
  '''A class implementing the disjoint-set forest data structure.

  Methods:
    make_set: Make a disjoint set out of a single node.

    find: Find the root of the tree for a particular node.  This function
      also flattens the tree if run.

    union: Join two trees together.  The tree with the smaller rank is
      joined as a subtree to the tree with the larger rank.
  '''

  def __init__(self, name=None):
