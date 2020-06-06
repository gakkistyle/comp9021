concat(a, Y, Y).
concat(f(X), Y, f(Z)) :- concat(X, Y, Z).
concat(g(X), Y, g(Z)) :- concat(X, Y, Z).

compress(a, a).
compress(f(a), f(a)).
compress(g(a), g(a)).
compress(f(f(X)), Y) :- compress(f(X), Y).
compress(g(g(X)), Y) :- compress(g(X), Y).
compress(f(g(X)), f(Y)) :- compress(g(X), Y).
compress(g(f(X)), g(Y)) :- compress(f(X), Y).

accumulator_reverse(a, X, X).
accumulator_reverse(f(X), Y, Z) :- accumulator_reverse(X, f(Y), Z).
accumulator_reverse(g(X), Y, Z) :- accumulator_reverse(X, g(Y), Z).
reverse(X, Y) :-  accumulator_reverse(X, a, Y).

relation(X, Y, Z) :- concat(X, Y, U), compress(U, V), reverse(V, Z).
relation(X, Y, Z) :- concat(Y, X, U), compress(U, V), reverse(V, Z).
