


'''
Draws three coloured dodecagrams, separed by a distance of one third
the length of the edges, and centred in the window that displays them.
'''


from turtle import *


edge_length = 150
angle = 150


def draw_dodecagram(colour):
    color(colour)
   
    for _ in range(12):
        forward(edge_length)
        left(angle)
   

def teleport(distance):
    penup()      
    forward(distance)
    pendown()


# Make sure that the dodecagrams are centred horizontally in the window that displays them.
# Without the following statement, the left end of the horizontal edge of the green dodecagram,
# from which the drawing starts, would be at the centre of the screen
# (so the dodecagrams are not quite centred vertically).
teleport(- edge_length // 2)
# Draw the middle dodecagram, then the left dodecagram, then the right dodecagram.
draw_dodecagram('green')
teleport(- 4 * edge_length // 3)
draw_dodecagram('red')
teleport(8 * edge_length // 3)
draw_dodecagram('blue')
