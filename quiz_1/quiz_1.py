# COMP9021 19T3 - Rachid Hamadi
# Quiz 1 *** Due Thursday Week 2


import sys
from random import seed, randrange


try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 2, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)

mapping_as_a_list = []
one_to_one_part_of_mapping = {}
nonkeys = []

# INSERT YOUR CODE HERE

#nonkeys
for i in range (1,upper_bound):
	if i not in mapping.keys():
		nonkeys.append(i)

#mapping as a list
for i in range (0,upper_bound):
    if i not in mapping.keys():
        mapping_as_a_list.append(None)
    else:
        mapping_as_a_list.append(mapping[i])

#one-to-one part
#I use two loops to compare all the elenment in the mapping_as_a_list
#(mapping_as_a_list has the same value of the mapping),if the program finds
#two equal values,the trigger which is  0 will turn to 1,indicating the
#one_to_one_part_of_mapping will not take this value.
for i in range (0,upper_bound):
    trigger = 0
    if mapping_as_a_list[i] != None:
        for j in range(0,upper_bound):
            if(mapping_as_a_list[i]==mapping_as_a_list[j] and i!=j):
                trigger = 1
                break
        if trigger ==0:
            one_to_one_part_of_mapping[i]=mapping_as_a_list[i]

print()
print('The mappings\'s so-called "keys" make up a set whose number of elements is '+str(len(mapping))+'.')
print('\nThe list of integers between 1 and', upper_bound - 1, 'that are not keys of the mapping is:')
print('  ', nonkeys)
print('\nRepresented as a list, the mapping is:')
print('  ', mapping_as_a_list)
# Recreating the dictionary, inserting keys from smallest to largest,
# to make sure the dictionary is printed out with keys from smallest to largest.
one_to_one_part_of_mapping = {key: one_to_one_part_of_mapping[key]
                                      for key in sorted(one_to_one_part_of_mapping)
                             }
print('\nThe one-to-one part of the mapping is:')
print('  ', one_to_one_part_of_mapping)


