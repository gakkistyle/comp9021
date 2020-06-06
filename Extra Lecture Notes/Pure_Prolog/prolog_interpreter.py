# Written by Eric Martin for COMP9021


'''
A Prolog interpreter for definite logic programs.
Illustrates the use of a deque for depth-first and breadth-first search
for a solution.

'''


from collections import deque
from itertools import islice

from logic import *


class Conjunction(list):
    class ConjunctionError(Exception):
        pass

    def __init__(self, conjuncts):
        super().__init__(conjuncts)

    def predicate_and_function_symbols(self):
        predicate_symbols = {}
        function_symbols = {}
        for atom in self:
            atom_predicate_symbol, atom_function_symbols =\
                    atom.predicate_and_function_symbols()
            if not consistently_add_to(atom_predicate_symbol,
                                       predicate_symbols
                                      ):
                raise Conjunction.ConjunctionError(f'{self}: predicate symbol '
                                                   'used with many arities'
                                                  )
            if not consistently_merge_to(atom_function_symbols,
                                         function_symbols
                                        ):
                raise Conjunction.ConjunctionError(f'{self}: function symbol '
                                                   'used with many arities'
                                                  )
        if predicate_symbols.keys() & function_symbols.keys():
            raise Conjunction.ConjunctionError(f'{self}: symbol used as '
                                               'predicate and function symbol'
                                              )
        return predicate_symbols, function_symbols


class Rule:
    class RuleError(Exception):
        pass

    def __init__(self, head, body=[]):
        self.head = head
        self.body = body
        self.variables =  self.head.variables()
        for atom in self.body:
            self.variables |= atom.variables() 

    def __str__(self):
        if not self.body:
            return self.head.__str__() + '.'
        return ' :- '.join((self.head.__str__(),
                            ', '.join(atom.__str__() for atom in self.body)
                           )
                          ) + '.'

    def predicate_and_function_symbols(self):
        head_predicate_symbol, head_function_symbols =\
                self.head.predicate_and_function_symbols()
        if not self.body:
            return {head_predicate_symbol[0]: head_predicate_symbol[1]},\
                   head_function_symbols
        predicate_symbols, function_symbols =\
                self.body.predicate_and_function_symbols()        
        if not consistently_add_to(head_predicate_symbol, predicate_symbols):
            raise Rule.RuleError(f"{self}: Head's predicate symbol used with "
                                 'different arity in body'
                                )
        if not consistently_merge_to(head_function_symbols, function_symbols):
            raise Rule.RuleError(f'{self}: Function symbol used with '
                                 'different arities in head and body'
                                )
        if predicate_symbols.keys() & function_symbols.keys():
            raise Rule.RuleError(f'{self}: symbol used as predicate and '
                                 'function symbols, one in head, the other '
                                 'in body'
                                )
        return predicate_symbols, function_symbols

    def parse_rule(expression):
        '''
        >>> rule = Rule.parse_rule('father(bob, jack).')
        >>> print(rule.head)
        father(bob, jack)
        >>> for atom in rule.body: print(atom)
        >>> rule = Rule.parse_rule('grandparent(X, Y) :-\
                                       parent(X, Z), parent(Z, Y).'\
                                  )
        >>> print(rule.head)
        grandparent(X, Y)
        >>> for atom in rule.body: print(atom)
        parent(X, Z)
        parent(Z, Y)
        '''
        if expression[-1] != '.':
            raise Rule.RuleError(f'{expression}: does not end in a full stop')
        rule = expression[: -1].split(':-')
        if not (1 <= len(rule) <= 2):
            raise Rule.RuleError(f'{expression}: syntactically invalid')
        head = Expression.parse_item(rule[0])
        if not head:
            raise Rule.RuleError(f'{expression}: syntactically incorrect head')
        if len(rule) == 1:
            rule = Rule(head)
        else:
            body = Expression.parse_item(rule[1], parse_single_subitem=False)
            if not body:
                raise Rule.RuleError(f'{expression}: syntactically incorrect '
                                     'body'
                                    )
            rule = Rule(head, Conjunction(body))
        rule.predicate_and_function_symbols()
        return rule


