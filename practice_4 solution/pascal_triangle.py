import sys

def jiecheng(num1,num2):
	if num2 == 0:
		return 1
	result = 1
	for num in range(1,num2+1):
		result = result*(num1-num+1)/(num2-num+1)
	return result

def jiecheng_for_tri(row,index):
	return int((jiecheng(row-1,index-1)))

try:
	row = int(input('Enter a nonnegative integer: '))
except ValueError:
	print('wrong!')
	sys.exit()

if row == 0:
	print(1)

else:
	interval = len(str(jiecheng_for_tri(row+1,(1+(row+1)//2))))
	space = ' '
	for i in range (1,row+2):
		print(f'{space*interval*(row+1-i)}',end = '')
		for j in range(1,i+1):
			print(f'{jiecheng_for_tri(i,j):{interval}}',end = '')
			print(space*interval,end='')
		print()





