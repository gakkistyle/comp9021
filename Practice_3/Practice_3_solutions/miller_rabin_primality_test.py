# COMP9021 Practice 3 - Solutions

from math import sqrt


def claims_is_not_prime(a, p):
    '''
    >>> claims_is_not_prime(2, 41041)
    True
    >>> claims_is_not_prime(3, 667)
    True
    >>> claims_is_not_prime(2, 991)   # Prime indeed
    False
    >>> claims_is_not_prime(3, 61609) # Prime indeed
    False
    >>> claims_is_not_prime(2, 2047)  # Actually not prime
    False
    >>> claims_is_not_prime(3, 121)   # Actually not prime
    False
    >>> claims_is_not_prime(5, 781)   # Actually not prime
    False
    >>> claims_is_not_prime(7, 25)    # Actually not prime
    False
    '''
    bits = bin(p - 1)[2: ]
    rightmost_1_index = bits.rindex('1')
    power = a
    for b in bits[1: rightmost_1_index + 1]:
        power = power ** 2 % p
        if b == '1':
            power = power * a % p
    if power == 1:
        return False
    previous_is_not_minus_1 = power != p - 1
    for _ in range(len(bits) - rightmost_1_index - 1):
        power = power ** 2 % p
        if power == 1:
            return previous_is_not_minus_1
        previous_is_not_minus_1 = power != p - 1 
    return True

def miller_rabin_primality_test(witnesses, p):
    '''
    >>> miller_rabin_primality_test([8, 13, 15], 103565)
    False
    >>> miller_rabin_primality_test([20, 21], 31327)     # Prime indeed
    True
    >>> miller_rabin_primality_test([20, 25, 30], 42127) # Actually not prime
    True
    '''
    return not any(claims_is_not_prime(a, p) for a in witnesses)

def smallest_miller_rabin_primality_test_failure(witnesses, upper_bound):
    '''
    # FIRST TEST TAKES A FEW SECONDS
    # SECOND TEST TAKES MORE THAN A MINUTE
    >>> smallest_miller_rabin_primality_test_failure([2, 3], 10_000_000)
    1373653
    >>> smallest_miller_rabin_primality_test_failure([2, 3, 5], 30_000_000)
    25326001
    '''
    sieve = sieve_of_primes_up_to(upper_bound)
    for i in range(max(witnesses) // 2 + 1, len(sieve)):
        if not sieve[i] and miller_rabin_primality_test(witnesses, 2 * i + 1):
            return 2 * i + 1
    
def sieve_of_primes_up_to(n):
    # We let primes_sieve encode the sequence (2, 3, 5, 7, 9, 11, ..., n')
    # with n' equal to n if n is odd and n - 1 is n is even.
    # The index of n' is n_index
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
  
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
