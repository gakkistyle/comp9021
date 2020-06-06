# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 4
 

'''
Will be tested with a at equal equal to 2 and b at most equal to 10_000_000.
'''
    

import sys
from math import sqrt,ceil
def isprime(n):
    if n == 2:
        return True
    for i in range(2,ceil(sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def f(a, b):
    '''
    >>> f(2, 2)
    There is a unique prime number beween 2 and 2.
    >>> f(2, 3)
    There are 2 prime numbers between 2 and 3.
    >>> f(2, 5)
    There are 3 prime numbers between 2 and 5.
    >>> f(4, 4)
    There is no prime number beween 4 and 4.
    >>> f(14, 16)
    There is no prime number beween 14 and 16.
    >>> f(3, 20)
    There are 7 prime numbers between 3 and 20.
    >>> f(100, 800)
    There are 114 prime numbers between 100 and 800.
    >>> f(123, 456789)
    There are 38194 prime numbers between 123 and 456789.
    '''
    number_of_primes_at_most_equal_to_b = 0
    # Insert your code here
    for i in range(a,b+1):
        if isprime(i):
            number_of_primes_at_most_equal_to_b += 1
    
    if not number_of_primes_at_most_equal_to_b:
        print(f'There is no prime number beween {a} and {b}.')
    elif number_of_primes_at_most_equal_to_b == 1:
        print(f'There is a unique prime number beween {a} and {b}.')
    else:
        print(f'There are {number_of_primes_at_most_equal_to_b} prime numbers between {a} and {b}.')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
