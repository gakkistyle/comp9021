# COMP9021 Term 3 2019


import tkinter as tk
import tkinter.messagebox
from random import shuffle
from math import log


class SortingExperimenter(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Sorting experimenter')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label = 'Sorting experimenter Help', menu = help_menu)
        help_menu.add_command(label = 'Boldface', command = self.boldface_help)
        help_menu.add_command(label = 'Blue', command = self.blue_help)
        help_menu.add_command(label = 'Red', command = self.red_help)
        help_menu.add_command(label = 'Yellow', command = self.yellow_help)
        help_menu.add_command(label = 'Green', command = self.green_help)
        self.config(menu = menubar)

        possible_sorting_algorithms = ('Bubble sort', 'Selection sort', 'Insertion sort', 'Shell sort',
                                       'Merge sort', 'Quick sort', 'Heap sort', 'Batcher sort')
        self.selected_sorting_algorithm = possible_sorting_algorithms[0]
        self.list_to_sort = ListToSort()
        self.set_initialisation_interface(possible_sorting_algorithms)
        self.set_user_input_interface()
        self.list_to_sort.pack()
        self.set_control_interface(self.selected_sorting_algorithm)
        self.list_to_sort.display_list(10)
        self.tracing = False

    def boldface_help(self):
        tkinter.messagebox.showinfo('Boldface',
            'When two numbers are being compared, they become boldface.')

    def blue_help(self):
        tkinter.messagebox.showinfo('Blue',
            'Blue is the colour of the "live" numbers.\n\n'
            'For iterative algorithms, all numbers are blue unless their current status '
            'is special and they receive a different colour.\n\n'
            'For recursive algorithms (Quick sort, Merge sort), the numbers in blue (together with '
            'or excepted those whose status is special and which receive a different colour) are '
            'those involved in the current recursive call.')

    def red_help(self):
        tkinter.messagebox.showinfo('Red',
            'For all algorithms except Merge sort, two numbers are colored red when they are about '
            'to be swapped.\n\n'
            'For Merge sort, a number is coloured in red when it is about to be copied to a location '
            'indicated by a star.')

    def yellow_help(self):
        tkinter.messagebox.showinfo('Yellow',
            'Yellow is used:\n'
            ' - when a number is being compared with another number (so its font is boldface), will '
            'not be swapped, and is not known to be in place,\n'
            ' - or when a number has been copied from somewhere else (which except for Merge sort, '
            'means that it has been swapped with another number) and is not known to have been put '
            'in place.')

    def green_help(self):
        tkinter.messagebox.showinfo('Green',
            'Green is the colour of the numbers that have been put in place.\n\n'
            'For Insertion sort and Shell sort, this happens at the very end.\n\n'
            'For Bubble sort, this can happen earlier.\n\n'
            'For all other algorithms, this has to happen earlier for some numbers.')

    def set_initialisation_interface(self, possible_sorting_algorithms):
        initialisation_buttons = tk.Frame(bd = 30)
        self.sorting_algorithms_button = tk.Menubutton(initialisation_buttons,
                                                       text = 'Sorting algorithm')
        self.sorting_algorithms_button.pack(padx = 20, side = tk.LEFT)
        sorting_algorithms = tk.Menu(self.sorting_algorithms_button)
        for sorting_algorithm in possible_sorting_algorithms:
            sorting_algorithms.add_command(label = sorting_algorithm,
                                           command = lambda p = sorting_algorithm:
                                                       self.update_selected_algorithm_and_interfaces(p))
        self.sorting_algorithms_button.config(menu = sorting_algorithms)
        self.default_input_button = tk.Button(initialisation_buttons, text = 'Default input',
                                              command = self.list_to_sort.set_default_input)
        self.default_input_button.pack(padx = 20, side = tk.LEFT)
        self.reverse_input_button = tk.Button(initialisation_buttons, text = 'Reverse input',
                                              command = self.list_to_sort.reverse_input)
        self.reverse_input_button.pack(padx = 20, side = tk.LEFT)
        self.randomise_input_button = tk.Button(initialisation_buttons, text = 'Randomise input',
                                                command = self.list_to_sort.set_randomise_input)
        self.randomise_input_button.pack(padx = 20, side = tk.LEFT)
        self.input_size_button = tk.Menubutton(initialisation_buttons, text = 'Input size')
        self.input_size_button.pack(padx = 20)
        input_size = tk.Menu(self.input_size_button)
        for i in range(2, 21):
            input_size.add_command(label = '{:2d}'.format(i),
                                   command = lambda p = i: self.list_to_sort.display_list(p))
        initialisation_buttons.pack()
        self.input_size_button.config(menu = input_size)

    def set_user_input_interface(self):
        self.user_input_interface = tk.Frame(bd = 10)
        self.input = tk.Entry(self.user_input_interface, width = 36)
        self.input_button = tk.Button(self.user_input_interface, text = 'Set input',
                                      command = lambda p = self.input: self.list_to_sort.set_input(p))
        self.input_button.pack(side = tk.LEFT)
        self.input.pack()
        self.user_input_interface.pack()

    def set_control_interface(self, selected_sorting_algorithm):
        control_buttons = tk.Frame(bd = 30)
        self.algorithm_button = tk.Button(control_buttons, width = 14,
                                          text = 'Start ' + selected_sorting_algorithm,
                                          command = self.start_or_stop_sorting)
        self.algorithm_button.pack(padx = 80, side = tk.LEFT)
        self.step_button = tk.Button(control_buttons, text = 'Step', state = tk.DISABLED,
                                     command = self.step)
        self.step_button.pack(padx = 80)
        control_buttons.pack()

    def update_selected_algorithm_and_interfaces(self, selected_sorting_algorithm):
        self.selected_sorting_algorithm = selected_sorting_algorithm
        self.update_interfaces(selected_sorting_algorithm)

    def update_interfaces(self, selected_sorting_algorithm):
        if self.tracing:
            self.algorithm_button.config(text = 'Stop ' + selected_sorting_algorithm)
            step_button_state = tk.NORMAL
            other_buttons_state = tk.DISABLED
        else:
            self.algorithm_button.config(text = 'Start ' + selected_sorting_algorithm)
            step_button_state = tk.DISABLED
            other_buttons_state = tk.NORMAL
        self.step_button.config(state = step_button_state)
        self.sorting_algorithms_button.config(state = other_buttons_state)
        self.default_input_button.config(state = other_buttons_state)
        self.reverse_input_button.config(state = other_buttons_state)
        self.randomise_input_button.config(state = other_buttons_state)
        self.input_size_button.config(state = other_buttons_state)
        self.input_button.config(state = other_buttons_state)
        self.input.config(state = other_buttons_state)

    def start_or_stop_sorting(self):
        self.tracing = not self.tracing
        self.update_interfaces(self.selected_sorting_algorithm)
        if self.tracing:
            self.original_list = list(self.list_to_sort.list)
            if self.selected_sorting_algorithm == 'Merge sort':
                self.list_to_sort.display_extra_list()
                self.list_to_sort.extra_list[: self.list_to_sort.length] = (
                                                     self.list_to_sort.list[: self.list_to_sort.length])
            if self.selected_sorting_algorithm == 'Batcher sort':
                # The algorithm assumes that the length of the list to sort is a power of 2
                largest_power_of_two_at_most_equal_to_length_of_list = (
                                                             2 ** int(log(self.list_to_sort.length, 2)))
                if largest_power_of_two_at_most_equal_to_length_of_list != self.list_to_sort.length:
                    self.list_to_sort.display_list(largest_power_of_two_at_most_equal_to_length_of_list)
            for i in range(self.list_to_sort.length):
                self.list_to_sort.displayed_list.itemconfig(self.list_to_sort.cells[i],
                                                            fill = ListToSort.live_item_colour)
            if self.selected_sorting_algorithm == 'Bubble sort':
                self.executing_algorithm = self.list_to_sort.trace_bubble_sort()
            elif self.selected_sorting_algorithm == 'Selection sort':
                self.executing_algorithm = self.list_to_sort.trace_selection_sort()
            elif self.selected_sorting_algorithm == 'Insertion sort':
                self.executing_algorithm = self.list_to_sort.trace_insertion_sort()
            elif self.selected_sorting_algorithm == 'Shell sort':
                self.executing_algorithm = self.list_to_sort.trace_shell_sort()
            elif self.selected_sorting_algorithm == 'Merge sort':
                self.executing_algorithm = self.list_to_sort.trace_merge_sort()
            elif self.selected_sorting_algorithm == 'Quick sort':
                self.executing_algorithm = self.list_to_sort.trace_quick_sort()
            elif self.selected_sorting_algorithm == 'Heap sort':
                self.executing_algorithm = self.list_to_sort.trace_heap_sort()
            elif self.selected_sorting_algorithm == 'Batcher sort':
                self.executing_algorithm = self.list_to_sort.trace_batcher_sort()
        else:
            self.list_to_sort.list = self.original_list
            for i in range(self.list_to_sort.length):
                self.list_to_sort.displayed_list.itemconfig(self.list_to_sort.cells[i],
                                                            text = self.list_to_sort.list[i],
                                                            fill = 'black',
                                                            font = ('normal', 0, 'normal'))
            if self.selected_sorting_algorithm == 'Merge sort':
                self.list_to_sort.displayed_extra_list.delete(tk.ALL)

    def step(self):
        try:
            next(self.executing_algorithm)
        except StopIteration:
            self.start_or_stop_sorting()


class ListToSort(tk.Frame):
    line_colour = '#8B4513'
    cell_size = 40
    live_item_colour = '#0000FF'
    moving_item_colour = '#DC143C'
    nonmoving_item_colour = '#FFD700'
    in_place_item_colour = '#228B22'

    def __init__(self):
        tk.Frame.__init__(self, bd = 10, padx = 20, pady = 20)
        self.displayed_list = tk.Canvas(self, width = 20 * self.cell_size + 5,
                                        height = 1.4 * self.cell_size + 5)
        self.displayed_list.pack()
        self.displayed_extra_list = tk.Canvas(self, width = 20 * self.cell_size + 5,
                                              height = 1.4 * self.cell_size + 5)
        self.displayed_extra_list.pack()
        self.list = list(range(20))
        self.extra_list = [None] * 20
        self.cells = [None] * 20
        self.extra_cells = [None] * 20

    def update_displayed_numbers(self):
        for i in range(self.length):
            self.displayed_list.itemconfig(self.cells[i], text = self.list[i])

    def update_displayed_extra_numbers(self):
        for i in range(self.length):
            self.displayed_extra_list.itemconfig(self.extra_cells[i], text = self.extra_list[i])

    def display_list(self, length):
        self.length = length
        self.offset = (20 - self.length) * self.cell_size / 2 + 5
        self.displayed_list.delete(tk.ALL)
        self.displayed_list.create_line(self.offset, 5, self.offset + self.length * self.cell_size, 5,
                                        width = 0.3, fill = self.line_colour)
        self.displayed_list.create_line(self.offset, 5 + self.cell_size,
                                        self.offset + self.length * self.cell_size, 5 + self.cell_size,
                                        width = 0.3, fill = self.line_colour)
        for i in range(self.length + 1):
            self.displayed_list.create_line(self.offset + i * self.cell_size, 5,
                                            self.offset + i * self.cell_size, 5 + self.cell_size,
                                            width = 0.3, fill = self.line_colour)
        for i in range(self.length):
            self.cells[i] = self.displayed_list.create_text(self.offset + (i + 0.5) * self.cell_size,
                                                            5 + self.cell_size / 2, text = self.list[i])
            self.displayed_list.create_text(self.offset + (i + 0.5) * self.cell_size,
                                            5 + self.cell_size * 1.2, text = i,
                                            font = ('normal', 7, 'normal'))

    def display_extra_list(self):
        self.offset = (20 - self.length) * self.cell_size / 2 + 5
        self.displayed_extra_list.create_line(self.offset, 5,
                                              self.offset + self.length * self.cell_size, 5,
                                              width = 0.3, fill = self.line_colour)
        self.displayed_extra_list.create_line(self.offset, 5 + self.cell_size,
                                              self.offset + self.length * self.cell_size,
                                              5 + self.cell_size, width = 0.3,
                                              fill = self.line_colour)
        for i in range(self.length + 1):
            self.displayed_extra_list.create_line(self.offset + i * self.cell_size, 5,
                                                  self.offset + i * self.cell_size, 5 + self.cell_size,
                                                  width = 0.3, fill = self.line_colour)
        for i in range(self.length):
            self.extra_cells[i] = self.displayed_extra_list.create_text(
                                                  self.offset + (i + 0.5) * self.cell_size,
                                                  5 + self.cell_size / 2,
                                                  text = self.list[i], fill = self.live_item_colour)

    def set_default_input(self):
        self.list = list(range(20))
        self.update_displayed_numbers()

    def reverse_input(self):
        self.list[: self.length] = reversed(self.list[: self.length])
        self.update_displayed_numbers()

    def set_input(self, input):
        L = input.get().split()
        input.delete(0, tk.END)
        for i in range(20):
            try:
                self.list[i] = int(L[i])
            except (ValueError, IndexError):
                self.list[i] = 0
        for i in range(self.length):
            self.displayed_list.itemconfig(self.cells[i], text = self.list[i])

    def set_randomise_input(self):
        L = self.list[: self.length]
        shuffle(L)
        self.list[: self.length] = L
        self.update_displayed_numbers()

    def trace_bubble_sort(self):
        bound = self.length - 1
        swapped = True
        while swapped and bound:
            swapped = False
            new_bound = 0
            for i in range(bound):
                if self.list[i] > self.list[i + 1]:
                    self.displayed_list.itemconfig(self.cells[i], fill = self.moving_item_colour,
                                                   font = ('normal', 0, 'bold'))
                    self.displayed_list.itemconfig(self.cells[i + 1], fill = self.moving_item_colour,
                                                   font = ('normal', 0, 'bold'))
                    yield
                    self.list[i], self.list[i + 1] = self.list[i + 1], self.list[i]
                    if bound == 1 and i == 0:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.in_place_item_colour,
                                                       font = ('normal', 0, 'normal'))
                    else:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.nonmoving_item_colour,
                                                       font = ('normal', 0, 'normal'))
                    if i + 1 == bound:
                        self.displayed_list.itemconfig(self.cells[i + 1], text = self.list[i + 1],
                                                       fill = self.in_place_item_colour,
                                                       font = ('normal', 0, 'normal'))
                    else:
                        self.displayed_list.itemconfig(self.cells[i + 1], text = self.list[i + 1],
                                                       fill = self.nonmoving_item_colour,
                                                       font = ('normal', 0, 'normal'))
                    swapped = True
                    new_bound = i
                    yield
                    if bound != 1 or i:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.live_item_colour)
                else:
                    self.displayed_list.itemconfig(self.cells[i], fill = self.nonmoving_item_colour,
                                                   font = ('normal', 0, 'bold'))
                    self.displayed_list.itemconfig(self.cells[i + 1], fill = self.nonmoving_item_colour,
                                                   font = ('normal', 0, 'bold'))
                    yield
                    self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[i + 1], font = ('normal', 0, 'normal'))
                    if i + 1 == bound:
                        for j in range(new_bound + 1, bound + 1):
                            self.displayed_list.itemconfig(self.cells[j],
                                                           fill = self.in_place_item_colour)
                        if new_bound == 0:
                            self.displayed_list.itemconfig(self.cells[0],
                                                           fill = self.in_place_item_colour)
                        yield
            bound = new_bound

    def trace_selection_sort(self):
        for i in range(self.length - 1):
            index_of_min = i
            self.displayed_list.itemconfig(self.cells[index_of_min], fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'bold'))
            for j in range(i + 1, self.length):
                self.displayed_list.itemconfig(self.cells[j], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                if self.list[j] < self.list[index_of_min]:
                    self.displayed_list.itemconfig(self.cells[index_of_min],
                                                   fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    index_of_min = j
                else:
                    self.displayed_list.itemconfig(self.cells[j], fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[index_of_min], font = ('normal', 0, 'normal'))
            if index_of_min != i:
                self.displayed_list.itemconfig(self.cells[index_of_min], fill = self.moving_item_colour)
                self.displayed_list.itemconfig(self.cells[i], fill = self.moving_item_colour)
                yield
                self.list[i], self.list[index_of_min] = self.list[index_of_min], self.list[i]
                self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                               fill = self.in_place_item_colour)
                if i == self.length - 2 or self.length == 2:
                    self.displayed_list.itemconfig(self.cells[index_of_min],
                                                   text = self.list[index_of_min],
                                                   fill = self.in_place_item_colour)
                    yield
                else:
                    self.displayed_list.itemconfig(self.cells[index_of_min],
                                                   text = self.list[index_of_min],
                                                   fill = self.nonmoving_item_colour)
                    yield
                    self.displayed_list.itemconfig(self.cells[index_of_min],
                                                   fill = self.live_item_colour)
            else:
                self.displayed_list.itemconfig(self.cells[index_of_min],
                                               fill = self.in_place_item_colour)
                if i == self.length - 2 or self.length == 2:
                    self.displayed_list.itemconfig(self.cells[i + 1], fill = self.in_place_item_colour)
                yield

    def trace_insertion_sort(self):
        for i in range(1, self.length):
            j = i
            while j and self.list[j - 1] > self.list[j]:
                self.displayed_list.itemconfig(self.cells[j - 1], fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[j], fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.list[j - 1], self.list[j] = self.list[j], self.list[j - 1]
                if j != 1 or i != self.length - 1:
                    self.displayed_list.itemconfig(self.cells[j - 1], text = self.list[j - 1],
                                                   fill = self.nonmoving_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[j], text = self.list[j],
                                                   fill = self.nonmoving_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    yield
                    self.displayed_list.itemconfig(self.cells[j], fill = self.live_item_colour)
                else:
                    self.displayed_list.itemconfig(self.cells[j - 1], text = self.list[j - 1],
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[j], text = self.list[j],
                                                   font = ('normal', 0, 'normal'))
                j -= 1
            if j:
                self.displayed_list.itemconfig(self.cells[j - 1], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[j], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[j - 1], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
                self.displayed_list.itemconfig(self.cells[j], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
            elif i == self.length - 1:
                for i in range(self.length):
                    self.displayed_list.itemconfig(self.cells[i], fill = self.in_place_item_colour)
                yield
                return
            else:
                self.displayed_list.itemconfig(self.cells[j], fill = self.live_item_colour)
        for i in range(self.length):
            self.displayed_list.itemconfig(self.cells[i], fill = self.in_place_item_colour)
        yield

    def trace_shell_sort(self):
        for n in range(self.length // 2, 0, -1):
            # We use Pratt's method which uses as gaps all numbers of the form 2^i * 3^j
            p = n
            while p % 2 == 0:
                p //= 2
            while p % 3 == 0:
                p //= 3
            if p != 1:
                continue
            for i in range(n, 2 * n):
                for j in range(i, self.length, n):
                    k = j
                    while k >= n and self.list[k - n] > self.list[k]:
                        self.displayed_list.itemconfig(self.cells[k - n],
                                                       fill = self.moving_item_colour,
                                                       font = ('normal', 0, 'bold'))
                        self.displayed_list.itemconfig(self.cells[k], fill = self.moving_item_colour,
                                                       font = ('normal', 0, 'bold'))
                        yield
                        self.list[k - n], self.list[k] = self.list[k], self.list[k - n]
                        if n != 1 or k != n or j != self.length - n:
                            self.displayed_list.itemconfig(self.cells[k - n], text = self.list[k - n],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[k], text = self.list[k],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                            self.displayed_list.itemconfig(self.cells[k], fill = self.live_item_colour)
                        else:
                            self.displayed_list.itemconfig(self.cells[k - n], text = self.list[k - n],
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[k], text = self.list[k],
                                                           font = ('normal', 0, 'normal'))
                        k -= n
                    if k - n >= 0:
                        self.displayed_list.itemconfig(self.cells[k - n],
                                                       fill = self.nonmoving_item_colour,
                                                       font = ('normal', 0, 'bold'))
                        self.displayed_list.itemconfig(self.cells[k], fill = self.nonmoving_item_colour,
                                                       font = ('normal', 0, 'bold'))
                        yield
                        self.displayed_list.itemconfig(self.cells[k - n], fill = self.live_item_colour,
                                                       font = ('normal', 0, 'normal'))
                        self.displayed_list.itemconfig(self.cells[k], fill = self.live_item_colour,
                                                       font = ('normal', 0, 'normal'))
                    elif n == 1 and j == self.length - n:
                        for i in range(self.length):
                            self.displayed_list.itemconfig(self.cells[i],
                                                           fill = self.in_place_item_colour)
                        yield
                        return
                    else:
                        self.displayed_list.itemconfig(self.cells[k], fill = self.live_item_colour)
        for i in range(self.length):
            self.displayed_list.itemconfig(self.cells[i], fill = self.in_place_item_colour)
        yield

    def trace_merge_sort(self):
        for i in range(self.length):
            self.displayed_list.itemconfig(self.cells[i], fill = 'black')
            self.displayed_extra_list.itemconfig(self.extra_cells[i], fill = 'black')
        for step in self.trace_mergesort(self.list, self.extra_list, 0, self.length, 0):
            yield step

    def trace_mergesort(self, L1, L2, start, end, depth):
        if end == start:
            return
        if end == start + 1:
            if depth == 0:
                self.displayed_list.itemconfig(self.cells[start], fill = self.in_place_item_colour)
                yield
            else:
                self.displayed_list.itemconfig(self.cells[start], fill = self.live_item_colour)
                self.displayed_extra_list.itemconfig(self.extra_cells[start],
                                                     fill = self.live_item_colour)
                yield
                self.displayed_list.itemconfig(self.cells[start], fill = 'black')
                self.displayed_extra_list.itemconfig(self.extra_cells[start], fill = 'black')
            return
        half_length = start + (end - start) // 2
        yield from self.trace_mergesort(L2, L1, start, half_length, depth + 1)
        yield from self.trace_mergesort(L2, L1, half_length, end, depth + 1)
        for i in range(start, end):
            self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
            self.displayed_extra_list.itemconfig(self.extra_cells[i], fill = self.live_item_colour)
        yield
        i = start
        i1 = start
        i2 = half_length
        while i1 < half_length and i2 < end:
            if depth % 2:
                self.displayed_list.itemconfig(self.cells[i1], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[i2], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
            else:
                self.displayed_extra_list.itemconfig(self.extra_cells[i1],
                                                     fill = self.nonmoving_item_colour,
                                                     font = ('normal', 0, 'bold'))
                self.displayed_extra_list.itemconfig(self.extra_cells[i2],
                                                     fill = self.nonmoving_item_colour,
                                                     font = ('normal', 0, 'bold'))
                yield
            if L2[i1] <= L2[i2]:
                if depth % 2:
                    self.displayed_list.itemconfig(self.cells[i1], fill = self.moving_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[i2], fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_extra_list.itemconfig(self.extra_cells[i], text = '*')
                    yield
                    L1[i] = L2[i1]
                    self.displayed_list.itemconfig(self.cells[i1], fill = self.live_item_colour)
                    self.displayed_extra_list.itemconfig(self.extra_cells[i], text = self.extra_list[i],
                                                         fill = self.nonmoving_item_colour)
                    yield
                    self.displayed_extra_list.itemconfig(self.extra_cells[i],
                                                         fill = self.live_item_colour)
                else:
                    self.displayed_extra_list.itemconfig(self.extra_cells[i1],
                                                         fill = self.moving_item_colour,
                                                         font = ('normal', 0, 'normal'))
                    self.displayed_extra_list.itemconfig(self.extra_cells[i2],
                                                         fill = self.live_item_colour,
                                                         font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[i], text = '*')
                    yield
                    L1[i] = L2[i1]
                    self.displayed_extra_list.itemconfig(self.extra_cells[i1],
                                                         fill = self.live_item_colour)
                    if depth:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.nonmoving_item_colour)
                    else:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.in_place_item_colour)
                    yield
                    if depth:
                        self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
                i1 += 1
            else:
                if depth % 2:
                    self.displayed_list.itemconfig(self.cells[i1], fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[i2], fill = self.moving_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    self.displayed_extra_list.itemconfig(self.extra_cells[i], text = '*')
                    yield
                    L1[i] = L2[i2]
                    self.displayed_list.itemconfig(self.cells[i2], fill = self.live_item_colour)
                    self.displayed_extra_list.itemconfig(self.extra_cells[i], text = self.extra_list[i],
                                                         fill = self.nonmoving_item_colour)
                    yield
                    self.displayed_extra_list.itemconfig(self.extra_cells[i],
                                                         fill = self.live_item_colour)
                else:
                    self.displayed_extra_list.itemconfig(self.extra_cells[i1],
                                                         fill = self.live_item_colour,
                                                         font = ('normal', 0, 'normal'))
                    self.displayed_extra_list.itemconfig(self.extra_cells[i2],
                                                         fill = self.moving_item_colour,
                                                         font = ('normal', 0, 'normal'))
                    self.displayed_list.itemconfig(self.cells[i], text = '*')
                    yield
                    L1[i] = L2[i2]
                    self.displayed_extra_list.itemconfig(self.extra_cells[i2],
                                                         fill = self.live_item_colour)
                    if depth:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.nonmoving_item_colour)
                    else:
                        self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                       fill = self.in_place_item_colour)
                    yield
                    if depth:
                        self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
                i2 += 1
            i += 1
        while i1 < half_length:
            if depth % 2:
                self.displayed_list.itemconfig(self.cells[i1], fill = self.moving_item_colour)
                self.displayed_extra_list.itemconfig(self.extra_cells[i], text = '*')
                yield
                L1[i] = L2[i1]
                self.displayed_list.itemconfig(self.cells[i1], fill = self.live_item_colour)
                self.displayed_extra_list.itemconfig(self.extra_cells[i], text = self.extra_list[i],
                                                     fill = self.nonmoving_item_colour)
                yield
                self.displayed_extra_list.itemconfig(self.extra_cells[i], fill = self.live_item_colour)
            else:
                self.displayed_extra_list.itemconfig(self.extra_cells[i1],
                                                     fill = self.moving_item_colour)
                self.displayed_list.itemconfig(self.cells[i], text = '*')
                yield
                L1[i] = L2[i1]
                self.displayed_extra_list.itemconfig(self.extra_cells[i1], fill = self.live_item_colour)
                if depth:
                    self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                   fill = self.nonmoving_item_colour)
                else:
                    self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                   fill = self.in_place_item_colour)
                yield
                if depth:
                    self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
            i1 += 1
            i += 1
        while i2 < end:
            if depth % 2:
                self.displayed_list.itemconfig(self.cells[i2], fill = self.moving_item_colour)
                self.displayed_extra_list.itemconfig(self.extra_cells[i], text = '*')
                yield
                L1[i] = L2[i2]
                self.displayed_list.itemconfig(self.cells[i2], fill = self.live_item_colour)
                self.displayed_extra_list.itemconfig(self.extra_cells[i], text = self.extra_list[i],
                                                     fill = self.nonmoving_item_colour)
                yield
                self.displayed_extra_list.itemconfig(self.extra_cells[i], fill = self.live_item_colour)
            else:
                self.displayed_extra_list.itemconfig(self.extra_cells[i2],
                                                     fill = self.moving_item_colour)
                self.displayed_list.itemconfig(self.cells[i], text = '*')
                yield
                L1[i] = L2[i2]
                self.displayed_extra_list.itemconfig(self.extra_cells[i2], fill = self.live_item_colour)
                if depth:
                    self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                   fill = self.nonmoving_item_colour)
                else:
                    self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                                   fill = self.in_place_item_colour)
                yield
                if depth:
                    self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
            i2 += 1
            i += 1
        if depth:
            for i in range(start, end):
                self.displayed_list.itemconfig(self.cells[i], fill = 'black')
                self.displayed_extra_list.itemconfig(self.extra_cells[i], fill = 'black')

    def trace_quick_sort(self):
        yield from self._trace_quick_sort(0, self.length - 1)

    def _trace_quick_sort(self, start, last):
        if last < start:
            return
        if last == start:
            self.displayed_list.itemconfig(self.cells[start], fill = self.in_place_item_colour)
            yield
            return
        for i in range(start, last + 1):
            self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
        split_point_container = [None]
        yield from self.trace_partition(start, last, split_point_container)
        if split_point_container[0] != start:
            for i in range(start, split_point_container[0]):
                self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
            for i in range(split_point_container[0] + 1, last + 1):
                self.displayed_list.itemconfig(self.cells[i], fill = 'black')
            yield
        else:
            for i in range(start, split_point_container[0]):
                self.displayed_list.itemconfig(self.cells[i], fill = 'black')
        for i in range(split_point_container[0] + 1, last + 1):
            self.displayed_list.itemconfig(self.cells[i], fill = 'black')
        yield from self._trace_quick_sort(start, split_point_container[0] - 1)
        if start < split_point_container[0] < last:
            for i in range(split_point_container[0] + 1, last + 1):
                self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
            yield
        yield from self._trace_quick_sort(split_point_container[0] + 1, last)

    def trace_partition(self, start, end, split_point_container):
        pivot_value = self.list[start]
        left_mark = start + 1
        right_mark = end
        while True:
            self.displayed_list.itemconfig(self.cells[start], fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'bold'))
            while left_mark <=  right_mark and self.list[left_mark] <= pivot_value:
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
                left_mark += 1
            if left_mark <= right_mark:
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
            while right_mark >  left_mark and self.list[right_mark] >= pivot_value:
                self.displayed_list.itemconfig(self.cells[right_mark],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[right_mark], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
                right_mark -= 1
            if right_mark >  left_mark:
                self.displayed_list.itemconfig(self.cells[right_mark],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[right_mark],
                                               fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
            else:
                break
            self.displayed_list.itemconfig(self.cells[start], fill = self.live_item_colour,
                                           font = ('normal', 0, 'normal'))
            if left_mark != right_mark:
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.moving_item_colour)
                self.displayed_list.itemconfig(self.cells[right_mark], fill = self.moving_item_colour)
                yield
                self.list[left_mark], self.list[right_mark] = (self.list[right_mark],
                                                                                   self.list[left_mark])
                self.displayed_list.itemconfig(self.cells[left_mark], text = self.list[left_mark],
                                               fill = self.nonmoving_item_colour)
                self.displayed_list.itemconfig(self.cells[right_mark], text = self.list[right_mark],
                                               fill = self.nonmoving_item_colour)
                yield
                self.displayed_list.itemconfig(self.cells[left_mark], fill = self.live_item_colour)
                self.displayed_list.itemconfig(self.cells[right_mark], fill = self.live_item_colour)
                left_mark += 1
                right_mark -= 1
        if left_mark == right_mark:
            right_mark -= 1
        if right_mark > start:
            self.displayed_list.itemconfig(self.cells[start], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[right_mark], fill = self.moving_item_colour)
            yield
            self.list[start], self.list[right_mark] = self.list[right_mark], self.list[start]
            self.displayed_list.itemconfig(self.cells[start], text = self.list[start],
                                           fill = self.nonmoving_item_colour)
            self.displayed_list.itemconfig(self.cells[right_mark], text = self.list[right_mark],
                                           fill = self.in_place_item_colour)
            yield
        else:
            self.displayed_list.itemconfig(self.cells[start], fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            yield
        split_point_container[0] = right_mark

    def trace_heap_sort(self):
        for i in range(self.length // 2 - 1, -1, -1):
            yield from self.trace_bubble_down(i, self.length)
        for i in range(self.length - 1, 2, -1):
            self.displayed_list.itemconfig(self.cells[0], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            self.displayed_list.itemconfig(self.cells[i], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            yield
            self.list[0], self.list[i] = self.list[i], self.list[0]
            self.displayed_list.itemconfig(self.cells[0], text = self.list[0],
                                           fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                           fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            yield
            self.displayed_list.itemconfig(self.cells[0], fill = self.live_item_colour)
            if i > 2:
                yield from self.trace_bubble_down(0, i)
        if self.length > 2:
            self.displayed_list.itemconfig(self.cells[0], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            self.displayed_list.itemconfig(self.cells[2], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            yield
            self.list[0], self.list[2] = self.list[2], self.list[0]
            self.displayed_list.itemconfig(self.cells[0], text = self.list[0],
                                           fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[2], text = self.list[2],
                                           fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            yield
        if self.list[0] > self.list[1]:
            self.displayed_list.itemconfig(self.cells[0], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            self.displayed_list.itemconfig(self.cells[1], fill = self.moving_item_colour,
                                           font = ('normal', 0, 'bold'))
            yield
            self.list[0], self.list[1] = self.list[1], self.list[0]
            self.displayed_list.itemconfig(self.cells[0], text = self.list[0],
                                           fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[1], text = self.list[1],
                                           fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            yield
        else:
            self.displayed_list.itemconfig(self.cells[0], fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'bold'))
            self.displayed_list.itemconfig(self.cells[1], fill = self.nonmoving_item_colour,
                                           font = ('normal', 0, 'bold'))
            yield
            self.displayed_list.itemconfig(self.cells[0], fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            self.displayed_list.itemconfig(self.cells[1], fill = self.in_place_item_colour,
                                           font = ('normal', 0, 'normal'))
            yield

    def trace_bubble_down(self, i, length):
        while True:
            index_of_greatest_child = 2 * i + 1
            if index_of_greatest_child >= length:
                break
            if index_of_greatest_child < length - 1:
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child + 1],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                if self.list[index_of_greatest_child] < self.list[index_of_greatest_child + 1]:
                    self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                                   fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
                    index_of_greatest_child = index_of_greatest_child + 1
                else:
                    self.displayed_list.itemconfig(self.cells[index_of_greatest_child + 1],
                                                   fill = self.live_item_colour,
                                                   font = ('normal', 0, 'normal'))
            if self.list[i] >= self.list[index_of_greatest_child]:
                self.displayed_list.itemconfig(self.cells[i], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               fill = self.live_item_colour,
                                               font = ('normal', 0, 'normal'))
                break
            else:
                self.displayed_list.itemconfig(self.cells[i], fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.list[i], self.list[index_of_greatest_child] = (self.list[index_of_greatest_child],
                                                                                           self.list[i])
                self.displayed_list.itemconfig(self.cells[i], text = self.list[i],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'normal'))
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               text = self.list[index_of_greatest_child],
                                               fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'normal'))
                yield
                self.displayed_list.itemconfig(self.cells[i], fill = self.live_item_colour)
                self.displayed_list.itemconfig(self.cells[index_of_greatest_child],
                                               fill = self.live_item_colour)
            i = index_of_greatest_child

    def trace_batcher_sort(self):
        if self.length == 2:
            if self.list[0] > self.list[1]:
                self.displayed_list.itemconfig(self.cells[0], fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[1], fill = self.moving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.list[0], self.list[1] = self.list[1], self.list[0]
                self.displayed_list.itemconfig(self.cells[0], text = self.list[0],
                                               fill = self.in_place_item_colour,
                                               font = ('normal', 0, 'normal'))
                self.displayed_list.itemconfig(self.cells[1], text = self.list[1],
                                               fill = self.in_place_item_colour,
                                               font = ('normal', 0, 'normal'))
                yield
                return
            else:
                self.displayed_list.itemconfig(self.cells[0], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                self.displayed_list.itemconfig(self.cells[1], fill = self.nonmoving_item_colour,
                                               font = ('normal', 0, 'bold'))
                yield
                self.displayed_list.itemconfig(self.cells[0], fill = self.in_place_item_colour,
                                               font = ('normal', 0, 'normal'))
                self.displayed_list.itemconfig(self.cells[1], fill = self.in_place_item_colour,
                                               font = ('normal', 0, 'normal'))
                yield
                return
        half_size, size = 1, 2
        while half_size < self.length:
            for group in range(self.length // size):
                top = group * size
                for i in range(half_size):
                    if self.list[top + i] > self.list[top + i + half_size]:
                        if half_size * 2 == self.length and top == 0 and i == 0:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.list[top + i], self.list[top + i + half_size] = (
                                                     self.list[top + i + half_size], self.list[top + i])
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           text = self.list[top + i],
                                                           fill = self.in_place_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           text = self.list[top + i + half_size],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.live_item_colour)
                        elif half_size * 2 == self.length and top == 0 and i + 1 == half_size:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.list[top + i], self.list[top + i + half_size] = (
                                                     self.list[top + i + half_size], self.list[top + i])
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           text = self.list[top + i],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           text = self.list[top + i + half_size],
                                                           fill = self.in_place_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.live_item_colour)
                        else:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.list[top + i], self.list[top + i + half_size] = (
                                                     self.list[top + i + half_size], self.list[top + i])
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           text = self.list[top + i],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           text = self.list[top + i + half_size],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.live_item_colour)
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.live_item_colour)
                    else:
                        if half_size * 2 == self.length and top == 0 and i == 0:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.in_place_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.live_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                        elif half_size * 2 == self.length and top == 0 and i + 1 == half_size:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.live_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.in_place_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            yield
                        else:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.nonmoving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.live_item_colour,
                                                           font = ('normal', 0, 'normal'))
                            self.displayed_list.itemconfig(self.cells[top + i + half_size],
                                                           fill = self.live_item_colour,
                                                           font = ('normal', 0, 'normal'))
            span, double_span = half_size // 2, half_size
            while span:
                skip = half_size // span
                for group in range(self.length // double_span):
                    if (group + 1) % skip == 0:
                        continue
                    top = span + group * double_span;
                    for i in range(span):
                        if self.list[top + i] > self.list[top + i + span]:
                            self.displayed_list.itemconfig(self.cells[top + i],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            self.displayed_list.itemconfig(self.cells[top + i + span],
                                                           fill = self.moving_item_colour,
                                                           font = ('normal', 0, 'bold'))
                            yield
                            self.list[top + i], self.list[top + i + span] = (self.list[top + i + span],
                                                                                     self.list[top + i])
                            if half_size * 2 == self.length and span == 1:
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               text = self.list[top + i],
                                                               fill = self.in_place_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               text = self.list[top + i + span],
                                                               fill = self.in_place_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                yield
                            else:
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               text = self.list[top + i],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               text = self.list[top + i + span],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                yield
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               fill = self.live_item_colour)
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               fill = self.live_item_colour)
                        else:
                            if half_size * 2 == self.length and span == 1:
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'bold'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'bold'))
                                yield
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               fill = self.in_place_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               fill = self.in_place_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                yield
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               font = ('normal', 0, 'normal'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               font = ('normal', 0, 'normal'))
                            else:
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'bold'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               fill = self.nonmoving_item_colour,
                                                               font = ('normal', 0, 'bold'))
                                yield
                                self.displayed_list.itemconfig(self.cells[top + i],
                                                               fill = self.live_item_colour,
                                                               font = ('normal', 0, 'normal'))
                                self.displayed_list.itemconfig(self.cells[top + i + span],
                                                               fill = self.live_item_colour,
                                                               font = ('normal', 0, 'normal'))
                span //= 2
                double_span //= 2
            half_size *= 2
            size *= 2


if __name__ == '__main__':
    SortingExperimenter().mainloop()
