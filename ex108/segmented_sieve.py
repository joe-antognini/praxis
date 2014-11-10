#! /usr/bin/env python

import bitarray as bt
from math import sqrt
if __name__ == '__main__':
  from sieve_erato import sieve_erato
else:
  from ..ex002.sieve_erato import sieve_erato

def segmented_sieve(L, R, B):
  '''Perform a segmented Sieve of Eratosthenes.'''

  # Typechecking
  if (R - L) % B != 0:
    raise ValueError('segmented_sieve(): B must divide R - L')

  # First compute the primes less than sqrt(R).
  divisors = sieve_erato(int(sqrt(R)))

  Q = [-(L + 1 + (2*i + 3)) / 2 % (2*i + 3) if n != 0 else 0 for i, n in
    enumerate(divisors)]
  for block in xrange((R - L) / (2 * B)):
    lst = bt.bitarray(B)
    lst.setall(True)
    for i, p in enumerate(divisors):
      if p:
        lst[Q[i]::2*i+3] = False
    Q = [(Q[i] - B) % (2*i + 3) if n != 0 else 0 for i, n in
      enumerate(divisors)]
    yield lst

def segsievebt2lst(ba, min_n, i, block_size):
  '''Take a bitarray from the segmented sieve result and print it as a list
  of ints.'''
  lst = []
  for j, elem in enumerate(ba):
    if elem:
      lst.append(min_n + 2 * i * block_size + (2*j+1))
  return lst

if __name__ == '__main__':
  MIN_N = 100
  MAX_N = 200
  BLOCK_SIZE = 10
  for I, BLOCK in enumerate(segmented_sieve(MIN_N, MAX_N, BLOCK_SIZE)):
    print segsievebt2lst(BLOCK, MIN_N, I, BLOCK_SIZE)
