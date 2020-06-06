# COMP9021 Term 3 2019


'''
Generates an initial segment of the list of prime numbers based on
Euler sieveswitching between sets and sorted lists for a more effective
implementation.
'''


from math import sqrt

from input_output import *


def generate_primes():
    print('I will generate all prime numbers in the range [2, n] '
          'for the n of your choice.'
         )
    nicely_display(*sequence_and_max_size_from(
                        sieve_of_primes_up_to(input_int(min_value=2)))
                                              )


def sieve_of_primes_up_to(n):
    sieve = list(range(2, n + 1))
    i = 0
    while sieve[i] <= round(sqrt(n)):
        sieve_as_set = set(sieve)
        k = 0
        while True:
            factor = sieve[i] * sieve[i + k]
            if factor > n:
                break
            sieve_as_set.remove(factor)
            k += 1
        sieve = sorted(sieve_as_set)
        i += 1
    return sieve


def sequence_and_max_size_from(sieve):
    return sieve, len(str(sieve[-1]))


if __name__ == '__main__':
    generate_primes()
