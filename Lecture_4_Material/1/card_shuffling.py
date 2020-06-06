# COMP9021 Term 3 2019


import tkinter as tk
from random import randrange


class CardShuffling(tk.Tk):
    background_colour = '#D3D3D3'
    deck_size = 52

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Card Shuffling Simulator')
        display = tk.Frame(self, bd=50)
        display.grid(column=7)
        # self. is necessary to avoid that the variable be garbage
        # collected after the class has been created.
        self.card_images = [None] * self.deck_size
        self.cards_to_display = [None] * self.deck_size
        for i in range(self.deck_size):
            self.card_images[i] = tk.PhotoImage(file='Cards/' + str(i + 1)
                                                     + '.gif'
                                               )
            self.cards_to_display[i] = tk.Canvas(
                                            display, width=74, height=100,
                                            background=self.background_colour
                                                )
        tk.Button(display, text='Reset', command=self.reset).grid(row=4,
                                                                  column=4,
                                                                  pady=40
                                                                 )
        tk.Button(display, text='Shuffle', command=self.shuffle).grid(row=4,
                                                                      column=8
                                                                     )
        tk.Label(display, text='Number of times the deck has been shuffled:'
                ).grid(row=5, column=5, columnspan=4)
        self.shuffles = 0
        self.nb_of_times_shuffled = tk.StringVar()
        self.nb_of_times_shuffled.set(0)
        tk.Label(display, width=2, height=1,
                 textvariable=self.nb_of_times_shuffled).grid(row=5, column=9)
        # deck[0] and deck[1] will alternatively play the roles of a
        # deck before and after shuffling, the latter being determined
        # from the former.
        self.deck = [list(range(self.deck_size)), [None] * 52]
        self.switch = True
        self.reset()

    def reset(self):
        deck = self.deck[self.switch]
        deck[: self.deck_size] = range(self.deck_size)
        self.shuffles = 0
        self.nb_of_times_shuffled.set(0)
        self.display_deck()

    def shuffle(self):
        # Binomial distribution to determine where to cut.
        # Flip a coin 52 times and let the number of heads and tails
        # (say, 0 and 1, respectively) determine the sizes of stack_1
        # and stack_2, respectively.
        cut = sum(randrange(2) for _ in range(self.deck_size))
        if cut == 0 or cut == self.deck_size:
            return
        deck_before = self.deck[self.switch]
        deck_after = self.deck[not self.switch]
        i = 0
        stack_1_i = 0
        stack_2_i = cut
        both_stacks_size = self.deck_size
        # The probability of letting the lower card from stack_1 rather
        # than the lower card from stack_2 join deck_after is given by
        # the size of stack_1 divided by the sum of the sizes of both
        # stacks; e.g.:
        # - 1/3 is the size of stack_1 is half the size of stack_2,
        # - 1/2 if both stacks are of equal size,
        # - 2/3 is the size of stack_1 is twice the size of stack_2.
        while stack_1_i < cut and stack_2_i < self.deck_size:
            which_stack = randrange(both_stacks_size)
            both_stacks_size -= 1
            if which_stack < cut - stack_1_i:
                deck_after[i] = deck_before[stack_1_i]
                stack_1_i += 1
            else:
                deck_after[i] = deck_before[stack_2_i]
                stack_2_i += 1
            i += 1
        # Only cards from stack_1 are left.
        if stack_1_i < cut:
            deck_after[i :] = deck_before[stack_1_i : cut]
        # Only cards from stack_2 are left.
        else:
            deck_after[i :] = deck_before[stack_2_i :]
        self.switch = not self.switch
        self.shuffles += 1
        self.nb_of_times_shuffled.set(self.shuffles)
        self.display_deck()

    def display_deck(self):
        deck = self.deck[self.switch]
        for i in range(self.deck_size):
            self.cards_to_display[i].delete(tk.ALL)
            # Ace to King of Hearts, then
            # Ace to King of Clubs, then
            # King to Ace of Diamonds, then
            # King to Ace of Spades.
            self.cards_to_display[i].create_image(
                               40, 53, image=self.card_images[deck[i]]
                                                 )
            self.cards_to_display[i].grid(row=i // 13, column=i % 13)


if __name__ == '__main__':
    CardShuffling().mainloop()