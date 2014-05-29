#! /usr/bin/env python

#
# pi
#
# Calculate the 1000th digit of pi using the Chudnovsky formula
#

from math import *
from decimal import *

getcontext().prec = 1050
precision = Decimal('1e-1030')

def not_converged(x, x_prev):
  '''Return True if the sum has not converged to sufficient precision.'''
  if x == Decimal('0'):
    return True
  elif abs(x - x_prev) >= precision:
    return True
  else:
    return False

sum = Decimal('0')
sum_prev = sum
k = 0
while not_converged(sum, sum_prev):
  sum_prev = sum
  numer = factorial(6 * k) * (13591409 + 545140134 * k)
  denom = factorial(3 * k) * factorial(k)**3 * (-640320)**(3 * k)
  frac = Decimal(str(numer)) / Decimal(str(denom))
  frac *= 12 / (Decimal('640320')**3).sqrt()
  sum += frac
  k += 1

pi_string = str(1 / sum)
print 'The 1000th digit of pi after the decimal is:', pi_string[1001]
