#! /usr/bin/env python

#
# Flavius Josephus
#
# Programming Praxis
# Exercise 5
# http://programmingpraxis.com/2009/02/19/flavius-josephus/
# 

def josephus(n, m):
  '''Solves the Josephus Problem.  The problem is as follows.  n people
  stand in a circle.  Every mth person is killed.  What is the order in
  which people are killed, and where should one stand in order to be the
  last to survive?  This function returns a list containing the positions
  in which people are killed.'''

  lst = range(n)
  ans = []

  i = 0
  j = 0
  while len(lst) != 1:
    if (i + 1) % m == 0:
      ans.append(lst.pop(j))
      j -= 1
    
    i += 1
    j += 1
    if j >= len(lst):
      j = 0

  ans.append(lst[0])
  return ans

print josephus(41, 3)
