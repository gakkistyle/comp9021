# COMP9021 Term 3 2019


import tkinter as tk
import tkinter.messagebox
from random import randrange


class GameOfLife(tk.Tk):
    delay = 600
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Game of Life')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Game of Life Help', menu=help_menu)
        help_menu.add_command(label='Rules of the game',
                              command=self.rules_help
                             )
        help_menu.add_command(label='The "Seed" button',
                              command=self.seed_button_help
                             )
        help_menu.add_command(label='The "Next state" button',
                              command=self.next_state_button_help
                             )
        help_menu.add_command(label='The "Start/Stop evolution" button',
                              command=self.evolution_button_help
                             )
        self.config(menu=menubar)

        self.board = Board()
        buttons = tk.Frame(bd=20)
        self.seed_button = tk.Menubutton(buttons, text='Seed')
        self.seed_button.pack(padx=30, side=tk.LEFT)
        densities = tk.Menu(self.seed_button)
        densities.add_command(label=' 0%', command=self.board.empty_board)
        for i in range(10, 50, 5):
            densities.add_command(label=f'{i}%',
                                  command=lambda p=i: self.board.seed(p)
                                 )
        densities.add_command(label='Gosper Glider Gun',
                              command=self.board.create_gosper_glider_gun
                             )
        self.seed_button.config(menu=densities)
        self.next_state_button = tk.Button(buttons, text='Next state',
                                           command=self.board.update
                                          )
        self.next_state_button.pack(padx=30, side=tk.LEFT)
        self.evolution_button = tk.Button(buttons, text='Start evolution',
                                          width=13, command=self.evolve
                                         )
        self.evolution_button.pack(padx=30)
        buttons.pack()
        self.board.pack()
        self.evolving = False

    def rules_help(self):
        tkinter.messagebox.showinfo(
                    'Rules of the game',
                    'A cell comes into existence at an empty spot when '
                    'that spot is surrounded by exactly 3 cells.\n\n'
                    'A cell survives iff it is surrounded by exactly 2 '
                    'or 3 cells.'
                                   )

    def seed_button_help(self):
        tkinter.messagebox.showinfo(
                    'The "Seed" button',
                    'This button allows one to generate a random '
                    'population of cells with an expected density '
                    'ranging from 10 to 45 in steps of 5, plus a value '
                    'of 0 to start with an empty board, plus a special '
                    'initial population known as "Gosper Glider '
                    'Gun".\n\nClicking on the board allows one to add '
                    'cells and remove cells.'
                                   )

    def next_state_button_help(self):
        tkinter.messagebox.showinfo(
                    'The Next state button',
                    'This button allows one to apply the rules of the '
                    'game once.'
                                   )

    def evolution_button_help(self):
        tkinter.messagebox.showinfo(
                    'The "Start/Stop evolution" button',
                    'This button allows one to apply the rules of the '
                    'game for as long as wished, and to stop it once '
                    'it has been started.\n\nWhen evolution proceeds, '
                    'both other buttons become inactive, and the '
                    'button displays "Stop evolution".\n\nWhen '
                    'evolution does not proceed, all buttons are '
                    'active and the button displays "Start evolution".'
                                   )

    def evolve(self):
        if not self.evolving:
            self.evolving = True
            self.seed_button.config(state=tk.DISABLED)
            self.next_state_button.config(state=tk.DISABLED)
            self.evolution_button.config(text='Stop evolution')
            self.keep_evolving()
        else:
            self.evolving = False
            self.evolution_button.config(text='Start evolution')
            self.seed_button.config(state=tk.NORMAL)
            self.next_state_button.config(state=tk.NORMAL)

    def keep_evolving(self):
        if self.evolving:
            self.board.update()
            self.after(self.delay, self.keep_evolving)


