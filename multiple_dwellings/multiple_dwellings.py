#! /usr/bin/env python

#
# Multiple Dwellings
# Solve a simple logic puzzle
#
# Programming Praxis
# Exercise 7
# http://programmingpraxis.com/2009/02/20/multiple-dwellings/
#

def all_perms(elements):
  if len(elements) <= 1:
    yield elements
  else:
    for perm in all_perms(elements[1:]):
      for i in range(len(elements)):
        yield perm[:i] + elements[0:1] + perm[i:]

building = ['b', 'c', 'f', 'm', 's']

for perm in all_perms(building):
  # Baker does not live on the top floor
  if perm[4] == 'b':
    continue

  # Cooper does not live on the bottom floor
  if perm[0] == 'c':
    continue

  # Fletcher does not live on either the top or bottom floor
  if perm[0] == 'f' or perm[4] == 'f':
    continue

  # Miller lives on a higher floor than Cooper
  cont = False
  for elem in perm:
    if elem == 'c':
      break
    elif elem == 'm':
      cont = True
      break
  if cont:
    continue

  # Smith does not live on a floor next to Fletcher
  for i, elem in enumerate(perm):
    if elem == 'f':
      if i >= 1:
        if perm[i-1] == 's':
          cont = True
          break
      if i <= 3:
        if perm[i+1] == 's':
          cont = True
          break
  if cont:
    continue

  # Fletcher does not live on a floor next to Cooper.
  for i, elem in enumerate(perm):
    if elem == 'c':
      if i >= 1:
        if perm[i-1] == 'f':
          cont = True
          break
      if i <= 3:
        if perm[i+1] == 'f':
          cont = True
          break
  if cont:
    continue

  print perm
