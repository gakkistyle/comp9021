# COMP9021 Practice 3 - Solutions


'''
Implements a function encode(a, b) and a function decode(n) for the one-to-one mapping
from the set of pairs of integers onto the set of natural numbers described as follows:

                      16  15  14  13  12
                      17  4   3   2   11
                      18  5   0   1   10
                      19  6   7   8   9
                      20  21  ...

That is, starting from the point (0,0) of the plane, we move to (1,0)
and then spiral counterclockwise.
'''


from math import sqrt


def encode(a, b):
    '''
    >>> encode(0, 0)
    0
    >>> encode(1, 0)
    1
    >>> encode(1, 1)
    2
    >>> encode(0, 1)
    3
    >>> encode(-1, 1)
    4
    >>> encode(-1, 0)
    5
    >>> encode(-1, -1)
    6
    >>> encode(0, -1)
    7
    >>> encode(1, -1)
    8
    >>> encode(2, -1)
    9
    >>> encode(2, 0)
    10
    >>> encode(2, 1)
    11
    >>> encode(2, 2)
    12
    >>> encode(1, 2)
    13
    >>> encode(0, 2)
    14
    >>> encode(-1, 2)
    15
    >>> encode(-2, 2)
    16
    >>> encode(-2, 1)
    17
    >>> encode(-2, 0)
    18
    >>> encode(-2, -1)
    19
    >>> encode(-2, -2)
    20
    >>> encode(4, -2)
    50
    '''
    # Based on largest square centered on (0, 0) not containing (a, b)
    half_side = max(abs(a) - 1, abs(b) - 1)
    if a == half_side + 1 and b == -half_side - 1:
        return (2 * half_side + 3) ** 2 - 1
    square_area = (2 * half_side + 1) ** 2
    if a == half_side + 1:
        return square_area + half_side + b
    if b == half_side + 1:
        return square_area + 3 * half_side  + 2 - a
    if a == -half_side - 1:
        return square_area + 5 * half_side + 4 - b
    return square_area + 7 * half_side + 6 + a
        
    
def decode(n):
    '''
    >>> decode(0)
    (0, 0)
    >>> decode(1)
    (1, 0)
    >>> decode(2)
    (1, 1)
    >>> decode(3)
    (0, 1)
    >>> decode(4)
    (-1, 1)
    >>> decode(5)
    (-1, 0)
    >>> decode(6)
    (-1, -1)
    >>> decode(7)
    (0, -1)
    >>> decode(8)
    (1, -1)
    >>> decode(9)
    (2, -1)
    >>> decode(10)
    (2, 0)
    >>> decode(11)
    (2, 1)
    >>> decode(12)
    (2, 2)
    >>> decode(13)
    (1, 2)
    >>> decode(14)
    (0, 2)
    >>> decode(15)
    (-1, 2)
    >>> decode(16)
    (-2, 2)
    >>> decode(17)
    (-2, 1)
    >>> decode(18)
    (-2, 0)
    >>> decode(19)
    (-2, -1)
    >>> decode(20)
    (-2, -2)
    >>> decode(50)
    (4, -2)
    '''
    # Based on smallest square centered on (0, 0) containing the pair encoded by n
    sqrt_n_plus_one = int(sqrt(n + 1))
    # In case sqrt() approximates an integer from below.
    if sqrt_n_plus_one ** 2 < n + 1:
        sqrt_n_plus_one += 1
    half_side = sqrt_n_plus_one // 2
    side = half_side * 2 + 1
    square_area = side ** 2
    offset = square_area - n - 1
    if offset < side:
        return half_side - offset, -half_side
    if offset < 2 * side - 1:
        return -half_side, -3 * half_side + offset
    if offset < 3 * side - 2:
        return -5 * half_side + offset, half_side
    return half_side, 7 * half_side - offset
    


if __name__ == '__main__':
    import doctest
    doctest.testmod()
