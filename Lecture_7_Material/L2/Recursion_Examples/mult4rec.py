# COMP9021 Term 3 2019
# Rachid Hamadi

def mult4(n):
	if n == 1:
		return 4
	return mult4(n-1) + 4
	
print(mult4(5))