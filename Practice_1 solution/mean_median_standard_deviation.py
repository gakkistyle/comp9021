"""
 prompts the user for a strictly positive integer, 
 nb_of_elements, generates a list of nb_of_elements random 
 integers between - 50 and 50, prints out the list, computes the mean, 
 the median and the standard deviation in two ways, that is,using 
 or not the functions from the statistics module, and prints them out. 
"""

from random import seed,randrange
import sys
import numpy as np

try:
	arg_for_seed = int(input('Inout a seed for the random number generator: '))
except ValueError:
	print('Input is not an integer,giving up!')
	sys.exit()
try:
	nb_of_elements = int(input('How many elemnets do you want to generate? '))
except ValueError:
	print('Input is not an integer,giving up.')
	sys.exit()
if nb_of_elements <= 0:
	print('Input should be strictly positive,giving up')
	sys.exit()

seed(arg_for_seed)
L = [randrange(-51,51) for _ in range(nb_of_elements)]
print('\nThe list is:',L)
print()

sum = 0
for l in L:
	sum +=l
mean = sum/nb_of_elements

L.sort()
if(nb_of_elements%2==0):
	median = (L[int((nb_of_elements-1)//2)]+L[int(nb_of_elements/2)])/2
else:
	median = L[int(nb_of_elements//2)]

sign = 0
for i in range(nb_of_elements):
	sign += (L[i]-mean)**2
standard_deviation = (sign/nb_of_elements)**0.5

print('The mean is %.2f.'%mean)
print('The median is %.2f.'%median)
print('The standard deviation is %.2f.'%standard_deviation)

print('')
print('Confirming with functions from the statistics module:')
print('The mean is %.2f.'%np.mean(L))
print('The median is %.2f.'%np.median(L))
print('The standard deviation is %.2f.'%np.std(L))










