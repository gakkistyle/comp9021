# COMP9021 Term 3 2019


'''
Vigenere cipher:
- Encryption
- Decryption
- Breaking key

Example for the key ABRACADABRA and the beginning of the text
"Alice's Adventures in Wonderland" by  Lewis Carroll (Charles Lutwidge
 Dodgson), writing ' for \', \ for \\, † for \t, and ® for \n:
0         1         2         3         4         5         6         
0123456789012345678901234567890123456789012345678901234567890123456789
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'(
ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ †®012345678
BCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ †®0123456789
CDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ †®0123456789a
DEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ †®0123456789ab
RSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ †®0123456789abcdefghijklmnop

                                             7         8         9
                                             012345678901234567890123456
                                             )*+,-./:;<=>?@[\]^_`{|}~ †®
                                             9abcdefghijklmnopqrstuvwxyz
                                             abcdefghijklmnopqrstuvwxyzA
                                             bcdefghijklmnopqrstuvwxyzAB
                                             cdefghijklmnopqrstuvwxyzABC
                                             qrstuvwxyzABCDEFGHIJKLMNOPQ

ABRACADABRA
Alice was b           +W*MQx*K$OL
eginning to           OR*XZS!Qy?Y
get very ti           xR&$z&R"*O$
red of sitt           S#&NzYSx$*$
ing by her            $T/QzL,xS&"
sister on t           x$*#&O%xZ/x
he bank, an           $S&xNK!UdOK
'''


from string import printable
from collections import Counter
from operator import itemgetter 
from itertools import product
from re import split


# From most frequent to least frequent letter in English
etaoin = {'etaoinshrdlcumwfgypbvkjxqz'[i]: i for i in range(26)}
# We eliminate from printable \r, \x0b (vertical tab) and \x0c
# (form feed)
characters = printable[: -3]
shifts = {characters[i]: i for i in range(len(characters))}
dictionary_file = 'dictionary.txt'
# Default parameters to try and break the key
max_key_length = 16
n_gram_range = range(3, 6)
etaoin_length = 6
nb_of_options_for_subkey = 2
fraction_of_letters = .7
fraction_of_words = .5


def encrypt_file(key, filename, encrypted_filename=None):
    try:
        with open(filename) as file:
            if encrypted_filename:
                with open(encrypted_filename, 'w') as encrypted_file:
                    print(encrypt(key, file.read()), end='',
                          file=encrypted_file
                         )
            else:
                return encrypt(key, file.read())
    except FileNotFoundError:
        print(f'Could not open {filename}, giving up.')


def decrypt_file(key, filename, decrypted_filename=None):
    try:
        with open(filename) as file:
            if decrypted_filename:
                try:
                    with open(decrypted_filename, 'x') as decrypted_file:
                        print(decrypt(key, file.read()), file=decrypted_file)
                except FileExistsError:
                    print(f'{decrypted_filename} exists, giving up.')
            else:
                return decrypt(key, file.read())
    except FileNotFoundError:
        print(f'Could not open {filename}, giving up.')


def break_key_for_file(filename):
    try:
        with open(filename) as file:
            break_key(file.read())
    except FileNotFoundError:
        print(f'Could not open {filename}, giving up.')


def encrypt(key, text):
    return encrypt_or_decrypt(key, text, 1)


def decrypt(key, text):
    return encrypt_or_decrypt(key, text, -1)


def encrypt_or_decrypt(key, text, mode):
    return ''.join(characters[(shifts[text[i]]
                               + shifts[key[i % len(key)]] * mode
                              ) % len(shifts)
                             ] for i in range(len(text))
                  )


def break_key(text):
    try:
        with open(dictionary_file) as file:
            dictionary = {w.strip().lower() for w in file}
    except FileNotFoundError:
        print(f'Could not open the file {dictionary_file}, giving up.')
        return
    for key_length in key_lengths_from_most_to_least_promising(text):
        print(f'\nNow working with keys of length {key_length}')
        # Each subkey will be assigned one of the
        # nb_of_options_for_subkey many characters  according to a
        # frequency analysis of that part of the text it encodes (more
        # precisely, the n-th subkey encodes every key_length-th
        # character in text, starting with the n-th character).
        subkeys = []
        for n in range(key_length):
            scores = []
            for subkey in characters:
                decrypted_column = decrypt(subkey, text[n :: key_length])
                # We prefer the subkeys with the highest etaoin scores.
                # When two subkeys have the same etaoin score, we prefer
                # the one with the highest proportion of lowercase
                # letters over all letters plus 1 (to avoid dividing by
                # 0).
                nb_of_lowercase_letters = 0
                nb_of_letters = 1
                letters = (c for c in decrypted_column if c.isalpha())
                for c in letters:
                    nb_of_letters += 1
                    if c.islower():
                        nb_of_lowercase_letters += 1
                scores.append((subkey,
                               etaoin_score(decrypted_column, etaoin_length),
                               nb_of_lowercase_letters / nb_of_letters
                              )
                             )
            scores.sort(key=itemgetter(1, 2), reverse=True)
            subkeys.append(x[0] for x in scores[: nb_of_options_for_subkey])
        for key in (''.join(subkey) for subkey in product(*subkeys)):
            print('\r', key, end='')
            decrypted_text = decrypt(key, text)
            if looks_like_English(decrypted_text, dictionary):
                print('\nWhat about this?\n')
                print(decrypted_text[: 200], '...', sep='')
                print()
                print('Enter Y[es] if happy, otherwise press any key '
                      "and I'll keep working."
                     )
                yes_or_no = input('> ')
                if yes_or_no in {'YES', 'Yes', 'yes', 'Y', 'y'}:
                    print(f'The key is: "{key}"')
                    return
    print('Sorry, I did my best...')


