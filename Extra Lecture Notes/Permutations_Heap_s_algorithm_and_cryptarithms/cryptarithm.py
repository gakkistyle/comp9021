# COMP9021 Term 3 2019


'''
Cryptarithm solver.
'''


def solve(cryptarithm):
    '''
    >>> solve('SEND + MORE == MONEY')
    9567 + 1085 == 10652
    >>> solve('DO + YOU + FEEL == LUCKY')
    57 + 870 + 9441 == 10368
    >>> solve('ZEROES + ONES == BINARY')
    698392 + 3192 == 701584
    '''
    letters_starting_a_word = set()
    letters_not_starting_a_word = set()
    in_word = False
    for c in cryptarithm:
        if str.isalpha(c):
            if not in_word:
                letters_starting_a_word.add(c)
                in_word = True
            else:
                letters_not_starting_a_word.add(c)
        else:
            in_word = False
    letters_not_starting_a_word -= letters_starting_a_word
    all_letters = list(letters_not_starting_a_word)\
                  + list(letters_starting_a_word)
    if len(all_letters) > 10:
        print('There are more than 10 letters,',
              ' this is not a valid cryptarithm.'
             )
        return
    digits = [str(i) for i in range(10)]
    for _ in generate_possible_solutions(digits, len(letters_starting_a_word),
                                         len(letters_not_starting_a_word)
                                        ):
        equation = cryptarithm.translate(str.maketrans(dict(
                            zip(all_letters, digits[10 - len(all_letters) :])
                                                           )
                                                      )
                                        )
        try:
            if eval(equation): 
                print(equation)
        # Ignore divisions by 0
        except ArithmeticError:
            pass


# Permutes the last "length" members of L[: start + size], using "size"
# many indexes in L, the first of which is "start". Assumes that
# "length" is at most equal to "size".
def permute(digits, start, size, length):
    if length == 0:
        yield
        if size > 1:
            # "Simulates" the permutation of the "size" first elements
            # of L[start :] by computing what would be the last
            # permutation.
            if size % 2 or size == 2:
                digits[start], digits[start + size - 1] =\
                        digits[start + size - 1], digits[start]
            elif size == 4:
                digits[start : start + 3], digits[start + 3] =\
                        digits[start + 1 : start + 4], digits[start]
            else:
                digits[start : start + 2],\
                 digits[start + 2 : start + size - 2],\
                  digits[start + size - 2], digits[start + size - 1] =\
                   digits[start + size - 3 : start + size - 1],\
                    digits[start + 1 : start + size - 3],\
                     digits[start + size - 1], digits[start]
    else:
        size -= 1
        length -= 1
        for i in range(size):
            yield from permute(digits, start, size, length)
            if size % 2:
                digits[start + i], digits[start + size] =\
                        digits[start + size], digits[start + i]
            else:
                digits[start], digits[start + size] =\
                        digits[start + size], digits[start]
        yield from permute(digits, start, size, length)

# Generates permutations of digits where the last length_1 members of
# digits take arbitary nonzero values and the previous length_2 members
# of digits take other arbitary values (0 being possibly one of them).
def generate_possible_solutions(digits, length_1, length_2):
    adjusted_length_2 = length_2
    # Once nonzero digits have been allocated to all letters starting a
    # word, if all digits that remain have to be used for the letters
    # not starting a word, then there is no need to allocate the last
    # one once all others have been allocated.
    if length_2 == 10 - length_1:
        adjusted_length_2 -= 1
    adjusted_length_1 = length_1
    # If all nonzero digits have to be used for the letters starting a
    # word, then there is no need to allocate the last one once all
    # others have been allocated.
    if length_1 == 9:
        adjusted_length_1 -= 1
    size = 10 - length_1
    for _ in permute(digits, 1, 9, adjusted_length_1):
        first_size_digits = list(digits[: size])
        yield from permute(digits, 0, size, adjusted_length_2)
        digits[: size] = first_size_digits


if __name__ == '__main__':
    import doctest
    doctest.testmod()
