#! /usr/bin/env python

#
# Bingo probability calculator
#
# Programming Praxis
# Problem 3
# http://programmingpraxis.com/2009/02/19/bingo/
#

from random import *
import numpy as np
import time

start_time = time.time()

class Card:
  def __init__(self):
    self.card = np.zeros([5, 5])
    self.card[:, 0] = sample(range(1, 16), 5)
    self.card[:, 1] = sample(range(16, 31), 5)
    self.card[:, 2] = sample(range(31, 46), 5)
    self.card[:, 3] = sample(range(46, 61), 5)
    self.card[:, 4] = sample(range(61, 76), 5)
    
    self.marks = np.zeros([5, 5])
    self.marks[2, 2] = 1

  def mark(self, n):
    self.marks[np.where(self.card == n)] = 1

  def check_bingo(self):
    # First check rows
    for i in range(5):
      if np.array_equal(self.marks[i], 5 * [1]):
        return True

    # Check columns
    for i in range(5):
      if np.array_equal(self.marks[:, i], 5 * [1]):
        return True

    # Lastly check the two diagonals
    if [self.marks[i, i] for i in range(5)] == 5 * [1]:
      return True
    if [self.marks[i, 4-i] for i in range(5)] == 5 * [1]:
      return True

    # If we haven't returned by now, then there is no Bingo.
    return False

# Run a Monte Carlo sequence for a single card.
nruns = 3000
turns_mean = 0
for i in range(nruns):
  nums = range(1, 76)
  shuffle(nums)
  card = Card()

  turns = 0
  for n in nums:
    turns += 1
    if n in card.card:
      card.mark(n)

    if card.check_bingo():
      turns_mean += turns / float(nruns)
      break

print "First bingo in single card:", turns_mean

def run_bingo(cards, nums):
  '''Runs a bingo game on a set of bingo cards.'''
  turns = 0
  for n in nums:
    turns += 1
    for card in cards:
      if n in card.card:
        card.mark(n)

      if card.check_bingo():
        return turns

# Run a Monte Carlo sequence for a 500-card competition.
nruns = 30
ncards = 500
turns_mean = 0
for i in range(nruns):
  nums = range(1, 76)
  shuffle(nums)
  cards = [Card() for i in range(ncards)]

  turns_mean += run_bingo(cards, nums) / float(nruns)

print "First bingo in 500 cards:", turns_mean

print "Running time:", time.time() - start_time
