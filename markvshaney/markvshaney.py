#! /usr/bin/env python

def add_string(tbl, words):
  '''
  Add the string of words to the table.  The first two words are the key and
  the third is appended to a list containing all words following the first
  two.

  Parameters:
    tbl: dictionary
      The dictionary to which the new entiry will be added.

    words: list
      The sequence of words to be added to the dictionary.
  '''

  key = ' '.join([words[0], words[1]])
  if key in tbl:
    lst = tbl[key][:]
    lst.append(words[2])
    tbl[key] = lst
  else:
    tbl[key] = [words[2]]

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

  # First read the entire file into memory and generate a list containing
  # all words in order.
  with open(filename) as infile:
    lst = []
    for line in infile:
      words = line.split()
      for word in words:
        lst.append(word.strip())

  # Now generate the dictionary.
  for i in range(len(lst)-2):
    tbl = add_string(tbl, lst[i:i+3])
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
  key = random.choice(tbl.keys())
  while not key.istitle():
    key = random.choice(tbl.keys())
  while (nwords <= maxwords) or (word3[-1] != '.'):
    word1, word2 = key.split()
    word3 = random.choice(tbl[key])

    nchar += len(word1) + 1
    if nchar >= maxchar:
      print 
      nchar = len(word1) + 1
    print word1,
    nwords += 1

    key = ' '.join([word2, word3])

  print word2, word3,

if __name__ == '__main__':
  tbl = gen_table('iliad.txt')
  markvshaney(tbl)
