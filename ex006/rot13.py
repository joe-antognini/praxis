#! /usr/bin/env python

#
# ROT13
#
# Programming Praxis
# Exercise 6
# http://programmingpraxis.com/contents/chron/
#

from string import *

def rot13(str):
  '''Returns a string with all alphabet characters shifted by 13
  letters.'''
  lst = []
  for char in str:
    if char in ascii_lowercase:
      i = ascii_lowercase.index(char)
      i += 13
      i %= 26
      lst.append(ascii_lowercase[i])
    elif char in ascii_uppercase:
      i = ascii_uppercase.index(char)
      i += 13
      i %= 26
      lst.append(ascii_uppercase[i])
    else:
      lst.append(char)

  return ''.join(lst)

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    test_str = 'Cebtenzzvat Cenkvf vf sha!'
    print rot13(test_str)
  else:
    arg_string = ' '.join(sys.argv[1:])
    print rot13(arg_string)
