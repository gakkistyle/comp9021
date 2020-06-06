% Test queries:

% father(X, jack).
% X = bob.
  
% grandparent(john, X).
% X = jack ;
% X = sandra ;
  
father(bob, jack).
father(bob, sandra).
father(john, bob).
father(john, mary).
mother(jane, jack).
mother(jane, sandra).
mother(emily, bob).
mother(emily, mary).

parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).
son(X, Y) :- parent(Y, X), male(X).  
daughter(X, Y) :- parent(Y, X), female(X).
brother(X, Y) :- male(X), parent(Z, X), parent(Z, Y).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
