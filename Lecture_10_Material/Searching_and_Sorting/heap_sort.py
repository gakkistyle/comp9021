# COMP9021 Term 3 2019


from random import shuffle


def heap_sort(L):
    '''
    >>> L = []
    >>> heap_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> heap_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> heap_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> heap_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> heap_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> heap_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> heap_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    if len(L) < 2:
        return
    for i in range(len(L) // 2 - 1, -1, -1):
        bubble_down(L, i, len(L))
    for i in range(len(L) - 1, 2, -1):
        L[0], L[i] = L[i], L[0]
        bubble_down(L, 0, i)
    if len(L) > 2:
        L[0], L[2] = L[2], L[0]
    if L[0] > L[1]:
        L[0], L[1] = L[1], L[0]

def bubble_down(L, i, length):
    while True:
        index_of_greatest_child = 2 * i + 1
        if index_of_greatest_child >= length:
            return
        if (index_of_greatest_child < length - 1 and
                 L[index_of_greatest_child] < L[index_of_greatest_child + 1]):
            index_of_greatest_child = index_of_greatest_child + 1
        if L[i] >= L[index_of_greatest_child]:
            return
        else:
            L[i], L[index_of_greatest_child] = L[index_of_greatest_child], L[i]
        i = index_of_greatest_child


if __name__ == '__main__':
    import doctest
    doctest.testmod()
