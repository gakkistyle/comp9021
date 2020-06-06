# COMP9021 Practice 7 - Solutions


from random import choice, sample
from collections import defaultdict


class Target:
    '''
    Generates a target, that is, a 3 x 3 grid of distinct letters
    such that at least one 9-letter word is made from all letters in the target.
    The aim of the puzzle is to find words consisting of distinct letters all in the target,
    one of which has to be the letter at the centre of the target.

    To create a target object, three keyword only arguments can be provided:
    - dictionary, meant to be the file name of a dictionary storing all valid words,
      with a default value named dictionary.txt, for a default dictionary supposed to be stored
      in the working directory;
    - target, with a default value of None, otherwise meant to be a 9-letter string defining
      a valid target (in case it is not valid, it will be ignored and a random target will be
      generated as if that argument had not been provided);
    - minimal_length, for the minimal length of words to discover, with a default value of 4.
    '''
    def __init__(self, *, dictionary = 'dictionary.txt', target = None, minimal_length = 4):
        self.dictionary = dictionary
        self.minimal_length = minimal_length
        with open(self.dictionary) as lexicon:
            # A dictionary whose keys are all words consisting of distinct letters;
            # the value for a given key is the set of characters that occur in the key (word),
            # to avoid computing the latter from the former more than once,
            # which is useful only when change_target() is called.
            self.words = dict(filter(lambda x: len(x[0]) == len(x[1]), ((word, set(word))
                                                     for word in (line.rstrip() for line in lexicon)
                                                                       )
                                    )
                             )
        # A list of all sets of 9 characters from which a 9-letter word can be built.
        self.targets_letters = [self.words[word] for word in self.words if len(word) == 9]
        if target:
            self.target_letters = set(target)
            if len(target) == 9 and self.target_letters in self.targets_letters:
                self.target = target
            else:
                target = None
                print(f'{target} is not a valid target, a random one will be generated instead.')
        if not target:
            self.target_letters = choice(self.targets_letters)
            # A string made of the letters in self.target_letters in a random order.
            self.target = ''.join(sample(self.target_letters, 9))
        self.solutions = self._solve_target()

    def __str__(self):
        target = ''
        for i in range(9):
            if i % 3 == 0:
                target += f'\n       ___________\n\n      | {self.target[i]} |'
            else:
                target += f' {self.target[i]} |'
        target += '\n       ___________\n'
        return target

    def __repr__(self):
        return f'Target(dictionary = {self.dictionary}, minimal_length = {self.minimal_length})'
       
    def _solve_target(self):   
        solutions = defaultdict(list)
        for word in self.words:
            if (self.minimal_length <= len(word) and
                self.target[4] in self.words[word] and
                self.words[word] <= self.target_letters):
                solutions[len(word)].append(word)
        return solutions

    def number_of_solutions(self):
        print(f'In decreasing order of length between 9 and {self.minimal_length}:')
        for length in range(9, self.minimal_length - 1, -1):
            nb_of_solutions = len(self.solutions[length])
            if nb_of_solutions == 1:
                print(f'    1 solution of length {length}')
            elif nb_of_solutions > 1:
                print(f'    {nb_of_solutions} solutions of length {length}')
        
    def give_solutions(self, minimal_length = None):
        '''
        By default, all solutions are displayed, unless minimal_length is passed as an argument,
        in which case only solutions of length at least that value are displayed.
        '''
        if minimal_length is None:
            minimal_length = self.minimal_length
        for length in range(9, minimal_length - 1, -1):
            if not self.solutions[length]:
                continue
            if length != 9:
                print()
            if len(self.solutions[length]) == 1:
                print(f'Solution of length {length}:\n    {self.solutions[length][0]}')
            else:               
                print(f'Solutions of length {length}:')
                for solution in self.solutions[length]:
                    print(f'    {solution}')

    def change_target(self, to_be_replaced, to_replace):
        '''
        Both arguments are meant to be strings.
        The target will be modified if:
        - to_be_replaced and to_replace are different strings of the same length;
        - all letters in to_be_replaced are distinct and occur in the current target;
        - replacing each letter in to_be_replaced by the corresponding letter in to_replace
          yields a valid target.
        If those conditions are not satisfied then the method prints out a message indicating
        that the target was not changed.
        If the target was changed but consists of the same letters, and with the same letter
        at the centre, then the method prints out a message indicating that the solutions
        are not changed.
        '''
        if to_be_replaced != to_replace and len(to_be_replaced) == len(to_replace):
            letters_to_be_replaced = set(to_be_replaced)
            if letters_to_be_replaced <= self.target_letters:
                new_target_letters = self.target_letters - letters_to_be_replaced | set(to_replace)
                if new_target_letters in self.targets_letters:
                    old_target_letters = self.target_letters
                    old_letter_at_centre = self.target[4]
                    self.target_letters = new_target_letters
                    self.target = self.target.translate(str.maketrans(to_be_replaced, to_replace))
                    if self.target_letters != old_target_letters or\
                                                             self.target[4] != old_letter_at_centre:
                        self.solutions = self._solve_target()
                    else:
                        print('The solutions are not changed.')
                    return
        print('The target was not changed.')
