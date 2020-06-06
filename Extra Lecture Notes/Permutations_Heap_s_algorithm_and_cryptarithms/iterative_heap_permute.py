# COMP9021 Term 3 2019


'''
An iterative implementation of Heap's algorithms to generate the
permutations of a list.
'''


def iterative_heap_permute(L):
    '''
    >>> list(list(L) for L in iterative_heap_permute([0]))
    [[0]]
    >>> list(list(L) for L in iterative_heap_permute([0, 1]))
    [[0, 1], [1, 0]]
    >>> list(list(L) for L in iterative_heap_permute([0, 1, 2]))
    [[0, 1, 2], [1, 0, 2], [2, 0, 1], [0, 2, 1], [1, 2, 0], [2, 1, 0]]
    >>> list(list(L) for L in iterative_heap_permute([0, 1, 2, 3]))
    [[0, 1, 2, 3], [1, 0, 2, 3], [2, 0, 1, 3], [0, 2, 1, 3], \
[1, 2, 0, 3], [2, 1, 0, 3], [3, 1, 0, 2], [1, 3, 0, 2], [0, 3, 1, 2], \
[3, 0, 1, 2], [1, 0, 3, 2], [0, 1, 3, 2], [0, 2, 3, 1], [2, 0, 3, 1], \
[3, 0, 2, 1], [0, 3, 2, 1], [2, 3, 0, 1], [3, 2, 0, 1], [3, 2, 1, 0], \
[2, 3, 1, 0], [1, 3, 2, 0], [3, 1, 2, 0], [2, 1, 3, 0], [1, 2, 3, 0]]
    '''
    yield L
    stack = [(0, i) for i in range(len(L) - 1, 0, -1)]
    while stack:
        low, high = stack.pop()
        if high % 2:
            L[low], L[high] = L[high], L[low]
        else:
            L[0], L[high] = L[high], L[0]
        yield L
        if low + 1 != high:
            stack.append((low + 1, high))
        for i in range(high - 1, 0, -1):
            stack.append((0, i))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
