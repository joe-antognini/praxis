#! /usr/bin/env python

#
# RPN Calculator
#
# Programming Praxis
# Problem 1
# http://programmingpraxis.com/2009/02/19/rpn-calculator/
#

import sys

# Define the operations
oper = {'+' : lambda a, b: a + b, 
        '-' : lambda a, b: a - b, 
        '*' : lambda a, b: a * b, 
        '/' : lambda a, b: a / b}

stack = sys.argv[1:]

while len(stack) > 1:
  # We go through every element
  for i in range(len(stack)):
    # Until we get to an operator.  Then we apply it to the last two
    # elements.
    if stack[i] in oper:
      a = float(stack.pop(i-2))
      b = float(stack.pop(i-2))

      stack[i-2] = oper[stack[i-2]](a, b)
      break

print stack[0]
