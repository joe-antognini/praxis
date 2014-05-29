#! /usr/bin/env python

#
# pi
#
# Calculate the digits of pi using the Chudnovsky formula
#


from math import *
from decimal import *

def not_converged(x, x_prev, precision):
  '''Return True if the sum has not converged to sufficient precision.'''
  if x == Decimal('0'):
    return True
  elif abs(x - x_prev) >= precision:
    return True
  else:
    return False

def calc_pi(n):
  '''Calculate pi to n decimal places.'''

  # Set the numerical precision used
  getcontext().prec = n + 50
  precision = Decimal('1e-' + str(n + 25))

  sum = Decimal('0')
  sum_prev = sum
  k = 0
  while not_converged(sum, sum_prev, precision):
    sum_prev = sum
    numer = factorial(6 * k) * (13591409 + 545140134 * k)
    denom = factorial(3 * k) * factorial(k)**3 * (-640320)**(3 * k)
    frac = Decimal(str(numer)) / Decimal(str(denom))
    frac *= 12 / (Decimal('640320')**3).sqrt()
    sum += frac
    k += 1

  pi_string = str(1 / sum)
  return pi_string

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    print 'The 1000th digit of pi after the decimal is:', calc_pi(1000)[1001]
  elif len(sys.argv) == 2:
    try:
      n = int(sys.argv[1])
      print calc_pi(n)[:n+2]
    except ValueError:
      print >> sys.stderr, "pi.py: argument must be an integer"
  else:
    print "usage: pi.py [number of digits]"
