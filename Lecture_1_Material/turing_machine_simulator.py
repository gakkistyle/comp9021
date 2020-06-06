# Written by Eric Martin for COMP9021


import tkinter as tk
import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.simpledialog


class TuringMachineSimulator(tk.Tk):
    max_nb_of_steps = 1000

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Turing Machine Simulator')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='Turing Machine Simulator Help',
                            menu=help_menu
                           )
        help_menu.add_command(label='Tape', command=self.tape_help)
        help_menu.add_command(label='Program', command=self.program_help)
        help_menu.add_command(label='Execution', command=self.execution_help)
        self.config(menu=menubar)

        self.scrollable_tape = ScrollableTape()
        self.scrollable_tape.pack()
        self.program = Program()
        dashboard = tk.Frame()
        self.state = State(dashboard)
        self.state.pack(padx=20, side=tk.LEFT)
        self.iteration = Iteration(dashboard)
        self.iteration.pack(padx=20, side=tk.LEFT)
        self.status = Status(dashboard, self.program)
        self.status.pack(padx=20)
        dashboard.pack()
        buttons = tk.Frame(bd=20)
        self.next_phase = 'Start'
        self.next_phase_button = tk.Button(buttons, text='Start', width=5,
                                           command=self.change_interface
                                          )
        self.next_phase_button.pack(padx=30, side=tk.LEFT)
        self.step_button = tk.Button(buttons, text='Step', command=self.step,
                                     state=tk.DISABLED
                                    )
        self.step_button.pack(padx=30, side=tk.LEFT)
        self.continue_button = tk.Button(buttons, text='Continue',
                                         command=self.run_further,
                                         state=tk.DISABLED
                                        )
        self.continue_button.pack(padx=30)
        buttons.pack()
        self.program.pack()

    def tape_help(self):
        tkinter.messagebox.showinfo(
                'Tape',
                'The tape always contains an "origin" cell.\n\nControl '
                'clicking to the right or to the left of the current '
                'rightmost or leftmost cell, respectively, adds a new '
                'cell.\n\n Control clicking on the current rightmost '
                'or leftmost added cell removes it.\n\nClicking on any '
                'cell flips the bit it contains from 1 to 0 or from 0 '
                'to 1.'
                                    )

    def program_help(self):
        tkinter.messagebox.showinfo(
                'Program',
                'A program is a set of instructions of the form\n'
                '    (state_1, bit_1, state_2, bit_2, dir)\n'
                'where state_1 and state_2 have to be alphanumeric '
                'words with at most 8 characters, bit_1 and bit_2 have '
                'to be 0 or 1, and dir has to be L or R.\n\nWhen the '
                'TM machine is in state state_1 with its head pointing '
                'to a cell containing bit_1, then it changes bit_1 to '
                'bit_2 in that cell, modifies its state to state_2, '
                'and moves its head one cell to the right or to the '
                'left as determined by dir.\n\nThe TM machine is '
                'supposed to be deterministic, hence the program '
                'should not contain two instructions starting with '
                'the same pair (state_1, bit_1).\n\nThe program can '
                'contain comments, namely, lines starting with #.'
                                    )

    def execution_help(self):
        tkinter.messagebox.showinfo(
                'Execution',
                'When the leftmost button displays Start, the status '
                'indicator is red, the tape can be modified, the '
                'program can be edited, the Step and Continue buttons '
                'are disabled, and no State or Iteration is '
                'displayed.\n\n Once this button has been pressed, it '
                'displays Stop, the status indicator is green, the '
                'tape cannot be modified, the program cannot be '
                'edited, and the current State and Iteration are '
                'displayed.\n\nWhen execution stops, either because no '
                'instruction can be executed or because Stop has been '
                'pressed, the Step and Continue buttons are disabled '
                'and the leftmost button displays Reset; it has to be '
                'pressed to restore the tape to its initial '
                'configuration, with only the "origin" cell '
                'containing 1.\n\nPressing the Start button prompts '
                'the user for an initial state, which has to be an '
                'alphanumeric word with at most 8 characters, and '
                'commences execution provided at least one cell '
                'contains 1, in which case the head initially points '
                'to the leftmost cell containing 1.\n\nThe Step button '
                'executes one instruction, if possible; otherwise '
                'execution stops.\n\nThe Continue buttom executes up '
                'to 1,000 instructions, if possible; otherwise '
                'execution stops.\n\nThe Stop button allows one to '
                'start a new excution in case it is either not '
                'desirable or not possible to terminate execution with '
                'a sequence of clicks on the Step or Continue buttons.'
                                    )

    def change_interface(self):
        {'Start': self.start, 'Stop': self.stop, 'Reset': self.reset
        }[self.next_phase]()

    def start(self):
        if not self.program.read_instructions():
            return
        initial_state = tkinter.simpledialog.askstring('Starting program',
                                                       'Enter initial state: '
                                                      )
        if initial_state is None:
            return
        if not StateName(initial_state).check_syntactic_validity():
            return
        # Look for leftmost 1
        for i in range(len(self.scrollable_tape.cells[0]) - 1, -1, -1):
            if self.scrollable_tape.bits[0][i] == 1:
                self.scrollable_tape.tape.itemconfig(
                        self.scrollable_tape.cells[0][i], fill='red',
                        font=('normal', 0, 'bold')
                                                    )
                self.current_index = -i
                break
        else:
            for i in range(1, len(self.scrollable_tape.cells[1])):
                if self.scrollable_tape.bits[1][i] == 1:
                    self.scrollable_tape.tape.itemconfig(
                            self.scrollable_tape.cells[1][i],
                            fill='red', font=('normal', 0, 'bold')
                                                        )
                    self.current_index = i
                    break
            else:
                tkinter.messagebox.showerror(
                        'Tape error',
                        'Cannot run, no bit is set to 1 in tape'
                                            )
                return
        self.status.running_program(True)
        self.update_phase('Stop')
        self.current_bit = 1
        self.current_state = initial_state
        self.current_iteration = 0
        self.iteration.update(0)
        self.state.update(initial_state)

    def reset(self):
        self.scrollable_tape.reset()
        self.update_phase('Start')

    def step(self):
        state, bit = self.current_state, self.current_bit
        if (state, bit) not in self.program.instructions:
            self.status.running_program(False)
            self.update_phase('Reset')
            return
        new_state, new_bit, direction = self.program.instructions[state, bit]
        self.state.update(new_state)
        self.current_iteration += 1
        self.iteration.update(self.current_iteration)
        i = self.current_index
        side = i > 0
        j = abs(i)
        self.scrollable_tape.bits[side][j] = new_bit
        if i == 0:
            self.scrollable_tape.bits[not side][0] = new_bit
        self.scrollable_tape.tape.itemconfig(
                self.scrollable_tape.cells[side][j], text=new_bit,
                fill='black', font=('normal', 0, 'normal')
                                            )
        i += direction
        side = i > 0
        j = abs(i)
        if j >= len(self.scrollable_tape.bits[side]):
            self.scrollable_tape.add_cell_to_end(side)
        self.scrollable_tape.tape.itemconfig(
                self.scrollable_tape.cells[side][j],
                fill='red', font=('normal', 0, 'bold')
                                            )
        self.current_bit = self.scrollable_tape.bits[side][j]
        self.current_index = i
        self.current_state = new_state

    def run_further(self):
        if self.next_phase == 'Stop':
            bound = self.current_iteration + self.max_nb_of_steps
        while self.next_phase == 'Stop' and self.current_iteration < bound:
            self.step()

    def stop(self):
        self.status.running_program(False)
        self.update_phase('Reset')

    def update_phase(self, phase):
        self.next_phase = phase
        self.next_phase_button.config(text=phase)
        if phase == 'Start':
            self.state.update('')
            self.iteration.update('')
        elif phase == 'Stop':
            self.step_button.config(state=tk.NORMAL)
            self.continue_button.config(state=tk.NORMAL)
        else:
            self.step_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.DISABLED)


