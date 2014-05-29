#! /usr/bin/env python

#
# Sieve of Eratosthenes
#
# Programming Praxis
# Problem 2
# http://programmingpraxis.com/2009/02/19/sieve-of-eratosthenes/
#

import sys, time
import numpy as np
from math import sqrt

start_time = time.time()

if len(sys.argv) != 2:
  print "usage: python 2.py n"
  sys.exit(1)

try:
  n = int(sys.argv[1])
except ValueError:
  print "error: argument must be an integer"
  sys.exit(1)

if n < 2:
  print "error: argument must be greater than or equal to 2"
  sys.exit(1)

if n == 2:
  print "2"
  sys.exit(0)

# Only use a list with odd numbers
# (Optimization #1)
primes = [2, 3]
prime_i = 1
lst = np.zeros([len(np.arange(5, n+1, 2)), 2])
lst[:, 0] = np.arange(5, n+1, 2)

# Only need to do work up to the square root of the maximum number
# (Optimization #3)
while primes[prime_i] < sqrt(n):
  # For any prime we are looking at, anything in the list that is less
  # than the square of the prime must also be prime.  
  # (Optimization #2)
  min_i = np.where(lst[:, 0] == primes[prime_i]**2)[0]
  new_primes = [elem[0] for elem in lst[:min_i] if elem[1] == 0]
  lst[:min_i, 1] = np.ones(len(lst[:min_i]))
  for elem in new_primes:
    primes.append(elem)

  lst[min_i::primes[prime_i], 1] = \
    np.ones(len(lst[min_i::primes[prime_i]]))
  prime_i += 1
  print int(primes[prime_i])

for elem in lst:
  if elem[1] == 0:
    primes.append(elem[0])
print "Number of primes:", len(primes)

print "Running time:", time.time() - start_time, "seconds"
