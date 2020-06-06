record = []
for i in range(10,80):
	li = []
	si = str(i)
	for e in si:
		li.append(e)
	if li[0] == li[1]:
		continue
	for j in range(20,90):
		lj = []
		sj = str(j)
		for e in sj:
			if e not in li:
				lj.append(e)
		if len(lj) != 2 or lj[0] == lj[1]:
			continue
		for k in range(30,100):
			lk = []
			sk = str(k)
			num = i*j*k
			for e in sk:
				if e not in li+lj:
					lk.append(e)
			if len(lk) != 2 or lk[0] == lk[1] or num < 100000 or num > 999999:
				continue
			sn = str(num)
			sum = li + lj + lk
			for e in sn:
				if e in sum:
					sum.remove(e)
			if sum == [] and num not in record:
				record.append(num)
				print(f'{i} X {j} X {k} = {num}')





