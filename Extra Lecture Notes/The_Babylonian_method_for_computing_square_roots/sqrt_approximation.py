# COMP9021 Term 3 2019


'''
Estimates the square root of a given number, up to a given precision,
using the Babylonian method.

'''


def square_root(a, ε):
    '''
    >>> square_root(2, 0.0001)
    1.4142135623746899
    >>> square_root(3, 0.000001)
    1.7320508075688772
    >>> square_root(4, 0.0000001)
    2.000000000000002
    '''
    def iterate(f, x):
        while True:
            next_x = f(x)
            yield next_x
            x = next_x

    x = 1
    approximating_sequence = iterate(lambda x: (x + a / x) / 2 , x)
    next_x = next(approximating_sequence)
    while abs(next_x - x) > ε:
        next_x, x = next(approximating_sequence), next_x
    return next_x


if __name__ == '__main__':
    import doctest
    doctest.testmod()
