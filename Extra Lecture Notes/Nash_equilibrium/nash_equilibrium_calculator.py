# COMP9021 Term 3 2019


import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from itertools import product
import re


players = 'Ruth', 'Charlie'


class NashEquilibriumCalculator(tk.Tk):
    cell_colour = '#F5F5F5'
    value_colour = '#330033'
    error_colour = '#FFCCCC'
    colours = {'Ruth': '#000099', 'Charlie': '#556B2F', 'Nash': '#CC0000'}

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Nash Equilibrium Calculator')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Nash Equilibrium Calculator Help',
                            menu=help_menu
                           )
        help_menu.add_command(label='Input', command=self.input_help)
        help_menu.add_command(label='Output', command=self.output_help)
        help_menu.add_command(label='Possible cases',
                              command=self.possible_cases_help
                             )
        self.config(menu=menubar)

        self.game_matrix = GameMatrix()
        self.game_matrix.pack()
        self.graph = tk.Canvas(self, width=140, height=140)
        self.graph.pack()
        special_expectations_0 = tk.StringVar()
        special_expectations_1 = tk.StringVar()
        tk.Label(self, textvariable=special_expectations_0, width=65).pack()
        tk.Label(self, textvariable=special_expectations_1, width = 65).pack()
        self.special_expectations = [special_expectations_0,
                                     special_expectations_1
                                    ]
        tk.Button(self, text='Compute Nash equilibria', width=20, pady=30,
                  command=self.display_graphics_and_special_information
                 ).pack()

    def input_help(self):
        tkinter.messagebox.showinfo(
                'Input',
                "Ruth's payoffs are the first member of the pair, and "
                "Charlie's payoffs the second member.\n\nRuth chooses "
                'the second column with probability p, and the first '
                'one with probability 1 - p. Charlie chooses the first '
                'row with probability q, and the second one with '
                'probability 1 - q.'
                                    )

    def output_help(self):
        tkinter.messagebox.showinfo(
                'Output',
                "Ruth's regret lines are displayed in blue, and "
                "Charlie's in green; their intersection is displayed "
                'in red.\n\nPure equilibria are displayed as red '
                'circles in corners of the graph and the corresponding '
                'cells are highlighted.\n\nWhen Ruth or Charlie uses a '
                "mixed strategy and the opponent's expected payoff "
                'does not depend on his or her choice of probability, '
                "then Ruth or Charlie's choice of probability and the "
                "choice of probability and the opponent's "
                'corresponding expected payoff are explicited. When '
                'the information for both is explicited, this '
                'corresponds to a nonpure Nash equilibrium, with the '
                'two regret lines intersecting at a position indicated '
                'indicated by a red circle.'
                                    )

    def possible_cases_help(self):
        tkinter.messagebox.showinfo(
                'Possible cases',
                'There are 9 possible cases for Ruth and for Charlie, '
                'so a total of 81 possible cases.\n\nEntered in the '
                'order lower left, upper left, lower right, upper '
                'right for Ruth and in the order lower left, lower '
                'right, upper left, upper right for Charlie, the 9 '
                'cases can be illustrated with the following '
                'values:\n\n'
                '      1 2 2 4\n'
                '      0 -1 0 0\n'
                '      3 1 1 4\n'
                '      1 1 0 1\n'
                '      4 2 2 1\n'
                '      -1 -1 0 -1\n'
                '      2 3 4 -3\n'
                '      0 1 0 0\n'
                '      0 0 0 0'
                                    )

    def display_graphics_and_special_information(self):
        self.game_matrix.restore_default_colours()
        self.special_expectations[0].set('')
        self.special_expectations[1].set('')
        self.graph.delete(tk.ALL)
        if self.game_matrix.get_payoffs():
            self.analyse_game(self.game_matrix.payoffs_per_player)
            self.draw_regret_lines_and_highlight_cells()
            self.display_special_information()

    def analyse_game(self, payoffs_per_player):
        # Let a1, a2, a3 and a4 denote payoffs[0][0][0],
        # payoffs[0][0][1], payoffs[0][1][0] and payoffs[0][1][1],
        # respectively.
        # Let b1, b2, b3 and b4 denote payoffs[1][0][0],
        # payoffs[1][0][1], payoffs[1][1][0] and payoffs[1][1][1],
        # respectively.
        # Set D[0] = a1  -a2 - a3 + a4 and D[1] = b1 - b2 - b3 + b4.
        # Set E[0] = a3 - a1 and E[1] = b2 - b1.
        # Set F[0] = a2 - a1 and F[1] = b3 - b1.
        #
        # When Ruth selects the second column with probability p
        # and Charlie selects the second row with probability q,
        # Ruths' expectation is equal to
        # (D[0] * q + E[0]) * p + F[0] * q + a1
        # and Charlie's expectation is equal to
        # (D[1] * p + E[1]) * q + F[1] * p + b1.
        # Both players maximise their expectation, which determines:
        # - Ruth's No Regret graph, consisting of all pairs of numbers
        # of the form:
        #   * (0, q) with D[0] * q + E[0] < 0
        #   * (p, q) with 0 <= p <= 1 and D[0] * q + E[0] == 0
        #   * (1, q) with D[0] * q + E[0] > 0
        # - Charlie's No Regret graph, consisting of all pairs of
        # numbers of the form:
        #   * (p, 0) with D[1] * p + E[1] < 0
        #   * (p, q) with 0 <= q <= 1 and D[1] * p + E[1] == 0
        #   * (q, 1) with D[1] * q + E[1] > 0
        #
        # When there exists a unique q in [0, 1] with
        # D[0] * q + E[0] == 0,
        # then that q is recorded as probas['Ruth'];
        # moreover, if q is in (0, 1) then Ruth's corresponding
        # expectation, which does not depend on p and is equal to
        # F[0] * q + a1, is recorded as self.expectations['Ruth'].
        # When there exists a unique p in [0, 1] with
        # D[1] * p + E[1] == 0, then that p is recorded as
        # probas['Charlie']; moreover, if p is in (0, 1) then
        # Charlie's corresponding expectation, which does not depend on
        # q and is equal to F[1] * p + b1, is recorded as
        # self.expectations['Charlie'].
        # When there is a largest q in [0,1] with
        # D[0] * q' + E[0] < 0 for all q' < q,
        # then (0, q) is recorded as segments['Ruth'][0].
        # When there is a largest p in [0,1] with
        # D[1] * p' + E[1] < 0 for all p' < p,
        # then (0, p) is recorded as segments['Charlie'][0].
        # When there is a smallest q in [0,1] with
        # D[0] * q' + E[0] > 0 for all q' > q,
        # then (q, 1) is recorded as segments['Ruth'][1].
        # When there is a smallest p in [0,1] with
        # D[1] * p' + E[1] > 0 for all p' > p,
        # then (p, 1) is recorded as segments['Charlie'][1].
        self.all_good = set()
        self.segments = {player: [None, None] for player in players}
        self.probas = dict.fromkeys(players)
        self.expectations = dict.fromkeys(players)
        D = dict.fromkeys(players)
        E = dict.fromkeys(players)
        F = dict.fromkeys(players)
        for player in players:
            payoffs = payoffs_per_player[player]
            D[player] = payoffs[0][0] - payoffs[0][1] - payoffs[1][0]\
                        + payoffs[1][1]
            E[player] = payoffs[int(player == 'Ruth')]\
                               [int(player == 'Charlie')] - payoffs[0][0]
            if D[player]:
                cut = -E[player] / D[player]
                if cut < 0 or cut > 1:
                    self.segments[player][1 - int(E[player] < 0)] = 0, 1
                else:
                    self.probas[player] = cut
                    if cut in {0, 1}:
                        self.segments[player][int((cut == 1) ^ (D[player] > 0))
                                             ] = 0, 1
                    else:
                        F[player] = payoffs[int(player == 'Charlie')]\
                                           [int(player == 'Ruth')]\
                                    - payoffs[0][0]
                        self.expectations[player] =\
                                F[player] * self.probas[player] + payoffs[0][0]
                        self.segments[player][int(D[player] < 0)] =\
                                                         0, self.probas[player]
                        self.segments[player][int(D[player] > 0)] =\
                                                         self.probas[player], 1
            elif E[player]:
                self.segments[player][1 - int(E[player] < 0)] = 0, 1
            else:
                self.all_good.add(player)

    def is_pure_equilibrium(self, i, j):
        return all(X[0] in self.all_good or\
                   self.segments[X[0]][X[1]]\
                   and self.segments[X[0]][X[1]][X[2]] == X[2]\
                   or self.probas[X[0]] == j for X in {(players[0], i, j),
                                                       (players[1], j, i)
                                                      }
                  )

    def draw_rectangle(self, colour):
        self.graph.create_rectangle(5, 5, 105, 105, fill=colour,
                                    outline=colour
                                   )

    def draw_line(self, x1, y1, x2, y2, colour):
        self.graph.create_line(x1, y1, x2, y2, fill=colour, width=2)

    def draw_rectangles(self):
        if 'Ruth' in self.all_good:
            if 'Charlie' in self.all_good:
                self.draw_rectangle(self.colours['Nash'])
            else:
                self.draw_rectangle(self.colours['Ruth'])
        elif 'Charlie' in self.all_good:
            self.draw_rectangle(self.colours['Charlie'])

    def draw_outer_lines(self):
        x_y = {'Ruth': lambda x, j1, j2: (100 * x + 5, 100 * (1 - j2) + 5,
                                          100 * x + 5, 100 * (1 - j1) + 5
                                         ),
               'Charlie': lambda y, i1, i2: (100 * i1 + 5, (1 - y) * 100 + 5,
                                             100 * i2 + 5, (1 - y) * 100 + 5
                                            )
              }
        for i in range(2):
            for player_1, player_2 in {players, reversed(players)}:
                if self.segments[player_1][i]:
                    # In case the segment S under consideration
                    # intersects an inner line segment S' (of length 1)
                    # for the other player, then S' has been drawn
                    # already. The intersection of S and S' is drawn
                    # again using 'Nash' colour.
                    colour = self.colours[player_1]\
                            if player_2 not in self.all_good\
                               and (self.probas[player_2] is None or
                                    self.probas[player_2] != i
                                   ) else self.colours['Nash']
                    self.draw_line(
                            *x_y[player_1](i, self.segments[player_1][i][0],
                                           self.segments[player_1][i][1]
                                          ), colour
                                  )

    def draw_inner_lines(self):
        x_y = {'Ruth': lambda p: (5, 100 * (1 - p) + 5, 105,
                                  100 * (1 - p) + 5
                                 ),
               'Charlie': lambda p: (100 * p + 5, 5, 100 * p + 5, 105)
              }
        for player_1, player_2 in {players, reversed(players)}:
            if self.probas[player_1] is not None:
                if player_2 in self.all_good:
                    self.draw_line(*x_y[player_1](self.probas[player_1]),
                                   self.colours['Nash']
                                  )
                else:
                    self.draw_line(*x_y[player_1](self.probas[player_1]),
                                   self.colours[player_1]
                                  )

    def draw_intersecting_nash_equilibria(self):
        if self.expectations['Ruth'] is not None\
           and self.expectations['Charlie'] is not None:
            self.graph.create_oval(self.probas['Charlie'] * 100 + 3,
                                   (1 - self.probas['Ruth']) * 100 + 3,
                                   self.probas['Charlie'] * 100 + 7,
                                   (1 - self.probas['Ruth']) * 100 + 7,
                                   fill=self.colours['Nash'],
                                   outline=self.colours['Nash']
                                  )

    def draw_and_highlight_pure_nash_equilibria(self):
        for i, j in product(range(2), repeat=2):
            if self.is_pure_equilibrium(i, j):
                self.graph.create_oval((i * 100 + 3, (1 - j) * 100 + 3,
                                        i * 100 + 7, (1 - j) * 100 + 7
                                       ), fill=self.colours['Nash'],
                                       outline=self.colours['Nash']
                                      )
                self.game_matrix.cells[i][j].config(fg=self.colours['Nash'])

    def draw_regret_lines_and_highlight_cells(self):
        self.draw_rectangles()
        self.draw_inner_lines()
        self.draw_outer_lines()
        self.draw_intersecting_nash_equilibria()
        self.draw_and_highlight_pure_nash_equilibria()

    def display_special_information(self):
        if self.expectations['Ruth'] is not None:
            self.special_expectations[0].set(
                     f"When Charlie uses proba q = {self.probas['Ruth']:.2f}"
                     f", Ruth's expectation is {self.expectations['Ruth']:.2f}"
                                            )
        if self.expectations['Charlie'] is not None:
            self.special_expectations[1].set(
               f"When Ruth uses proba p = {self.probas['Charlie']:.2f}"
               f", Charlie's expectation is {self.expectations['Charlie']:.2f}"
                                            )


