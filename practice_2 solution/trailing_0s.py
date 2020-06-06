import sys
from math import factorial

try:
	num = int(input('Input a nonnegative integer: '))
except ValueError:
	print('Incorrect input, giving up.')
	sys.exit()

if num < 0:
	print('Incorrect input, giving up.')
	sys.exit()

def devide_by_10(num):
    count = 0
    n = factorial(num)
    while (n%10) == 0:
        n = n//10
        count=count+1
    return count

def str_use(num):
    n = factorial(num)
    count = 0
    str_num = str(n)
    i = -1
    while str_num[i]=='0':
        i=i-1
        count=count+1
    return count

def easy_way(num):
    count = 0
    if num == 0:
        return 0
    else:
        for i in range(1,num+1):
            j = i
            while j % 5 == 0:
                count = count + 1
                j = j / 5
        return count

print(f'Computing the number of trailing 0s in {num}! by dividing by 10 for long enough:',devide_by_10(num))
print(f'Computing the number of trailing 0s in {num}! by converting it into a string:',str_use(num))
print(f'Computing the number of trailing 0s in {num}! the smart way:',easy_way(num))
