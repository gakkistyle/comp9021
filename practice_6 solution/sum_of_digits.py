digits = input('Input a number that we will use as available digits: ')

disired_sum = int(input('Input a number that represents the desired sum: '))


count = 0
for i in range(len(digits)-1):
	sub = disired_sum - int(digits[i])
	if sub == 0:
		count = count+1
		continue
	elif sub < 0:
		continue
	else:
		j = i+1
		subcopy = sub
		while sub > 0 and j<len(digits):
			if sub-int(digits[j]) <0:
				j = j+1
				continue
			if
			sub = sub- int(digits[j])
			if sub == 0:
				count += 1
				j = j+1
				sub = subcopy
				continue
			if sub in digits[]
			j = j+1


if count == 0:
	print('There is no solution.')
elif count == 1:
	print('There is a unique solution.')
else:
	print(f'There are {count} solutions.')





 