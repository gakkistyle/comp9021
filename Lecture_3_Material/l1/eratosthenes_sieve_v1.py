# COMP9021 Term 3 2019


'''
Generates an initial segment of the list of prime numbers based on
Eratosthenes sieve using the the most straightforward approach.
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
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return sieve


def sequence_and_max_size_from(sieve):
    largest_prime = len(sieve) - 1
    while not sieve[largest_prime]:
        largest_prime -= 1
    return (p for p in range(2, len(sieve)) if sieve[p]),\
           len(str(largest_prime))

    
if __name__ == '__main__':
    generate_primes()
