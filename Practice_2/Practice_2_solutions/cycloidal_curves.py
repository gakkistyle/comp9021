# COMP9021 Practice 2 - Solutions


'''
Prompts the user to
- choose between drawing either a hypotrochoid or an epitrochoid,
- input the radius of the fixed circle,
- input the radius of the rolling circle,
- input the distance between the drawing point and the centre of the rolling circle,
and uses turtle to draw the chosen hypotrochoid or epitrochoid.

Gives the user the option to save the file as a pdf after the picture has been drawn.
'''


from math import gcd, radians, cos, sin
import os

from PIL import Image
import turtle


# save needs /usr/local/bin/gs
os.environ['PATH'] += ':/usr/local/bin'


def save(trochoid, R, r, d):
    filename = ''.join((trochoid, '_', str(R), '_', str(r), '_', str(d)))
    eps_filename = filename + '.eps'
    turtle.getcanvas().postscript(file = eps_filename)
    Image.open(eps_filename).save(filename + '.pdf', 'pdf')
    os.remove(eps_filename)


user_input = turtle.textinput('Hypotrochoid or Epitrochoid?', 'Provide no input for an '
                                                     'Epitrochoid, and any input for a Hypotrochoid'
                             )
direction = 2 * (user_input == '') - 1
trochoid = 'Epitrochoid' if direction == 1 else 'Hypotrochoid'
dim = min(turtle.screensize())
min_R, max_R = 10, dim - 10
R = turtle.numinput('Fixed circle', f'Radius R between {min_R} and {max_R}: ',
                                                                      minval = min_R, maxval = max_R
                   )
R = round(R)
# max_r defined in such a way that centre of rolling circle is at most dim away from origin.
min_r, max_r = 10, dim - direction * R
r = turtle.numinput('Rolling circle', f'Radius r between {min_r} and {max_r}: ',
                                                                      minval = min_r, maxval = max_r
                   )
r = round(r)
# d defined in such a way that drawing point is at most dim away from origin.
min_d, max_d = (0, dim - R - direction * r) if direction == 1 or r < R else (0, dim - r + R)
d = turtle.numinput('Point', 'Distance d to centre of rolling circle '
                                    f'between {min_d} and {max_d}: ', minval = min_d, maxval = max_d
                   )
d = round(d)
period = r // gcd(r, R)
turtle.title(f'{trochoid} for R = {R}, r = {r}, d = {d} -- Period = {period}')
a = R + direction * r
b = a / r
turtle.hideturtle()
turtle.up()
turtle.setx(a - direction * d)
turtle.down()
turtle.fillcolor('green') if direction == 1 else turtle.fillcolor('yellow')    
turtle.begin_fill()
if d == 0:
    # It is a circle, we draw it only once rather than period many times.
    period = 1
for i in range(0, 360 * period + 1):
    print(i)
    theta = radians(i)
    psi = b * theta
    turtle.goto(a * cos(theta) - direction * d * cos(psi), a * sin(theta) - d * sin(psi))
turtle.end_fill()
turtle.listen()
# Press S after trochoid has been drawn to save it as a pdf.
turtle.onkey(lambda trochoid = trochoid, R = R, r = r, d = d: save(trochoid, R, r, d), 'S')
turtle.mainloop()
