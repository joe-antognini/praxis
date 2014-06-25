#! /usr/bin/env python

def gen_table(filename):
  '''
  Generate a table of three-word strings from a learning text.

  Parameters:
    filename: string
      Name of the file containing the learning text.

  Returns:
    tbl: list
      A dictionary in which two words index the third in a consecutive
      string.
  '''

  with open(filename) as infile:
    tbl = []
    for line in infile:
      words = line.split()
      for i in range(len(words[:-2])):
        lst
        
