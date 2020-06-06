from turtle import *

edge_length = 50
angle1 = 60
angle2 = 120

def draw_hexagram(color1,color2):
	color(color1)
	for _ in range(3):
		forward(edge_length)
		color(color2)
		left(angle1)
		forward(edge_length)
		right(angle2)
		forward(edge_length)
		color(color1)
		left(angle1)
		forward(edge_length)
		right(angle2)

def teleport(distance):
	penup()
	forward(-3*distance/2)
	pendown()

teleport(edge_length)
draw_hexagram('blue','red')

