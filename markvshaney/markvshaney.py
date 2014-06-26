#! /usr/bin/env python

def add_string(tbl, word1, word2, word3):
  '''
  Add the string of words to the table.  The first two words are the key and
  the third is appended to a list containing all words following the first
  two.
  '''

  # TODO Fix bug in which tbl[key] returns None
  key = ' '.join([word1, word2])
  if key in tbl:
    lst = tbl[key]
    print lst
    tbl[key] = lst.append(word3)
  else:
    tbl[key] = [word3]

  return tbl

def gen_table(filename, tbl={}):
  '''
  Generate a table of three-word strings from a learning text.

  Parameters:
    filename: string
      Name of the file containing the learning text.

    tbl: dictionary, optional
      A dictionary to append the new learning text to.

  Returns:
    tbl: list
      A dictionary in which two words index the third in a consecutive
      string.
  '''

  # We will store the data as a dictionary.  The dictionary is indexed by
  # the first two words of a three word string.  The entry is a list
  # composed of the set of all words following the first two words.

  # TODO Deal with edge cases of empty or 1 word lines
  with open(filename) as infile:
    firstline = True
    for line in infile:
      words = line.split()
      if not firstline:
        word1, word2 = words[:2]
        tbl = add_string(tbl, prev1, prev2, word1)
        tbl = add_string(tbl, prev2, word1, word2)
      for i in range(len(words[:-2])):
        word1, word2, word3 = words[i:i+3]
        tbl = add_string(tbl, word1, word2, word3)
      prev1, prev2 = words[-2:]
      firstline = False
  
  return tbl

def markvshaney(tbl, maxwords=500, maxchar=80):
  '''
  Run the Mark V. Shanney algorithm given a table three word strings and
  print out a given number of words of random text.  The code will exceed
  the given number in order to complete a sentence.

  Parameters:
    tbl: dictionary
      A table indexed by two word strings that returns a list containing all
      possible third words following the first two.

    maxwords: int, optional
      The number of words of text to generate.  The code will exceed this
      number to complete a sentence.

    maxchar: int, optional
      The maximum number of characters of text to print to a line.

  Returns:
    Prints text
  '''

  import random
  nwords = 0
  nchar = 0

  # Start with a random key
  key = random.choice(tbl.keys()).split()
  while nwords <= maxwords:
    word1, word2 = key.split()
    word3 = random.choice(tbl[key])

    nchar += len(word1) + 1
    if nchar >= maxchar:
      print 
      nchar = len(word1) + 1
    print word1,

    key = ' '.join([word2, word3])

if __name__ == '__main__':
  tbl = gen_table('dickens.txt')
  markvshaney(tbl)
