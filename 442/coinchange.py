#! /usr/bin/env python

def coin_count(n, coins):
  '''Calculate the number of ways to produce n cents given an unlimited
  number of pennies, nickels, dimes, and quarters.

  Input:
    n: int
      The target number of cents
    coins: list
      The kinds of coins available

  Output:
    int
      The number of ways to reach the target number of cents
  '''

  if len(coins) == 0:
    return 0

  coin = coins.pop()
  if coin > n:
    return coin_count(n, coins[:])
  elif coin == n:
    return 1 + coin_count(n, coins[:])
  else:
    result1 = coin_count(n, coins[:])
    coins.append(coin)
    result2 = coin_count(n-coin, coins)
    return result1 + result2

def coin_list(n, coins):
  '''Calculate the number of combinations of coins that will produce n
  cents.

  Input:
    n: int
      The target number of cents
    coins: list
      The kinds of coins available

  Output:
    list
      A list of lists of combinations of coins that produce n cents.
  '''

  coin = coins.pop()
  if coin > n:
    if coins:
      return coin_list(n, coins[:])
    else:
      return []
  elif coin == n:
    if coins:
      result = coin_list(n, coins[:])
      result.append([n])
      return result
    else:
      return [[n]]
  else:
    if coins:
      result1 = coin_list(n, coins[:])
    else:
      result1 = []
    coins.append(coin)
    result2 = coin_list(n-coin, coins)
    result2[0].append(coin)
    return result1 + result2

if __name__ == '__main__':
  print coin_count(40, [1, 5, 10, 25])
  print coin_list(40, [1, 5, 10, 25])
