# COMP9021 Practice 1 - Solutions


'''
Prompts the user for a strictly positive integer, nb_of_elements,
generates a list of nb_of_elements random integers between 0 and 19, prints out the list,
computes the number of elements strictly less 5, 10, 15 and 20, and prints those out.
'''


from random import seed, randrange
import sys


# Prompts the user for a seed for the random number generator,
# and for a strictly positive number, nb_of_elements.
try:
    arg_for_seed = int(input('Input a seed for the random number generator: '))
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()   
try:
    nb_of_elements = int(input('How many elements do you want to generate? '))
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()
if nb_of_elements <= 0:
    print('Input should be strictly positive, giving up.')
    sys.exit()
# Generates a list of nb_of_elements random integers between 0 and 19.
seed(arg_for_seed)
L = [randrange(20) for _ in range(nb_of_elements)]
print('\nThe list is:', L)
print()
# - intervals[0] to record the number of elements between 0 and 4,
#   that is, elements e such that e // 5 == 0
# - intervals[1] to record the number of elements between 5 and 9
#   that is, elements e such that e // 5 == 1
# - intervals[2] to record the number of elements between 10 and 14
#   that is, elements e such that e // 5 == 2
# - intervals[3] to record the number of elements between 15 and 19
#   that is, elements e such that e // 5 == 3
intervals = [0] * 4
for e in L:
    intervals[e // 5] += 1
for i in range(4):
    if intervals[i] == 0:
        print('There is no element', end = ' ')
    elif intervals[i] == 1:
        print('There is 1 element', end = ' ')
    else:
        print(f'There are {intervals[i]} elements', end = ' ')
    print(f'between {5 * i} and {5 * i + 4}.')
