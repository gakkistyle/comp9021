# COMP9021 Term 3 2019


'''
A quadratic equation is represented as a dictionary whose keys are
a, b, c, root_1 and root_2. The value of a should be different to 0.

A dictionary QuadraticEquation packages the following functions:
* initialise(), to create an equation -- by default, the value of a is
  set to 1 and the values of b and c are set to 0;
* update() to change the parameters of an equation;
* display() to nicely display an equation.

Whether the parameters are changed by initialise() when the equation
is created or by a call to update(), a, b and c have to be explicitly
named.

The roots are automatically computed when the equation is created or
when some parameter is updated.
'''


from math import sqrt


def initialise(*, a=1, b=0, c=0):
    '''
    >>> QuadraticEquation['initialise'](a=0, b=1)
    a cannot be equal to 0.
    >>> eq1 = QuadraticEquation['initialise']()
    >>> eq1['a']
    1
    >>> eq1['b']
    0
    >>> eq1['c']
    0
    >>> eq1['root_1']
    0.0
    >>> eq1['root_2']
    >>> eq2 = QuadraticEquation['initialise'](b=4)
    >>> eq2['a']
    1
    >>> eq2['b']
    4
    >>> eq2['c']
    0
    >>> eq2['root_1']
    -4.0
    >>> eq2['root_2']
    0.0
    >>> eq3 = QuadraticEquation['initialise'](a=1, b=3, c=2)
    >>> eq3['a']
    1
    >>> eq3['b']
    3
    >>> eq3['c']
    2
    >>> eq3['root_1']
    -2.0
    >>> eq3['root_2']
    -1.0
    >>> QuadraticEquation['update'](eq3, a=0)
    a cannot be equal to 0.
    >>> QuadraticEquation['update'](eq3, b=-1)
    >>> eq3['root_1']
    >>> eq3['root_2']
    >>> QuadraticEquation['update'](eq3, c=0.3, a=0.5)
    >>> eq3['root_1']
    0.3675444679663241
    >>> eq3['root_2']
    1.632455532033676
    '''
    if a == 0:
        print('a cannot be equal to 0.')
        return
    equation = {'a': a, 'b': b, 'c': c, 'root_1': None, 'root_2': None}
    QuadraticEquation['compute_roots'](equation)
    return equation


def display(equation):
    '''
    >>> QuadraticEquation['display'](QuadraticEquation['initialise']())
    x^2 = 0
    >>> QuadraticEquation['display'](QuadraticEquation['initialise']\
                                                            (c=-5, a=2)\
                                    )
    2x^2 - 5 = 0
    >>> QuadraticEquation['display'](QuadraticEquation['initialise']\
                                                      (b=1, a=-1, c=-1)\
                                    )
    -x^2 + x - 1 = 0

    '''
    a, b, c = equation['a'], equation['b'], equation['c']
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
    a, b, c = equation['a'], equation['b'], equation['c']
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        equation['root_1'] = equation['root_2'] = None
    elif delta == 0:
        equation['root_1'] = -b / (2 * a)
        equation['root_2'] = None
    else:
        sqrt_delta = sqrt(delta)
        equation['root_1'] = (-b - sqrt_delta) / (2 * a)
        equation['root_2'] = (-b + sqrt_delta) / (2 * a)


def update(equation, *, a=None, b=None, c=None):
    if a == 0:
        print('a cannot be equal to 0.')
        return
    if a is not None:
        equation['a'] = a
    if b is not None:
        equation['b'] = b
    if c is not None:
        equation['c'] = c
    QuadraticEquation['compute_roots'](equation)


QuadraticEquation = {'initialise': initialise,
                     'display': display,
                     'compute_roots': compute_roots,
                     'update': update
                    }


if __name__ == '__main__':
    import doctest
    doctest.testmod()
