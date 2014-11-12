#! /usr/bin/env python

if __name__ == '__main__':
  from segmented_sieve import *
else:
  from ..ex108.segmented_sieve import segmented_sieve

def brute_countprimes(n):
  '''Count the number of primes up to n using a segmented sieve of
  Eratosthenes.'''

  blocksize = int(1e8)
  nprimes = 1
  if blocksize > n:
    primes = sieve_erato(n)
    nprimes += sum(primes)
  else:
    primes = sieve_erato(2*blocksize)
    nprimes += sum(primes)
    for primes in segmented_sieve(2*blocksize, 
      n + 2*blocksize - (n%(2*blocksize)), blocksize):
      nprimes += sum(primes)
    nprimes -= sum(primes[(n%(2*blocksize)+1)/2:])
  return nprimes

if __name__ == '__main__':
  print brute_countprimes(2038074745)