class ScrollableTape(tk.Frame):
    tape_colour = '#FFFAF0'
    cell_colour = '#8B7765'
    cell_size = 30
    nb_of_cells_without_scroll = 21
    cell_proportion_for_endspace = 2.2

    def __init__(self):
        tk.Frame.__init__(self, bd=10, padx=20)
        self.set_original_conditions()
        w = (self.nb_of_cells_without_scroll
             + 2 * self.cell_proportion_for_endspace
            ) * self.cell_size
        self.tape = tk.Canvas(self, width=w, height=self.cell_size + 1,
                              bg=self.tape_colour
                             )
        self.draw_minimal_tape()
        self.tape.grid(row=0)
        scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL,
                                 command=self.tape.xview
                                )
        self.tape.config(xscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, sticky=tk.EW)
        self.tape.bind('<1>', self.flip_bit)
        self.tape.bind('<Control-1>', self.add_or_remove_cell)

    # To start with, only one cell is displayed. More cells can be
    # displayed to the right (expanding the list self.cells[1]) or to
    # the left (expanding the list self.cells[0]), the lists
    # self.cells[1] and self.cells[0] being handles to the textual
    # display of the bits they store, which are recorded in self.bits[1]
    # and self.bits[0], respectively.
    # self.max_indexes[1] and self.max_indexes[0] record  the number of
    # these extra cells, respectively.
    # We use i to refer to the ith-cell on the right, and -i to refer to
    # the ith-cell on the left.
    def set_original_conditions(self):
        self.max_indexes = [0, 0]
        self.bits = [1], [1]
        self.cells = [None], [None]
        self.lines = [None], [None]

    def determine_left_boundary(self):
        return -(self.max_indexes[0] + self.cell_proportion_for_endspace)\
               * self.cell_size

    def determine_right_boundary(self):
        return self.cell_size * (max(self.nb_of_cells_without_scroll,
                                     self.max_indexes[1]
                                    ) + self.cell_proportion_for_endspace
                                )

    def draw_minimal_tape(self):
        left_boundary = self.determine_left_boundary()
        right_boundary = self.determine_right_boundary()
        self.tape.config(scrollregion=(left_boundary, -(self.cell_size / 2),
                                       right_boundary, self.cell_size + 1
                                      )
                        )
        self.tape.delete(tk.ALL)
        self.tape.create_line(-0.5 * self.cell_size, 0, -0.5 * self.cell_size,
                              self.cell_size, width=2, fill=self.cell_colour
                             )
        self.cells[0][0] = self.tape.create_text(0, self.cell_size / 2,
                                                 text=self.bits[0][0]
                                                )
        self.tape.create_line(0.5 * self.cell_size, 0, 0.5 * self.cell_size,
                              self.cell_size, width=2, fill=self.cell_colour
                             )
        self.draw_horizontal_lines(left_boundary, right_boundary)

    def draw_horizontal_lines(self, left_boundary, right_boundary):
        self.tape.create_line(left_boundary, 0, right_boundary - left_boundary,
                              0, width=3, fill=self.cell_colour
                             )
        self.tape.create_line(left_boundary, self.cell_size, right_boundary,
                              self.cell_size, width=3, fill=self.cell_colour
                             )

    def add_cell_to_end(self, side):
        i = len(self.bits[side])
        if i > self.max_indexes[side]:
            self.max_indexes[side] = i
            left_boundary = self.determine_left_boundary()
            right_boundary = self.determine_right_boundary()
            self.tape.config(scrollregion=(left_boundary,
                                           -(self.cell_size / 2),
                                           right_boundary, self.cell_size + 1
                                          )
                            )
            self.draw_horizontal_lines(left_boundary, right_boundary)
        self.bits[side].append(0)
        self.cells[side].append(None)
        self.lines[side].append(None)
        s = side * 2 - 1
        self.cells[side][i] = self.tape.create_text(i * s * self.cell_size,
                                                    self.cell_size / 2, text=0
                                                   )
        self.lines[side][i] = self.tape.create_line(
                                      s * (i + 0.5) * self.cell_size, 0,
                                      s * (i + 0.5) * self.cell_size,
                                      self.cell_size, width=2,
                                      fill=self.cell_colour
                                                   )

    def flip_bit(self, event):
        if not self.master.next_phase == 'Start':
            return
        if 0 <= event.y <= self.cell_size:
            i = round(self.tape.canvasx(event.x) / self.cell_size)
            side = i > 0
            i = abs(i)
            if 0 <= i < len(self.cells[side]):
                self.bits[side][i] = not self.bits[side][i]
                self.tape.itemconfig(self.cells[side][i],
                                     text=self.bits[side][i]
                                    )

    def add_or_remove_cell(self, event):
        if not self.master.next_phase == 'Start':
            return
        if 0 <= event.y <= self.cell_size:
            i = round(event.widget.canvasx(event.x) / self.cell_size)
            if i == 0:
                return
            side = i > 0
            i = abs(i)
            if i == len(self.bits[side]) - 1:
                self.tape.delete(self.cells[side][i])
                self.tape.delete(self.lines[side][i])
                del self.bits[side][i]
                del self.cells[side][i]
                del self.lines[side][i]
            elif i == len(self.bits[side]):
                self.add_cell_to_end(side)

    def reset(self):
        del self.cells[0][1 :]
        del self.cells[1][1 :]
        del self.bits[0][1 :]
        del self.bits[1][1 :]
        del self.lines[0][1 :]
        del self.lines[1][1 :]
        self.set_original_conditions()
        self.max_indexes = [0, 0]
        self.draw_minimal_tape()


