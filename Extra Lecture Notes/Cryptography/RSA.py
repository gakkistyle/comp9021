# COMP9021 Term 3 2019

from math import gcd
from random import randrange


def diffie_hellman(p, g):
    print(f'Alice lets Bob know that p = {p} and g = {g}.')
    a = randrange(100)
    A = g ** a % p
    b = randrange(100)
    B = g ** b % p
    print(f'Alice sends {A} to Bob.')
    print(f'Bob sends {B} to Alice.')
    print(f'Alice computes the secret code as {B ** a % p}.')
    print(f'Bob computes the secret code as {A ** b % p}.')

 
def RSA(p, q):
    N = p * q
    phi_of_N = (p - 1) * (q - 1)
    e = 65537
    print(f'Alice publishes public key: N = {N}, e = {e}')
    _, d = bezout_coefficients(phi_of_N, e)
    # d does not have to be smaller than phi_of_N, but it has to be positive.
    d %= phi_of_N
    m = randrange(100)
    c = m ** e % N
    print(f'Bob encodes {m} as {c}.')
    print(f'Alice decodes {c} as {modular_exponentiation(c, d, N)}.')

def bezout_coefficients(a, b):
    '''
    Returns a pair (x, y) with ax + by = gcd(a, b)
    >>> a, b = bezout_coefficients(-1, 1)
    >>> a, b
    (0, 1)
    >>> a * -1 + b * 1 == gcd(-1, 1)
    True
    >>> a, b = bezout_coefficients(4, 6)
    >>> a, b
    (-1, 1)
    >>> a * 4 + b * 6 == gcd(4, 6)
    True
    >>> a, b = bezout_coefficients(782, 253)
    >>> a, b
    (1, -3)
    >>> a * 782 + b * 253 == gcd(782, 253)
    True
    >>> a, b = bezout_coefficients(-321, 654)
    >>> a, b
    (55, 27)
    >>> a * -321 + b * 654 == gcd(321, 654)
    True
    '''
    if b == 0:
        return 1, 0
    x, y = bezout_coefficients(b, a % b)
    return y, x - (a // b) * y


def modular_exponentiation(x, n, p):
    '''
    Returns x^n (mod p)
    >>> modular_exponentiation(2, 0, 10)
    1
    >>> modular_exponentiation(2, 1, 10)
    2
    >>> modular_exponentiation(2, 3, 10)
    8
    >>> modular_exponentiation(2, 4, 10)
    6
    >>> modular_exponentiation(2, 5, 10)
    2
    >>> modular_exponentiation(10 * 10_000_000, 10_000_000, 10)
    0
    >>> modular_exponentiation(9 * 10_000_000, 10_000_000, 31)
    25
    >>> modular_exponentiation(7 * 10_000_000, 10_000_000, 94)
    12
    '''
    if n == 0:
        return 1
    y = modular_exponentiation((x * x) % p, n // 2, p)
    if n % 2:
        y = (y * x) % p
    return y
 

if __name__ == '__main__':
    import doctest
    doctest.testmod()
