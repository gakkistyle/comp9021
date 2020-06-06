# COMP9021 Term 3 2019


'''
Uses data from the American Social Security Administration available
at https://www.ssa.gov/OACT/babynames/limits.html.
Determines from the relative frequency of given names in the population
of U.S. births the top 10 names that have disappeared and reappeared for
the longest period of time.
The data are stored in a directory "names", in files named "yobxxxx.txt"
with xxxx (the year of birth) ranging from 1880 to 2018.
'''


from collections import defaultdict
from pathlib import Path
import csv
import sys


names_dirname = Path('names')
if not names_dirname.exists():
    print(f'There is no directory named {names_dirname}, giving up...')
    sys.exit()
# A dictionnary where a key is a name and a value is the list of all
# years when the name was given.
years_per_name = defaultdict(list)
for filename in sorted(names_dirname.glob('*.txt')):
    year = int(filename.name[3 : 7])
    with open(filename) as file:
        csv_file = csv.reader(file)
        for name, _, _ in csv_file:
            years_per_name[name].append(year)
# A list of triples consisting of:
# - difference between year when a name was last given and first given
#   again,
# - year when name was last given,
# - name
revivals = [[years_per_name[name][i + 1] - years_per_name[name][i],
             years_per_name[name][i], name
            ] for name in years_per_name
                  for i in range(len(years_per_name[name]) - 1)
           ]
revivals.sort(key=lambda x: (-x[0], x[1], x[2]))
for i in range(10):
    print(f'{revivals[i][2]} was last used in {revivals[i][1]} '
          f'and then again in {revivals[i][1] + revivals[i][0]},',
          revivals[i][0], 'years later.'
         )

