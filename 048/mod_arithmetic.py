#! /usr/bin/env python

#
# A library of modular arithmetic functions.
#

from random import sample

def gcd(x, y):
  '''Recursively find the greatest common divisor using Euclid's
  algorithm.

  Parameters:
    x, y: int

  Returns: int
  '''

  if x < y:
    x, y = (y, x)
  if y == 0:
    return x
  else:
    return gcd(y, x % y)

def extended_euclid(a, b):
  '''Perform the extended Euclidean algorithm.

  Parameters:
    a, b: int
      Two non-negative integers with a >= b.

  Returns:
    d: int
      The greatest common divisor
    x, y: int
      Numbers such that ax + by = d
  '''

  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (a, b)):
    raise TypeError('extended_euclid(): parameters must be integers')
  if a < 0 or b < 0:
    raise ValueError('extended_euclid(): parameters must be non-negative')
  if b > a:
    raise ValueError(
      'extended_euclid(): a must be greater than or equal to b')

  # The algorithm
  if b == 0:
    return (1, 0, a)
  else:
    x1, y1, d = extended_euclid(b, a % b)
    return (y1, x1 - (a / b) * y1, d)

def isprime(x, k=100):
  '''Probabilistically check if x is prime.  This algorithm exploits
  Fermat's little theorem.

  Parameter:
    x: int

    k: int, optional
      The number of random numbers to test primality against.

  Returns: bool
    True if prime, False otherwise.
  '''

  # Typechecking
  if not isinstance(x, (int, long)):
    raise TypeError('isprime(): parameter must be an integer')

  if x <= 0:
    return False

  for i in sample(xrange(1, x), min(x-1, k)):
    if mod_exp(i, x-1, x) != 1:
      return False
  return True

def mod_add(x, y, n):
  '''Perform modular addition.

  Parameters:
    x, y: int
      Numbers to be added.

    n: int
      Modulo

  Returns:
    int
  '''

  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (x, y, n)):
    raise TypeError('mod_add(): parameters must be integers!')

  return (x + y) % n

def mod_sub(x, y, n):
  '''Perform modular subtraction.

  Parameters:
    x, y: int
      Numbers to be subtracted.

    n: int
      Modulo

  Returns:
    int
  '''

  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (x, y, n)):
    raise TypeError('mod_sub(): parameters must be integers!')

  return mod_add(x, -y, n)

def mod_mult(x, y, n):
  '''Perform modular multiplication.

  Parameters:
    x, y: int
      Numbers to be multiplied.

    n: int
      Modulo

  Returns:
    int
  '''

  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (x, y, n)):
    raise TypeError('mod_mult(): parameters must be integers!')

  return (x * y) % n

def mod_inv(a, n):
  '''Find the modular inverse.  If no modular inverse exists then a
  ZeroDivisionError is raised.

  Parameters:
    a: int

    n: int
      Modulo

  Returns: int
    The inverse if it exists.
  '''
  a %= n
  y, a_inv, d = extended_euclid(n, a)

  if d != 1:
    raise ZeroDivisionError
  else:
    return a_inv % n

def mod_div(x, y, n):
  '''Perform modular division.

  Parameters:
    x, y: int
      Numbers to be divided.

    n: int
      Modulo

  Returns:
    int
  '''

  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (x, y, n)):
    raise TypeError('mod_div(): parameters must be integers!')

  return mod_mult(x, mod_inv(y, n), n)

def mod_exp(a, b, n):
  '''Perform modular exponentiation.

  Parameters:
    x, y: int
      Numbers to be divided.

    n: int
      Modulo

  Returns:
    int
  '''
  
  # Typechecking
  if not all(isinstance(item, (int, long)) for item in (a, b, n)):
    raise TypeError('mod_exp(): parameters must be integers')
  if b < 0:
    raise ValueError('mod_exp(): exponent must be positive')

  # The algorithm
  if b == 0:
    return 1
  elif b % 2 == 0:
    half = mod_exp(a, b/2, n)
    return mod_mult(half, half, n)
  else:
    half = mod_exp(a, b/2, n)
    return mod_mult(a, mod_mult(half, half, n), n)

def mod_sqrt(a, n):
  '''Compute the modular square root.  This algorithm assumes that the
  modulus is prime.  If it is not or a square root does not exist, a
  ValueError is raised.

  Parameters:
    a: int

    n: int
      Modulo

  Returns: int
  '''