class Program(tk.Frame):
    label_colour = '#0B0974'
    program_box_colour = '#F0FFF0'
    program_selected_box_colour = '#E0EEE0'

    def __init__(self):
        tk.Frame.__init__(self, bd=30)
        tk.Label(self, text='Program', fg=self.label_colour, bd=10).pack()
        self.source_code = tkinter.scrolledtext.ScrolledText(
                                   self, width=23, height=20,
                                   highlightbackground=self.program_box_colour,
                                   highlightcolor=
                                           self.program_selected_box_colour
                                                            )
        self.source_code.pack()

    def read_instructions(self):
        self.instructions = {}
        source_instructions = self.source_code.get(0.0, tk.END)
        for instruction in source_instructions.splitlines():
            quintuple = instruction.split()
            if len(quintuple) == 0 or quintuple[0][0] == '#':
                continue
            if len(quintuple) != 5:
                tkinter.messagebox.showerror(
                        'Instruction error',
                        f'{instruction} is not a quintuple'
                                            )
                return False
            state, bit, new_state, new_bit, direction = quintuple
            if not StateName(state).check_syntactic_validity():
                return False
            if not Bit(bit).check_syntactic_validity():
                return False
            if not StateName(new_state).check_syntactic_validity():
                return False
            if not Bit(new_bit).check_syntactic_validity():
                return False
            if direction != 'L' and direction != 'R':
                tkinter.messagebox.showerror('Instruction error',
                                             f'{direction} should be L or R'
                                            )
                return False
            if (state, int(bit)) in self.instructions:
                tkinter.messagebox.showerror(
                        'Instruction error',
                        f'More than one instruction for pair ({state}, {bit})'
                                            )
                return False
            self.instructions[state, int(bit)] =\
                    new_state, int(new_bit), (direction == 'R') * 2 - 1
        return True


