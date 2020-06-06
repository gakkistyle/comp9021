# COMP9021 Practice 6 - Solutions


'''
Given a positive integer n, a magic square of order n is a matrix of size n x n
that stores all numbers from 1 up to n^2 and such that the sum of the n rows,
the sum of the n columns, and the sum of the two diagonals is constant,
hence equal to n(n^2+1)/2.
'''


from itertools import count


def is_magic_square(square):
    '''
    Checks whether a list of lists is a magic square.
    '''
    n = len(square)
    if any(len(line) != n for line in square):
        return False
    if {number for line in square for number in line} != set(range(1, n ** 2 + 1)):
        return False
    the_sum = n * (n ** 2 + 1) // 2
    if not_good_lines(square, the_sum):
        return False
    if not_good_lines([[square[i][j] for i in range(n)] for j in range(n)], the_sum):
        return False
    if sum(square[i][i] for i in range(n)) != the_sum:
        return False
    if sum(square[i][n - 1 - i] for i in range(n)) != the_sum:
        return False
    return True

def not_good_lines(square, the_sum):
    return any(sum(line) != the_sum for line in square)

def print_square(square):
    '''
    Prints out a magic square.
    '''
    field_width = len(str(len(square) ** 2))
    for line in square:
        print(' '.join(f'{number:{field_width}d}' for number in line))

def bachet_magic_square(n):
    '''
    Given an odd positive integer n, returns a magic square of order n thanks to
    the Bachet method, now described for n = 7.
    
    - Start with a square of size 2n-1 x 2n-1 filled as follows:
     .  .  .  .  .  .  1  .  .  .  .  .  .
     .  .  .  .  .  8  .  2  .  .  .  .  .
     .  .  .  . 15  .  9  .  3  .  .  .  .
     .  .  . 22  . 16  . 10  .  4  .  .  .
     .  . 29  . 23  . 17  . 11  .  5  .  .
     . 36  . 30  . 24  . 18  . 12  .  6  .
    43  . 37  . 31  . 25  . 19  . 13  .  7
     . 44  . 38  . 32  . 26  . 20  . 14  .
     .  . 45  . 39  . 33  . 27  . 21  .  .
     .  .  . 46  . 40  . 34  . 28  .  .  .
     .  .  .  . 47  . 41  . 35  .  .  .  .
     .  .  .  .  . 48  . 42  .  .  .  .  .
     .  .  .  .  .  . 49  .  .  .  .  .  .

    - Then 4 times:
      * Shift the n // 2 top rows n rows below:
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  . 22  . 16  . 10  .  4  .  .  .
     .  . 29  . 23  . 17  . 11  .  5  .  .
     . 36  . 30  . 24  . 18  . 12  .  6  .
    43  . 37  . 31  . 25  . 19  . 13  .  7
     . 44  . 38  . 32  1 26  . 20  . 14  .
     .  . 45  . 39  8 33  2 27  . 21  .  .
     .  .  . 46 15 40  9 34  3 28  .  .  .
     .  .  .  . 47  . 41  . 35  .  .  .  .
     .  .  .  .  . 48  . 42  .  .  .  .  .
     .  .  .  .  .  . 49  .  .  .  .  .  .
      * Rotate clockwise by 90 degrees:
     .  .  .  .  .  . 43  .  .  .  .  .  .
     .  .  .  .  . 44  . 36  .  .  .  .  .
     .  .  .  . 45  . 37  . 29  .  .  .  .
     .  .  . 46  . 38  . 30  . 22  .  .  .
     .  . 47 15 39  . 31  . 23  .  .  .  .
     . 48  . 40  8 32  . 24  . 16  .  .  .
    49  . 41  9 33  1 25  . 17  .  .  .  .
     . 42  . 34  2 26  . 18  . 10  .  .  .
     .  . 35  3 27  . 19  . 11  .  .  .  .
     .  .  . 28  . 20  . 12  .  4  .  .  .
     .  .  .  . 21  . 13  .  5  .  .  .  .
     .  .  .  .  . 14  .  6  .  .  .  .  .
     .  .  .  .  .  .  7  .  .  .  .  .  .

    Eventually, one reads the magic square off the centre:
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  . 22 47 16 41 10 35  4  .  .  .
     .  .  .  5 23 48 17 42 11 29  .  .  .
     .  .  . 30  6 24 49 18 36 12  .  .  .
     .  .  . 13 31  7 25 43 19 37  .  .  .
     .  .  . 38 14 32  1 26 44 20  .  .  .
     .  .  . 21 39  8 33  2 27 45  .  .  .
     .  .  . 46 15 40  9 34  3 28  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
     .  .  .  .  .  .  .  .  .  .  .  .  .
      
    '''
    if n % 2 == 0:
        return
    N = 2 * n - 1
    square = [[None] * N for _ in range(N)]
    k = count(1)
    for i in range(n):
        for j in range(n):
            square[i + j][j + n - i - 1] = next(k)
    s = (n - 1) // 2
    for _ in range(4):
        for i in range(s):
            for j in range(n - i - 1, n + i, 2):
                square[i + n][j] = square[i][j]
        square = [[square[N - 1 - i][j] for i in range(N)] for j in range(N)]
    return [line[s: s + n] for line in square[s: s + n]]

