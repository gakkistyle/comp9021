# COMP9021 Term 3 2019


'''
Generates an initial segment of the list of prime numbers based on Eratosthenes sieve
without encoding the even numbers greater than 2.
'''


from math import sqrt
from itertools import chain

from input_output import *


def generate_primes():
    print('I will generate all prime numbers in the range [2, n] '
          'for the n of your choice.'
         )
    nicely_display(*sequence_and_max_size_from(
                        sieve_of_primes_up_to(input_int(min_value=2)))
                  )


def sieve_of_primes_up_to(n):
    # We let primes_sieve encode the sequence
    # (2, 3, 5, 7, 9, 11, ..., n') with n' equal to n if n is odd
    #  and n - 1 is n is even. The index of n' is n_index.
    n_index = (n - 1) // 2
    sieve = [True] * (n_index + 1)
    for k in range(1, (round(sqrt(n)) + 1) // 2):
        if sieve[k]:
            # If k is the index of p then
            # 2 * k * (k + 1) is the index of p ** 2;
            # Also, we increment the value by 2p,
            # which corresponds to increasing the index by 2 * k + 1.
            for i in range(2 * k * (k + 1), n_index + 1, 2 * k + 1):
                sieve[i] = False
    return sieve


def sequence_and_max_size_from(sieve):
    largest_prime = len(sieve) - 1
    while not sieve[largest_prime]:
        largest_prime -= 1
    return chain((2,), (2 * p + 1 for p in range(1, len(sieve)) if sieve[p])),\
           len(str(largest_prime))


if __name__ == '__main__':
    generate_primes()
