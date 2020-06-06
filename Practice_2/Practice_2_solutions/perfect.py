# COMP9021 Practice 2 - Solutions


'''
Prompts the user for an integer N and finds all perfect numbers up to N.
Quadratic complexity, can deal with small values only.
'''


import sys


try:
    N = int(input('Input an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

for i in range(2, N + 1):
    # 1 divides i, so counts for one divisor.
    # It is enough to look at 2, ..., i // 2 as other potential divisors.
    if 1 + sum(j for j in range(2, i // 2 + 1) if i % j == 0) == i:
        print(i, 'is a perfect number.')
