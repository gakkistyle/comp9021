# COMP9021 Practice 1 - Solutions


'''
Prompts the user for a strictly positive integer, nb_of_elements,
generates a list of nb_of_elements random integers between -50 and 50, prints out the list,
computes the mean, the median and the standard deviation in two ways,
that is, using or not the functions from the statistics module, and prints them out.
'''


from random import seed, randint
from math import sqrt
from statistics import mean, median, pstdev
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
# Generates a list of nb_of_elements random integers between -50 and 50.
seed(arg_for_seed)
L = [randint(-50, 50) for _ in range(nb_of_elements)]
# Prints out the list, computes the mean and standard deviation and median of the list,
# and prints them out.
print('\nThe list is:' , L)
print()
the_mean = sum(L) / nb_of_elements
the_standard_deviation = sqrt(sum(x ** 2 for x in L) / nb_of_elements - the_mean ** 2)
L.sort()
the_median = L[nb_of_elements // 2] if nb_of_elements % 2 else\
                                         (L[(nb_of_elements - 1) // 2] + L[nb_of_elements // 2]) / 2
print(f'The mean is {the_mean:.2f}.')
print(f'The median is {the_median:.2f}.')
print(f'The standard deviation is {the_standard_deviation:.2f}.')
print('\nConfirming with functions from the statistics module:')
print(f'The mean is {mean(L):.2f}.')
print(f'The median is {median(L):.2f}.')
print(f'The standard deviation is {pstdev(L):.2f}.')

