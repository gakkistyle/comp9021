# COMP9021 Term 3 2019


'''
Uses data from the American Social Security Administration available
at https://www.ssa.gov/OACT/babynames/limits.html.
Splits the data on the relative frequency of given names in the
population of U.S. births into females and males, removing the field
that determines the classification.
The data are stored in a directory "names", in files named "yobxxxx.txt"
with xxxx (the year of birth) ranging from 1880 to 2018.
They will be copied in a directory "names_per_gender", otherwise keeping
the same file structure.
'''


from pathlib import Path
import csv
import sys
import os


names_dirname = Path('names')
if not names_dirname.exists():
    print(f'There is no directory named {names_dirname}, giving up...')
    sys.exit()
names_per_gender_dirname = Path('names_per_gender')
if names_per_gender_dirname.exists():
    print('A directory named', names_per_gender_dirname, 'already '
          'exists.\nBetter safe than sorry, giving up.'
         )
    sys.exit()
female_subdirname = names_per_gender_dirname / 'female'
male_subdirname = names_per_gender_dirname / 'male'
os.mkdir(names_per_gender_dirname)
os.mkdir(female_subdirname)
os.mkdir(male_subdirname)
for filename in names_dirname.glob('*.txt'):
    with open(filename) as file,\
         open(female_subdirname / filename.name, 'w') as female_file,\
         open(male_subdirname / filename.name, 'w') as male_file:
        csv_file = csv.reader(file)
        female_csv_file = csv.writer(female_file)
        male_csv_file = csv.writer(male_file)
        csv_file_per_gender = {'F': female_csv_file, 'M': male_csv_file}
        for name, gender, tally in csv_file:
            csv_file_per_gender[gender].writerow((name, tally))
