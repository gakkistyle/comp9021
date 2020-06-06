# COMP9021 Term 3 2019


import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import numpy as np
from random import randrange
from itertools import accumulate


class BarnsleyFern(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Barnsley Fern')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Barnsley Fern Help', menu=help_menu)
        help_menu.add_command(label='Affine transformations',
                              command=self.affine_transformations_help
                             )
        help_menu.add_command(label='Displayed parameters',
                              command=self.displayed_parameters_help
                             )
        help_menu.add_command(label='Fern species',
                              command=self.fern_species_help
                             )
        self.config(menu=menubar)
        fern_selection_board = tk.Frame(bd=20)
        predefined_ferns_button = tk.Menubutton(fern_selection_board,
                                                text='Predefined ferns'
                                               )
        predefined_ferns_button.pack(padx=30, pady=30)
        predefined_ferns = tk.Menu(predefined_ferns_button)
        for species in 'Black Spleenwort', 'Culcita', 'Cyclosorus':
            predefined_ferns.add_command(label=species,
                                         command=lambda fern_species=species:
                                                self.display_fern(fern_species)
                                        )
        predefined_ferns_button.config(menu=predefined_ferns)
        fern_parameters_board = FernParametersBoard()
        self.drawing = Drawing(fern_parameters_board)
        self.drawing.pack(padx=30, side=tk.LEFT)
        fern_selection_board.pack()
        fern_parameters_board.pack()
        draw_buttons = tk.Frame(bd=20)
        tk.Button(draw_buttons, text='Draw custom fern',
                  command=lambda fern_species='Custom':
                                         self.display_fern(fern_species)
                 ).pack(padx=20, side=tk.LEFT)
        draw_buttons.pack()
        self.displayed_fern=tk.StringVar()
        tk.Label(draw_buttons, textvariable=self.displayed_fern, width=16,
                 fg=Fern.colour
                ).pack(pady=40)
        self.displayed_fern.set('Black Spleenwort')

    def affine_transformations_help(self):
        tkinter.messagebox.showinfo(
                'Affine transformations',
                'A fern is a fixed point A of four affine '
                'transformations T1, T2, T3 and T4, each of wich maps '
                'a point (x, y) to\n    (ax + by + e, cx + dy + f)\n'
                'for some real numbers a, b, c, d, e and f, i.e., A is '
                'the union of T1(A), T2(A), T3(A) and T4(A).\n\n'
                'Denoting by L and R the largest left and right '
                'leaflets, respectively, T2, T3 and T4 are determined '
                'by the image of 3 noncolinear points:\n'
                ' - T2 maps the tip of the fern to itself and the tips '
                'of L and R to the tips of the second largest left and '
                'right leaflets of the fern, respectively.\n'
                ' - T3 and T4 map the bottom of the stem of the fern '
                'to the bottom of the stems of L and R and the tips of '
                'the largest left and right leaflets of the fern to '
                'the tips of the largest left and right leaflets of L '
                'and R, respectively.\n'
                ' - As for T1, it is best described as projecting all '
                'points of the fern on the y-axis before applying a '
                'contraction.'
                                    )

    def displayed_parameters_help(self):
        tkinter.messagebox.showinfo(
                'Displayed parameters',
                'For each of T1, T2, T3 and T4, the parameters are '
                'displayed as\n'
                '    a    b    e\n'
                '    c    d    f\n\n'
                'The number to the right represents the probability '
                'that the corresponding transformation be applied to '
                'the current point, starting from point (0,0), located '
                'at the bottom of the stem of the fern.\n\nFactor can '
                'be used to scale the picture of the fern up or down.'
                                    )

    def fern_species_help(self):
        tkinter.messagebox.showinfo(
                'Fern species',
                'Three predefined fern species can be selected, with '
                'the corresponding parameters being automatically '
                'displayed. The parameters can be set to any value to '
                'display a custom fern, provided that:\n'
                ' - a, b, c, d, e and f are floating point numbers;\n'
                ' - the weights are nonnegative integers that sum up '
                'to 100;\n'
                ' - the scaling factor is a strictly positive integer.'
                                    )

    def display_fern(self, fern_species):
        self.displayed_fern.set(fern_species)
        self.drawing.display_fern(fern_species)


