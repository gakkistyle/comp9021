# COMP9021 Practice 7 - Solutions


import re


def diophantine(equation):
    '''
    >>> diophantine('1x + 1y = 0')
    1x + 1y = 0 has as solutions all pairs of the form
        (n, -n) with n an arbitrary integer.
    >>> diophantine('-1x + 1y = 0')
    -1x + 1y = 0 has as solutions all pairs of the form
        (n, n) with n an arbitrary integer.
    >>> diophantine('1x - 1y = 0')
    1x - 1y = 0 has as solutions all pairs of the form
        (n, n) with n an arbitrary integer.
    >>> diophantine('-1x - 1y = 0')
    -1x - 1y = 0 has as solutions all pairs of the form
        (n, -n) with n an arbitrary integer.
    >>> diophantine('1x + 1y = -1')
    1x + 1y = -1 has as solutions all pairs of the form
        (n, -1 - n) with n an arbitrary integer.
    >>> diophantine('-1x + 1y = 1')
    -1x + 1y = 1 has as solutions all pairs of the form
        (n, 1 + n) with n an arbitrary integer.
    >>> diophantine('4x + 6y = 9')
    4x + 6y = 9 has no solution.
    >>> diophantine('4x + 6y = 10')
    4x + 6y = 10 has as solutions all pairs of the form
        (1 + 3n, 1 - 2n) with n an arbitrary integer.
    >>> diophantine('71x+83y=2')
    71x + 83y = 2 has as solutions all pairs of the form
        (69 + 83n, -59 - 71n) with n an arbitrary integer.
    >>> diophantine('  782  x  +  253  y  =  92')
    782x + 253y = 92 has as solutions all pairs of the form
        (4 + 11n, -12 - 34n) with n an arbitrary integer.
    >>> diophantine('-123x -456y = 78')
    -123x - 456y = 78 has as solutions all pairs of the form
        (118 + 152n, -32 - 41n) with n an arbitrary integer.
    >>> diophantine('-321x +654y = -87')
    -321x + 654y = -87 has as solutions all pairs of the form
        (149 + 218n, 73 + 107n) with n an arbitrary integer.
    '''
    a_x_plus_b, c = re.split('y\s*=', re.sub(' ', '', equation))
    c = int(c)
    a, b = a_x_plus_b.split('x')
    a = int(a)
    b = int(b)
    if b >= 0:
        equation = f'{a}x + {b}y = {c}'
    else:
        equation = f'{a}x - {-b}y = {c}'
    # gcd = gcd(|a|,|b|)
    # x|a| + y|b| = gcd
    gcd, x, y = extended_euclid(abs(a), abs(b))
    if c % gcd:
        print(equation, 'has no solution.')
        return
    m = c // gcd
    a_sign = 2 * (a > 0) - 1
    b_sign = 2 * (b > 0) - 1
    x *= a_sign * m
    y *= b_sign * m
    # At this point, x.a + y.b = c.
    # Since lcm(a,b).gcd(a,b) = |a||b|,
    # solutions are of the form x.a + |b|/gcd.n + y.b - sign_product|a|/gcd.n = c,
    # hence of the form x.a + x_step.n + y.b - sign_product.y_step.n = c.
    x_step = abs(b) // gcd
    y_step = abs(a) // gcd
    sign_product = a_sign * b_sign
    # As x_step is positive, x%x_step is positive.
    # Changing x to x%x_step requires to:
    # - if x//x_step > 0, subtracting x_step from x, x//x_step times;
    # - if x//x_step < 0, adding x_step to x, -(x//x_step) times.
    # It is then necessary to:
    # - if x//x_step > 0, addding sign_product.y_step to y, x//x_step times;
    # - if x//x_step < 0, subtracting sign_product.y_step from x, -(x//x_step) times.
    y += x // x_step * sign_product * y_step
    x %= x_step
    if x_step == 1:
        x_step = '' 
    if y_step == 1:
        y_step = ''
    print(equation, 'has as solutions all pairs of the form')
    if not x:
        if x_step == '':
            print('    (n,', end = ' ')
        else:
            print(f'    ({x} + {x_step}n,', end = ' ')
    else: 
        print(f'    ({x} + {x_step}n,', end = ' ')
    if not y:
        if y_step == '':
            print(f'{sign_product == 1 and "-n" or "n"})', end = ' ')
        else:
            print(f'{-sign_product * y_step}n)', end = ' ')
    elif sign_product < 0:
        print(f'{y} + {y_step}n)', end = ' ')
    else:
        print(f'{y} - {y_step}n)', end = ' ')
    print('with n an arbitrary integer.')
    
def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x, y = extended_euclid(b, a % b)
    return gcd, y, x - (a // b) * y


if __name__ == '__main__':
    import doctest
    doctest.testmod()
