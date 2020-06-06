join(e, X, X).
join(l(H, T), X, l(H, Y)) :- join(T, X, Y).
