# COMP9021 Practice 7 - Solutions

'''
Given strictly positive integers N and D, outputs N / D in the form
                 1 / d_1 + ... + 1 / d_k
if N < D, and in the form
                 p + 1 / d_1 + ... + 1 /d_k
if N >= D,
- for one function, applying Fibonacci's method (which yields a unique decomposition),
- for another function, determining all decompositions of minimal length (which might yield
  many decompositions).
'''


from math import gcd


def reduce(numerator, denominator):
    the_gcd = gcd(numerator, denominator)
    return numerator // the_gcd, denominator // the_gcd

def subtract(numerator, denominator, unit_denominator):
    '''
    Returns the reduced form of (numerator / denominator) - (1 / unit_denominator)
    '''
    numerator = numerator * unit_denominator - denominator
    denominator *= unit_denominator
    return reduce(numerator, denominator)

def fibonacci_decomposition(N, D):
    print(f'{N}/{D} = ', end = '')
    numerator, denominator = reduce(N, D)
    numerator %= denominator
    if not numerator:
        print(N // D)
        return
    if N > D:
        print(f'{N // D} + ', end = '')
    decomposition = []
    while denominator % numerator:
        unit_denominator = denominator // numerator + 1
        decomposition.append(unit_denominator)
        numerator, denominator = subtract(numerator, denominator, unit_denominator)
    decomposition.append(denominator)
    print(' + '.join(f'1/{unit_denominator}' for unit_denominator in decomposition))

def shortest_length_decompositions(N, D):
    '''
    Displays all decompositions of the form N / D = 1/d_1 + 1/d_2 + ... + 1/k such that:
    - d_1 > d_2 > ... > d_k;
    - k is minimal.
    
    >>> shortest_length_decompositions(2, 3)
    2/3 = 1/2 + 1/6
    >>> shortest_length_decompositions(2, 5)
    2/5 = 1/3 + 1/15
    >>> shortest_length_decompositions(2, 7)
    2/7 = 1/4 + 1/28
    >>> shortest_length_decompositions(2, 9)
    2/9 = 1/5 + 1/45
    2/9 = 1/6 + 1/18
    >>> shortest_length_decompositions(2, 11)
    2/11 = 1/6 + 1/66
    >>> shortest_length_decompositions(3, 4)
    3/4 = 1/2 + 1/4
    >>> shortest_length_decompositions(3, 5)
    3/5 = 1/2 + 1/10
    >>> shortest_length_decompositions(3, 7)
    3/7 = 1/3 + 1/11 + 1/231
    3/7 = 1/3 + 1/12 + 1/84
    3/7 = 1/3 + 1/14 + 1/42
    3/7 = 1/3 + 1/15 + 1/35
    3/7 = 1/4 + 1/6 + 1/84
    3/7 = 1/4 + 1/7 + 1/28
    >>> shortest_length_decompositions(3, 8)
    3/8 = 1/3 + 1/24
    3/8 = 1/4 + 1/8
    >>> shortest_length_decompositions(3, 10)
    3/10 = 1/4 + 1/20
    3/10 = 1/5 + 1/10
    >>> shortest_length_decompositions(3, 11)
    3/11 = 1/4 + 1/44
    >>> shortest_length_decompositions(4, 5)
    4/5 = 1/2 + 1/4 + 1/20
    4/5 = 1/2 + 1/5 + 1/10
    >>> shortest_length_decompositions(4, 7)
    4/7 = 1/2 + 1/14
    >>> shortest_length_decompositions(4, 9)
    4/9 = 1/3 + 1/9
    >>> shortest_length_decompositions(4, 11)
    4/11 = 1/3 + 1/33
    >>> shortest_length_decompositions(5, 6)
    5/6 = 1/2 + 1/3
    >>> shortest_length_decompositions(5, 7)
    5/7 = 1/2 + 1/5 + 1/70
    5/7 = 1/2 + 1/6 + 1/21
    5/7 = 1/2 + 1/7 + 1/14
    >>> shortest_length_decompositions(5, 8)
    5/8 = 1/2 + 1/8
    >>> shortest_length_decompositions(5, 9)
    5/9 = 1/2 + 1/18
    >>> shortest_length_decompositions(5, 11)
    5/11 = 1/3 + 1/9 + 1/99
    5/11 = 1/3 + 1/11 + 1/33
    5/11 = 1/4 + 1/5 + 1/220
    >>> shortest_length_decompositions(6, 7)
    6/7 = 1/2 + 1/3 + 1/42
    >>> shortest_length_decompositions(6, 11)
    6/11 = 1/2 + 1/22
    >>> shortest_length_decompositions(7, 8)
    7/8 = 1/2 + 1/3 + 1/24
    7/8 = 1/2 + 1/4 + 1/8
    >>> shortest_length_decompositions(7, 9)
    7/9 = 1/2 + 1/4 + 1/36
    7/9 = 1/2 + 1/6 + 1/9
    >>> shortest_length_decompositions(7, 10)
    7/10 = 1/2 + 1/5
    >>> shortest_length_decompositions(7, 11)
    7/11 = 1/2 + 1/8 + 1/88
    7/11 = 1/2 + 1/11 + 1/22
    >>> shortest_length_decompositions(8, 9)
    8/9 = 1/2 + 1/3 + 1/18
    >>> shortest_length_decompositions(8, 11)
    8/11 = 1/2 + 1/5 + 1/37 + 1/4070
    8/11 = 1/2 + 1/5 + 1/38 + 1/1045
    8/11 = 1/2 + 1/5 + 1/40 + 1/440
    8/11 = 1/2 + 1/5 + 1/44 + 1/220
    8/11 = 1/2 + 1/5 + 1/45 + 1/198
    8/11 = 1/2 + 1/5 + 1/55 + 1/110
    8/11 = 1/2 + 1/5 + 1/70 + 1/77
    8/11 = 1/2 + 1/6 + 1/17 + 1/561
    8/11 = 1/2 + 1/6 + 1/18 + 1/198
    8/11 = 1/2 + 1/6 + 1/21 + 1/77
    8/11 = 1/2 + 1/6 + 1/22 + 1/66
    8/11 = 1/2 + 1/7 + 1/12 + 1/924
    8/11 = 1/2 + 1/7 + 1/14 + 1/77
    8/11 = 1/2 + 1/8 + 1/10 + 1/440
    8/11 = 1/2 + 1/8 + 1/11 + 1/88
    8/11 = 1/3 + 1/4 + 1/7 + 1/924
    >>> shortest_length_decompositions(9, 10)
    9/10 = 1/2 + 1/3 + 1/15
    >>> shortest_length_decompositions(9, 11)
    9/11 = 1/2 + 1/4 + 1/15 + 1/660
    9/11 = 1/2 + 1/4 + 1/16 + 1/176
    9/11 = 1/2 + 1/4 + 1/20 + 1/55
    9/11 = 1/2 + 1/4 + 1/22 + 1/44
    9/11 = 1/2 + 1/5 + 1/10 + 1/55
    >>> shortest_length_decompositions(10, 11)
    10/11 = 1/2 + 1/3 + 1/14 + 1/231
    10/11 = 1/2 + 1/3 + 1/15 + 1/110
    10/11 = 1/2 + 1/3 + 1/22 + 1/33
    '''
    numerator, denominator = reduce(N, D)
    numerator %= denominator
    if not numerator:
        print(f'{N}/{D} = {N // D}')
        return
    length = 1
    while True:
        length += 1
        decompositions = fixed_length_decompositions(length, numerator, denominator, 2)
        if decompositions:
            for decomposition in decompositions:
                print(f'{N}/{D} = ', end = '')
                if N > D:
                    print(f'{N // D} + ', end = '')
                print(' + '.join(f'1/{unit_denominator}' for unit_denominator in decomposition))
            return

def fixed_length_decompositions(length, N, D, minimum):
    '''
    Returns the list of all lists of the form [d_1, d_2, ..., d_length] such that:
    - N / D = 1/d_1 + 1/d_2 + ... + 1/d_length;
    - minimum >= d_1 > d_2 > ... > d_length.
    '''
    if length == 1:
        if N == 1:
            return [[D]]
        return
    decompositions = []
    # Since we want N / D to be a sum of length many distinct terms,
    # the largest one being 1 / unit_denominator,
    # 1 / unit_denominator * length should be greater than N / D,
    # which is equivalent to unit_denominator < D * length / N,
    # which, since N and D are relatively prime, is equivalent to:
    #   - unit_denominator < D * length // N if N does not divide length;
    #   - unit_denominator < (D * length // N) + 1 if N divides length.   
    upper_bound = D * length // N
    if length % N:
        upper_bound += 1
    # 1 / unit_denominator should be smaller than N / D,
    # which is equivalent to unit_denominator > D / N,
    # which is equivalent to unit_denominator > D // N.   
    for unit_denominator in range(max(D // N + 1, minimum), upper_bound):
        numerator, denominator = subtract(N, D, unit_denominator)
        further_decompositions = fixed_length_decompositions(length - 1, numerator, denominator,
                                                                               unit_denominator + 1
                                                            )
        if further_decompositions:
            for decomposition in further_decompositions:
                decompositions.append([unit_denominator] + decomposition)
    return decompositions

   
if __name__ == '__main__':
    import doctest
    doctest.testmod()
