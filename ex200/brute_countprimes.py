#! /usr/bin/env python

if __name__ == '__main__':
  from segmented_sieve import segmented_sieve
else:
  from ..ex108.segmented_sieve import segmented_sieve

def brute_countprimes(n):
  '''Count the number of primes up to n using a segmented sieve of
  Eratosthenes.'''

  blocksize = int(1e9)
  nprimes = 1
  for block in xrange(0, n, blocksize):
    primes = segmented_sieve(0, n
