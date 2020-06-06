# COMP9021 Practice 5 - Solutions


'''
Prompts the user for a string w of lowercase letters and outputs the longest
sequence of consecutive letters that occur in w, but with possibly other letters
in between, starting as close as possible to the beginning of w.
'''


import sys


word = input('Please input a string of lowercase letters: ')
if not all(c.islower() for c in word):
    print('Incorrect input.')
    sys.exit()
longest_length = 0
start = None
current_start = 0
while current_start < len(word) - longest_length:
    current_length = 1
    last_in_sequence = ord(word[current_start])
    for i in range(current_start + 1, len(word)):
        if ord(word[i]) - last_in_sequence == 1:
            current_length += 1
            last_in_sequence = ord(word[i])
    if current_length > longest_length:
        longest_length = current_length
        start = current_start
    while current_start < len(word) - 1 and\
                                       ord(word[current_start + 1]) - ord(word[current_start]) == 1:
        current_start += 1
    current_start += 1
print('The solution is:', ''.join(chr(ord(word[start]) + i) for i in range(longest_length)))
