# COMP9021 Term 3 2019


'''
Represents a quadratic equation as a class with a, b, c, root_1 and
root_2 as data. By default, a is set to 1 and b and c are set to 0.

The parameters can be changed with the update() function.

Whether the parameters are changed when the equation is created or by a
call to the update() function, a, b and c have to be explictly named.

The roots are automatically computed when the equation is created or
when some parameter is updated.
'''


from math import sqrt


class QuadraticEquationError(Exception):
    pass


class QuadraticEquation:
    '''
    >>> eq = QuadraticEquation.__new__(QuadraticEquation)
    >>> QuadraticEquation.__init__(eq, a=0, b=1)
    Traceback (most recent call last):
    ...
    QuadraticEquationError: a cannot be equal to 0.
    >>> eq1 = QuadraticEquation.__new__(QuadraticEquation)
    >>> QuadraticEquation.__init__(eq1)
    >>> eq1.a
    1
    >>> eq1.b
    0
    >>> eq1.c
    0
    >>> eq1.root_1
    0.0
    >>> eq1.root_2
    >>> eq2 = QuadraticEquation.__new__(QuadraticEquation)
    >>> QuadraticEquation.__init__(eq2, b=4)
    >>> eq2.a
    1
    >>> eq2.b
    4
    >>> eq2.c
    0
    >>> eq2.root_1
    -4.0
    >>> eq2.root_2
    0.0
    >>> eq3 = QuadraticEquation.__new__(QuadraticEquation)
    >>> QuadraticEquation.__init__(eq3, a=1, b=3, c=2)
    >>> eq3.a
    1
    >>> eq3.b
    3
    >>> eq3.c
    2
    >>> eq3.root_1
    -2.0
    >>> eq3.root_2
    -1.0
    >>> QuadraticEquation.update(eq3, a=0)
    Traceback (most recent call last):
    ...
    QuadraticEquationError: a cannot be equal to 0.
    >>> QuadraticEquation.update(eq3, b=-1)
    >>> eq3.root_1
    >>> eq3.root_2
    >>> QuadraticEquation.update(eq3, c=0.3, a=0.5)
    >>> eq3.root_1
    0.3675444679663241
    >>> eq3.root_2
    1.632455532033676
    >>>
    >>> # USUAL ALTERNATIVE SYNTAX
    >>>
    >>> QuadraticEquation(a=0, b=1)
    Traceback (most recent call last):
    ...
    QuadraticEquationError: a cannot be equal to 0.
    >>> eq1 = QuadraticEquation()
    >>> eq1.a
    1
    >>> eq1.b
    0
    >>> eq1.c
    0
    >>> eq1.root_1
    0.0
    >>> eq1.root_2
    >>> eq2 = QuadraticEquation(b=4)
    >>> eq2.a
    1
    >>> eq2.b
    4
    >>> eq2.c
    0
    >>> eq2.root_1
    -4.0
    >>> eq2.root_2
    0.0
    >>> eq3 = QuadraticEquation(a=1, b=3, c=2)
    >>> eq3.a
    1
    >>> eq3.b
    3
    >>> eq3.c
    2
    >>> eq3.root_1
    -2.0
    >>> eq3.root_2
    -1.0
    >>> eq3.update(a=0)
    Traceback (most recent call last):
    ...
    QuadraticEquationError: a cannot be equal to 0.
    >>> eq3.update(b=-1)
    >>> eq3.root_1
    >>> eq3.root_2
    >>> eq3.update(c=0.3, a=0.5)
    >>> eq3.root_1
    0.3675444679663241
    >>> eq3.root_2
    1.632455532033676
    '''
    def __init__(self, *, a=1, b=0, c=0):
        if a == 0:
            raise QuadraticEquationError('a cannot be equal to 0.')
        self.a = a
        self.b = b
        self.c = c
        self.compute_roots()

    def __repr__(self):
        '''
        >>> QuadraticEquation()
        QuadraticEquation(a=1, b=0, c=0)
        >>> QuadraticEquation(c=-5, a=2)
        QuadraticEquation(a=2, b=0, c=-5)
        >>> QuadraticEquation(b=1, a=-1, c=-1)
        QuadraticEquation(a=-1, b=1, c=-1)
        '''
        return f'QuadraticEquation(a={self.a}, b={self.b}, c={self.c})'

    def __str__(self):
        '''
        >>> print(QuadraticEquation())
        x^2 = 0
        >>> print(QuadraticEquation(c=-5, a=2))
        2x^2 - 5 = 0
        >>> print(QuadraticEquation(b=1, a=-1, c=-1))
        -x^2 + x - 1 = 0
        '''
        if self.a == 1:
            displayed_equation = 'x^2'
        elif self.a == -1:
            displayed_equation = '-x^2'
        else:
            displayed_equation = f'{self.a}x^2'
        if self.b == 1:
            displayed_equation += ' + x'
        elif self.b == -1:
            displayed_equation += ' - x'           
        elif self.b > 0:
            displayed_equation += f' + {self.b}x'
        elif self.b < 0:
            displayed_equation += f'- {-self.b}x'
        if self.c > 0:
            displayed_equation += f' + {self.c}'
        elif self.c < 0:
            displayed_equation += f' - {-self.c}'
        return f'{displayed_equation} = 0'

    def compute_roots(self):
        delta = self.b ** 2 - 4 * self.a * self.c
        if delta < 0:
            self.root_1 = self.root_2 = None
        elif delta == 0:
            self.root_1 = -self.b / (2 * self.a)
            self.root_2 = None
        else:
            sqrt_delta = sqrt(delta)
            self.root_1 = (-self.b - sqrt_delta) / (2 * self.a)
            self.root_2 = (-self.b + sqrt_delta) / (2 * self.a)

    def update(self, *, a=None, b=None, c=None):
        if a == 0:
            raise QuadraticEquationError('a cannot be equal to 0.')
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b
        if c is not None:
            self.c = c
        self.compute_roots()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
