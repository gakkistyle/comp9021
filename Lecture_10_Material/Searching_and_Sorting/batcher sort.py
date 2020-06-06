# COMP9021 Term 3 2019


from random import shuffle


# Assumes that len(L) is a power of 2
def batcher_sort(L):
    '''
    >>> L = []
    >>> batcher_sort(L)
    >>> L
    []
    >>> L = [0]
    >>> batcher_sort(L)
    >>> L
    [0]
    >>> L = [0, 1]
    >>> batcher_sort(L)
    >>> L
    [0, 1]
    >>> L = [1, 0]
    >>> batcher_sort(L)
    >>> L
    [0, 1]
    >>> L = list(range(8))
    >>> batcher_sort(L)
    >>> L
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> L.reverse()
    >>> batcher_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> shuffle(L)
    >>> batcher_sort(L)
    >>> L    
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    half_size, size = 1, 2
    while half_size < len(L):
        for group in range(0, len(L) // size):
            top = group * size
            for i in range(half_size):
                if L[top + i] > L[top + i + half_size]:
                    L[top + i], L[top + i + half_size] = L[top + i + half_size], L[top + i]
        span, double_span = half_size // 2, half_size
        while span:
            skip = half_size // span
            for group in range(len(L) // double_span):
                if (group + 1) % skip == 0:
                    continue
                top = span + group * double_span;
                for i in range(span):
                    if L[top + i] > L[top + i + span]:
                        L[top + i], L[top + i + span] = L[top + i + span], L[top + i]
            span //= 2
            double_span //= 2
        half_size *= 2
        size *= 2


if __name__ == '__main__':
    import doctest
    doctest.testmod()
