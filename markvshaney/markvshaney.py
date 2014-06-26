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

  # We will store the data as a dictionary.  The dictionary is indexed by
  # the first two words of a three word string.  The entry is a list
  # composed of the set of all words following the first two words.

  with open(filename) as infile:
    tbl = {}
    for line in infile:
      words = line.split()
      for i in range(len(words[:-2])):
        word1, word2 = words[i:i+2]
        