def factors_from_successive_n_grams(num, min_value):
    '''
    >>> tuple(factors_from_successive_n_grams(2, 3))
    ()
    >>> tuple(factors_from_successive_n_grams(4, 3))
    (4,)
    >>> tuple(factors_from_successive_n_grams(40, 3))
    (4, 5, 8, 10)
    >>> tuple(factors_from_successive_n_grams(100, 3))
    (4, 5, 10)
    '''
    return (i for i in range(min_value, max_key_length + 1) if num % i == 0)


def all_collected_factors(text):
    # Kasiski examination
    # Collecting all factors between n and max_key_length of the
    # distances between the starts of two consecutive occurrences of an
    # n-gram, with n in gram_range (so between 3 and 5 by default). 
    # The length of the key to discover is likely to be one of the most
    # frequent factors.
    for n in n_gram_range:
        for i in range(len(text) - 2 * n + 1):
            j = text.find(text[i : i + n], i + n)
            if j != -1:
                yield from factors_from_successive_n_grams(j - i, n)


def key_lengths_from_most_to_least_promising(text):
    # The Caesar cipher will be tried first.
    yield 1
    # We prefer the most frequent divisors.
    # When two divisors have the same count, we prefer the largest one.
    key_lengths =\
            [x[0] for x in sorted(Counter(all_collected_factors(text)).items(),
                                  key=itemgetter(1, 0), reverse=True
                                 )
            ]
    yield from key_lengths
    # Keys of any length at most equal to max_key_length will be tried
    # if needed.
    yield from\
            (i for i in range(2, max_key_length + 1) if i not in key_lengths)


def etaoin_score(text, length):
    '''
    # In 'Three masts' we have, in a case insensitive manner and
    # w.r.t. the reverse order of the letters in
    # 'etaoinshrdlcumwfgypbvkjxqz':
    #   - 's', 't' and 'e', occuring twice
    #   - 'm', 'r', 'h' and 'a', occurring once.
    >>> etaoin_score('Three masts', 1) #  's'        'e'
    0
    >>> etaoin_score('Three masts', 2) #  'st'       'et'
    1
    >>> etaoin_score('Three masts', 3) #  'ste'      'eta'
    2
    >>> etaoin_score('Three masts', 4) #  'stem'     'etao'
    2
    >>> etaoin_score('Three masts', 5) #  'stemr'    'etaoi'
    2
    >>> etaoin_score('Three masts', 6) #  'stemrh'   'etaoin'
    2
    >>> etaoin_score('Three masts', 7) #  'stemrha'  'etaoins'
    4
    >>> etaoin_score('Three masts', 8) #  'stemrha'  'etaoinsh'
    5
    >>> etaoin_score('Three masts', 9) #  'stemrha'  'etaoinshr'
    6
    >>> etaoin_score('Three masts', 10) # 'stemrha'  'etaoinshrd'
    6
    '''
    letter_counts = Counter(c.lower() for c in text if c.isalpha())
    ranked_letters = sorted(letter_counts,
                            key=lambda x: (letter_counts[x], etaoin[x]),
                            reverse=True
                           )
    return sum(1 for i in range(min(length, len(ranked_letters)))
                     if etaoin[ranked_letters[i]] < length
              )


def looks_like_English(text, dictionary):
    if sum(1 for c in text if c.isalpha()) / len(text) < fraction_of_letters:
        return False
    possible_words = split('[^a-zA-Z]+', text)
    nb_of_words = sum(1 for w in possible_words if w in dictionary)
    return nb_of_words / len(possible_words) > fraction_of_words


if __name__ == '__main__': 
    import doctest
    doctest.testmod()    