def siamese_magic_square(n):
    '''
    Given an odd positive integer n, returns a magic square of order n thanks to
    the Siamese method, that starts with 1 put at the centre of the first row,
    and having placed number k < n^2, places number k+1 by moving diagonally up and right
    by one cell, wrapping around when needed (as if a torus was made out of the square),
    unless that cell is already occupied, in which case k+1 is placed below the cell
    where k is (with no need to wrap around).

    For instance, for n = 7, one obtains:
    30 39 48  1 10 19 28
    38 47  7  9 18 27 29
    46  6  8 17 26 35 37
     5 14 16 25 34 36 45
    13 15 24 33 42 44  4
    21 23 32 41 43  3 12
    22 31 40 49  2 11 20
    '''
    if n % 2 == 0:
        return
    square = [[None] * n for _ in range(n)]
    k = count(1)
    i, j = 0, n // 2
    square[i][j] = next(k)
    for _ in range(n ** 2 - 1):
        i1, j1 = (i - 1) % n, (j + 1) % n
        i, j = (i + 1, j) if square[i1][j1] else (i1, j1)
        square[i][j] = next(k)
    return square

def lux_magic_square(n):
    '''
    Given a positive integer n of the form 4*k + 2 with k a strictly positive integer,
    returns a magic square of order n thanks to the LUX method, which proceeds as follows.
    Consider a matrix of size 2k+1 x 2k+1 that consists of:
    - k+1 rows of Ls,
    - 1 row of Us, and
    - k-1 rows of Xs,
    and then exchange the U in the middle with the L above it.
    For instance, when n = 10, that matrix is:
    L  L  L  L  L
    L  L  L  L  L
    L  L  U  L  L
    U  U  L  U  U
    X  X  X  X  X
    Explore all cells of this matrix as for the Siamese method, that is, starting at the cell
    at the centre of the first row, and then by moving diagonally up and right by one cell,
    wrapping around when needed (as if a torus was made out of the matrix), unless that cell
    has been visited already, in which case one moves down one cell (with no need to wrap around).
    The contents of every visited cell is then replaced by
    - i+4 i+1
      i+2 i+3
      if the cell contains L
    - i+1 i+4
      i+2 i+3
      if the cell contains U
    - i+1 i+4
      i+3 i+2
      if the cell contains X
    with i being the last number that has been used (starting with i = 0).
    
    For instance, for n = 10, one obtains:
     68  65  96  93   4   1  32  29  60  57
     66  67  94  95   2   3  30  31  58  59
     92  89  20  17  28  25  56  53  64  61
     90  91  18  19  26  27  54  55  62  63
     13  16  21  24  49  52  77  80  85  88
     15  14  23  22  51  50  79  78  87  86
     37  40  45  48  73  76  81  84   9  12
     39  38  47  46  75  74  83  82  11  10
     41  44  69  72  97 100   5   8  33  36
     43  42  71  70  99  98   7   6  35  34

    '''
    if n < 6 or n % 4 != 2:
        return
    k = count(1)
    square = [[None] * n for _ in range(n)]
    def process_U_cell():
        square[2 * i][2 * j] = next(k)
        square[2 * i + 1][2 * j] = next(k)
        square[2 * i + 1][2 * j + 1] = next(k)
        square[2 * i][2 * j + 1] = next(k)
    def process_L_cell():
        square[2 * i][2 * j + 1] = next(k)
        square[2 * i + 1][2 * j] = next(k)
        square[2 * i + 1][2 * j + 1] = next(k)
        square[2 * i][2 * j] = next(k)
    def process_X_cell():
        square[2 * i][2 * j] = next(k)
        square[2 * i + 1][2 * j + 1] = next(k)
        square[2 * i + 1][2 * j] = next(k)
        square[2 * i][2 * j + 1] = next(k)
    N = n // 2
    patterns = {(i, j): process_L_cell for i in range(N // 2 + 1) for j in range(N)}
    patterns.update(((N // 2 + 1, j), process_U_cell) for j in range(N))
    patterns.update(((i, j), process_X_cell) for i in range(N // 2 + 2, N) for j in range(N))
    patterns[N // 2, N // 2], patterns[N // 2 + 1, N // 2] = patterns[N // 2 + 1, N // 2],\
                                                                            patterns[N // 2, N // 2]
    i, j = 0, N // 2
    patterns[i, j]()
    for _ in range(N ** 2 - 1):
        i1, j1 = (i - 1) % N, (j + 1) % N
        i, j = (i + 1, j) if square[2 * i1][2 * j1] else (i1, j1)
        patterns[i, j]()
    return square
