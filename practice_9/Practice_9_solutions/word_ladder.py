# COMP9021 Practice 9 - Solutions


from collections import defaultdict, deque
import sys


'''
Computes all transformations from a word word_1 to a word word_2, consisting of
sequences of words of minimal length, starting with word_1, ending in word_2,
and such that two consecutive words in the sequence differ by at most one letter.
All words have to occur in a dictionary with name dictionary.txt, stored in the
working directory.
'''


dictionary_file = 'dictionary.txt'

def get_words_and_word_relationships():
    try:
        with open(dictionary_file) as dictionary:
            lexicon = set()
            contextual_slots = defaultdict(list)
            for word in dictionary:
                word = word.rstrip()
                lexicon.add(word)
                for i in range(len(word)):
                    contextual_slots[word[: i], word[i + 1: ]].append(word)
            closest_words = defaultdict(set)
            for slot in contextual_slots:
                for i in range(len(contextual_slots[slot])):
                    for j in range(i + 1, len(contextual_slots[slot])):
                        closest_words[contextual_slots[slot][i]].add(contextual_slots[slot][j])
                        closest_words[contextual_slots[slot][j]].add(contextual_slots[slot][i])
            print(closest_words)
            return lexicon, closest_words
    except FileNotFoundError:
        print(f'Could not open {dictionary_file}. Giving up...')
        sys.exit()

def word_ladder(word_1, word_2):
    lexicon, closest_words = get_words_and_word_relationships()
    word_1 = word_1.upper()
    word_2 = word_2.upper()
    if len(word_1) != len(word_2) or word_1 not in lexicon or word_2 not in lexicon:
        return []
    if word_1 == word_2:
        return [[word_1]]
    solutions = []
    queue = deque([[word_1]])
    while queue:
        word_sequence = queue.pop()
        last_word = word_sequence[-1]
        for word in closest_words[last_word]:
            if word == word_2:
                if not solutions or len(solutions[-1]) > len(word_sequence):
                    solutions.append(word_sequence + [word])
            elif not solutions and word not in word_sequence:
                queue.appendleft(word_sequence + [word])
    return solutions