class Drawing(tk.Frame):
    dim = 600
    half_dim = dim // 2
    error_colour = '#FFCCCC'
    nb_of_iterations = 20000
    
    def __init__(self, fern_parameters_board):
        tk.Frame.__init__(self, padx=20, pady=20)
        self.fern_parameters_board = fern_parameters_board
        self.drawing = tk.Canvas(self, width=self.dim, height=self.dim + 50)
        self.drawing.pack()
        self.fern = BlackSpleenwort()
        self.draw_fern()

    def display_fern(self, fern_species):
        if fern_species == 'Custom':
            self.fern = Fern()
            self.fern_parameters_board.factor.config(bg='white')
            for n in range(4):
                self.fern_parameters_board.weights[n].config(bg='white')
                for i in range(2):
                    self.fern_parameters_board.translation_vectors[n][i]\
                        .config(bg='white')
                    for j in range(2):
                        self.fern_parameters_board\
                            .linear_coefficients[n][i][j].config(bg='white')
            incorrect_input = False
            try:
                self.fern.factor = int(self.fern_parameters_board.factor.get())
            except ValueError:
                self.fern_parameters_board.factor.config(bg=self.error_colour)
                incorrect_input = True
            if self.fern.factor <= 0:
                self.fern_parameters_board.factor.config(bg=self.error_colour)
                incorrect_input = True
            for n in range(4):
                try:
                    self.fern.weights[n] =\
                            int(self.fern_parameters_board.weights[n].get())
                except ValueError:
                    self.fern_parameters_board.weights[n]\
                        .config(bg=self.error_colour)
                    incorrect_input = True
                if self.fern.weights[n] < 0:
                    self.fern_parameters_board.weights[n]\
                        .config(bg=self.error_colour)
                    incorrect_input = True
                for i in range(2):
                    try:
                        self.fern.translation_vectors[n][i] =\
                                float(self.fern_parameters_board
                                          .translation_vectors[n][i].get()
                                     )
                    except ValueError:
                        self.fern_parameters_board.translation_vectors[n][i]\
                            .config(bg=self.error_colour)
                        incorrect_input = True
                    for j in range(2):
                        try:
                            self.fern.linear_coefficients[n][i][j] =\
                                  float(self.fern_parameters_board
                                            .linear_coefficients[n][i][j].get()
                                       )
                        except ValueError:
                            self.fern_parameters_board\
                                .linear_coefficients[n][i][j]\
                                .config(bg=self.error_colour)
                            incorrect_input = True
            if incorrect_input:
                return
            if sum(self.fern.weights) != 100:
                for n in range(4):
                    self.fern_parameters_board.weights[n]\
                        .config(bg=self.error_colour)
                tkinter.messagebox.showerror('Incorrect input',
                                             'Weights should sum to 100'
                                            )
                return
        else:
            self.fern = {'Black Spleenwort': BlackSpleenwort(),
                         'Culcita': Culcita(), 'Cyclosorus': Cyclosorus()
                        }[fern_species]
            self.fern_parameters_board.update_parameters(self.fern)
        self.drawing.delete(tk.ALL)
        self.draw_fern()

    def draw_fern(self):
        translation_vectors = [np.array([[translation_vector[0]],
                                         [translation_vector[1]]
                                        ]
                                       ) for translation_vector in
                                                  self.fern.translation_vectors
                              ]
        linear_coefficients = [np.array(linear_coefficients)
                                       for linear_coefficients in
                                                  self.fern.linear_coefficients
                              ]
        accumulated_weights = list(accumulate(self.fern.weights))
        point = np.array([[0], [0]])
        for _ in range(self.nb_of_iterations):
            r = randrange(100)
            for n in range(4):
                if r < accumulated_weights[n]:
                    point = linear_coefficients[n] @ point\
                            + translation_vectors[n]
                    x, y = point[0, 0] * self.fern.factor,\
                           point[1, 0] * self.fern.factor
                    self.drawing.create_oval(self.half_dim + x - 0.3,
                                             self.dim - y - 0.3,
                                             self.half_dim + x + 0.3,
                                             self.dim - y + 0.3,
                                             fill=Fern.colour,
                                             outline=Fern.colour
                                            )
                    break


