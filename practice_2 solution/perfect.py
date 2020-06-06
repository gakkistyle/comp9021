import sys

try:
	num=int(input('Input an integer: '))
except ValueError:
	print('It is not an integer,giving up.')
	sys.exit()

if num<= 0:
	print('It is not a positive integer,giving up.')
	sys.exit()

perfect = []
for i in range(1,num):
	divisor = []
	for j in range(1,i//2+1):
		if i%j == 0:
			divisor.append(j)
	if divisor:
		s = sum(divisor)
		if s == i:
			perfect.append(i)


for _ in perfect:
	print(_,'is a perfect number.')

	
