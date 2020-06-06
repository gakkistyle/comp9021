from math import sqrt

def finddivisors(num):
	result = []
	for i in range(1,num+1):
		if num % i == 0:
			result.append(i)
	return result

def isprime(n):
	for i in range(2,int(sqrt(n))+1):
		if n% i == 0:
			return False
	return True

def factorsprint(num):
	subfactors = []
	for i in finddivisors(num):
		if i ==1 or i == num:
			continue
		else:
			if isprime(i):
				subfactors.append(i)
	result = []
	while num != 1:
		for e in subfactors:
			if num % e == 0:
				result.append(str(e))
				num = num // e

	result.sort()
	printresult = ''
	for _ in range(len(result)):

		if _+1 < len(result) and result[_] == result[_+1]:
			printresult = printresult + result[_]+'^'
		elif _+1 < len(result):
			printresult = printresult + result[_]+'x'
		else:
			printresult = printresult + result[_]
	return printresult


def make_hasse_diagram(num):
	factors = {}
	vertices = {}
	edges = {}
	divisors = finddivisors(num)
	primes = [n for n in divisors if isprime(n)]
	for _ in divisors:
		if _ == 1:
			factors[_] = '1' 
		if isprime(_):
			factors[_] = str(_)
		else :
			factors[_] = factorsprint(_)
	return factors
	#return (factors,vertices,edges)



print(make_hasse_diagram(30))

