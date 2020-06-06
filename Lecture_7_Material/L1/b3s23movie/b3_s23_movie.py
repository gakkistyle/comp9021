# COMP9021 Term 3 2019


import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from argparse import ArgumentParser
from itertools import count
import os
import sys


def evolve(i):
    global grid
    number_of_neighbours = np.zeros(grid.shape)
    number_of_neighbours[1 : -1, 1 : -1] =\
            grid[: -2, : -2] + grid[: -2, 1 : -1] + grid[: -2, 2 :]\
            + grid[1 : -1, : -2] + grid[1 : -1, 2 :]  + grid[2 :, : -2]\
            + grid[2 :, 1 : -1]  + grid[2 :, 2 :]
    grid = np.logical_or(np.logical_and(grid == 1, number_of_neighbours == 2),
                         number_of_neighbours == 3
                        ).astype(np.int)
    population_state.set_data(grid)
    current_iteration.set_text(f'Iteration: {str(i)}')
    return population_state, current_iteration


def keep_going_or_stop():
    for i in count():
        if any(grid[1, 1 : -1]) or any(grid[-2, 1 : -1])\
           or any(grid[1 : -1, 1]) or any(grid[1 : -1, -2]):
            return
        yield i           


parser = ArgumentParser()
parser.add_argument('--rle_filename', dest='rle_filename', required=True)
parser.add_argument('--figure_size', dest='figure_size',
                    default=(10, 10), nargs=2, type=int
                   )
parser.add_argument('--pattern_size_multiplier',
                    dest='pattern_size_multiplier', default=5, type=int
                   )
parser.add_argument('--max_nb_of_iterations', dest='max_nb_of_iterations',
                    default=1_000, type=int
                   )
parser.add_argument('--animation_intervals', dest='animation_intervals',
                    default=20, type=int
                   )
args = parser.parse_args()
rle_filename = args.rle_filename
figure_size = args.figure_size
pattern_size_multiplier = args.pattern_size_multiplier
max_nb_of_iterations = args.max_nb_of_iterations
animation_intervals = args.animation_intervals
if not rle_filename.endswith('.rle'):
    print('Wrong file format,', rle_filename, 'should have .rle extension')
    sys.exit()
try:
    with open(rle_filename) as file:
        for line in file:
            if line.startswith('#'):
                continue
            x, y = (int(e) for e in re.search('(\d+)[^\d]*(\d+)',
                                              line
                                             ).groups()
                   )
            break
        lines = ''.join(line.strip() for line in file)[: -1].split('$')
    size = max(x, y) * pattern_size_multiplier
    grid = np.zeros((size, size), np.int)
    i, j = (size - y) // 2, (size - x) // 2
    for line in lines:
        # Originally: $
        if not line:
            i += 1
            continue
        # Originally: {some_number}$
        if line.isdigit():
            i += int(line)
            continue
        line, nb_of_new_lines = re.match('(.*[^\d])(\d*)', line).groups()
        # run_spans will be of the form
        #v[n_0, n_1, n_2, n_3, ..., n_{2k}, n_{2k+1}].
        # Sequences of living cells range from index n_{2i} included to
        # index n_{2i+1} excluded, i <= k.
        line = line.split('b')
        # {maybe_some_number}o...
        if line[0].find('o') >= 0:
            run_spans = [j]           
        else:
            try:
                # {some_number}b...
                run_spans = [j + int(line.pop(0))]
            except ValueError:
                # Originally: b...
                run_spans = [j + 1]                
        for e in line:
            # Originally: ...b{maybe_some_number}$
            if not e:
                break
            # ...{maybe_some_number}o{maybe_some_number}...
            for run_span in e.split('o'):
                try:
                    run_spans.append(run_spans[-1] + int(run_span))
                except ValueError:
                    run_spans.append(run_spans[-1] + 1)
        for n in range(len(run_spans) // 2):
            grid[i, run_spans[2 * n] : run_spans[2 * n + 1]] = 1
        try:
            # Originally: ...{o_or_b}{some_number}$
            i += int(nb_of_new_lines)
        except ValueError:
            # Originally: ...{o_or_b}$
            i += 1
except FileNotFoundError:
    print('Could not open', rle_file, 'giving up.')
figure = plt.figure(figsize=figure_size, dpi=192)
plt.xticks([])
plt.yticks([])
population_state = plt.imshow(grid)
current_iteration = plt.text(5, -5, '', c = 'red')
evolution = animation.FuncAnimation(figure, evolve, frames=keep_going_or_stop,
                                    interval=animation_intervals,
                                    save_count=max_nb_of_iterations
                                   )
filename = re.sub('\..*', '', rle_filename)
if os.path.isfile(filename + '.mp4'):
    for i in count(1):
        mp4_filename = ''.join((filename, '_', str(i), '.mp4'))
        if not os.path.isfile(mp4_filename):
            break
else:
    mp4_filename = filename + '.mp4'
evolution.save(mp4_filename)
