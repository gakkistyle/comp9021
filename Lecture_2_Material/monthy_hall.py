# COMP9021 Term 3 2019


'''
Simulates the Monty Hall problem.
- A car is hidden behind 3 doors.
- The contestant randomly choses a door.
- The game host opens a door behind which there is no car.
- The contestant then has the option to change her mind and open another
  door.

Prompts the user for the number of times the game is played, and whether
the contestant opts for switching door or not.

Displays the details of the game for the few first games, set to a
maximum of 6 by default, and prints out the proportion of games being
won.
'''


from random import choice, randrange


def set_simulation():
    while True:
        try:
            nb_of_games = int(input('How many games should I simulate? '))
            if nb_of_games <= 0:
                raise ValueError
            break
        except ValueError:
            print('Your input is incorrect, try again.')
    while True:
        contestant_switches = input('Should the contestant switch? ')
        if contestant_switches.istitle():
            contestant_switches = contestant_switches.lower()
        if contestant_switches in {'yes', 'y'}:
            contestant_switches = True
            print('I keep in mind you want to switch.')
            break
        if contestant_switches in {'no', 'n'}:
            contestant_switches = False
            print("I keep in mind you don't want to switch.")
            break
        print('Your input is incorrect, try again.')
    return nb_of_games, contestant_switches


def simulate(nb_of_games_to_display=6):
    nb_of_games, contestant_switches = set_simulation()
    print('Starting the simulation with the contestant', end=' ')
    if not contestant_switches:
        print('not ', end='')
    print('switching doors.\n')
    nb_of_wins = 0
    for i in range(nb_of_games):
        doors = ['A', 'B', 'C']
        winning_door = choice(doors)
        if i < nb_of_games_to_display:
            print('\tContestant does not know it, but car '
                  f'happens to be behind door {winning_door}.'
                 )
        first_chosen_door = doors.pop(randrange(3))
        if i < nb_of_games_to_display:
            print(f'\tContestant chooses door {first_chosen_door}.')
        if not contestant_switches:
            second_chosen_door = first_chosen_door
        if first_chosen_door == winning_door:
            opened_door = doors.pop(randrange(2))
            if contestant_switches:
                second_chosen_door = doors[0]
            else:
                nb_of_wins += 1
        else:
            doors.remove(winning_door)
            opened_door = doors[0]
            if contestant_switches:
                second_chosen_door = winning_door
                nb_of_wins += 1
        if i < nb_of_games_to_display:
            print(f'\tGame host opens door {opened_door}.')
            print(f'\tContestant chooses door {second_chosen_door}', end=' ')
            print('and wins.\n') if second_chosen_door == winning_door\
                                 else print('and looses.\n')
        elif i == nb_of_games_to_display:
            print('...\n')
    print(f'Contestant won {nb_of_wins / nb_of_games * 100:.2f}% of games.')


if __name__ == '__main__':
    simulate()
