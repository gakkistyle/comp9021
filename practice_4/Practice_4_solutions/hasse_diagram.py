# COMP9021 Practice 3 - Solutions


from collections import defaultdict, namedtuple
from functools import reduce
from itertools import product
from operator import mul, itemgetter
from pprint import pprint


def make_hasse_diagram(n):
    '''
    >>> HD = make_hasse_diagram(12)
    >>> HD # doctest: +ELLIPSIS
    HasseDiagram(factors=..., edges=..., vertices=...)
    >>> HD.factors
    {1: '1', 2: '2', 3: '3', 4: '2^2', 6: '2x3', 12: '2^2x3'}
    >>> pprint(HD.vertices)
    {1: ([], [2, 3]),
     2: ([1], [4, 6]),
     3: ([1], [6]),
     4: ([2], [12]),
     6: ([2, 3], [12]),
     12: ([4, 6], [])}
    >>> HD.edges
    {2: [(1, 2), (2, 4), (3, 6), (6, 12)], 3: [(1, 3), (2, 6), (4, 12)]}
    >>> HD = make_hasse_diagram(30)
    >>> HD # doctest: +ELLIPSIS
    HasseDiagram(factors=..., edges=..., vertices=...)
    >>> HD.factors
    {1: '1', 2: '2', 3: '3', 5: '5', 6: '2x3', 10: '2x5', 15: '3x5', 30: '2x3x5'}
    >>> pprint(HD.vertices)
    {1: ([], [2, 3, 5]),
     2: ([1], [6, 10]),
     3: ([1], [6, 15]),
     5: ([1], [10, 15]),
     6: ([2, 3], [30]),
     10: ([2, 5], [30]),
     15: ([3, 5], [30]),
     30: ([6, 10, 15], [])}
    >>> pprint(HD.edges)
    {2: [(1, 2), (3, 6), (5, 10), (15, 30)],
     3: [(1, 3), (2, 6), (5, 15), (10, 30)],
     5: [(1, 5), (2, 10), (3, 15), (6, 30)]}
    '''
    prime_factors = {}
    p = 2
    while n != 1:
        if n % p == 0:
            k = 1
            while n % p == 0:
                n //= p
                k += 1
            # prime_factors[p] is 1 + p's multiplicity in n
            prime_factors[p] = k
        p += 1
    factors = {1: '1'}
    edges = {p: set() for p in prime_factors}
    vertices = defaultdict(lambda: (set(), set()))
    vertices[1][1].update(prime_factors)
    possible_powers = product(*(range(i) for i in prime_factors.values()))
    # Discard (0, ..., 0): 1 is special
    next(possible_powers)
    for powers in possible_powers:
        factor = reduce(mul, (p ** m for (p, m) in zip(prime_factors, powers)))
        factors[factor] = 'x'.join(m == 1 and str(p) or '^'.join((str(p), str(m)))
                                       for (p, m) in zip(prime_factors, powers) if m
                                  )
        for (p, m) in filter(itemgetter(1), zip(prime_factors, powers)):
            smaller_factor = factor // p
            edges[p].add((smaller_factor, factor))
            vertices[smaller_factor][1].add(factor)
            vertices[factor][0].add(smaller_factor)
    sorted_factors = sorted(factors)
    return namedtuple('HasseDiagram',
                      ['factors', 'edges', 'vertices']
                     )({factor: factors[factor] for factor in sorted_factors},
                       {p: sorted(edges[p]) for p in prime_factors},
                       {v: (sorted(vertices[v][0]), sorted(vertices[v][1]))
                               for v in sorted_factors
                       }
                      )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    