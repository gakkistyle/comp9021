# COMP9021 19T3 - Rachid Hamadi
# Quiz 7 *** Due Thursday Week 9
#
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.
def colour_shapes():
    return True
    # Replace pass above with your code

track = []
largest = 0
tem_spike = 0
def max_number_of_spikes(nb_of_shapes):
    global largest
    global tem_spike
    grid_extend = grid_plus()
    for i in range(1,len(grid_extend)-1):
        for j in range(1,len(grid_extend[0])-1):
            if grid_extend[i][j] == 1:
                search_spike(i,j)
                if tem_spike > largest:
                    largest = tem_spike
                tem_spike = 0

    return largest

def grid_plus():
    grid_plus = [[0, 0] for _ in range(len(grid))]
    _ = 0
    for row in grid:
        for e in row:
            grid_plus[_].insert(-1, e)
        _ = _ + 1
    return [[0] * (len(grid[0]) + 2), *grid_plus, [0] * (len(grid[0]) + 2)]

    # Replace pass above with your code
def search_spike(i,j):
    global tem_spike
    extend_grid = grid_plus()
    if extend_grid[i-1][j] == 0 and extend_grid[i+1][j] == 0 and extend_grid[i][j-1] ==0 and extend_grid[i][j+1] == 0:
        return
    else:
        if [i,j] not in track:
            track.append([i,j])
            if (extend_grid[i][j-1] + extend_grid[i][j+1] + extend_grid[i-1][j] + extend_grid[i+1][j] == 1):
                tem_spike += 1
            if extend_grid[i][j+1] == 1:
                search_spike(i,j+1)
            if extend_grid[i+1][j] == 1:
                search_spike(i+1,j)
            if extend_grid[i][j-1] == 1:
                search_spike(i,j-1)
            if extend_grid[i-1][j] == 1:
                search_spike(i-1,j)
            else:
                return
        else:
            return




# Possibly define other functions here    


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
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
