import sys
try:
	num = int(input('Enter strictly positive number: '))
except ValueError:
	print('sys exit')
	sys.exit()

if num <= 0:
	print('sys exit')
	sys.exit()

line = []
pointer = 65

for i in range(1,num+1):
	space = ''
	for _ in range(num - i):
		space += ' '
	print(space,end = '')
	track = []
	for j in range(i):
		print(chr(pointer),end = '')
		if j != i-1:
			track.append(chr(pointer))
		if pointer < 90:
			pointer += 1
		else:
			pointer = 65
	for k in range(-1,-len(track)-1,-1):
		print(track[k],end = '')
	print()

	
