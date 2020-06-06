# COMP9021 Term 3 2019


from random import shuffle


def bubble_sort(L):
    '''
    >>> L = []
    >>> bubble_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> bubble_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> bubble_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> bubble_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> bubble_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> bubble_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> bubble_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    bound = len(L) - 1
    swapped = True
    while swapped and bound:
        swapped = False
        for i in range(bound):
            if L[i] > L[i + 1]:
                L[i], L[i + 1] = L[i + 1], L[i]
                swapped = True
                bound = i


if __name__ == '__main__':
    import doctest
    doctest.testmod()
