import sys

alphabet = input('Please input a string of lowercase letters: ')
if alphabet.isalpha() == False and alphabet.islower() == False:
	print('This is not a valid input.')
	sys.exit()
alpha = []
for e in alphabet:
	alpha.append(e)

alpha.sort()
result = [[]]

index = 0
for _ in range(len(alpha)):
	if _+1 < len(alpha) and ord(alpha[_+1])-ord(alpha[_]) == 1 and alphabet.index(alpha[_])<alphabet.index(alpha[_+1]):
		if(len(result[0])) == 0:
			result[index] += alpha[_]
		result[index]+= alpha[_+1]
	elif _+2 < len(alpha) and  ord(alpha[_+1])-ord(alpha[_]) > 1 and alphabet.index(alpha[_+1])<alphabet.index(alpha[_+2]):
		result.append([alpha[_+1]])
		index = index+1

length = []
for e in result:
	length.append(len(e))
biggest_index = 0
for l in range(1,len(length)):
	if length[l] > length[biggest_index]:
		biggest_index = l
	elif l!=biggest_index and length[l] == length[biggest_index]:
		index1 = alpha.index(result[l][0])
		index2 = alpha.index(result[biggest_index][0])
		if index1 < index2:
			biggest_index = l

print('The solution is:',''.join(result[biggest_index]))