class LogicProgram:
    class LogicProgramError(Exception): 
        pass

    class QueryError(Exception):
        pass

    def __init__(self, filename):
        self.program = []
        self.predicate_symbols = {}
        self.function_symbols = {}
        rule_nb = 0
        with open(filename) as file:
            for rule in file:
                rule = rule.strip()
                if not rule or rule.startswith('%'):
                    continue
                rule = Rule.parse_rule(rule)
                rule_nb += 1
                rule_predicate_symbols, rule_function_symbols =\
                        rule.predicate_and_function_symbols()
                if not consistently_merge_to(rule_predicate_symbols,
                                             self.predicate_symbols
                                            )\
                   or not consistently_merge_to(rule_function_symbols,
                                                self.function_symbols
                                               ):
                    raise LogicProgram.LogicProgramError(
                             f'Symbol arity in rule nb {rule_nb} '
                             'inconsistent with arities in previous rules'
                                                        )
                rule_variables = rule.head.variables()
                for atom in rule.body:
                    rule_variables |= atom.variables()
                underscore_index =\
                        rule.head.individualise_underscores(rule_variables)
                for atom in rule.body:
                    underscore_index =\
                            atom.individualise_underscores(rule_variables,
                                                           underscore_index
                                                          )
                self.program.append(rule)
        if self.predicate_symbols.keys() & self.function_symbols.keys():
            raise LogicProgram.LogicProgramError('Symbol used as predicate '
                                                 'and function symbols'
                                                )

    def solve(self, query, depth_first=True):
        query = Conjunction(Expression.parse_item(query,
                                                  parse_single_subitem=False
                                                 )
                           )
        query_predicate_symbols, query_function_symbols =\
                query.predicate_and_function_symbols()
        if any(predicate_symbol not in self.predicate_symbols
               or query_predicate_symbols[predicate_symbol]
               != self.predicate_symbols[predicate_symbol]
                    for predicate_symbol in query_predicate_symbols
              ):
            raise LogicProgram.QuerryError(f'{query}: predicate symbol '
                                           'in query not in program'
                                          )
        if any(function_symbol not in self.function_symbols
               or query_function_symbols[function_symbol]
               != self.function_symbols[function_symbol]
                    for function_symbol in query_function_symbols
              ):
            raise LogicProgram.QuerryError(f'{query}: function symbol '
                                           'in query not in program'
                                          )               
        query_variables = {var for atom in query for var in atom.variables()}
        # A list of pairs consisting of:
        # - a list of goals to be solved, and
        # - the substitution to apply to the variables that occur in the
        #   query as determined by the unifications computed so far.
        goals_solution_pairs = deque([(deque(query),
                                       {var: Term(var)
                                            for var in query_variables
                                       }
                                      )
                                     ]
                                    )
        while goals_solution_pairs:
            goals, solution = goals_solution_pairs.popleft()
            if not goals:
                yield {var: solution[var].__str__() for var in solution}
                continue
            reserved_variables = query_variables\
                                 | {var for atom in goals
                                           for var in atom.variables()
                                   }
            goal = goals.popleft()
            next_goals_solution_pairs = deque()
            for rule in self.program:
                variable_renaming =\
                        Expression.fresh_variables(rule.variables,
                                                   reserved_variables
                                                  )
                head = rule.head.rename_variables(variable_renaming)
                mgu = goal.unify(head)
                if mgu is not None:
                    new_goals = deque(atom.rename_variables(variable_renaming)
                                         .substitute(mgu) for atom in rule.body
                                     )
                    new_goals.extend(goal.substitute_in_copy(mgu)
                                          for goal in goals
                                    )
                    next_goals_solution_pairs.append(
                                   (new_goals,
                                    {var: solution[var].substitute_in_copy(mgu)
                                         for var in solution
                                    }
                                   )
                                                    )
            if depth_first:
                goals_solution_pairs.extendleft(
                                        reversed(next_goals_solution_pairs)
                                               )
            else:
                goals_solution_pairs.extend(next_goals_solution_pairs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print('TESTING DEPTH FIRST')
    LP = LogicProgram('prolog_ex_1.pl')
    print('A few queries for prolog_ex_1.pl')
    print('  Solutions to sisterof(victoria, harry):')
    for solution in LP.solve('sisterof(victoria, harry)'):
        print('   ', solution)
    print('  Solutions to sisterof(alice, harry):')
    for solution in LP.solve('sisterof(alice, harry)'):
        print('   ', solution)
    print('  Solutions to sisterof(alice, X):')
    for solution in LP.solve('sisterof(alice, X)'):
        print('   ', solution)
    print('  Solutions to sisterof(alice, X), loves(X, wine):')
    for solution in LP.solve('sisterof(alice, X), loves(X, wine)'):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_6.pl')
    print('A query for prolog_ex_6.pl')
    print('  Solutions to relation(f(f(f(g(f(a))))), f(f(g(g(a)))), X):')
    for solution in LP.solve('relation(f(f(f(g(f(a))))), f(f(g(g(a)))), X)'):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_2.pl')
    print('A few queries for prolog_ex_2.pl')
    print('  Solutions to father(X, jack):')
    for solution in LP.solve('father(X, jack)'):
        print('   ', solution)
    print('  Solutions to grandparent(john, X):')
    for solution in LP.solve('grandparent(john, X)'):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_3.pl')
    print('A query for prolog_ex_3pl')
    print('  Solutions to loves(Who, What):')
    for solution in LP.solve('loves(Who, What)'):
        print('   ', solution)
    print()
    
    LP = LogicProgram('prolog_ex_4.pl')
    print('A few queries for prolog_ex_4.pl')
    print('  Solutions to conflict(R1, R2, b):')
    for solution in LP.solve('conflict(R1, R2, b)'):
        print('   ', solution)
    print('  Solutions to conflict(R1, R2, b), color(R1, C, b):')
    for solution in LP.solve('conflict(R1, R2, b), color(R1, C, b)'):
        print('   ', solution)

    print('TESTING BREADTH FIRST')
    LP = LogicProgram('prolog_ex_1.pl')
    print('A few queries for prolog_ex_1.pl')
    print('  Solutions to sisterof(victoria, harry):')
    for solution in LP.solve('sisterof(victoria, harry)', False):
        print('   ', solution)
    print('  Solutions to sisterof(alice, harry):')
    for solution in LP.solve('sisterof(alice, harry)', False):
        print('   ', solution)
    print('  Solutions to sisterof(alice, X):')
    for solution in LP.solve('sisterof(alice, X)', False):
        print('   ', solution)
    print('  Solutions to sisterof(alice, X), loves(X, wine):')
    for solution in LP.solve('sisterof(alice, X), loves(X, wine)', False):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_6.pl')
    print('A query for prolog_ex_6.pl')
    print('  Solutions to relation(f(f(f(g(f(a))))), f(f(g(g(a)))), X):')
    for solution in LP.solve('relation(f(f(f(g(f(a))))), f(f(g(g(a)))), X)',\
                             False\
                            ):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_2.pl')
    print('A few queries for prolog_ex_2.pl')
    print('  Solutions to father(X, jack):')
    for solution in LP.solve('father(X, jack)', False):
        print('   ', solution)
    print('  Solutions to grandparent(john, X):')
    for solution in LP.solve('grandparent(john, X)', False):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_3.pl')
    print('A query for prolog_ex_3.pl')
    print('  Solutions to loves(Who, What):')
    for solution in LP.solve('loves(Who, What)',False):
        print('   ', solution)
    print()
    
    LP = LogicProgram('prolog_ex_4.pl')
    print('A few queries for prolog_ex_4.pl')
    print('  Solutions to conflict(R1, R2, b):')
    for solution in LP.solve('conflict(R1, R2, b)', False):
        print('   ', solution)
    print('  Solutions to conflict(R1, R2, b), color(R1, C, b):')
    for solution in LP.solve('conflict(R1, R2, b), color(R1, C, b)', False):
        print('   ', solution)
    print()

    LP = LogicProgram('prolog_ex_5.pl')
    print('A query for prolog_ex_5.pl')
    print('  Solutions to join(X, X, Y):')
    for solution in islice(LP.solve('join(X, X, Y)'), 3):
        print('   ', solution)
