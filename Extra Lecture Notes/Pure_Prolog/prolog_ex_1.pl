% http://groups.engin.umd.umich.edu/CIS/course.des/cis479/prolog/family.pro

  
sisterof(X, Y) :- parents(X, M, F), female(X), parents(Y, M, F).

parents(edward, victoria, albert).
parents(harry, victoria, albert).
parents(alice, victoria, albert).
female(alice).

loves(harry, wine).
loves(alice, wine).  
