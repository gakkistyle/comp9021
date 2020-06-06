# COMP9021 Practice 1 - Solutions


'''
Draws an hexagram centred in the window that displays it,
with the colour of the tips alternating red and blue.
'''


from turtle import *


edge_length = 150
angle = 120


def draw_triangle(colour):
    color(colour)
    for _ in range(3):
        forward(edge_length // 3)
        penup()
        forward(edge_length // 3)
        pendown()
        forward(edge_length // 3)
        left(angle)


# Make sure that the hexagram is centred horizontally in the window that displays it.
penup()
forward(- edge_length // 2)
pendown()
draw_triangle('red')
penup()
forward(edge_length // 3)
left(angle)
forward(2 * edge_length // 3)
left(180)
pendown()
draw_triangle('blue')
