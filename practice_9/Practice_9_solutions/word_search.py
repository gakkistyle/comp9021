# COMP9021 Practice 9 - Solutions


from collections import defaultdict


class WordSearch:
    '''
    Records the contents of a file that contains n lines with m letters for some n and m,
    possibly with spaces between the letters and possibly with blank lines.
    Such a contents is intended to be the grid of a word search game: words are given that
    have to be found in the grid, being read horizontally, vertically or diagonally, in
    either direction.
    '''
    def __init__(self, filename):
        with open(filename) as file:
            self.grid = [''.join(c for c in line if not c.isspace())
                                                              for line in file if not line.isspace()
                        ]
        self.x_dim = len(self.grid[0])
        self.y_dim = len(self.grid)
        # The keys of self.rays are the letters that occur in the grid.
        # For such a letter c, the value of c in self.rays is a list of length
        # the number of occurrences of c in the grid; each member of the list
        # records the x and y coordinates of that occurrence of c
        # (the x-axis pointing East, the y-axis pointing South)
        # and for each of the 8 directions, the sequence of letters in the grid
        # that starts at that location and extends in that direction all the way
        # to the boundary of the grid.       
        self.rays = defaultdict(list)
        for y in range(self.y_dim):
            for x in range(self.x_dim):
                self.rays[self.grid[y][x]].append(((x, y), self._rays_per_direction(y, x)))

    def __str__(self):
        return '\n'.join(' '.join(c for c in line) for line in self.grid)

    def _rays_per_direction(self, y, x):
        return dict((('N', ''.join(self.grid[j][x] for j in range(y, -1, -1))),
                     ('NE', ''.join(self.grid[j][i]
                                           for (j, i) in zip(range(y, -1, -1), range(x, self.x_dim))
                                   )
                     ),
                     ('E', ''.join(self.grid[y][i] for i in range(x, self.x_dim))),
                     ('SE', ''.join(self.grid[j][i]
                                       for (j, i) in zip(range(y, self.y_dim), range(x, self.x_dim))
                                   )
                     ),
                     ('S', ''.join(self.grid[j][x] for j in range(y, self.y_dim))),
                     ('SW', ''.join(self.grid[j][i]
                                           for (j, i) in zip(range(y, self.y_dim), range(x, -1, -1))
                                   )
                     ),
                     ('W', ''.join(self.grid[y][i] for i in range(x, -1, -1))),
                     ('NW', ''.join(self.grid[j][i]
                                               for (j, i) in zip(range(y, -1, -1), range(x, -1, -1))
                                   )
                     )
                    )
                   )

    def locate_word_in_grid(self, word):
        '''
        Returns None if word cannot be read in the grid.
        Otherwise, returns the x and y coordinates of an occurrence
        of the first letter of word, and the direction to follow
        (N, NE, E, SE, S, SW, W or NW) to read the whole word from
        that point onwards.
        '''
        for ((x, y), rays) in self.rays[word[0]]:
            for direction in rays:
                if rays[direction].startswith(word):
                    return (x, y, direction)

    def locate_words_in_grid(self, *words):
        return dict((word, self.locate_word_in_grid(word)) for word in words)
            
    def display_word_in_grid(self, word):
        '''
        In case word can indeed be read from the grid,
        prints out the grid with all characters being displayed in lowercase,
        except for those that make up word, displayed in uppercase.
        '''
        grid = [[c.lower() for c in line] for line in self.grid]
        try:
            x, y, direction = self.locate_word_in_grid(word)
            if direction == 'N':
                for j in range(y, y - len(word), -1):
                    grid[j][x] = grid[j][x].upper()
            elif direction == 'NE':                
                for (j, i) in zip(range(y, y - len(word), -1), range(x, x + len(word))):
                    grid[j][i] = grid[j][i].upper()
            elif direction == 'E':
                for i in range(x, x + len(word)):
                    grid[y][i] = grid[y][i].upper()
            elif direction == 'SE':
                for (j, i) in zip(range(y, y + len(word)), range(x, x + len(word))):
                    grid[j][i] = grid[j][i].upper()
            elif direction == 'S':
                for j in range(y, y + len(word)):
                    grid[j][x] = grid[j][x].upper()
            elif direction == 'SW':
                for (j, i) in zip(range(y, y + len(word)), range(x, x - len(word), -1)):
                    grid[j][i] = grid[j][i].upper()
            elif direction == 'W':
                for i in range(x, x - len(word), -1):
                    grid[y][i] = grid[y][i].upper()
            elif direction == 'NW':
                for (j, i) in zip(range(y, y - len(word), -1), range(x, x - len(word), -1)):
                    grid[j][i] = grid[j][i].upper()
            print('\n'.join(' '.join(c for c in line) for line in grid))
        except TypeError:
            pass
        

if __name__ == '__main__':
    import pprint
    ws = WordSearch('word_search_1.txt')
    print('Testing with grid for metals')
    print()
    print(ws)
    print()
    metal = 'PLATINUM'
    print(f'{metal}: {ws.locate_word_in_grid(metal)}')
    metal = 'SODIUM'
    print(f'{metal}: {ws.locate_word_in_grid(metal)}')
    metals = ('PLATINUM', 'COPPER', 'MERCURY', 'TUNGSTEN', 'MAGNESIUM', 'ZINC', 'MANGANESE',
              'TITANIUM', 'TIN', 'IRON', 'LITHIUM', 'CADMIUM', 'GOLD', 'COBALT', 'SILVER',
              'NICKEL', 'LEAD', 'IRIDIUM', 'URANIUM', 'SODIUM')
    located_metals = ws.locate_words_in_grid(*metals)
    pprint.pprint(located_metals)
    print()    
    for metal in metals:
        print(metal, end = ':\n')
        ws.display_word_in_grid(metal)
        print()
    print()

    ws = WordSearch('word_search_2.txt')
    print('Testing with grid for fruits')
    print()
    print(ws)
    print()
    fruit = 'RASPBERRY'
    print(f'{fruit}: {ws.locate_word_in_grid(fruit)}')
    fruit = 'PEAR'
    print(f'{fruit}: {ws.locate_word_in_grid(fruit)}')
    fruits = ('RASPBERRY', 'LIME', 'BLACKBERRY', 'BLUEBERRY', 'WATERMELON', 'ORANGE',
              'BANANA', 'PAPAYA', 'LEMON', 'KIWI', 'GRAPE', 'APPLE', 'PEAR', 'MANGOE')
    located_fruits = ws.locate_words_in_grid(*fruits)
    pprint.pprint(located_fruits)
    print()    
    for fruit in fruits:
        print(fruit, end = ':\n')
        ws.display_word_in_grid(fruit)
        print()
