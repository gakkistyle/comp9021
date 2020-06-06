# COMP9021 Practice 2 - Solutions


'''
Prompts the user to input an integer N at least equal to 10 and computes
the number of trailing 0's in N! in three different ways.
'''


import sys
from math import factorial


def first_computation(x):
    nb_of_trailing_0s = 0
    while x % 10 == 0:
        nb_of_trailing_0s += 1
        x //= 10
    return nb_of_trailing_0s

def second_computation(x):
    if len(x) < 2:
        return 0
    i = 1
    while True:
        if x[-i] != '0':
            return i - 1
        i += 1

def third_computation(x):
    nb_of_trailing_0s = 0
    power_of_five = 5
    while x >= power_of_five:
        nb_of_trailing_0s += x // power_of_five
        power_of_five *= 5
    return nb_of_trailing_0s


try:
    the_input = int(input('Input a nonnegative integer: '))
    if the_input < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
the_input_factorial = factorial(the_input)
print(f'Computing the number of trailing 0s in {the_input}! by dividing by 10 for long enough:',
      first_computation(the_input_factorial))
print(f'Computing the number of trailing 0s in {the_input}! by converting it into a string:',
      second_computation(str(the_input_factorial)))
print(f'Computing the number of trailing 0s in {the_input}! the smart way:',
      third_computation(the_input))
