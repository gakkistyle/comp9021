# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 *** Due Thursday Week 5
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.


import sys


def is_valid(word, arity):
    nb_of_Left_parenthesis = 0
    nb_of_right_parenthesis = 0
    nb_of_comma = 0
    word_no_space = ''.join(word.split(' '))
    if len(word_no_space) == 0:
        return False
    for j in range(len(word)):
        if j!=0 and word[j] == ' ' and (word[j-1].isalpha() or word[j-1] =='_'):
            while(word[j] == ' '):
                j = j+1
            if word[j] == '_' or word[j].isalpha():
                return False
    for i in range(len(word_no_space)):
        if arity == 0:
            for e in word_no_space:
                if e.isalpha() == False and e != '_':
                    return False
            return True
        if word_no_space[i].isalpha() == False \
                and word_no_space[i] != ',' and word_no_space[i] != '(' and word_no_space[i] != ')' \
                and word_no_space[i] != '_' :
            return False
        if word_no_space[i] == ',':
            if  i == len(word_no_space)-1 or word_no_space[i-1] == '('\
               or word_no_space[i+1] == ')'  or word_no_space[i+1] == '('or word_no_space[i+1] == ',' :
                return  False
            else:
                nb_of_comma += 1
        if word_no_space[i] == '(':
            if  i == len(word_no_space)-1 or word_no_space[i+1] == ')'   \
                or (word_no_space[i-1].isalpha() == False and word_no_space[i-1] != '_'):
                return False
            else:
                nb_of_Left_parenthesis += 1
        if word_no_space[i]  == ')':
            if i != len(word_no_space)-1 and (word_no_space[i+1].isalpha() or word_no_space[i+1] == '_'):
                return False
            nb_of_right_parenthesis += 1
    if nb_of_right_parenthesis != nb_of_Left_parenthesis or \
        nb_of_Left_parenthesis==0  \
        or (arity-1)*nb_of_Left_parenthesis != nb_of_comma:
        return False
    else:
        return  True

    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

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