class Board(tk.Frame):
    dim = 80
    cell_size = 8
    board_colour = '#F6FFFE'
    line_colour = '#E5FAF8'
    cell_colour = '#830505'
    
    def __init__(self):
        tk.Frame.__init__(self, bd=10, padx=20, pady=20)
        # We add a "band" around the board, with values that will remain
        # False, to avoid checking for boundary conditions.
        self.cells = [[[False] * (self.dim + 2)
                           for _ in range(self.dim + 2)
                      ] for _ in range(2)
                     ]
        self.drawn_cells = [[False] * self.dim for _ in range(self.dim)]
        self.colours = self.board_colour, self.cell_colour
        self.board = tk.Canvas(self, width=self.dim * self.cell_size + 5,
                               height=self.dim * self.cell_size + 5,
                               bg=self.board_colour
                              )
        self.switch = False
        self.draw_board()
        self.board.pack()
        self.board.bind('<1>', self.flip_cell)

    def empty_board(self):
        cells = self.cells[self.switch]
        for i in range(1, self.dim + 1):
            for j in range(1, self.dim + 1):
                cells[i][j] = False
        self.draw_cells()

    def seed(self, density):
       cells = self.cells[self.switch]
       for i in range(1, self.dim + 1):
            for j in range(1, self.dim + 1):
                cells[i][j] = randrange(100) < density
       self.draw_cells()

    def create_gosper_glider_gun(self):
        self.empty_board()
        cells = self.cells[self.switch]
        cells[26][2] = True; cells[24][3] = True; cells[26][3] = True
        cells[14][4] = True; cells[15][4] = True; cells[22][4] = True
        cells[23][4] = True; cells[36][4] = True; cells[37][4] = True
        cells[13][5] = True; cells[17][5] = True; cells[22][5] = True
        cells[23][5] = True; cells[36][5] = True; cells[37][5] = True
        cells[2][6] = True; cells[3][6] = True; cells[12][6] = True
        cells[18][6] = True; cells[22][6] = True; cells[23][6] = True
        cells[2][7] = True; cells[3][7] = True; cells[12][7] = True
        cells[16][7] = True; cells[18][7] = True; cells[19][7] = True
        cells[24][7] = True; cells[26][7] = True; cells[12][8] = True
        cells[18][8] = True; cells[26][8] = True; cells[13][9] = True
        cells[17][9] = True; cells[14][10] = True; cells[15][10] = True
        self.draw_cells()

    def draw_board(self):
        for i in range(self.dim + 1):
            self.board.create_line(5, 5 + self.cell_size * i,
                                   5 + self.cell_size * self.dim,
                                   5 + self.cell_size * i, width=0.5,
                                   fill=self.line_colour
                                  )
            self.board.create_line(5 + self.cell_size * i, 5,
                                   5 + self.cell_size * i,
                                   5 + self.cell_size * self.dim, width=0.5,
                                   fill=self.line_colour
                                  )

    def draw_cells(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.board.delete(self.drawn_cells[i][j])
        for i in range(self.dim):
            for j in range(self.dim):
                self.drawn_cells[i][j] = self.board.create_oval(
                      6 + self.cell_size * i, 6 + self.cell_size * j,
                      4 + self.cell_size * (i + 1),
                      4 + self.cell_size * (j + 1),
                      fill=self.colours[self.cells[self.switch][i + 1][j + 1]],
                      outline=self.board_colour
                                                               )

    def flip_cell(self, event):
        if not self.master.evolving\
           and 5 <= event.x <= self.cell_size * self.dim + 5\
           and 5 <= event.y <= self.cell_size * self.dim + 5:
            i = int((self.board.canvasx(event.x) - 5) / self.cell_size)
            j = int((self.board.canvasx(event.y) - 5) / self.cell_size)
            self.board.delete(self.drawn_cells[i][j])
            self.cells[self.switch][i + 1][j + 1] =\
                    not self.cells[self.switch][i + 1][j + 1]
            self.drawn_cells[i][j] = self.board.create_oval(
                      6 + self.cell_size * i, 6 + self.cell_size * j,
                      4 + self.cell_size * (i + 1),
                      4 + self.cell_size * (j + 1),
                      fill=self.colours[self.cells[self.switch][i + 1][j + 1]],
                      outline=self.board_colour
                                                           )

    def update(self):
        cells = self.cells[self.switch]
        new_cells = self.cells[not self.switch]
        for i in range(1, self.dim + 1):
            for j in range(1, self.dim + 1):
                count = cells[i - 1][j - 1] + cells[i - 1][j]\
                        + cells[i - 1][j + 1] + cells[i][j - 1]\
                        + cells[i][j + 1] + cells[i + 1][j - 1]\
                        + cells[i + 1][j] + cells[i + 1][j + 1]
                new_cells[i][j] = not cells[i][j] and count == 3\
                                  or cells[i][j] and 2 <= count <= 3
        self.switch = not self.switch
        self.draw_cells()


if __name__ == '__main__':
    GameOfLife().mainloop()
