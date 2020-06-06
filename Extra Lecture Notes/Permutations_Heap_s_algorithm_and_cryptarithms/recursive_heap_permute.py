# COMP9021 Term 3 2019


'''
A recursive implementation of Heap's algorithms to generate the
permutations of a list.
'''


def heap_permute_by_recursion(L):
    '''
    >>> list(list(L) for L in heap_permute_by_recursion([0]))
    [[0]]
    >>> list(list(L) for L in heap_permute_by_recursion([0, 1]))
    [[0, 1], [1, 0]]
    >>> list(list(L) for L in heap_permute_by_recursion([0, 1, 2]))
    [[0, 1, 2], [1, 0, 2], [2, 0, 1], [0, 2, 1], [1, 2, 0], [2, 1, 0]]
    >>> list(list(L) for L in heap_permute_by_recursion([0, 1, 2, 3]))
    [[0, 1, 2, 3], [1, 0, 2, 3], [2, 0, 1, 3], [0, 2, 1, 3], \
[1, 2, 0, 3], [2, 1, 0, 3], [3, 1, 0, 2], [1, 3, 0, 2], [0, 3, 1, 2], \
[3, 0, 1, 2], [1, 0, 3, 2], [0, 1, 3, 2], [0, 2, 3, 1], [2, 0, 3, 1], \
[3, 0, 2, 1], [0, 3, 2, 1], [2, 3, 0, 1], [3, 2, 0, 1], [3, 2, 1, 0], \
[2, 3, 1, 0], [1, 3, 2, 0], [3, 1, 2, 0], [2, 1, 3, 0], [1, 2, 3, 0]]
    '''
    yield from recursive_heap_permute(L, len(L))


def recursive_heap_permute(L, length):
    if length <= 1:
        yield L
    else:
        length -= 1
        for i in range(length):
            yield from recursive_heap_permute(L, length)
            if length % 2:
                L[i], L[length] = L[length], L[i]
            else:
                L[0], L[length] = L[length], L[0]
        yield from recursive_heap_permute(L, length)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
