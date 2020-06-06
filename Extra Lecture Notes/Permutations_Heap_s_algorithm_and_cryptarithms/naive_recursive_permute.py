# COMP9021 Term 3 2019


'''
A naive recursive method to generate all permutations of a set.
'''


def naive_recursive_permute(S):
    '''
    >>> list(naive_recursive_permute({0}))
    [[0]]
    >>> list(naive_recursive_permute({0, 1}))
    [[0, 1], [1, 0]]
    >>> list(naive_recursive_permute({0, 1, 2}))
    [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    >>> list(naive_recursive_permute({0, 1, 2, 3}))    
    [[0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], \
[0, 3, 1, 2], [0, 3, 2, 1], [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], \
[1, 2, 3, 0], [1, 3, 0, 2], [1, 3, 2, 0], [2, 0, 1, 3], [2, 0, 3, 1], \
[2, 1, 0, 3], [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0], [3, 0, 1, 2], \
[3, 0, 2, 1], [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0]]
    '''
    if len(S) <= 1:
        yield list(S)
    else:
        for x in S:
            for P in naive_recursive_permute(S - {x}):
                yield [x] + P


if __name__ == '__main__':
    import doctest
    doctest.testmod()
