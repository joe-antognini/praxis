#! /usr/bin/env python

from math import log, sqrt
from sieve_erato import sieve_erato

def memoize(f):
  class memodict(dict):
    def __init__(self, f):
      self.f = f
    def __call__(self, *args):
      return self[args]
    def __missing__(self, key):
      ret = self[key] = self.f(*key)
      return ret
  return memodict(f)

def prime_n(n):
  '''Return the n'th prime.'''
  if n == 0:
    return 1
  j = 0
  count = 1
  while count != n:
    primes = sieve_erato(int(2**j * log(n) * n))
    count = 1
    for i, elem in enumerate(primes):
      if elem:
        count += 1
        if count == n:
          break
    j += 1
  return 2*i + 3

@memoize
def legendre_phi(x, a, acc=0):
  '''Calculate Legendre's phi function.'''
  
  if x == 0:
    return 0

  while a > 1:
    p_a = prime_n(a)
    (x, a, acc) = (x, a-1, legendre_phi(x/p_a, a-1) + acc)
  return (x+1)/2 - acc

def legendre_pi(n):
  '''Calculate the number of primes less than or equal to n using Legendre's
  algorithm.'''

  if n == 2:
    return 1
  elif n == 3:
    return 2
  else:
    a = legendre_pi(int(sqrt(n)))
    return legendre_phi(n, a) + a - 1

if __name__ == '__main__':
  print legendre_pi(int(1e6))
