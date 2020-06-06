# COMP9021 Term 3 2019
# Rachid Hamadi

def add(a,b):
	if b == 0:
		return a
	return add(a,b-1) + 1
	
print(add(4,9))
