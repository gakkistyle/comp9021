# COMP9021 Practice 3 - Solutions


'''
Finds all triples of consecutive positive three-digit integers each of which
is the sum of two squares.
'''


def nb_of_consecutive_squares(n):
    if not sums_of_two_squares[n]:
        return 0
    if not sums_of_two_squares[n + 1]:
        return 1
    if not sums_of_two_squares[n + 2]:
        return 2
    return 3


# The smallest integer whose square is a 4-digit number.
upper_bound = 32
# For all n in [100, 999], if n is found to be of the form a^2 + b^2
# then sums_of_two_squares[n] will be set to (a, b) for the minimal
# such pair (a, b) w.r.t. the natural ordering of pairs of integers.
# Note that we waste the 100 first elements of the list;
# we can afford it and this choice makes the program simpler.
sums_of_two_squares = [None] * 1_000
for i in range(upper_bound):
    for j in range(i, upper_bound):
        n = i * i + j * j
        if n < 100:
            continue
        if n >= 1_000:
            break
        if not sums_of_two_squares[n]:
            sums_of_two_squares[n] = i, j
for n in range(100, 1_000):
    i = nb_of_consecutive_squares(n)
    if i < 3:
        # There is no potential triple before n + i + 1;
        # the loop will increment n by 1.
        n += i
        continue
    print(f'({n}, {n + 1}, {n + 2}) '
          f'(equal to ({sums_of_two_squares[n][0]}^2+{sums_of_two_squares[n][1]}^2, '
          f'{sums_of_two_squares[n + 1][0]}^2+{sums_of_two_squares[n + 1][1]}^2, '
          f'{sums_of_two_squares[n + 2][0]}^2+{sums_of_two_squares[n + 2][1]}^2)) '
          'is a solution.'
         )
    # We assume we could have two solutions of the form
    # (n, n + 1, n + 2) and (n + 1, n + 2, n + 3)
    # (but as the solution shows, this never happens...),
    # hence n is incremented by only 1 in the next iteration of the loop.
    # We could avoid checking that sums_of_two_squares[n + 1] and
    # sums_of_two_squares[n + 2] are not equal to 0, but why make the program
    # more complicated for no significant gain?

