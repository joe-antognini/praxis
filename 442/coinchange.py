#! /usr/bin/env python

def coin_count(n):
  '''Calculate the number of ways to produce n cents given an unlimited
  number of pennies, nickels, dimes, and quarters.

  Input:
    n: int
      The target number of cents

  Output:
    int
      The number of ways to reach the target number of cents
  '''

  count = 0
  coins = (1, 5, 10, 25)
  for coin in coins:
    if coin > n:
      continue
    elif n == coin:
      count += 1
    else:
      count += coin_count(n - coin)
  return count

if __name__ == '__main__':
  print coin_count(6)
