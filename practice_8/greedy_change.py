num = int(input('Input the desired amount: '))

diction = {'$100':0,'$50':0,'$20':0,'$10':0,'$5':0,'$2':0,'$1':0}

while num != 0:
	if num>=100:
		diction['$100'] += 1
		num = num -100
		continue
	if num>=50:
		diction['$50'] += 1
		num = num - 50
		continue
	if num>=20:
		diction['$20'] += 1
		num = num - 20
		continue
	if num>= 10:
		diction['$10'] += 1
		num = num - 10
		continue
	if num >= 5:
		diction['$5'] += 1
		num = num - 5
		continue
	if num >= 2:
		diction['$2'] += 1
		num = num - 2
		continue
	if num == 1:
		diction['$1'] += 1
		num = num - 1
		continue

sum = 0
for value in diction.values():
	sum += value
if sum == 1 :
	print(f'1 banknote is needed.')
else:
	print(f'{sum} banknotes are needed.')

print('The detail is:')
for key in diction.keys():
	if diction[key] > 0:
		print(f'{key:>{4}}: {diction[key]}')

