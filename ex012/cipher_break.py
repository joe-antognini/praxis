#! /usr/bin/env python

from math import log
from scipy.stats import binom
import numpy
import binascii
import string
import sys

en_freq_table = {
  'a' : .08167,
  'b' : .01492,
  'c' : .02782,
  'd' : .04253,
  'e' : .12702,
  'f' : .02228,
  'g' : .02015,
  'h' : .06094,
  'i' : .06966,
  'j' : .00153,
  'k' : .00772,
  'l' : .04025,
  'm' : .02406,
  'n' : .06749,
  'o' : .07507,
  'p' : .01929,
  'q' : .00095,
  'r' : .05987,
  's' : .06327,
  't' : .09056,
  'u' : .02758,
  'v' : .00978,
  'w' : .02360,
  'x' : .00150,
  'y' : .01974,
  'z' : .00074,
  '.' : .01306,
  ',' : .01232,
  ';' : .00064,
  ':' : .00068,
  '!' : .00066,
  '?' : .00112,
  '\'': .00486,
  '"' : .00534,
  '-' : .00306,
  ' ' : .16667,
  '\n': 1e-2}

def read_cipher(filename):
  '''Read in the cipher and return it as a string of bytes.'''

  intdata = []
  with open(filename) as infile:
    for line in infile:
      for n in line.split():
        intdata.append(int(n))

  encrypt_str = ''.join(map(chr, intdata))
  return encrypt_str

def fixedXOR(a, b):
  '''Take the XOR of two equal length arrays of bytes.'''

  # Make sure the data are the same length.
  if len(a) != len(b):
    raise ValueError('fixedXOR(): data arrays must be the same length!')
  if type(a) is not str or type(b) is not str:
    raise TypeError('fixedXOR(): input must be a string!')

  c = ''.join(map(chr, [ord(i) ^ ord(j) for i, j in zip(a, b)]))
  return c

def score_string(s):
  '''Score a string based on its letter frequency compared to the average
  English letter frequencies.  This is done by returning a log likelihood for
  the given frequency distribution in the input string.

  Parameters:
    s: str

  Returns:
    lenscore: float
      The primary score based on how many characters in the alphabet the
      string returns.
    freqscore: float
      The secondary score based on letter frequencies.
  '''

  # Typechecking
  if type(s) is not str:
    raise TypeError('score_string(): input must be string!')

  s_letter_count = {}
  for letter in en_freq_table:
    s_letter_count[letter] = 0

  # Get the frequency distribution
  for char in s:
    if char in string.ascii_uppercase:
      s_letter_count[char.lower()] += 1
    elif char in en_freq_table:
      s_letter_count[char] += 1
    elif ord(char) > 126:
      return (0, -numpy.inf)

  total_letters = sum(s_letter_count.values())
  if total_letters == 0:
    return (0, -numpy.inf)

  score = 0
  for char in s_letter_count:
    score += log(binom.pmf(s_letter_count[char], total_letters, 
               en_freq_table[char]))

  return (total_letters, score)

def single_byte_xor(instring):
  '''Crack a cypher that has been xor'd against a single character.'''
  maxscore = (0, -numpy.inf)
  maxstring = ''
  maxchar = ''
  for char in [chr(x) for x in range(128)]:
    s = fixedXOR(instring, (len(instring) / len(char)) * char)
    lenscore, freqscore = score_string(s)
    if lenscore > maxscore[0]:
      maxscore = (lenscore, freqscore)
      maxstring = s
      maxchar = char
    elif lenscore == maxscore[0] and freqscore > maxscore[1]:
      maxscore = (lenscore, freqscore)
      maxstring = s
      maxchar = char
  return (maxstring, maxchar)

def hamming_distance(str1, str2):
  '''Compute the Hamming distance between str1 and str2 (represented as
  bytes).'''

  distance = 0
  for a, b in zip(str1, str2):
    for x, y in zip('{0:08b}'.format(ord(a)), '{0:08b}'.format(ord(b))):
      if x != y:
        distance += 1

  return distance

def find_keysize(data):
  '''Given a string of bytes find the keysize by finding the smallest edit
  distance between blocks of different keysizes.'''

  key_distances = []  
  for keysize in range(1, 20*8):
    blocks = [data[i*keysize:(i+1)*keysize] for i in range(4)]
    block_distances = []
    for i in range(len(blocks)-1):
      block1 = blocks[i]
      for block2 in blocks[i+1:]:
        block_distances.append(hamming_distance(block1, block2))
    key_distances.append(float(sum(block_distances)) / len(block_distances)
      / keysize)

  min_keysize = key_distances.index(min(key_distances)) + 1
  return min_keysize

def break_repeating_key_xor(data):
  '''Break text that has been encrypted with repeating key XOR.'''
  keysize = find_keysize(data)
  blocks = [data[i::keysize] for i in range(keysize)]
  decrypt_blocks = []
  decrypt_key = ''
  for block in blocks:
    decrypt_data = single_byte_xor(block)
    decrypt_blocks.append(decrypt_data[0])
    decrypt_key += decrypt_data[1]
  decrypt_str = ''
  for i in range(len(decrypt_blocks[0])):
    for block in decrypt_blocks:
      if i < len(block):
        decrypt_str += block[i]
  return (decrypt_str, decrypt_key[:(keysize/6)])

if __name__ == '__main__':
  encrypt_data = read_cipher('cipher.txt')
  decrypt_data =  break_repeating_key_xor(encrypt_data)
  print "Key:", decrypt_data[1]
  print "Decrypted text:"
  print decrypt_data[0]
