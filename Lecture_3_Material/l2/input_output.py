# COMP9021 Term 3 2019


'''
Utility to prompt the user for an integer with a range that can be
specified, until the user input is of the expected type, and to
nicely display the list of prime numbers from various sieves.
'''


def input_int(prompt = 'What do you want it to be? ',
              min_value = float('-inf'), max_value = float('inf')
             ):
    while True:
        try:
            input_value = int(input(prompt))
            if input_value < min_value or input_value > max_value:
                raise ValueError
            return input_value
        except ValueError:
            print('Incorrect input. ', end='')

            
def nicely_display(sequence, max_size):
    field_width = max_size + 2
    nb_of_fields = 80 // field_width
    count = 0
    for e in sequence:
        print(f'{e:{field_width}d}', end='')
        count += 1
        if count % nb_of_fields == 0:
            print()
    if count % nb_of_fields:
        print()
