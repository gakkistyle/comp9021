# COMP9021 Practice 1 - Solutions


'''
Draws an octagram, the inscribed octagon being coloured yellow,
and the colour of the triangles alternating red and blue.
'''


from turtle import *


small_edge_length = 100
long_edge_length = 180
angle = 45


def draw_triangle(i, colour):
    home()
    right((i + 0.5) * angle)
    forward(long_edge_length)
    pendown()
    color(colour)    
    begin_fill()
    goto(vertices[i])
    goto(vertices[i + 1])
    end_fill()
    penup()


vertices = []
penup()
for i in range(8):
    right(i * angle)
    forward(small_edge_length)
    vertices.append(pos())
    home()
vertices.append(vertices[0])
pendown()
color('yellow')
begin_fill()
for v in vertices:
    goto(v)
end_fill()
penup()
for i in range(4):
    draw_triangle(2 * i, 'blue')
    draw_triangle(2 * i + 1, 'red')
