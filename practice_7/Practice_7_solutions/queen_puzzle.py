# COMP9021 Practice 7 - Solutions


'''
Solves the n-queen puzzle: place n chess queens on an n x n chessboard so that
no queen is attacked by any other queen.

We generate permutations of  [0, 1, ..., n-1],
a permutation [k_0, k_1, ..., k_{n-1}]
requesting to place the queen of the first row in the (k_0+1)-st column,
the queen of the second row in the (k_1+1)-nd column, etc.

We create an object for an n-queen puzzle thanks to which we can:
 - print out the number of tested permutations;
 - print out the number of solutions;
 - display a given solution.
'''


class QueenPuzzle:
    def __init__(self, board_size):
        self.board_size = board_size
        self.nb_of_solutions = 0
        self.nb_of_tested_permutations = 0
        self.skip_size = 0
        self.solutions = []
        self._solve_puzzle()

    def print_nb_of_solutions(self):
        print(self.nb_of_solutions)

    def print_nb_of_tested_permutations(self):
        print(self.nb_of_tested_permutations)


    def print_solution(self, n):
        for i in range(self.board_size):
            k = self.solutions[n]
            for j in range(self.board_size):
                print(f' {int(j == k)}', end = '')
            print()
        print()

    def _solve_puzzle(self):
        L = list(range(self.board_size))
        for L in self._heap_permute(L, self.board_size):
            self.nb_of_tested_permutations += 1
            # Starting from the penultimate row and making our way up
            # to the first row, we check whether the queen on that row
            # is not attacked by any queen on a lower row.
            for n in range(self.board_size - 2, -1, -1):
                good_permutation = True
                for i in range(n + 1, self.board_size):
                    if abs(L[i] - L[n]) == i - n:
                        if n > 1:
                            # We skip the permutations of the first n rows
                            # if the queen on the (n+1)st row is attacked
                            # by a queen on a lower row.
                            self.skip_size = n
                        good_permutation = False
                        break
                if not good_permutation:
                    break
            if good_permutation:
                self.nb_of_solutions += 1
                self.solutions.append(list(L))

    def _heap_permute(self, L, length):
        if length == 1:
            yield L
        else:
            length -= 1
            for i in range(length):
                for L in self._heap_permute(L, length):
                    yield L
                    if self.skip_size > length:
                        yield L
                        return
                    if self.skip_size == length:
                        self._skip_permutations(L, self.skip_size)
                        self.skip_size = 0
                        break
                if length % 2:
                    L[i], L[length] = L[length], L[i]
                else:
                    L[0], L[length] = L[length], L[0]
            for L in self._heap_permute(L, length):
                yield L
                if self.skip_size == length:
                    self._skip_permutations(L, self.skip_size)
                    self.skip_size = 0
                    return

    def _skip_permutations(self, L, skip_size):
        if skip_size % 2 or skip_size == 2:
           L[0], L[skip_size - 1] = L[skip_size - 1], L[0]
        elif skip_size == 4:
            L[: 3], L[3] = L[1: 4], L[0]
        else:
            L[: 2], L[2: skip_size - 2], L[skip_size - 2], L[skip_size - 1] = \
                L[skip_size - 3: skip_size - 1], L[1: skip_size - 3], L[skip_size - 1], L[0]
    
