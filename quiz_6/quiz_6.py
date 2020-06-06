# COMP9021 19T3 - Rachid Hamadi
# Quiz 6 *** Due Thursday Week 8
#
# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)



def findmax(count):
    lar = 0
    for i in range(len(count)):
        for j in range(i+1,len(count)):
            size = (min(count[i:j+1]))*(j-i+1)
            if lar<size:
                lar = size
    return lar



def size_of_largest_parallelogram():
    grid_plus = [[0, 0] for _ in range(10)]
    _ = 0
    for row in grid:
        for e in row:
            grid_plus[_].insert(-1, e)
        _ = _ + 1
    framed_grid = [[0] * 12, *grid_plus, [0] * 12]
    largest = 0
    for i in range(1,11):
        j = 1
        while j <11:
            if framed_grid[i][j] and framed_grid[i][j+1] and framed_grid[i+1][j] and framed_grid[i+1][j+1]:
                count = [2]
                i_c = i
                j_c = j+2
                while framed_grid[i_c][j_c] == 1:
                    count[0] += 1
                    j_c = j_c+1
                i_c = i_c +1
                while framed_grid[i_c][j] and framed_grid[i_c][j+1]:
                    count.append(2)
                    j_c = j+2
                    while framed_grid[i_c][j_c]:
                        count[-1] += 1
                        j_c += 1
                    i_c += 1
                sub_largest = findmax(count)
                largest = max(largest,sub_largest)
            j += 1
    for i in range(1,11):
        j = 1
        while j <11:
            if framed_grid[i][j] == 1 and framed_grid[i][j+1] == 1 and framed_grid[i+1][j-1] and framed_grid[i+1][j]:
                count = [2]
                i_c = i
                j_c = j+2
                while framed_grid[i_c][j_c] == 1:
                    count[0] += 1
                    j_c = j_c+1
                i_c = i_c +1
                j_c = j
                while framed_grid[i_c][j_c-1] and framed_grid[i_c][j_c]:
                    count.append(2)
                    j_cc = j_c+1
                    while framed_grid[i_c][j_cc]:
                        count[-1] += 1
                        j_cc += 1
                    i_c += 1
                    j_c -= 1
                sub_largest = findmax(count)
                largest = max(largest,sub_largest)
            j += 1
    for i in range(1,11):
        j = 1
        while j <11:
            if framed_grid[i][j] == 1 and framed_grid[i][j+1] == 1 and framed_grid[i+1][j+1] and framed_grid[i+1][j+2]:
                count = [2]
                i_c = i
                j_c = j+2
                while framed_grid[i_c][j_c] == 1:
                    count[0] += 1
                    j_c = j_c+1
                i_c = i_c +1
                j_c = j
                while framed_grid[i_c][j_c+1] and framed_grid[i_c][j_c+2]:
                    count.append(2)
                    j_cc = j_c+3
                    while framed_grid[i_c][j_cc]:
                        count[-1] += 1
                        j_cc += 1
                    i_c += 1
                    j_c += 1
                sub_largest = findmax(count)
                largest = max(largest,sub_largest)
            j += 1
    return largest

    # REPLACE PASS ABOVE WITH YOUR CODE


# POSSIBLY DEFINE OTHER FUNCTIONS


try:
    
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')
