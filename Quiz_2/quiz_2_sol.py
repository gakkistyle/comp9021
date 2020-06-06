# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 Solution

import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

keys_in_cycles = set()
for key in keys:
    if key in keys_in_cycles:
        continue
    i = key
    cycle = []
    while i not in cycle and i in keys:
        cycle.append(i)
        i = mapping[i]
    if i == key:
        cycles.append(cycle)
        keys_in_cycles.update(cycle)

reversed_dict = {value: [key for key in mapping if mapping[key] == value]
                 for value in sorted(mapping.values())
                }
lengths = sorted({len(reversed_dict[key]) for key in reversed_dict})
reversed_dict_per_length = {length : {key: reversed_dict[key]
                                         for key in reversed_dict
                                            if len(reversed_dict[key]) == length
                                     } for length in lengths
                           }

print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)

