# COMP9021 Term 3 2019


'''
Discovers all triples (a,b,c) of natural numbers such that:
- a < b < c;
- a, b and c are perfect squares;
- 0 occurs in none of a, b and c;
- every nonzero digit occurs exactly once in one of a, b and c.

Extracts digits using the % and // operators and encodes them as a
natural number.
'''


from math import sqrt
    

def digits_if_ok(number, digits_seen_before):
    while number:
        number, digit = divmod(number, 10)
        digits_seen_now = digits_seen_before | 1 << digit
        if digits_seen_now == digits_seen_before:
            return
        digits_seen_before = digits_seen_now
    return digits_seen_before


nb_of_solutions = 0
# A largest possible value for a is 997: otherwise, b would consist of at least
# 3 digits and c would consist of at least 4 digits, for a total of at least 10
# digits.
for i in range(1, int(sqrt(997)) + 1):
    a = i ** 2
    # a_digits_and_0 is not None iff all digits in a are distinct and not equal
    # to 0.
    a_digits_and_0 = digits_if_ok(a, 1)
    if not a_digits_and_0:
        continue
    # A largest possible value for b is 9998: otherwise, c would consist of at
    # least 5 digits and a takes at least one digit, for a total of at least 10
    # digits.
    for j in range(i + 1, int(sqrt(9998)) + 1):
        b = j ** 2
        # a_b_digits_and_0 is not None iff all digits in a are distinct,
        # distinct to 0, and distinct to all digits in a.
        a_b_digits_and_0 = digits_if_ok(b, a_digits_and_0)
        if not a_b_digits_and_0:
            continue
        # Since we need 3 perfect squares and use up each of the 9 nonzero
        # digits once and only once, c can consist of at most 7 digits, leaving
        # one digit to a and 1 digit to b. There are three 1-digit nonzero
        # perfect squares: 1, 4 and 9. So a largest possible value for c is
        # obtained by setting a to 1, b to 4, and c to 9876532.
        for k in range(j + 1, int(sqrt(9876532)) + 1):
            c = k ** 2
            a_b_c_digits_and_0 = digits_if_ok(c, a_b_digits_and_0)
            # a_b_c_digits_and_0 is not None iff all digits in c are distinct,
            # distinct to 0, and distinct to all digits in a and b.
            if not a_b_c_digits_and_0 or a_b_c_digits_and_0 != 2 ** 10 - 1:
                continue
            print(f'{a:7} {b:7} {c:7}')
            nb_of_solutions += 1
print('\nAltogether,', nb_of_solutions, 'solutions have been found.')
