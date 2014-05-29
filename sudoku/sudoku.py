#! /usr/bin/env python

#
# Programming Praxis
# Sudoku
#
# Joe Antognini
# December 25, 2012
#

import numpy as np
import sys
from time import sleep
from copy import deepcopy

class Board:
  def __init__(self, lst):
    '''Define the board.  Zeros represent unknowns.'''
    if lst.shape == (9, 9):
      self.board = np.zeros([9, 9, 9])
      for i, row in enumerate(lst):
        for j, elem in enumerate(row):
          if elem != 0:
            self.board[i, j, elem-1] = elem
    elif lst.shape == (9, 9, 9):
      self.board = deepcopy(lst)
    else:
      raise TypeError

    old_board = deepcopy(self.board)
    self.constrain()
    while not np.array_equal(old_board, self.board):
      old_board = deepcopy(self.board)
      self.constrain()

  def in_row(self, i, j, n):
    '''Determines if a number is already in a particular row.'''
    row_constraints = []
    for elem in self.board[i, :j]:
      nonzero_elems = [item for item in elem if item != 0]
      if len(nonzero_elems) == 1:
        row_constraints.append(nonzero_elems[0])
    for elem in self.board[i, j+1:]:
      nonzero_elems = [item for item in elem if item != 0]
      if len(nonzero_elems) == 1:
        row_constraints.append(nonzero_elems[0])
    if n in row_constraints:
      return True
    else:
      return False

  def in_col(self, i, j, n):
    '''Determines if a number is already in a particular column.'''
    col_constraints = []
    for elem in self.board[:i, j]:
      nonzero_elems = [item for item in elem if item != 0]
      if len(nonzero_elems) == 1:
        col_constraints.append(nonzero_elems[0])
    for elem in self.board[i+1:, j]:
      nonzero_elems = [item for item in elem if item != 0]
      if len(nonzero_elems) == 1:
        col_constraints.append(nonzero_elems[0])
    if n in col_constraints:
      return True
    else:
      return False

  def in_box(self, i, j, n):
    '''Determines if a number is already in a particular box.'''
    box_constraints = []
    for p, elem1 in enumerate(self.board[i-(i%3):i-(i%3)+3, 
      j-(j%3):j-(j%3)+3]):
      for q, elem in enumerate(elem1):
        nonzero_elems = [item for item in elem if item != 0]
        if len(nonzero_elems) == 1 and (i % 3 != p or j % 3 != q):
          box_constraints.append(nonzero_elems[0])
    if n in box_constraints:
      return True
    else:
      return False

  def constrain(self):
    '''Run through the board and eliminate possibilities.'''
    for i in range(9):
      for j in range(9):
        if len([elem for elem in self.board[i, j] if elem != 0]) != 1:
          for k in range(1, 10):
            if not self.in_row(i, j, k) and not self.in_col(i, j, k):
              if not self.in_box(i, j, k):
                self.board[i, j, k-1] = k
                continue
            self.board[i, j, k-1] = 0

  def print_board(self):
    '''Print the board in a pleasing way.'''
    for i in range(9):
      if i == 3 or i == 6:
        print '------+-------+------'
      for j in range(9):
        if j == 3 or j == 6:
          print '|',
        nonzero = [elem for elem in self.board[i, j] if elem != 0]
        if len(nonzero) == 1:
          print int(nonzero[0]),
        else:
          print '.',
      print

def is_impossible(board):
  '''Determine if the board is impossible.'''
  for i in range(9):
    for j in range(9):
      possibilities = [elem for elem in board.board[i, j] if elem != 0]
      if len(possibilities) == 0:
        return True
  return False

def is_solved(board):
  '''Determine if the board is solved.'''
  for i in range(9):
    for j in range(9):
      possibilities = [elem for elem in board.board[i, j] if elem != 0]
      if len(possibilities) != 1:
        return False
  return True

def move(boards, moves):
  '''Make a move.  Go through the board until a spot with two or more
  possibilities is reached.  Pick one and create a new board.'''
  board = boards[-1]

  for i in range(9):
    for j in range(9):
      possibilities = [elem for elem in board.board[i, j] if elem != 0]
      if len(possibilities) > 1:
        new_board = deepcopy(board.board)
        choice = possibilities[0]
        for k in range(1, 10):
          if k != choice:
            new_board[i, j, k-1] = 0
        boards.append(Board(new_board))
        moves.append((i, j, choice))
        return
  raise Exception
        
def solve(boards):
  '''Pick a possibility and recursively work through the consequences.
  Returns False if we've reached a contradiction.'''
  moves = []

  while not is_solved(boards[-1]):
    board = boards[-1]

    # See if we have an impossible position.  If we do, back up.
    if is_impossible(board):
      boards.pop()
      board = boards[-1]
      i, j, k = moves.pop()
      board.board[i, j, k-1] = 0

      # We now have an edge condition.  If we had two choices and just
      # eliminated one, we would now accidentally set the other choice as a
      # constraint.  This would keep this 
      possibilities = [n for n in board.board[i, j] if n != 0]
      if len(possibilities) == 1:
        choice = possibilities[0]
        new_board = deepcopy(board.board)
        boards.append(Board(new_board))
        moves.append((i, j, choice))
    else:
      # If we don't have an impossible position, make a move.
      move(boards, moves)
    
if __name__ == '__main__'
  # A sample problem
  board = Board(np.array(
   [[0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 8, 2, 0, 0, 0, 0, 6, 0],
    [5, 0, 0, 0, 0, 4, 1, 0, 2],
    [8, 0, 0, 1, 4, 0, 0, 0, 5],
    [0, 0, 0, 9, 0, 6, 0, 0, 0],
    [3, 0, 0, 0, 5, 8, 0, 0, 6],
    [2, 0, 6, 4, 0, 0, 0, 0, 7],
    [0, 1, 0, 0, 0, 0, 3, 8, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0]]))

  # One sample problem
  #board = Board(np.array([[7, 0, 0, 1, 0, 0, 0, 0, 0],
  #  [0, 2, 0, 0, 0, 0, 0, 1, 5],
  #  [0, 0, 0, 0, 0, 6, 3, 9, 0],
  #  [2, 0, 0, 0, 1, 8, 0, 0, 0],
  #  [0, 4, 0, 0, 9, 0, 0, 7, 0],
  #  [0, 0, 0, 7, 5, 0, 0, 0, 3],
  #  [0, 7, 8, 5, 0, 0, 0, 0, 0],
  #  [5, 6, 0, 0, 0, 0, 0, 4, 0],
  #  [0, 0, 0, 0, 0, 1, 0, 0, 2]]))

  boards = [board]

  board.print_board()
  print
  print "Solving..."
  print

  try:
    solve(boards)
  except IndexError:
    print "Board has no solution!"
    sys.exit(1)

  boards[-1].print_board()
  print
