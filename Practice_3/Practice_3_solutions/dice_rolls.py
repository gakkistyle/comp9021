# COMP9021 Practice 3 - Solutions


'''
Prompts the user twice, for strictly positive integers s_1, ..., s_k intended to represent
the number of sides of some dice, and for an integer N meant to represent the number of times
these dice should be cast. If the first input is empty, then a single six-sided die will be used.
If the first input is not empty, then any part of it which is not a strictly positive integer
will be replaced by. If the second input is empty or is not a strictly positive integer, then
the number of rolls will be set to 1,000.

Generates N times k random numbers between 1 and s_1, ..., s_k, respectively, sums them up,
and displays the N sums in the form of a histogram, created as an object of class Bar of
the pygal module, that can be displayed in a browser by opening a file named dice_rolls.svg.
'''


from random import randint

from pygal import Bar
from pygal.style import Style


input_values = input('Enter N strictly positive integers (number of sides of N dice): ').split()
if input_values:
    dice = []
    incorrect_input = False
    for i in input_values:
        try:
            nb_of_sides = int(i)
            if nb_of_sides <= 0:
                raise ValueError
            dice.append(nb_of_sides)
        except ValueError:
            dice.append(6)
            incorrect_input = True
    if incorrect_input:
        print('Some of the values, incorrect, have been replaced with the default value of 6.')
else:
    print('You did not enter any value, a single standard six-sided die will be rolled.')
    dice = [6]
print()
try:
    nb_of_rolls = int(input('Enter the desired number of rolls: '))
    if nb_of_rolls < 1:
        raise ValueError
except ValueError:
    print('Input was not provided or invalid, so the default value of 1,000 will be used.')
    nb_of_rolls = 1_000
rolls = [sum(randint(1, nb_of_sides) for nb_of_sides in dice) for _ in range(nb_of_rolls)]
range_of_sums = range(len(dice), sum(dice) + 1)
counts = [rolls.count(i) for i in range_of_sums]
counts = [{'value': count, 'label': f'Frequency: {count / nb_of_rolls:.2f}'} for count in counts]
histogram = Bar(style = Style(colors = ('#228B22',), major_label_font_size = 12),
                                                                                 show_legend = False
               )
histogram.title = f'Simulation for {nb_of_rolls} rolls of the dice: {sorted(dice)}'
histogram.x_labels = [str(i) for i in range_of_sums]
histogram.x_title = 'Possible sums'
histogram.y_title = 'Counts'
histogram.add('', counts)
histogram.render_to_file('dice_rolls.svg')
