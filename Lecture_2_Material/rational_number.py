# COMP9021 Term 3 2019


'''
A number of functions to essentially, get as input two nonempty strings
of digits, sigma and tau, and compute natural numbers a and b such that
a / b is reduced and equal to 0.(sigma)(tau)(tau)(tau)(tau)...
'''


def determine_reduced_fraction_from_pattern_and_repeated_pattern():
    '''
    Gets as input two nonempty strings of digits, sigma and tau, and
    computes natural numbers a and b such that a / b is reduced and
    equal to 0.(sigma)(tau)(tau)(tau)(tau)...
    '''
    output_result(*determine_reduced_fraction(*get_both_inputs()))


def determine_reduced_fraction(sigma, tau):
    '''   
    >>> determine_reduced_fraction('0', '0')
    (0, 1)
    >>> determine_reduced_fraction('0', '1')
    (1, 90)
    >>> determine_reduced_fraction('1', '0')
    (1, 10)
    >>> determine_reduced_fraction('1', '1')
    (1, 9)
    >>> determine_reduced_fraction('9', '9')
    (1, 1)
    >>> determine_reduced_fraction('23', '905')
    (11941, 49950)
    >>> determine_reduced_fraction('1', '234')
    (137, 1110)
    >>> determine_reduced_fraction('234', '1')
    (2107, 9000)
    >>> determine_reduced_fraction('000', '97')
    (97, 99000)
    >>> determine_reduced_fraction('97', '000')
    (97, 100)
    >>> determine_reduced_fraction('01234', '543210')
    (51439249, 4166662500)
    '''
    return reduce_fraction(*compute_fraction(sigma, tau))


def compute_fraction(sigma, tau):
    '''
    Based on the computation
            0.(sigma)(tau)(tau)(tau)...
          = sigma * 10^{-|sigma|} + tau(10^{-|sigma|-|tau|}
                                        + 10^{-|sigma|-2|tau|}
                                        + ...
                                       )
          = sigma * 10^{-|sigma|} +
            tau * 10^{-|sigma|-|tau|} / (1 - 10^{-|tau|})
          = sigma * 10^{-|sigma|} +
            tau * 10^{-|sigma|} / (10^{|tau|} - 1)
          = [sigma * 10^{-|sigma|} * (10^{|tau|} - 1)
             + tau * 10^{-|sigma|}
            ] / (10^{|tau|} - 1)
          = [sigma * (10^{|tau|} - 1) + tau] /
            [(10^{|tau|} - 1) * 10^{|sigma|}]
                                  
    >>> compute_fraction('0', '0')
    (0, 90)
    >>> compute_fraction('0', '1')
    (1, 90)
    >>> compute_fraction('1', '0')
    (9, 90)
    >>> compute_fraction('1', '1')
    (10, 90)
    >>> compute_fraction('9', '9')
    (90, 90)
    >>> compute_fraction('23', '905')
    (23882, 99900)
    >>> compute_fraction('1', '234')
    (1233, 9990)
    >>> compute_fraction('234', '1')
    (2107, 9000)
    >>> compute_fraction('000', '97')
    (97, 99000)
    >>> compute_fraction('97', '000')
    (96903, 99900)
    >>> compute_fraction('01234', '543210')
    (1234541976, 99999900000)
    '''
    numerator = int(sigma) * (10 ** len(tau) - 1) + int(tau)
    denominator = (10 ** len(tau) - 1) * 10 ** len(sigma)
    return numerator, denominator


def reduce_fraction(numerator, denominator):
    '''
    >>> reduce_fraction(0, 1)
    (0, 1)
    >>> reduce_fraction(1, 90)
    (1, 90)
    >>> reduce_fraction(9, 90)
    (1, 10)
    >>> reduce_fraction(10, 90)
    (1, 9)
    >>> reduce_fraction(90, 90)
    (1, 1)
    >>> reduce_fraction(23882, 99900)
    (11941, 49950)
    >>> reduce_fraction(1233, 9990)
    (137, 1110)
    >>> reduce_fraction(2107, 9000)
    (2107, 9000)
    >>> reduce_fraction(97, 99000)
    (97, 99000)
    >>> reduce_fraction(96903, 99900)
    (97, 100)
    >>> reduce_fraction(1234541976, 99999900000)
    (51439249, 4166662500)
    '''
    if numerator == 0:
        return 0, 1
    the_gcd = gcd(numerator, denominator)
    return numerator // the_gcd, denominator // the_gcd


# Just to practice;
# in practice, we would just import gcd from the math module.
def gcd(a, b):
    '''
    Euclid's algorithm

    >>> gcd(0, 1)
    1
    >>> gcd(1, 90)
    1
    >>> gcd(9, 90)
    9
    >>> gcd(10, 90)
    10
    >>> gcd(90, 90)
    90
    >>> gcd(23882, 99900)
    2
    >>> gcd(1233, 990)
    9
    >>> gcd(2107, 9000)
    1
    >>> gcd(97, 9000)
    1
    >>> gcd(96903, 99900)
    999
    >>> gcd(1234541976, 99999900000)
    24
    '''
    while b:
        a, b = b, a % b
    return a


def get_both_inputs():
    print('We want to compute the reduced fraction, a / b,\n'
          '   that evaluates to .(sigma)(tau)(tau)(tau)...'
         )
    return get('sigma'), get('tau')


def get(sigma_or_tau):
    while True:
        value = input(f'Input {sigma_or_tau}: ')
        if value.isnumeric():
            return value
        print('Incorrect input, try again.')


def output_result(numerator, denominator):
    print(f'The fraction is: {numerator} / {denominator}')
    print(f'It evaluates to: {numerator / denominator}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