class StateName(str):
    def check_syntactic_validity(self):
        if self is None:
            tkinter.messagebox.showerror('State name error',
                                         'State name cannot be None'
                                        )
            return False
        if len(self) > 8:
            tkinter.messagebox.showerror(
                    'State name error',
                    f'{self} contains more than 8 characters'
                                        )
            return False
        if not self.isalnum():
            tkinter.messagebox.showerror('State name error',
                                         f'{self} not all nonalphanumeric'
                                        )
            return False
        return True


class Bit(str):
    def check_syntactic_validity(self):
        if self not in '01':
            tkinter.messagebox.showerror('Instruction error',
                                         f'{self} should be 0 or 1'
                                        )
            return False
        return True


class State(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='State: ', fg=Program.label_colour
                ).pack(side=tk.LEFT)
        self.state = tk.StringVar()
        tk.Label(self, width=8, textvariable=self.state).pack()

    def update(self, s):
        self.state.set(s)


class Iteration(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='  Iteration: ', fg=Program.label_colour
                ).pack(side=tk.LEFT)
        self.iteration = tk.StringVar()
        tk.Label(self, width=4, height=1, textvariable=self.iteration).pack()

    def update(self, i):
        self.iteration.set(i)


class Status(tk.Canvas):
    not_running_fill_colour = '#FF1E00'
    not_running_outline_colour = '#980023'
    running_fill_colour = '#25D500'
    running_outline_colour = '#007439'

    def __init__(self, master, program):
        tk.Canvas.__init__(self, master, width=20, height=20)
        self.status = self.create_oval(10, 10, 20, 20,
                                       fill=self.not_running_fill_colour,
                                       outline=self.not_running_outline_colour
                                      )
        self.pack()
        self.program = program

    def running_program(self, running):
        if running:
            self.itemconfig(self.status, fill=self.running_fill_colour,
                            outline=self.running_outline_colour
                           )
            self.program.source_code.config(state='disabled')
        else:
            self.itemconfig(self.status, fill=self.not_running_fill_colour,
                            outline=self.not_running_outline_colour
                           )
            self.program.source_code.config(state='normal')


if __name__ == '__main__':
    TuringMachineSimulator().mainloop()
