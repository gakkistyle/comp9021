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


def initialise(equation, *, a=1, b=0, c=0):
    '''
    >>> eq = QuadraticEquation.__new__(QuadraticEquation)
    >>> QuadraticEquation.__init__(eq, a=0, b=1)
    a cannot be equal to 0.
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
    a cannot be equal to 0.
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
    >>> QuadraticEquation(a=0, b=1) # doctest: +ELLIPSIS
    a cannot be equal to 0.
    ...
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
    a cannot be equal to 0.
    >>> eq3.update(b=-1)
    >>> eq3.root_1
    >>> eq3.root_2
    >>> eq3.update(c=0.3, a=0.5)
    >>> eq3.root_1
    0.3675444679663241
    >>> eq3.root_2
    1.632455532033676
    '''
    if a == 0:
        print('a cannot be equal to 0.')
        return
    equation.a = a
    equation.b = b
    equation.c = c
    QuadraticEquation.compute_roots(equation)


def display(equation):
    '''
    >>> QuadraticEquation.display(QuadraticEquation())
    x^2 = 0
    >>> QuadraticEquation.display(QuadraticEquation(c=-5, a=2))
    2x^2 - 5 = 0
    >>> QuadraticEquation.display(QuadraticEquation(b=1, a=-1, c=-1))
    -x^2 + x - 1 = 0
    '''
    a, b, c = equation.a, equation.b, equation.c
    if a == 1:
        displayed_equation = 'x^2'
    elif a == -1:
        displayed_equation = '-x^2'
    else:
        displayed_equation = f'{a}x^2'
    if b == 1:
        displayed_equation += ' + x'
    elif b == -1:
        displayed_equation += ' - x'           
    elif b > 0:
        displayed_equation += f' + {b}x'
    elif b < 0:
        displayed_equation += f'- {-b}x'
    if c > 0:
        displayed_equation += f' + {c}'
    elif c < 0:
        displayed_equation += f' - {-c}'
    print(displayed_equation, 0, sep=' = ')


def compute_roots(equation):
    a, b, c = equation.a, equation.b, equation.c
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        equation.root_1 = equation.root_2 = None
    elif delta == 0:
        equation.root_1 = -b / (2 * a)
        equation.root_2 = None
    else:
        sqrt_delta = sqrt(delta)
        equation.root_1 = (-b - sqrt_delta) / (2 * a)
        equation.root_2 = (-b + sqrt_delta) / (2 * a)


def update(equation, *, a=None, b=None, c=None):
    if a == 0:
        print('a cannot be equal to 0.')
        return
    if a is not None:
        equation.a = a
    if b is not None:
        equation.b = b
    if c is not None:
        equation.c = c
    QuadraticEquation.compute_roots(equation)


QuadraticEquation = type('QuadraticEquation', (),
                         {'__init__' : initialise, 'display': display,
                          'compute_roots': compute_roots, 'update': update
                         }
                        )
           
           
if __name__ == '__main__':
    import doctest
    doctest.testmod()
