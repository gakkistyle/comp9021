# COMP9021 Term 3 2019


'''
Solves the tower and 2 glass marbles problem. The user is prompted to
enter a number n of levels of a tower. Using 2 marbles, one has to
discover the highest level, if any, such that dropping a marble from
that level makes it break, using a strategy that minimises the number of
drops in the worst case (it is assumed that any marble would break when
dropped from a level where one marble breaks, and also when dropped from
any higher level; the marbles might not break when dropped from any
level).

The idea is to ask: what is the maximum height h of a tower such that an
answer can always be found with no more than d drops? It is easy to
verify that h is the largest integer such that
d + (d - 1) + (d - 2) + ... + 2 + 1 >= h, and that the strategy consists
in dropping the first glass from level d, then from level d + (d - 1),
then from level d + (d - 1) + (d - 2), ..., until the marble breaks, if
that ever happens. In case that happens and i is the least integer such
that the glass breaks when dropped from level
d + ... + (d - i - 1) + (d - i), then one drops the second glass from
level d + ... + (d - i - 1) + 1, and then from level
d + ... + (d - i - 1) + 2, etc., until the glass breaks, if that ever
hapens.
'''


from math import sqrt, ceil
from random import randint


while True:
    # The n from the program description.
    n = input('Enter the number of levels '
              '(a strictly positive number): '
             )
    try:
        n = int(n)
        if n <= 0:
            raise ValueError
        break
    except ValueError:
        print('Incorrect input, try again.')
d = ceil((sqrt(8 * n + 1) - 1) / 2)
if d == 1:
   print('At most 1 drop will be needed.\n')
else:
   print('At most', d, 'drops will be needed.\n')
# The highest level such that it is known that a marble dropped from
# that level does not break.
low = 0
# The smallest level such that it is known that a marble dropped from
# that level breaks (it is convenient to assume that a glass dropped
# from a level one more than the height of the tower breaks).
high = n + 1
drop = 0
which_marble = 'first'
# We randomly make marbles break on one of levels 1, 2, ..., n + 1
# (in case the value is n + 1, the marble does not break when dropped
# from any level of the tower).
breaking_level = randint(1, n + 1)
while low < high - 1:
    level = min(low + d, high - 1)
    drop += 1
    if breaking_level <= level:
       print(f'Drop #{drop} with {which_marble} marble, '
             f'from level {level}... marble breaks!'
             )
       which_marble = 'second'
       high = level
       d = 1
    else:
       print(f'Drop #{drop} with {which_marble} marble, '
             f'from level {level}... marble does not break!'
             )
       low = level
       if d > 1:
           d -= 1
if high == n + 1:
    print('Marbles are of best quality and do not break.')
elif high == 1:
    print(f'Marbles break when dropped from the first level.')
else:
    print(f'Marbles break when dropped from level {high}, not below.')        
