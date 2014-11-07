#! /usr/bin/env python

import bitarray as bt
from math import sqrt
from sieve_erato import sieve_erato

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
    print Q
    return lst


if __name__ == '__main__':
  print segmented_sieve(100, 200, 10)
