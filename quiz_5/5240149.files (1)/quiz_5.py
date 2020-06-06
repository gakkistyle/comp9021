# COMP9021 19T3 - Rachid Hamadi
# Quiz 5 *** Due Thursday Week 7
#
# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2,
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys


def encode(list_of_num):
    list_of_bin = [bin(e)[2:] for e in list_of_num]
    digit = ''
    for _ in range(len(list_of_bin)):
        for l in list_of_bin[_]:
            digit = digit + l*2
        if _ < len(list_of_bin) -1:
            digit += '0'
    result = int(digit,2)
    return result

    # REPLACE pass ABOVE WITH YOUR CODE    


def decode(num):
    orginal_bin = bin(num)[2:]
    result = []
    digit = ''
    i = 0
    while i < len(orginal_bin):
        if i+1 < len(orginal_bin) and orginal_bin[i] == orginal_bin[i+1]:
            digit = digit + orginal_bin[i]
            i += 2
        elif i+1 < len(orginal_bin) and orginal_bin[i] == '0' and orginal_bin[i+1] == '1':
            result.append(int(digit,2))
            digit = ''
            i += 1
        elif (i == len(orginal_bin)-1 and (orginal_bin[i] == '1' or orginal_bin[i] == '0') ) or (i+1 < len(orginal_bin) \
                                    and orginal_bin[i]=='1' and orginal_bin[i+1]=='0'):
            return None
    result.append(int(digit,2))
    return result


    # REPLACE pass ABOVE WITH YOUR CODE


# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))
