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

@memoize
def legendre_phi(x, a):
  '''Calculate Legendre's phi function.'''

  if a == 1:
    return (x+1)/2
  else:
    # Find the a'th prime
    j = 0
    count = 1
    while count != a:
      primes = sieve_erato(int(2**j * log(a) * a))
      count = 1
      for i, elem in enumerate(primes):
        if elem:
          count += 1
          if count == a:
            break
      j += 1
    p_a = 2*i + 3

    return legendre_phi(x, a-1) - legendre_phi(x / p_a, a-1)

def legendre_pi(n):
  '''Calculate the number of primes less than or equal to n using Legendre's
  algorithm.'''

  if n == 2:
    return 1
  else:
    a = legendre_pi(int(sqrt(n)))
    return legendre_phi(n, a) + a - 1

if __name__ == '__main__':
  print legendre_pi(int(1e4))
