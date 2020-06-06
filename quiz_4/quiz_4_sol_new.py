# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 Solution
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition: a word of the form $s(w_1,...,w_n)$ with $s$
# denoting a symbol and  $w_1$, ..., $w_n$ denoting either valid words
# or symbols, with spaces allowed at both ends and around parentheses
# and commas, is a valid word (as a particular case, when $n=0$,
# a word is valid iff it is a symbol).


import sys


def is_valid(word, arity):
    # Create "skeleton", a new word built from the first argument
    # by removing all spaces and replacing all symbols with X.
    in_word = False
    skeleton = []
    for c in word:
        if c == ' ':
            in_word = False # added by rachid in the new version 
            continue
        if c in ',()':
            skeleton.append(c)
            in_word = False
        elif not c.isalpha() and c != '_':
            return False
        elif not in_word:
            in_word = True
            skeleton.append('X')
    skeleton = ''.join(skeleton)
    if arity == 0:
        return skeleton == 'X'
    if skeleton == 'X':
        return arity == 0
    pattern = 'X(' + 'X,' * (arity - 1) + 'X)'
    while True:
        compressed_skeleton = skeleton.replace(pattern, 'X')
        if compressed_skeleton == skeleton:
            break
        skeleton = compressed_skeleton
    return skeleton == 'X'

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')