class Fern:
    colour = '#006400'

    def __init__(self,
                 linear_coefficients=[[[None] * 2 for _ in range(2)]
                                          for _ in range(4)
                                     ],
                 translation_vectors=[[None] * 2 for _ in range(4)],
                 weights=[None] * 4, factor=None
                ):
        self.translation_vectors = translation_vectors
        self.linear_coefficients = linear_coefficients
        self.weights = weights
        self.factor = factor


class BlackSpleenwort(Fern):
    def __init__(self):
        super().__init__((((0, 0), (0, 0.16)), ((0.85, 0.04), (-0.04, 0.85)),
                          ((0.2, -0.26), (0.23, 0.22)),
                          ((-0.15, 0.28), (0.26, 0.24))
                         ), ((0, 0), (0, 1.6), (0, 1.6), (0, 0.44)),
                         (1, 85, 7, 7), factor=Drawing.dim // 12
                        )


class Culcita(Fern):
    def __init__(self):
        super().__init__((((0, 0), (0, 0.25)), ((0.85, 0.02), (-0.02, 0.83)),
                          ((0.09, -0.28), (0.30, 0.11)),
                          ((-0.09, 0.28), (0.3, 0.09))
                         ), ((0, -0.14), (0, 1), (0, 0.6), (0, 0.7)),
                         (2, 84, 7, 7), factor=Drawing.dim // 6
                        )


class Cyclosorus(Fern):
    def __init__(self):
        super().__init__((((0, 0), (0, 0.25)), ((0.95, 0.005), (-0.005, 0.93)),
                          ((0.035, -0.2), (0.16, 0.04)),
                          ((-0.04, 0.2), (0.16, 0.04))
                         ), ((0, -0.4), (-0.002, 0.5), (-0.09, 0.02),
                             (0.083, 0.12)
                            ), (2, 94, 2, 2), factor=Drawing.dim // 8
                        )


class FernParametersBoard(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, bd=20)
        fern = BlackSpleenwort()
        self.linear_coefficients = [[[None] * 2 for _ in range(2)]
                                        for _ in range(4)
                                   ]
        self.translation_vectors = [[None] * 2 for _ in range(4)]
        self.weights = [None] * 4
        text_labels = {0: 'Stem', 1: 'Upper leaflets', 2: 'Lower left leaflet',
                       3: 'Lower right leaflet'
                      }
        for n in range(4):
            tk.Label(self, text=text_labels[n]).grid(row=3 * n, columnspan=4,
                                                     pady=5
                                                    )
            for i in range(2):
                for j in range(2):
                    self.linear_coefficients[n][i][j] =\
                            tk.Entry(self, bd=1, width=5)
                    self.linear_coefficients[n][i][j].grid(row=3 * n + i + 1,
                                                           column=j
                                                          )
                    self.linear_coefficients[n][i][j]\
                        .insert(0, fern.linear_coefficients[n][i][j])
                self.translation_vectors[n][i] = tk.Entry(self, bd=1, width=5)
                self.translation_vectors[n][i].grid(row=3 * n + i + 1,
                                                    column=2, padx=15
                                                   )
                self.translation_vectors[n][i]\
                    .insert(0, fern.translation_vectors[n][i])
            self.weights[n] = tk.Entry(self, bd=1, width=3)
            self.weights[n].grid(row=3 * n + 1, rowspan=2, column=3, padx=25)
            self.weights[n].insert(0, fern.weights[n])
        tk.Label(self, text='Factor').grid(row=12, pady=40)
        self.factor = tk.Entry(self, bd=1, width=4)
        self.factor.grid(row=12, column=1)
        self.factor.insert(0, fern.factor)

    def update_parameters(self, fern):
        self.factor.delete(0, tk.END)
        self.factor.insert(0, fern.factor)
        for n in range(4):
            self.weights[n].delete(0, tk.END)
            self.weights[n].insert(0, fern.weights[n])
            for i in range(2):
                self.translation_vectors[n][i].delete(0, tk.END)
                self.translation_vectors[n][i]\
                    .insert(0, fern.translation_vectors[n][i])
                for j in range(2):
                    self.linear_coefficients[n][i][j].delete(0, tk.END)
                    self.linear_coefficients[n][i][j]\
                        .insert(0, fern.linear_coefficients[n][i][j])


if __name__ == '__main__':
    BarnsleyFern().mainloop()
