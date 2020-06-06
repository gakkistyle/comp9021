# COMP9021 Term 3 2019


from random import shuffle


def selection_sort(L):
    '''
    >>> L = []
    >>> selection_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> selection_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> selection_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> selection_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> selection_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> selection_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> selection_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    for i in range(len(L) - 1):
        index_of_min = i
        for j in range(i + 1, len(L)):
            if L[j] < L[index_of_min]:
                index_of_min = j
        if index_of_min != i:
            L[i], L[index_of_min] = L[index_of_min], L[i]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
