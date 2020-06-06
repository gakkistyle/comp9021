num(o).
num(s(X)) :- num(X).

plus(o, Y, Y).
plus(s(X), Y, s(Z)) :- plus(X, Y, Z).

times(o, _, o).
times(s(X), Y, Z) :- times(X, Y, U), plus(U, Y, Z).

reduce(add(mult(A, x), B), add(mult(A, x), B)) :- num(A), num(B).
reduce(s(X), add(Y, s(Z))) :- reduce(X, add(Y, Z)).
reduce(o, add(mult(o, x), o)).
reduce(x, add(mult(s(o), x), o)).
reduce(add(X, Y), add(mult(N, x), M)) :- reduce(X, add(mult(N1, x), M1)), reduce(Y, add(mult(N2, x), M2)), plus(N1, N2, N), plus(M1, M2, M).
reduce(mult(X, Y), add(mult(N, x), M)) :- reduce(X, add(mult(o, x), M1)), reduce(Y, add(mult(N, x), M2)), plus(M1, M2, M).
reduce(mult(X, Y), add(mult(N, x), M)) :- reduce(X, add(mult(N, x), M1)), reduce(Y, add(mult(o, x), M2)), plus(M1, M2, M).

equiv(X, Y) :- reduce(X, Z), reduce(Y, Z).
       
