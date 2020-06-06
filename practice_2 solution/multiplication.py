count = []
numhun = []
numten = []
for huns in range(100,1000):
	for tens in range(10,100):
		four_digit = huns*(tens%10)
		three_digit = huns*(tens//10)
		if (tens%10)*huns<1000 or (tens//10)*huns>=1000 or four_digit+three_digit>9999:
			continue
		gewei = (huns%10)+(tens%10)+(four_digit%10)*2
		shiwei = ((huns%100)//10)+(tens//10)+(((four_digit%100)//10)+(three_digit%10))*2
		baiwei = (huns//100)+(((four_digit//100)%10)+((three_digit%100)//10))*2
		qianwei = ((four_digit//1000)+(three_digit//100))*2
		if gewei == shiwei and gewei == baiwei and gewei == qianwei:
			count.append(gewei)
			numhun.append(huns)
			numten.append(tens)
for _ in range(len(count)):
	print(f'{numhun[_]} * {numten[_]} = {numhun[_]*numten[_]}, all columns adding up to {count[_]}.')