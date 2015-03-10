#! /usr/bin/env python

import numpy as np

def digits_list(n):
  '''Return a list of the digits of an integer.'''
  ret = [(n / 10**i) % 10 for i in range(int(np.log10(n)) + 1)]
  ret.reverse()
  return ret

def from_digits_list(lst):
  '''Return an integer from the digits list.'''
  lst.reverse()
  n = 0
  for i, d in enumerate(lst):
    n += d * 10**i
  return n

def is_descending(n):
  '''Return True if the digits of the number are descending, False
  otherwise.'''

  prev_i = np.inf
  for i in digits_list(n):
    if i >= prev_i:
      return False
    prev_i = i

  return True

def magic1089(n):
  '''Do the Magic 1089 trick.'''
  
  if n < 100 or n >= 1000:
    raise ValueError('magic1089(): input must be three digits number')
  if not is_descending(n):
    raise ValueError('magic1089(): digits must be descending')
  
  digits = digits_list(n)
  rev_digits = digits[::-1]
  rev_n = from_digits_list(rev_digits)

  diff = n - rev_n
  rev_diff = from_digits_list(digits_list(diff)[::-1])

  return diff + rev_diff
