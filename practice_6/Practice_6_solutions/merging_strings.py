# COMP9021 Practice 6 - Solutions


'''
Say that two strings s_1 and s_2 can be merged into a third string s_3
if s_3 is obtained from s_1 by inserting arbitrarily in s_1 the characters in s_2,
respecting their order. For instance, the two strings ab and cd can be merged
into abcd, or cabd, or cdab, or acbd, or acdb..., but not into adbc nor into cbda.

Prompts the user for 3 strings and displays the output as follows:
- If no string can be obtained from the other two by merging, then the program
  outputs that there is no solution.
- Otherwise, the program outputs which of the strings can be obtained
  from the other two by merging.
'''


def can_merge(string_1, string_2, string_3):
    if not string_1 and string_2 == string_3:
        return True
    if not string_2 and string_1 == string_3:
        return True
    if not string_1 or not string_2:
        return False
    if string_1[0] == string_3[0] and can_merge(string_1[1: ], string_2, string_3[1: ]):
        return True
    if string_2[0] == string_3[0] and can_merge(string_1, string_2[1: ], string_3[1: ]):
        return True
    return False

ranks = 'first', 'second', 'third'
strings = [input(f'Please input the {rank} string: ') for rank in ranks]
last = 0
if len(strings[1]) > len(strings[0]):
    last = 1
if len(strings[2]) > len(strings[last]):
    last = 2
if last == 0:
    first, second = 1, 2
elif last == 1:
    first, second = 0, 2
else:
    first, second = 0, 1
if len(strings[last]) != len(strings[first]) + len(strings[second]) or\
                                      not can_merge(strings[first], strings[second], strings[last]):
    print('No solution')
else:
    print(f'The {ranks[last]} string can be obtained by merging the other two.')


    
