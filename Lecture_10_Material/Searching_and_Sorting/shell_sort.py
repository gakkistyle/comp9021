# COMP9021 Term 3 2019


from random import shuffle


def shell_sort(L):
    '''
    >>> L = []
    >>> shell_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> shell_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> shell_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> shell_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> shell_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> shell_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> shell_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    for n in range(len(L) // 2, 0, -1):
        # We use Pratt's method which uses as gaps all numbers of the form 2^i * 3^j
        p = n
        while p % 2 == 0:
            p //= 2
        while p % 3 == 0:
            p //= 3
        if p != 1:
            continue
        for i in range(n, 2 * n):
            for j in range(i, len(L), n):
                k = j
                while k >= n and L[k - n] > L[k]:
                    L[k - n], L[k] = L[k], L[k - n]
                    k -= n


if __name__ == '__main__':
    import doctest
    doctest.testmod()
