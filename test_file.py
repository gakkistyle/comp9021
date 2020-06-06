m = []
with open('maze_2.txt') as file:
	i = 0
	for l in file:
		m.append([])
		for e in l :
			if e.isdigit():
				m[i].append(int(e))
		i += 1		
print(m)