# COMP9021 Term 3 2019


'''
A module to create finite probability distributions and events for
those, with probabilities defined as fractions for accurate computations
and displays.

A distribution can be conditionalised on an event. The complement of an
event, the intersection and union of two events, and the
conditionalisation of an event by another, can be computed. Any event
can be printed out in a way that displays its extension as well as its
probability.

A function can determine whether two events are independent.
'''


from collections.abc import Set
from fractions import Fraction


class FiniteProbabilityDistributionError(Exception):
    pass


class FiniteProbabilityDistribution:
    '''
    A finite probability distribution can be created from a set of
    elementary outcomes, in which case the distribution is uniform, each
    elementary outcome receiving the same mass. Alternatively, it can be
    created from a dictionary whose keys are elementary outcomes, and
    whose values are fractions to represent their masses.
    '''
    def __init__(self, μ):
        if isinstance(μ, Set):
            if not len(μ):
                raise FiniteProbabilityDistributionError(
                                  'The sample space should not be empty'
                                                        )                
            self.μ = {outcome: Fraction(1, len(μ)) for outcome in μ}
        else:
            if any(not isinstance(proba, Fraction) for proba in μ.values()):
                raise FiniteProbabilityDistributionError(
                                     'Probabilities should be Fractions'
                                                        )
            if sum(μ.values()) != 1:
                raise FiniteProbabilityDistributionError(
                                      'Probabilities should add up to 1'
                                                        )
            self.μ = μ
    
    def conditionalised_by(self, event):
        if event.distribution.μ is not self.μ:
            raise FiniteProbabilityDistributionError(
                          'Cannot conditionalise distribution on event '
                          'for another probability distribution'
                                                    )
        if not event.probability:
            raise FiniteProbabilityDistributionError(
                                  'Cannot conditionalise on event with '
                                  'probability mass of 0'
                                                    )
        return FiniteProbabilityDistribution(
                    {outcome: self.μ[outcome] / event.probability
                         for outcome in event.outcomes
                    }
                                            )
            
    def __repr__(self):
            return f'FiniteProbabilityDistribution({self.μ})'

    def __str__(self):
        return '\n'.join(outcome + ' : ' + str(self.μ[outcome])
                             for outcome in sorted(self.μ)
                        )    


class Event:
    def __init__(self, distribution, outcomes=set()):
        if any(outcome not in distribution.μ for outcome in outcomes):
            raise FiniteProbabilityDistributionError(
                                'Event not for probability distribution'
                                                    )
        self.distribution = distribution
        self.outcomes = outcomes
        self.probability = sum(self.distribution.μ[outcome]
                                   for outcome in self.outcomes
                              )
    
    def __invert__(self):
        return Event(self.distribution,
                     set(self.distribution.μ) - self.outcomes
                    )

    def __and__(self, other):
        if self.distribution.μ is not other.distribution.μ:
            raise FiniteProbabilityDistributionError(
                               'Cannot take intersection of events for '
                               'distinct probability distributions'
                                                    )
        return Event(self.distribution, self.outcomes & other.outcomes)

    def __add__(self, other):
        if self.distribution.μ is not other.distribution.μ:
            raise FiniteProbabilityDistributionError(
                             'Cannot take union of events for distinct '
                             'probability distributions'
                                                    )
        return Event(self.distribution, self.outcomes | other.outcomes)

    def __or__(self, other):
        if self.distribution.μ is not other.distribution.μ:
            raise FiniteProbabilityDistributionError(
                             'Cannot conditionalise event on event for '
                             'another probability distribution'
                                                    )
        return Event(self.distribution.conditionalised_by(other),
                     self.outcomes & other.outcomes
                    )

    def __repr__(self):
            return f'Event({repr(self.distribution)}, {self.outcomes})'

    def __str__(self):
        return ''.join(('{', ', '.join(sorted(self.outcomes)), '} : ',
                        str(self.probability)
                       )
                      )


def are_independent(event_1, event_2):
    if event_1.distribution.μ is not event_2.distribution.μ:
        raise FiniteProbabilityDistributionError(
                     'Both events not for same probability distribution'
                                                )
    return event_1.probability * event_2.probability ==\
                                               (event_1 & event_2).probability


if __name__ == '__main__':
    pd_1 = FiniteProbabilityDistribution({'a': Fraction(3, 8),
                                          'b': Fraction(1, 8),
                                          'c': Fraction(1, 3),
                                          'd': Fraction(1, 6)
                                         }
                                        )
    print('First example distribution')
    print(pd_1, end='\n\n')
    E_1 = Event(pd_1, {'a', 'b'})
    print('E_1', end='\t\t')
    print(E_1)
    print('~E_1', end='\t\t')
    print(~E_1)
    print('\nDistribution conditionalised by E_1')
    print(pd_1.conditionalised_by(E_1), end='\n\n')
    E_2 = Event(pd_1, {'b', 'c', 'd'})
    print('E_2', end='\t\t')
    print(E_2)
    print('E_1 & E_2', end='\t')
    print(E_1 & E_2)
    print('E_1 + E_2', end='\t')
    print(E_1 + E_2)
    if are_independent(E_1, E_2):
        print('\nE_1 and E_2 are independent\n')
    else:
        print('\nE_1 and E_2 are not independent\n')        
    E_3 = Event(pd_1, {'b', 'd'})
    print('E_3', end='\t\t')
    print(E_3)
    print('E_3 | E_2', end='\t')
    print(E_3 | E_2)
    print('E_1 | E_2', end='\t')
    print(E_1 | E_2)
    print('E_1 | ~E_1', end='\t')
    print(E_1 | ~E_1)
    print('\n')

    pd_2 = FiniteProbabilityDistribution(set('abcdefghijkl'))
    print('Second example distribution')
    print(pd_2, end='\n\n')
    F_1 = Event(pd_2, set('abcdijkl'))
    print('F_1', end='\t\t')
    print(F_1)
    print('~F_1', end='\t\t')
    print(~F_1)
    print('\nDistribution conditionalised by F_1')
    print(pd_2.conditionalised_by(F_1), end='\n\n')
    F_2 = Event(pd_2, set('abcdef'))
    print('F_2', end='\t\t')
    print(F_2)
    print('F_1 & F_2', end='\t')
    print(F_1 & F_2)
    print('F_1 + F_2', end='\t')
    print(F_1 + F_2)
    if are_independent(F_1, F_2):
        print('\nF_1 and F_2 are independent\n')
    else:
        print('\nF_1 and F_2 are not independent\n')        
    F_3 = Event(pd_2, set('bce'))
    print('F_3', end='\t\t')
    print(F_3)
    print('F_3 | F_2', end='\t')
    print(F_3 | F_2)
    print('F_1 | F_2', end='\t')
    print(F_1 | F_2)
    print()

    try:
        pd = FiniteProbabilityDistribution(set())
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        pd = FiniteProbabilityDistribution({'a': 0.5, 'b': 0.5})
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        pd = FiniteProbabilityDistribution({'a': Fraction(1, 2),
                                            'b': Fraction(1, 3)
                                           }
                                          )
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        pd = pd_1.conditionalised_by(F_1)
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        E = Event(pd_1, set('aCd'))
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        print(E_1 & F_1)
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        print(E_1 + F_1)
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        print(E_1 | F_1)
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        print(E_1 | Event(pd_1))
    except FiniteProbabilityDistributionError as error:
        print(error)
    try:
        are_independent(E_1, F_1)
    except FiniteProbabilityDistributionError as error:
        print(error)
