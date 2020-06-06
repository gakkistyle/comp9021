# COMP9021 Practice 8 - Solutions


'''
Prompts the user for the face values of banknotes and their associated quantities,
as well as for an amount, and if possible, outputs the minimal number of banknotes
needed to match that amount, as well as the detail of how many banknotes
of each type value are used.
'''

from ast import literal_eval


def print_solution(solution):
    max_width = len(str(solution[-1][0])) + 1
    print('\n'.join(f'{"$" + str(value):>{max_width}}: {quantity}' for (value, quantity) in solution))
      
# Having banknote values ordered from largest to smallest
# might make the computation more efficient.
face_values = sorted(literal_eval(input('Input a dictionary whose keys represent banknote face values\n'
                                        'with as value for a given key the number of banknotes\n'
                                        'that are available for the corresponding face value:\n    '
                                       )
                                 ).items(), reverse = True
                    )
nb_of_face_values = len(face_values)
amount = int(input('Input the desired amount: '))

# minimal_combinations[sub_amount] will be a pair whose first element
# is the minimal number of banknotes needed to yield sub_amount,
# and whose second element is the list of all possible solutions,
# each solution being a dictionary with face values as keys and
# number of banknotes used as values.
minimal_combinations = [[0, []]] + [[float('inf'), []] for i in range(amount)]
for sub_amount in range(1, amount + 1):
    for i in range(nb_of_face_values):
        value = face_values[i][0]
        if sub_amount < value:
            continue
        if value == sub_amount:
            minimal_combinations[sub_amount] = [1, [{value : 1}]]
            break
        # Using "value" to get "sub_amount" would require more banknotes
        # than the minimum number of banknotes so far found out to sum up
        # to "sub_amount".
        if minimal_combinations[sub_amount - value][0] >= minimal_combinations[sub_amount][0]:
            continue
        for option in minimal_combinations[sub_amount - value][1]:
            # A banknote with face value "value" is available to complete
            # "option" and result in a sum of "sub_amount".
            if value not in option or option[value] < face_values[i][1]:
                # Moreover, it determines a new minimum to the number of
                # banknotes that can sum up to "sub_amount".
                if minimal_combinations[sub_amount - value][0] + 1 <\
                                                                minimal_combinations[sub_amount][0]:
                    minimal_combinations[sub_amount][0] =\
                               minimal_combinations[sub_amount - value][0] + 1
                    minimal_combinations[sub_amount][1].clear()
                extended_option = dict(option)
                if value not in option:
                    extended_option[value] = 1
                else:
                    extended_option[value] += 1
                if extended_option not in minimal_combinations[sub_amount][1]:
                    minimal_combinations[sub_amount][1].append(extended_option)
solutions = sorted(sorted(solution.items()) for solution in minimal_combinations[amount][1])
if not solutions:
    print('\nThere is no solution.')
elif len(solutions) == 1:
        print('\nThere is a unique solution:')
        print_solution(solutions[0])
else:
    print(f'\nThere are {len(solutions)} solutions:')
    for solution in solutions[: -1]:
        print_solution(solution)
        print()
    print_solution(solutions[-1])
        
        

