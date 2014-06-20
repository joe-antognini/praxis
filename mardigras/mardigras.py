#! /usr/bin/env python

def easter(y):
  '''
  Calculate the date of Easter.  The algorithm is due to J. M. Oudin (1940).

  Parameters:
    y: int
      The year to calculate the date of Easter

  Returns:
    date: date object
      The date of Easter
  '''

  import datetime

  if type(y) is not int:
    raise ValueError('year must be a string')

  c = y / 100
  n = y - 19 * (y / 19)
  k = (c - 17) / 25
  i = c - c / 4 - (c - k) / 3 + 19 * n + 15
  i = i - 30 * (i / 30)
  i = (i - (i / 28) * (1 - (i / 28) * (29 / (i + 1)) 
      * ((21 - n) / 11)))
  j = y + y / 4 + i + 2 - c + c / 4
  j = j - 7 * (j / 7)
  l = i - j
  m = 3 + (l + 40) / 44
  d = l + 28 - 31 * (m / 4)

  return datetime.date(y, m, d)

def mardigras(year):
  '''
  Calculate the date of Mardi Gras.  Mardi Gras is the Tuesday of the
  seventh week before Easter.

  Parameters:
    year: int
      The year to calculate the date of Mardi Gras
  
  Returns:
    date: date object
      The date of Mardi Gras
  '''

  import datetime
  return easter(year) + datetime.timedelta(weeks=-7, days=2)

if __name__ == '__main__':
  date1 = mardigras(1989)
  date2 = mardigras(2049)

  print date1.strftime('%B %-d, %Y')
  print date2.strftime('%B %-d, %Y')
