# COMP9021 19T3 - Rachid Hamadi
# Quiz 3 *** Due Thursday Week 4


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
     )
print()

# INSERT YOUR CODE HERE
read = '0'*nb_of_leading_zeroes + f'{int(code):o}'
len_read = len(read)
graph_list = [[on]]
current_location = [0,0]
for i in range(len_read):
    readstr = read[-i-1]
    raw = len(graph_list)
    colum = len(graph_list[0])
    if readstr == '0':
        if current_location[0] == 0:
            graph_list.insert(0,[off for num in range(colum)])
            graph_list[0][current_location[1]] = on
            continue
        if graph_list[current_location[0]-1][current_location[1]] == on:
            current_location[0] -= 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[0] -= 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '2':
        if current_location[1]==colum-1:
            for _ in range(raw):
                graph_list[_].append(off)
            current_location[1] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]][current_location[1]+1] == on:
            current_location[1]+= 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[1] += 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '4':
        if current_location[0] == raw-1:
            graph_list.append([off for num in range(colum)])
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]+1][current_location[1]] == on:
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[0] += 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '6':
        if current_location[1] == 0:
            for _ in range(raw):
                graph_list[_].insert(0,off)
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]][current_location[1]-1] == on:
            current_location[1] -= 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[1] -= 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '1':
        if current_location[0] == 0 and current_location[1] == colum-1:
            for _ in range(raw):
                graph_list[_].append(off)
            colum += 1
            graph_list.insert(0, [off for num in range(colum)])
            current_location[1] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[0] == 0:
            graph_list.insert(0, [off for num in range(colum)])
            current_location[1] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[1] == colum-1:
            for _ in range(raw):
                graph_list[_].append(off)
            current_location[0] -= 1
            current_location[1] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]-1][current_location[1]+1] == on:
            current_location[0] -= 1
            current_location[1] += 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[0] -= 1
        current_location[1] += 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '3':
        if current_location[0] == raw-1 and current_location[1] == colum-1:
            for _ in range(raw):
                graph_list[_].append(off)
            colum += 1
            graph_list.append([off for num in range(colum)])
            current_location[1] += 1
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[0] == raw-1:
            graph_list.append([off for num in range(colum)])
            current_location[1] += 1
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[1] == colum-1:
            for _ in range(raw):
                graph_list[_].append(off)
            current_location[1] += 1
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]+1][current_location[1]+1] == on:
            current_location[1] += 1
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[1] += 1
        current_location[0] += 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '5':
        if current_location[0] == raw-1 and current_location[1] == 0:
            for _ in range(raw):
                graph_list[_].insert(0,off)
            colum += 1
            graph_list.append([off for num in range(colum)])
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[0] == raw-1:
            graph_list.append([off for num in range(colum)])
            current_location[0] += 1
            current_location[1] -= 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[1] == 0:
            for _ in range(raw):
                graph_list[_].insert(0,off)
            current_location[0] += 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]+1][current_location[1]-1] == on:
            current_location[0] += 1
            current_location[1] -= 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[0] += 1
        current_location[1] -= 1
        graph_list[current_location[0]][current_location[1]] = on
        continue
    if readstr == '7':
        if current_location[0] == 0 and current_location[1] == 0:
            for _ in range(raw):
                graph_list[_].insert(0,off)
            colum += 1
            graph_list.insert(0,[off for num in range(colum)])
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[0] == 0:
            graph_list.insert(0,[off for num in range(colum)])
            current_location[1] -= 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if current_location[1] == 0:
            for _ in range(raw):
                graph_list[_].insert(0,off)
            current_location[0] -= 1
            graph_list[current_location[0]][current_location[1]] = on
            continue
        if graph_list[current_location[0]-1][current_location[1]-1] == on:
            current_location[0] -= 1
            current_location[1] -= 1
            graph_list[current_location[0]][current_location[1]] = off
            continue
        current_location[0] -= 1
        current_location[1] -= 1
        graph_list[current_location[0]][current_location[1]] = on
        continue


raw = len(graph_list)
colum = len(graph_list[0])

i = 0
sign = 0
for i in range(raw - 1, -1, -1):
    for j in range(colum):
        if graph_list[i][j] == on:
            sign = 1
            break
        else:
            if j == colum - 1:
                del graph_list[i]
                raw -= 1
    if sign == 1:
        sign = 0
        break

if raw == 0:
    colum = 0

i=0
for j in range(colum):
    if graph_list[0][j] == on:
        break
    else:
        if j == colum - 1:
            del graph_list[0]
            raw -= 1


for i in range(raw):
    if graph_list[i][0] == on:
        break
    else:
        if i == raw - 1:
            for i in range(raw):
                del graph_list[i][0]
            colum -= 1

i=0
j=0
for j in range(colum - 1, -1, -1):
    for i in range(raw):
        if graph_list[i][j] == on:
            sign = 1
            break
        else:
            if i == raw - 1:
                for i in range(raw):
                    del graph_list[i][j]
                colum -= 1
    if sign == 1:
        sign = 0
        break

for i in range(0,raw):
    for j in range(0,colum):
        print(graph_list[i][j],end='')
    print()