class GameMatrix(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, bd=20)
        self.create_matrix()

    def create_matrix(self):
        # The payoffs will be analysed as if they were entered from the
        # pair that Ruth and Charlie would chose with probabilities
        # p = 0 and q = 0, respectively, to the pair that Ruth and
        # Charlie would chose with probabilities p = 1 and q = 1,
        # respectively, with in-between first the pair that Ruth and
        # Charlie would chose with probabilities p = 0 and q = 1,
        # respectively, and then the pair that Ruth and Charlie would
        # chose with probabilities p = 1 and q = 0, respectively. These
        # four pairs of payoffs will be stored in self.cells[0][0],
        # self.cells[0][1], self.cells[1][0], self.cells[1][0],
        # respectively.
        self.cells = [[None] * 2 for _ in range(2)]
        self.payoffs_per_player = {player: [[None] * 2
                                       for _ in range(2)] for player in players
                                  }
        for i, j in product(range(2), repeat=2):
            self.cells[i][j] = tk.Entry(
                                    self, bd=4, width=9,
                                    bg=NashEquilibriumCalculator.cell_colour,
                                    fg=NashEquilibriumCalculator.value_colour
                                       )
            self.cells[i][j].grid(column=i, row=1 - j)
            self.cells[i][j].insert(0, '(0,0)')
        tk.Label(self, text='Ruth',
                 fg=NashEquilibriumCalculator.colours['Ruth']).grid(
                                                           columnspan=2, pady=5
                                                                   )
        tk.Label(self, text='Charlie',
                 fg=NashEquilibriumCalculator.colours['Charlie']).grid(
                                             row=0, rowspan=2, column=2, padx=5
                                                                      )

    def restore_default_colours(self):
        for i, j in product(range(2), repeat=2):
            self.cells[i][j].config(bg=NashEquilibriumCalculator.cell_colour,
                                    fg=NashEquilibriumCalculator.value_colour
                                   )

    def get_payoffs(self):
        correct_input = True
        for i, j in product(range(2), repeat=2):
            provided_input = self.cells[i][j].get()
            parsed_input = re.search('^ *\( *([+-]?(?:0|[1-9]\d*)) *, *'
                                     '([+-]?(?:0|[1-9]\d*)) *\) *$',
                                     provided_input
                                    )
            if not parsed_input:
                self.cells[i][j].config(
                         bg=NashEquilibriumCalculator.error_colour
                                       )
                correct_input = False
            else:
                self.cells[i][j].config(
                         bg=NashEquilibriumCalculator.cell_colour
                                       )
                self.payoffs_per_player['Ruth'][i][j] =\
                                                int(parsed_input.groups()[0])
                self.payoffs_per_player['Charlie'][i][j] =\
                                                int(parsed_input.groups()[1])
        if not correct_input:
            tkinter.messagebox.showerror(
                    'Incorrect input',
                    'Enter pairs of numbers separated by '
                    'a comma and surrounded by parentheses'
                                        )
            return False
        return True


if __name__ == '__main__':
    NashEquilibriumCalculator().mainloop()

