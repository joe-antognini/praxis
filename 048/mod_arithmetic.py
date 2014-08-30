#! /usr/bin/env python

#
# A library of modular arithmetic functions.
#

def coprime(x, y):
  '''Test whether two numbers are coprime.'''

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
  if not all(isinstance(item, int) for item in (x, y, n):
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
  if not all(isinstance(item, int) for item in (x, y, n):
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
  if not all(isinstance(item, int) for item in (x, y, n):
    raise TypeError('mod_mult(): parameters must be integers!')

  return (x * y) % n

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
  if not all(isinstance(item, int) for item in (x, y, n):
    raise TypeError('mod_div(): parameters must be integers!')

