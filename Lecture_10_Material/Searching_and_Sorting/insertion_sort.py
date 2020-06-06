# COMP9021 Term 3 2019


from random import shuffle


def insertion_sort(L):
    '''
    >>> L = []
    >>> insertion_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> insertion_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> insertion_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> insertion_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> insertion_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> insertion_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> insertion_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    for i in range(1, len(L)):
        j = i
        while j and L[j - 1] > L[j]:
            L[j - 1], L[j] = L[j], L[j - 1]
            j -= 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
