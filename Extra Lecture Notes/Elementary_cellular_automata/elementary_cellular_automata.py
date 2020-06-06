# %load elementary_cellular_automata.py
# COMP9021 Term 3 2019


import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from random import randint


class ElementaryCellularAutomata(tk.Tk):
    nb_of_steps = 300
    background_colour = '#F5F5F5'
    history_colour = 'green'

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Elementary Cellular Automata')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Elementary Cellular Automaton Help',
                            menu=help_menu
                           )
        help_menu.add_command(label='Input', command=self.input_help)
        self.config(menu=menubar)
        self.input = tk.Entry(self, width=8)
        self.input.grid()
        self.previous_rule_number = None
        self.displaying_random_history = False
        self.shown_rule_number = tk.StringVar()
        tk.Label(self, width=9, height=1, textvariable=self.shown_rule_number,
                 fg='magenta'
                ).grid(row=0, column=1)
        self.shown_rule = tk.Canvas(self, width=250, height=50)
        self.shown_rule.grid(row=0, column=1, columnspan=2, padx=(100, 0),
                             pady=10
                            )
        tk.Button(self, text='Display history from single 1',
                  command=self.work_from_single_1
                 ).grid(padx=(40, 0))
        self.shown_related_rule_numbers = tk.StringVar()
        tk.Label(self, width=87, height=1,
                 textvariable=self.shown_related_rule_numbers
                ).grid(row=1, column=1)
        tk.Button(self, text='Display history from random state',
                  command=self.work_from_random_state
                 ).grid(row=1, column=2, padx=(0, 40))
        self.history = tk.Canvas(self, width=self.nb_of_steps * 4 + 3,
                                 height=self.nb_of_steps * 2 + 5,
                                 bg=self.background_colour
                                )
        self.history.grid(columnspan=3, pady=20)

    def input_help(self):
        tkinter.messagebox.showinfo(
                'Input',
                'The input should be a nonnegative integer at most '
                'equal to 255, represented either in base 10 or in '
                'base 2 with exactly 8 bits.'
                                   )
    def get_rule(self):
        input = self.input.get()
        self.input.delete(0, tk.END)
        if input == '':
            if self.previous_rule_number is None:
                tkinter.messagebox.showerror('Rule error',
                                             'Please input a rule number'
                                            )
                return False
            return
        if not input.isdigit():
            self.warn_of_incorrect_input()
            return False
        if len(input) == 8:
            try:
                self.rule_number = int(input, 2)
            except ValueError:
                self.warn_of_incorrect_input()
                return False
            self.rule_bits = input
        else:
            if len(input) > 1 and input[0] == '0':
                self.warn_of_incorrect_input()
                return False
            self.rule_number = int(input)
            if self.rule_number >= 2 ** 8:
                self.warn_of_incorrect_input()
                return False
            self.rule_bits = f'{self.rule_number:08b}'
        # A rule R that in binary, is coded as
        #       b_0 b_1 b_2 b_2 b_2 b_2 b_6 b_7
        # maps
        # (0, 0, 0) to b_7
        # (0, 0, 1) to b_6
        # (0, 1, 0) to b_5
        # (0, 1, 1) to b_4
        # (1, 0, 0) to b_3
        # (1, 0, 1) to b_2
        # (1, 1, 0) to b_1
        # (1, 1, 1) to b_0
        self.rule = {(i // 4, i // 2 % 2, i % 2): int(self.rule_bits[7 - i])
                         for i in range(8)
                    }
        return True

    def display_rule_information(self):
        self.input.delete(0, tk.END)
        self.shown_rule_number.set('Rule ' + str(self.rule_number))
        mirrored_rule_number = int(self.mirror(self.rule_bits), 2)
        # Complementation exchanges the roles of 0 and 1,
        # so the complementary rule of a rule R maps
        # (a, b, c) to not R(not a, not b, not c).
        # Hence if R is the rule that in binary, is coded as
        #       b_0 b_1 b_2 b_3 b_4 b_5 b_6 b_7
        # then the complementary of R is coded in binary as
        #       ~b_7 ~b_6 ~b_5 ~b_4 ~b_3 ~b_2 ~b_1 ~b_0
        complementary_rule_bits = ''.join({'0': '1', '1': '0'}[c]
                                              for c in reversed(self.rule_bits)
                                         )
        complementary_rule_number = int(complementary_rule_bits, 2)
        mirrored_complementary_rule_number =\
                int(self.mirror(complementary_rule_bits), 2)
        self.shown_related_rule_numbers.set(
                'Mirrored rule: ' + str(mirrored_rule_number)
                + '            Complementary rule: '
                + str(complementary_rule_number)
                + '            Mirrored complementary rule: '
                + str(mirrored_complementary_rule_number)
                                           )
        self.shown_rule.delete(tk.ALL)
        self.shown_rule.create_line(5, 5, 245, 5)
        self.shown_rule.create_line(5, 25, 245, 25)
        self.shown_rule.create_line(5, 45, 245, 45)
        for i in range(9):
            self.shown_rule.create_line(i * 30 + 5, 5, i * 30 + 5, 45)
        for i in range(8):
            self.shown_rule.create_text(i * 30 + 20, 15, text=f'{7 - i:03b}')
            self.shown_rule.create_text(i * 30 + 20, 35, text=self.rule_bits[i]
                                       )

    def warn_of_incorrect_input(self):
        tkinter.messagebox.showerror('Rule error', 'Incorrect rule number')
        self.input.delete(0, tk.END)

    def mirror(self, rule_bits):
        # Reflection through a vertical axis,
        # so the mirrored rule of a rule R maps
        # (a, b, c) to R(c, b, a):
        return ''.join(self.rule_bits[i] for i in sorted(
                         range(8), key=lambda i: (i % 2, i // 2 % 2, i // 4)
                                                        )
                      )

    def work_from_single_1(self):
        input = self.get_rule()
        if input is False:
            return
        if input is None or self.previous_rule_number == self.rule_number:
            if self.displaying_history_from_single_1:
                return
        else:
            self.display_rule_information()
        self.history.delete(tk.ALL)
        # line[0] and line[1] will alternatively play the roles of a
        # line and the following line,  the latter being determined from
        # the former.
        line = [[0] * (2 * self.nb_of_steps + 1) for _ in range(2)]
        # Just a 1 in the middle
        line[0][self.nb_of_steps] = 1
        self.history.create_rectangle(2 * self.nb_of_steps + 3, 5,
                                      2 * self.nb_of_steps + 5, 7,
                                      fill=self.history_colour
                                     )
        a = False
        for i in range(1, self.nb_of_steps - 1):
            line_a = line[a]
            line_not_a = line[not a]
            #             .x.
            #            .xxx.
            #           .xxxxx.
            #          .xxxxxxx.
            # Triangle increases by one cell on each side for each new
            # line. All cells beyond the boundaries of the triangle and
            # on the same side have the same state which is also
            # computed (assigned to both "dots" around the x's) ...
            for j in range(self.nb_of_steps - i - 1, self.nb_of_steps + i + 2):
                self.compute_cell_state(line_a, line_not_a, j)
            # ... and propagated on the left side ...
            for j in range(self.nb_of_steps - i - 1):
                line_not_a[j] = line_not_a[self.nb_of_steps - i - 1]
            # ... and propagated on the right side.
            for j in range(self.nb_of_steps + i + 2, 2 * self.nb_of_steps + 1):
                line_not_a[j] = line_not_a[self.nb_of_steps + i + 1]
            a = not a
            self.display_history_line(line, a, i, 0)
        line_a = line[a]
        line_not_a = line[not a]
        # For the last line, we do not compute the state beyond the boundary
        # of the triangle (no assignment to both "dots" around the x's)
        for j in range(1, 2 * self.nb_of_steps):
            self.compute_cell_state(line_a, line_not_a, j)
        self.display_history_line(line, not a, self.nb_of_steps - 1, 0)
        self.previous_rule_number = self.rule_number
        self.displaying_history_from_single_1 = True

    def work_from_random_state(self):
        if self.get_rule() is False:
            return
        if self.previous_rule_number != self.rule_number:
            self.display_rule_information()
        self.history.delete(tk.ALL)
        # .............
        # ....xxxxx....
        # ....xxxxx....
        # ....xxxxx....
        # ....xxxxx....
        # We need to generate about twice as many random numbers as the
        # number of lines being displayed, because
        # - the leftmost x on the last row depends on the last . before
        #   the first x on the last row,
        # - which depends on the second last . before the first x on the
        #   second last row,
        # - which depends on the third last . before the first x on the
        #   third last row
        # ...
        line = [randint(0, 1) for _ in range(4 * self.nb_of_steps - 2)],\
               [0] * (4 * self.nb_of_steps - 2)
        self.display_history_line(line, 0, 0, self.nb_of_steps - 2)
        a = False
        for i in range(1, self.nb_of_steps):
            line_a = line[a]
            line_not_a = line[not a]
            for j in range(i, 4 * self.nb_of_steps - 2 - i):
                self.compute_cell_state(line_a, line_not_a, j)
            a = not a
            self.display_history_line(line, a, i, self.nb_of_steps - 2)
        self.previous_rule_number = self.rule_number
        self.displaying_history_from_single_1 = False

    def display_history_line(self, line, a, i, offset):
        line_a = line[a]
        for j in range(1, 2 * self.nb_of_steps):
            if line_a[j + offset]:
                self.history.create_rectangle(2 * j + 3, 2 * i + 5, 2 * j + 5,
                                              2 * i + 7,
                                              fill=self.history_colour
                                             )

    def compute_cell_state(self, previous_line, line, j):
        line[j] = self.rule[previous_line[j - 1], previous_line[j],
                            previous_line[j + 1]
                           ]


if __name__ == '__main__':
    ElementaryCellularAutomata().mainloop()

