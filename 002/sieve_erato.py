#! /usr/bin/env python

import bitarray as bt
from math import sqrt

def sieve_erato(n):
  '''Return a list of all primes less than or equal to a given number.

  Input:
    n: int
  
  Output:
    bitarray
      A bitarray where each bit is False if the number is not prime and True
      if it is prime. 
  '''

  lst = bt.bitarray((n+1)/2 - 1)
  lst.setall(True)

  imax = (int(sqrt(n)) - 1) / 2
  for i in xrange(imax):
    if lst[i]:
      lst[2*i*i+6*i+3::2*i+3] = False

  return lst

def sievebt2lst(ba):
  '''Take a bitarray from sieve_erato and print out the prime numbers.'''
  lst = [2]
  for i, elem in enumerate(ba):
    if elem:
      lst.append(2 * i + 3)
  return lst

if __name__ == '__main__':
  # Test case
  prime_array = sieve_erato(15485863)
  print sum(prime_array) + 1
