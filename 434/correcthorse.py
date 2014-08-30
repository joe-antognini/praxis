#! /usr/bin/env python

def correcthorse(password_length=4):
  '''
  Generate a password from random common English words.

  Parameters:
    password_length: int, optional
      The number of words in the password

  Returns:
    password: string
      A password consisting of common English words
  '''

  import random

  if type(password_length) is not int:
    raise ValueError('correcthorse(): password length must be integer')
  elif password_length <= 0:
    raise ValueError(
      'correcthorse(): password length must be positive definite.')

  words = []
  with open('google-10000-english-master/google-10000-english.txt') as infile:
    for line in infile:
      words.append(line)

  password = []
  for i in range(password_length):
    word = random.choice(words).strip()
    while (len(word) == 1) and (word != 'a' and word != 'i'):
      word = random.choice(words).strip()
    password.append(word)

  return ' '.join(password)

if __name__ == '__main__':
  print correcthorse()
