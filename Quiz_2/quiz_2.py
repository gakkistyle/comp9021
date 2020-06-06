# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 *** Due Thursday Week 3


import sys
from random import seed, randrange
from pprint import pprint
from collections import defaultdict
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

# INSERT YOUR CODE HERE

#use list done to store the keys that already being circles,
# so long as the keys have been recorded,we use continue to go on searching the next key
done = []
#search every key in mapping's keys and as long as mapping[key] is in keys,
# go on searching.Use a list called ready to record keys and values in every loop.
# until value matches the first key,which means we find out a circle,
#and if the value matches other values in the ready list,which means
# the following keys can be a circle,we break the while loop.
for key in mapping.keys():
    if key in done:
        continue
    if key == mapping[key]:
        done.append(key)
        cycles.append([key])
    else:
        ready = []
        value = mapping[key]
        ready.append(key)
        ready.append(value)
        while value in mapping.keys():
            next_key = value
            value = mapping.get(next_key)
            if ready[0] == value:
                done.extend(ready)
                cycles.append(ready)
                break
            elif value in ready:
                break
            ready.append(value)

"""
# what a piece of shit I wrote the first time!It can't work out the problem and got 
# me totally confused and frustrated.
kl = len(key)
subcycles = []
order_number = []
bingo = 0
for i in range(0,kl):
    for j in range(0,kl):
        if key[i] == value[j]:
            if i == j:
                bingo = 1
                order_number.append(i)
                break
            m = i
            n = j
            order_number = [i,j]
            while key[m] in value and key[n] in value and value[m] in key and value[n] in key:
                for k in range(0,kl):
                    if key[m] == value[k]:
                        m = k
                        order_number.append(m)
                        break
                for k in range(0,kl):
                    if value[n] == key[k]:
                        n = k
                        order_number.append(n)
                        break
                if m == n or key[m] == value[n]:
                    bingo = 1
                    break
            if bingo == 0:
                order_number=[]
    for e in order_number:
        if key[e] not in value or value[e] not in key:
            bingo = 0
    if bingo == 1:
        o2 = list(set(order_number))
        o2.sort()
        for e in o2:
            subcycles.append(key[e])
        cycles.append([e for e in subcycles])
        order_number=[]
        subcycles=[]
        bingo = 0
    else:
        order_number=[]
cycles.sort()
cycles2=[]
[cycles2.append(i) for i in cycles if not i in cycles2]
"""

key = list(mapping.keys())
value = list(mapping.values())
def indexs(num,value):
    indexk = []
    for _ in range(len(value)):
        if num == value[_]:
            indexk.append(key[_])
    return indexk,len(indexk)
count = []
dic = {}
o = list(set(value))
o.sort()
for v in o:
    dic[v],counts = indexs(v,value)
    count.append(counts)
count_ = list(set(count))
count_.sort()
for i in count_:
    Megadic = {}
    for k in dic.values():
        if len(k) == i:
            Megadic[mapping[k[0]]] = k
    reversed_dict_per_length[i] = Megadic


print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)


