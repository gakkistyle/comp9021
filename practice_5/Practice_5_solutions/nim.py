# COMP9021 Practice 5 - Solutions

from functools import reduce
from itertools import cycle
from operator import xor
from random import choice, randrange, seed
import sys


def nim_sum(piles):
    return reduce(xor, piles)

def display_piles(piles):
    squares = {False: '  ', True: '\u2b1b'}
    for h in range(max(piles), 0, -1):
        print('  '.join(squares[e >= h] for e in piles))

def random_move(piles, nonempty_locations):
    location = choice(nonempty_locations)
    update_piles(piles, nonempty_locations, location, randrange(piles[location]))

def smart_move(piles, nonempty_locations):
    the_nim_sum = nim_sum(piles)
    leftmost_1 = 1 << the_nim_sum.bit_length() - 1
    for location in nonempty_locations:
        if leftmost_1 & piles[location]:
            update_piles(piles, nonempty_locations, location, piles[location] ^ the_nim_sum)
            break

def update_piles(piles, nonempty_locations, location, nb_of_tokens_left):
    piles[location] = nb_of_tokens_left
    if not nb_of_tokens_left:
        nonempty_locations.remove(location)


try:
    piles = [int(n) for n in input('Describe the piles: ').split()]
    if any(n < 0 for n in piles):
        raise ValueError
except ValueError:
    print('Incorrect description, giving up!')
nonempty_locations = [i for i in range(len(piles)) if piles[i]]
players = 'First', 'Second'
winner = players[0] if nim_sum(piles) else players[1]
print(f'\n{winner} player will play smart and win!')
try:
    seed(int(input('Input seed if desired: ')))
except ValueError:
    pass
print('\nGame to be played:')
display_piles(piles)
players_turns = cycle(players)
while nonempty_locations:
    player = next(players_turns)
    if player == winner:
        print(f'\n{player} player making smart move:')
        smart_move(piles, nonempty_locations)
    else:
        print(f'\n{player} player making random move:')
        random_move(piles, nonempty_locations)
    display_piles(piles)
