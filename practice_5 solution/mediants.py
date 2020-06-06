import sys

def not_gcd(p,q):
	for i in range(2,min(p,q)+1):
		if p % i ==0 and q % i == 0:
			return True
	return False

def mediants_to(p,q):
	'''
    >>> mediants_to(1, 2)
    0/1     1/2     1/1
    >>> mediants_to(41, 152)
      0/1    *    1/2         1/1
      0/1    *    1/3         1/2
      0/1         1/4    *    1/3
      1/4    *    2/7         1/3
      1/4    *    3/11        2/7
      1/4         4/15   *    3/11
      4/15        7/26   *    3/11
      7/26   *   10/37        3/11
      7/26   *   17/63       10/37
      7/26       24/89   *   17/63
     24/89       41/152      17/63
    >>> mediants_to(71, 83)
     0/1       1/2   *   1/1
     1/2       2/3   *   1/1
     2/3       3/4   *   1/1
     3/4       4/5   *   1/1
     4/5       5/6   *   1/1
     5/6   *   6/7       1/1
     5/6      11/13  *   6/7
    11/13     17/20  *   6/7
    17/20     23/27  *   6/7
    23/27     29/34  *   6/7
    29/34     35/41  *   6/7
    35/41     41/48  *   6/7
    41/48     47/55  *   6/7
    47/55     53/62  *   6/7
    53/62     59/69  *   6/7
    59/69     65/76  *   6/7
    65/76     71/83      6/7

	'''
	if p <=0 or q <= 0 or p>=q or not_gcd(p,q):
		print('Wrong input.')
		sys.exit()
	else:
		first_u = 0
		first_d = 1
		second_u = 1
		second_d = 2
		third_u = 1
		third_d = 1
		lar = len(str(q))
		while p/q != second_u/second_d:
			if p/q < second_u/second_d:
				print(f'{first_u:{lar}d}/{first_d:<{lar}d}  *  {second_u:{lar}d}/{second_d:<{lar}d}     {third_u:{lar}d}/{third_d}')
				third_d = second_d
				third_u = second_u
				second_u = first_u + second_u
				second_d = first_d + second_d
			else:
				print(f'{first_u:{lar}d}/{first_d:<{lar}d}     {second_u:{lar}d}/{second_d:<{lar}d}  *  {third_u:{lar}d}/{third_d}')
				first_d = second_d
				first_u = second_u
				second_u = second_u + third_u
				second_d = second_d + third_d
		print(f'{first_u:{lar}d}/{first_d:<{lar}d}     {second_u:{lar}d}/{second_d:<{lar}d}     {third_u:{lar}d}/{third_d}')
		



if __name__ == '__main__':
	import doctest
	doctest.testmod()
