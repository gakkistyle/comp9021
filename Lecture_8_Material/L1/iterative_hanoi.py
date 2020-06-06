# COMP9021 Term 3 2019


'''
Iterative solution to the towers of Hanoi puzzle.
'''


def move_towers(n, start_position, end_position, extra_position):
    '''
    Move a tower of n disks from start_position to end_position,
    with extra_position available.

    >>> move_towers(4, 0, 2, 1)
    Move smallest disk from position 0 to position 1
    Move disk of size 2 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    Move disk of size 3 from position 0 to position 1
    Move smallest disk from position 2 to position 0
    Move disk of size 2 from position 2 to position 1
    Move smallest disk from position 0 to position 1
    Move disk of size 4 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    Move disk of size 2 from position 1 to position 0
    Move smallest disk from position 2 to position 0
    Move disk of size 3 from position 1 to position 2
    Move smallest disk from position 0 to position 1
    Move disk of size 2 from position 0 to position 2
    Move smallest disk from position 1 to position 2
    '''
    smallest_disk_position = 0
    direction = 1 - n % 2 * 2
    stacks = list(range(n, 0, -1)), [], []
    for i in range(2 ** n - 1):
        if i % 2 == 0:
            new_smallest_disk_position =\
                    (smallest_disk_position + direction) % 3
            print('Move smallest disk from position', smallest_disk_position,
                  'to position', new_smallest_disk_position
                 )
            stacks[new_smallest_disk_position].append(
                                        stacks[smallest_disk_position].pop()
                                                     )
            smallest_disk_position = new_smallest_disk_position
        else:
            from_position, to_position =\
                    sorted(((smallest_disk_position + 1) % 3,
                            (smallest_disk_position + 2) % 3
                           ), key=lambda x: not stacks[x] and n + 1
                                            or stacks[x][-1]
                          )
            stacks[to_position].append(stacks[from_position].pop())
            print('Move disk of size', stacks[to_position][-1],
                  'from position', from_position, 'to position', to_position
                 )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
