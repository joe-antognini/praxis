#! /usr/bin/env python

#
# longest_palindrome
#
# Find the longest palindrome in a string.
#

def longest_palindrome(s):
  '''Find the longest palindrome in a string.'''

  # First find all instances of a three-string palindrome, e.g., 'aba'
  max_length = 0
  for i in range(1, len(s)-1):
    # First do odd-length palindromes
    palindrome_length = 1
    j = 1
    while s[i-j] == s[i+j]: 
      palindrome_length += 2
      j += 1

      # Make sure we don't go out of bounds
      if (i - j < 0) or (i + j >= len(s)):
        break

    if palindrome_length > max_length:
      max_index = i
      max_length = palindrome_length

    # Next do even-length palindromes
    palindrome_length = 0
    j = 0
    while s[i-j] == s[i+1+j]:
      palindrome_length += 2
      j += 1

      # Make sure we don't go out of bounds
      if (i - j < 0) or (i + j + 1 >= len(s)):
        break

    if palindrome_length > max_length:
      max_index = i
      max_length = palindrome_length

  if max_length % 2 == 1:
    return s[max_index-(max_length-1)/2:max_index+(max_length-1)/2+1]
  else:
    return s[max_index-max_length/2-1:max_index+max_length/2+1]

if __name__ == '__main__':

  STRING = 'FourscoreandsevenyearsagoourfaathersbroughtforthonthiscontainentanewnationconceivedinzLibertyanddedicatedtothepropositionthatallmenarecreatedequalNowweareengagedinagreahtcivilwartestingwhetherthatnaptionoranynartionsoconceivedandsodedicatedcanlongendureWeareqmetonagreatbattlefiemldoftzhatwarWehavecometodedicpateaportionofthatfieldasafinalrestingplaceforthosewhoheregavetheirlivesthatthatnationmightliveItisaltogetherfangandproperthatweshoulddothisButinalargersensewecannotdedicatewecannotconsecratewecannothallowthisgroundThebravelmenlivinganddeadwhostruggledherehaveconsecrateditfaraboveourpoorponwertoaddordetractTgheworldadswfilllittlenotlenorlongrememberwhatwesayherebutitcanneverforgetwhattheydidhereItisforusthelivingrathertobededicatedheretotheulnfinishedworkwhichtheywhofoughtherehavethusfarsonoblyadvancedItisratherforustobeherededicatedtothegreattdafskremainingbeforeusthatfromthesehonoreddeadwetakeincreaseddevotiontothatcauseforwhichtheygavethelastpfullmeasureofdevotionthatweherehighlyresolvethatthesedeadshallnothavediedinvainthatthisnationunsderGodshallhaveanewbirthoffreedomandthatgovernmentofthepeoplebythepeopleforthepeopleshallnotperishfromtheearth'

  print longest_palindrome(STRING)
