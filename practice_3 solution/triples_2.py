from math import sqrt

for i in range(100,998):
	sign = 0
	stop = 0
	for _ in range(0,int(sqrt(i))+1):
		for q in range(_,int(sqrt(i))+1):
			if _**2 + q**2 == i:
				sign = 1
				list_i = [_,q]
				break
		if sign == 1:
			sign = 0
			break
		if _ == int(sqrt(i)):
			stop = 1
	if stop == 1:
		stop = 0
		continue
	for w in range(0,int(sqrt(i+1))+1):
		for e in range(w,int(sqrt(i+1))+1):
			if w**2 + e**2 == i+1:
				sign = 1
				list_j = [w,e]
				break
		if sign == 1:			
			sign = 0
			break
		if w == int(sqrt(i+1)):
			stop = 1
	if stop == 1:
		stop = 0
		continue
	for _ in range(0,int(sqrt(i+2))+1):
		for q in range(_,int(sqrt(i+2))+1):
			if _**2 + q**2 == i+2:
				sign = 1
				list_k = [_,q]
				break
		if sign == 1:
			sign = 0
			break
		if _ == int(sqrt(i+2)):
			stop = 1
	if stop == 1:
		stop = 0
		continue
	print(f'({i}, {i+1}, {i+2}) (equal to ({list_i[0]}^2+{list_i[1]}^2, {list_j[0]}^2+{list_j[1]}^2, {list_k[0]}^2+{list_k[1]}^2)) is a solution.')









