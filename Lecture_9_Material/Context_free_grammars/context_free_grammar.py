# COMP9021 Term 3 2019

from itertools import product


# So that we can use ε in the rules we pass as an argument to
# ContextFreeGrammar
ε = ''


class ContextFreeGrammar:
    '''
    The rules of the context free grammar are a dictionnary whose keys
    are the nonterminals and for each nonterminal N, the value
    associated with N is the set of productions of N, one of which is
    possibly ε (the empty production).
    A character is a nonterminal symbol iff it is an uppercase letter.

    >>> CFG = ContextFreeGrammar({'S': {'SS', '(S)', '()'}}, 'S')
    >>> CFG.without_ε.rules == CFG.rules
    True
    >>> CFG = ContextFreeGrammar({'S': {'bSbb', 'A'}, 'A': {'aA', ε}},\
                                 'S'\
                                )
    >>> CFG.without_ε.rules == {'S': {'A', 'bbb', 'bSbb'},\
                                'A': {'aA', 'a'}\
                               }
    True
    '''
    def __init__(self, rules, starting_symbol):
        self.rules = rules
        self.starting_symbol = starting_symbol
        generating_ε = self._generates_ε()
        self._starting_symbol_generates_ε = starting_symbol in generating_ε
        # All productions of ε are removed, possibly adding other
        # productions to generate the same language. That allows one to
        # guarantee that a nonempty word w belongs to the generated
        # language iff it can be generated thanks to a sequence of
        # productions consisting of words no longer than w.
        rules_without_ε = {nonterminal: rules[nonterminal]
                               for nonterminal in rules
                                   if nonterminal not in generating_ε
                          }
        for nonterminal in generating_ε:
            # In a production different to ε, an occurrence of a
            # nonterminal P is either kept or eliminated (doubling the
            # number of derived productions) in case ε can be generated
            # from P. For instance, if X can generate ε but Y cannot,
            # then the production aaXbYaX will give rise to the
            # productions:
            # - aaXbYaX
            # - aabYaX
            # - aaXbYa
            # - aabYa
            new_productions =\
          {''.join(symbols) for production in rules[nonterminal] if production
                                for symbols in product(
                        *((symbol, '') if symbol in generating_ε else (symbol,)
                              for symbol in production
                         )
                                                      )
          }
            new_productions -= {''}
            if new_productions:
                rules_without_ε[nonterminal] = new_productions
        self.without_ε = ContextFreeGrammarWithoutε(rules_without_ε,
                                                    self.starting_symbol
                                                   )

    def __str__(self):
        return '\n'.join(' -> '.join((f'{nonterminal}',
                                      ' | '.join(production or 'ε'
                                                     for production in
                                                sorted(self.rules[nonterminal])
                                                )
                                     )
                                    ) for nonterminal in
                                                   self._ordered_nonterminals()
                        )

    def _ordered_nonterminals(self):
        yield self.starting_symbol
        yield from sorted(self.rules.keys() - {self.starting_symbol})
        
    def _generates_ε(self):
        # We look for the set S1 of all symbols producing ε,  then for
        # the set S2 of all symbols producing a sequence of symbols in
        # S1, then for the set S3 of all symbols producing a sequence of
        # symbols in the union of S1 with S2...
        generating_ε = set()
        left_to_examine = self.rules.keys()
        while True:
            new_nonterminals_generating_ε = set()
            for nonterminal in left_to_examine:
                if any(production == '' or set(production) <= generating_ε
                           for production in self.rules[nonterminal]
                      ):
                    generating_ε.add(nonterminal)
                    new_nonterminals_generating_ε.add(nonterminal)
            if new_nonterminals_generating_ε:
                left_to_examine -= new_nonterminals_generating_ε
            else:
                break
        return generating_ε

    def can_generate_with_no_ε(self, word):
        '''
        >>> CFG = ContextFreeGrammar({'S': {'SS', '(S)', '()'}}, 'S')
        >>> CFG.can_generate_with_no_ε('()')
        True
        >>> CFG.can_generate_with_no_ε('(())')
        True
        >>> CFG.can_generate_with_no_ε('()()')
        True
        >>> CFG.can_generate_with_no_ε('(()())')
        True
        >>> CFG.can_generate_with_no_ε('((())())(((())))')
        True
        >>> CFG.can_generate_with_no_ε('(')
        False
        >>> CFG.can_generate_with_no_ε('())')
        False

        >>> CFG = ContextFreeGrammar({'S': {'A', 'bbb', 'bSbb'},\
                                      'A': {'aA', 'a'}\
                                     }, 'S'\
                                    )
        >>> CFG.can_generate_with_no_ε('')
        False
        >>> CFG.can_generate_with_no_ε('bbb')
        True
        >>> CFG.can_generate_with_no_ε('aa')
        True
        >>> CFG.can_generate_with_no_ε('babb')
        True
        >>> CFG.can_generate_with_no_ε('bbbbbb')
        True
        >>> CFG.can_generate_with_no_ε('bbaaabbbb')
        True
        >>> CFG.can_generate_with_no_ε('bbbaaaaaabbbbbb')
        True
        >>> CFG.can_generate_with_no_ε('bbbbb')
        False
        >>> CFG.can_generate_with_no_ε('bbabbbbb')
        False
        >>> CFG.can_generate_with_no_ε('bbabbbba')
        False
        '''
        if word == '':
            return False
        generated_bigrams = [('', self.starting_symbol)]
        seen_bigrams = set(generated_bigrams)
        while generated_bigrams:
            w_1, w_2 = generated_bigrams.pop()
            # bigram is a pair of the form (w_1, w_2) where all symbols
            # in w_1 are terminals.
            # - If w_2 is of the form tw where t is a terminal symbol,
            #   then (w_1, w_2) is replaced by (w_1t, w).
            # - Otherwise, if w_1 is not an initial segment of word,
            #   then (w_1, w_2) is dumped.
            # - Otherwise, if w_2 is empty, then either w_1 is word and
            #   word is known to have been generated, or (w_1, w_2) is
            #   dumped.
            # - Otherwise, w_2 is of the form Nw where N is a
            #   nonterminal symbol, and (w_1, w_2) is replaced by all
            #   pairs of the form (w_1, w'w) where w' can be produced
            #   from N and w_1w'w is not longer than word.
            while w_2 and not w_2[0].isupper():
                w_1, w_2 = w_1 + w_2[0], w_2[1 :]
            if not word.startswith(w_1):
                continue
            if not w_2:
                if len(w_1) == len(word):
                    return True
                continue
            for pattern in self.rules[w_2[0]]:
                if not pattern:
                    continue
                new_bigram = w_1, pattern + w_2[1 :]
                if len(new_bigram[0]) + len(new_bigram[1]) <= len(word)\
                   and new_bigram not in seen_bigrams:
                    generated_bigrams.append(new_bigram)
                    seen_bigrams.add(new_bigram)
        return False

    def can_generate(self, word):
        '''
        >>> CFG = ContextFreeGrammar({'S': {'SS', '(S)', '()'}}, 'S')
        >>> CFG.can_generate('')
        False
        >>> CFG.can_generate('()')
        True
        >>> CFG.can_generate('(())')
        True
        >>> CFG.can_generate('()()')
        True
        >>> CFG.can_generate('(()())')
        True
        >>> CFG.can_generate('((())())(((())))')
        True
        >>> CFG.can_generate('(')
        False
        >>> CFG.can_generate('())')
        False

        >>> CFG = ContextFreeGrammar({'S': {'bSbb', 'A'}, 'A': {'aA', ε}}, 'S')
        >>> CFG.can_generate('')
        True
        >>> CFG.can_generate('bbb')
        True
        >>> CFG.can_generate('aa')
        True
        >>> CFG.can_generate('babb')
        True
        >>> CFG.can_generate('bbbbbb')
        True
        >>> CFG.can_generate('bbaaabbbb')
        True
        >>> CFG.can_generate('bbbaaaaaabbbbbb')
        True
        >>> CFG.can_generate('bbbbb')
        False
        >>> CFG.can_generate('bbabbbbb')
        False
        >>> CFG.can_generate('bbabbbba')
        False
        '''
        if word == '':
            return self._starting_symbol_generates_ε
        return self.without_ε.can_generate(word)


class ContextFreeGrammarWithoutε(ContextFreeGrammar):
    def __init__(self, rules, starting_symbol):
        self.rules = rules
        self.starting_symbol = starting_symbol

    def can_generate(self, word):
        '''
        >>> CFG = ContextFreeGrammarWithoutε({'S': {'SS', '(S)', '()'}}, 'S')
        >>> CFG.can_generate('')
        False
        >>> CFG.can_generate('()')
        True
        >>> CFG.can_generate('(())')
        True
        >>> CFG.can_generate('()()')
        True
        >>> CFG.can_generate('(()())')
        True
        >>> CFG.can_generate('((())())(((())))')
        True
        >>> CFG.can_generate('(')
        False
        >>> CFG.can_generate('())')
        False
        '''
        return self.can_generate_with_no_ε(word)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
