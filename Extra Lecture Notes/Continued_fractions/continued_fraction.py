# COMP9021 Term 3 2019


'''
A class for fractions and a class for continued fractions, to
approximate fractions to decimals with an arbitrary precision, and to
approximate continued fractions, so square roots in particular, to
fractions and decimals with an arbitrary precision.
'''


import math
from itertools import cycle, chain, repeat
from fractions import Fraction 


class ContinuedFractionError(Exception):
    pass

        
class ContinuedFraction:
    '''
    If the continued fraction is finite, then we make sure it does not
    end in 1. Otherwise, periodic_expansion is made nonperiodic, and as
    much from finite_expansion is removed.
 
    >>> cf = ContinuedFraction()
    >>> cf
    ContinuedFraction([0], [])
    >>> print(cf)
    [0]
    >>> ContinuedFraction([])
    ContinuedFraction([0], [])
    >>> cf = ContinuedFraction([0, 1])
    >>> cf
    ContinuedFraction([1], [])
    >>> print(cf)
    [1]
    >>> cf = ContinuedFraction([1, 2, 1])
    >>> cf
    ContinuedFraction([1, 3], [])
    >>> print(cf)
    [1, 3]
    >>> cf = ContinuedFraction([0, 1], [1])
    >>> cf
    ContinuedFraction([0], [1])
    >>> print(cf)
    [0; 1...]
    >>> ContinuedFraction([0], [1, 1])
    ContinuedFraction([0], [1])
    >>> ContinuedFraction([0, 1], [1, 1])
    ContinuedFraction([0], [1])
    >>> ContinuedFraction([], [1, 1, 1])
    ContinuedFraction([0], [1])
    >>> ContinuedFraction([0, 1], [1, 1, 1])
    ContinuedFraction([0], [1])
    >>> cf = ContinuedFraction([0], [1, 2, 1, 2, 1, 2])
    >>> cf
    ContinuedFraction([0], [1, 2])
    >>> print(cf)
    [0; 1, 2...]
    >>> cf = ContinuedFraction([0, 2], [1, 2, 1, 2, 1, 2])
    >>> cf
    ContinuedFraction([0], [2, 1])
    >>> print(cf)
    [0; 2, 1...]
    >>> cf = ContinuedFraction([0, 1, 2, 3], [4, 2, 3, 4, 2, 3])
    >>> cf
    ContinuedFraction([0, 1], [2, 3, 4])
    >>> print(cf)
    [0, 1; 2, 3, 4...]
    >>> cf = ContinuedFraction([0, 1, 2, 3, 1], [4, 2, 3, 1])
    >>> cf
    ContinuedFraction([0, 1], [2, 3, 1, 4])
    >>> print(cf)
    [0, 1; 2, 3, 1, 4...]
    '''
    def __init__(self, finite_expansion=None, periodic_expansion=None):
        if finite_expansion is not None\
           and (not isinstance(finite_expansion, list)
                or any(not isinstance(e, int) for e in finite_expansion)
                or any(e <= 0 for e in finite_expansion[1 :])
               ):
            raise ContinuedFractionError('Incorrect finite expansion')
        if periodic_expansion is not None\
           and (not isinstance(periodic_expansion, list)
                or any(not isinstance(e, int) for e in periodic_expansion)
                or any(e <= 0 for e in periodic_expansion)
               ):
            raise ContinuedFractionError('Incorrect periodic expansion')
        
        self.finite_expansion = finite_expansion if finite_expansion else [0]
        if periodic_expansion:
            for i in range(1, len(periodic_expansion) // 2 + 1):
                if len(periodic_expansion) % i == 0 and periodic_expansion ==\
                      periodic_expansion[: i] * (len(periodic_expansion) // i):
                    periodic_expansion = periodic_expansion[: i]
                    break
            while len(self.finite_expansion) > 1\
                  and self.finite_expansion[-1] == periodic_expansion[-1]:
                    self.finite_expansion.pop()
                    periodic_expansion.insert(0, periodic_expansion.pop())
            self.periodic_expansion = periodic_expansion
        else:
            self.periodic_expansion = []
            if len(self.finite_expansion) > 1\
               and self.finite_expansion[-1] == 1:
                self.finite_expansion.pop()
                self.finite_expansion[-1] += 1
        
    def is_integral(self):
        return len(self.finite_expansion) == 1 and not self.periodic_expansion

    def is_rational(self):
        return not self.periodic_expansion

    def negation(self):
        '''
        >>> print(ContinuedFraction().negation())
        [0]
        >>> print(ContinuedFraction([1]).negation())
        [-1]
        >>> print(ContinuedFraction([-1]).negation())
        [1]
        >>> print(ContinuedFraction([0, 1]).negation())
        [-1]
        >>> print(ContinuedFraction([1, 2]).negation())
        [-2, 2]
        >>> print(ContinuedFraction([-2, 2]).negation())
        [1, 2]
        >>> print(ContinuedFraction([1, 3]).negation())
        [-2, 1, 2]
        >>> print(ContinuedFraction([-2, 1, 2]).negation())
        [1, 3]
        >>> print(ContinuedFraction([1], [1]).negation())
        [-2, 2; 1...]
        >>> print(ContinuedFraction([1, 3, 4], [5, 6]).negation())
        [-2, 1, 2, 4; 5, 6...]
        >>> print(ContinuedFraction([0, 1], [2, 3]).negation())
        [-1, 3; 3, 2...]
        >>> print(ContinuedFraction([-2, 1, 2, 4], [5, 6]).negation())
        [1, 3, 4; 5, 6...]
        '''
        # In case the periodic expansion is not empty, borrow from it so
        # as to make the length of the finite expansion at least 3, as
        # that simplifies the computation.
        if len(self.periodic_expansion) == 1:
            finite_expansion =\
                    self.finite_expansion + self.periodic_expansion * 2
        elif self.periodic_expansion:
            finite_expansion = self.finite_expansion + self.periodic_expansion
        else:
            finite_expansion = self.finite_expansion           
        periodic_expansion = self.periodic_expansion            
        if len(finite_expansion) == 1:
            return ContinuedFraction([-finite_expansion[0]])
        # In this case, finite_expansion is of length at least 3.
        if finite_expansion[1] == 1:
            return ContinuedFraction([-finite_expansion[0] - 1,
                                      1 + finite_expansion[2]
                                     ] + finite_expansion[3 :],
                                     periodic_expansion
                                    )
        return ContinuedFraction([-finite_expansion[0] - 1, 1,
                                  finite_expansion[1] - 1
                                 ] + finite_expansion[2 :], periodic_expansion
                                )

    def to_fraction(self):
        '''
        >>> print(ContinuedFraction().to_fraction())
        0
        >>> print(ContinuedFraction([0, 1]).to_fraction())
        1
        >>> print(ContinuedFraction([0, 2]).to_fraction())
        1/2
        >>> print(ContinuedFraction([0, 1, 1]).to_fraction())
        1/2
        >>> print(ContinuedFraction([2, 1, 4, 3]).to_fraction())
        45/16
        >>> print(ContinuedFraction([2, 1, 4, 2, 1]).to_fraction())
        45/16
        '''
        if not self.is_rational():
            return
        p1, p2 = 0, 1
        q1, q2 = 1, 0
        for a in self.finite_expansion:
            p1, p2 = p2, a * p2 + p1
            q1, q2 = q2, a * q2 + q1
        return Fraction(p2, q2)

    def approximate_as_fractions(self):
        '''
        >>> # sqrt(2)
        >>> fractions = ContinuedFraction([1], [2]).approximate_as_fractions()
        >>> for _ in range(10): print(next(fractions))
        1
        3/2
        7/5
        17/12
        41/29
        99/70
        239/169
        577/408
        1393/985
        3363/2378
        >>> # -sqrt(3)
        >>> fractions =\
                 ContinuedFraction([-2, 3], [1, 2]).approximate_as_fractions()
        >>> for _ in range(10): print(next(fractions))
        -2
        -5/3
        -7/4
        -19/11
        -26/15
        -71/41
        -97/56
        -265/153
        -362/209
        -989/571
        '''
        p1, p2 = 0, 1
        q1, q2 = 1, 0
        for a in chain(self.finite_expansion, cycle(self.periodic_expansion)):
            p1, p2 = p2, a * p2 + p1
            q1, q2 = q2, a * q2 + q1
            yield Fraction(p2, q2)

    def approximate_as_decimals(self, precision=1):
        '''
        >>> decimals = ContinuedFraction().approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        0
        0
        0
        >>> decimals = ContinuedFraction([2]).approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        2
        2
        2
        >>> decimals = ContinuedFraction([0, 2]).approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        0.5
        0.5
        0.5
        >>> decimals = ContinuedFraction([0, 3]).approximate_as_decimals(4)
        >>> for _ in range(5): print(next(decimals))
        0.3333
        0.33333333
        0.333333333333
        0.3333333333333333
        0.33333333333333333333
        >>> decimals = ContinuedFraction([-1, 1, 2]).approximate_as_decimals(4)
        >>> for _ in range(5): print(next(decimals))
        -0.3333
        -0.33333333
        -0.333333333333
        -0.3333333333333333
        -0.33333333333333333333
        >>> decimals =\
                ContinuedFraction([0, 1000000], [1]).approximate_as_decimals(2)
        >>> for _ in range(10): print(next(decimals))
        0.00
        0.0000
        0.000000
        0.00000099
        0.0000009999
        0.000000999999
        0.00000099999938
        0.0000009999993819
        0.000000999999381966
        0.00000099999938196639
        >>> # Golden ratio 
        >>> decimals = ContinuedFraction([1], [1]).approximate_as_decimals()
        >>> for _ in range(10): print(next(decimals))
        1.6
        1.61
        1.618
        1.6180
        1.61803
        1.618033
        1.6180339
        1.61803398
        1.618033988
        1.6180339887
        >>> # sqrt(2) 
        >>> decimals = ContinuedFraction([1], [2]).approximate_as_decimals(2)
        >>> for _ in range(10): print(next(decimals))
        1.41
        1.4142
        1.414213
        1.41421356
        1.4142135623
        1.414213562373
        1.41421356237309
        1.4142135623730950
        1.414213562373095048
        1.41421356237309504880
        >>> # -sqrt(3)
        >>> decimals =\
                ContinuedFraction([-2, 3], [1, 2]).approximate_as_decimals(4)
        >>> for _ in range(10): print(next(decimals))
        -1.7320
        -1.73205080
        -1.732050807568
        -1.7320508075688772
        -1.73205080756887729352
        -1.732050807568877293527446
        -1.7320508075688772935274463415
        -1.73205080756887729352744634150587
        -1.732050807568877293527446341505872366
        -1.7320508075688772935274463415058723669428
        '''
        if self.is_rational():
            yield from self.to_fraction().approximate_as_decimals(precision)
        else:
            if self.finite_expansion[0] >= 0 or self.is_integral():
                representation = str(self.finite_expansion[0]) + '.'
            else:
                representation = str(self.finite_expansion[0] + 1) + '.'          
            fractions = self.approximate_as_fractions()
            current_precision = precision
            # Ignore first fraction which is necessarily an integer.
            next(fractions)
            # Might be an integer, but next fraction will not be.
            fraction = next(fractions)
            s1 = next(fraction.precision_many_decimals(
                          abs(fraction.numerator) % fraction.denominator * 10,
                          fraction.denominator, current_precision
                                                      )
                     )
            while True:
                fraction = next(fractions)
                s2 = next(fraction.precision_many_decimals(
                           abs(fraction.numerator) % fraction.denominator * 10,
                           fraction.denominator, current_precision
                                                          )
                         )
                if s1 == s2:
                    representation += ''.join(str(d) for d in s1[-precision :])
                    yield representation
                    current_precision += precision
                s1 = s2
        
    def __repr__(self):
        return f'ContinuedFraction({self.finite_expansion}, '\
               f'{self.periodic_expansion})'

    def __str__(self):
        string = str(self.finite_expansion)
        if self.periodic_expansion:
            string = string[: -1] + '; '\
                     + str(self.periodic_expansion)[1 : -1] + '...]'
        return string


class Fraction(Fraction):
    def to_continued_fraction(self):
        '''
        >>> print(Fraction().to_continued_fraction())
        [0]
        >>> print(Fraction(2).to_continued_fraction())
        [2]
        >>> print(Fraction(-2).to_continued_fraction())
        [-2]
        >>> print(Fraction(1, 2).to_continued_fraction())
        [0, 2]
        >>> print(Fraction(1, -2).to_continued_fraction())
        [-1, 2]
        >>> print(Fraction(8, 5).to_continued_fraction())
        [1, 1, 1, 2]
        >>> print(Fraction(-8, 5).to_continued_fraction())
        [-2, 2, 2]
        >>> print(Fraction(15, 11).to_continued_fraction())
        [1, 2, 1, 3]
        >>> print(Fraction(-1080, -384).to_continued_fraction())
        [2, 1, 4, 3]
        '''
        factors = []
        a, b = abs(self.numerator), self.denominator
        while b:
            factors.append(a // b)
            a, b = b, a % b
        if self.numerator >= 0:
            return ContinuedFraction(factors)
        return ContinuedFraction(factors).negation()
        
    def approximate_as_decimals(self, precision=1):
        '''
        >>> decimals = Fraction().approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        0
        0
        0
        >>> decimals = Fraction(200).approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        200
        200
        200
        >>> decimals = Fraction(-200).approximate_as_decimals(2)
        >>> for _ in range(3): print(next(decimals))
        -200
        -200
        -200
        >>> decimals = Fraction(1, 2).approximate_as_decimals()
        >>> for _ in range(3): print(next(decimals))
        0.5
        0.5
        0.5
        >>> decimals = Fraction(1, 3).approximate_as_decimals(4)
        >>> for _ in range(3): print(next(decimals))
        0.3333
        0.33333333
        0.333333333333
        >>> decimals = Fraction(-7, 3).approximate_as_decimals(4)
        >>> for _ in range(3): print(next(decimals))
        -2.3333
        -2.33333333
        -2.333333333333
        >>> decimals = Fraction(-14, 30000).approximate_as_decimals(4)
        >>> for _ in range(3): print(next(decimals))
        -0.0004
        -0.00046666
        -0.000466666666
        >>> decimals = Fraction(3, 130).approximate_as_decimals(4)
        >>> for _ in range(3): print(next(decimals))
        0.0230
        0.02307692
        0.023076923076
        '''
        if self.denominator == 1:
            yield from repeat(str(self.numerator // self.denominator))
        if self.numerator > 0:
            representation = str(self.numerator // self.denominator) + '.'
        else:
            representation =\
                    '-' + str(abs(self.numerator) // self.denominator) + '.'
        for decimals in self.precision_many_decimals(
                               abs(self.numerator) % self.denominator * 10,
                               self.denominator, precision
                                                    ):
            representation += ''.join(str(d) for d in decimals)
            yield representation
        yield from repeat(representation)

    def precision_many_decimals(self, p, q, precision):
        while True:
            decimals = []
            for _ in range(precision):
                if not p:
                    yield decimals
                    return
                decimals.append(p // q)
                p = p % q * 10
            yield decimals
                    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
