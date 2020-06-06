% http://athena.ecs.csus.edu/~logicp/prolog/Prolog_Example_6.pdf

  
cat(fubby).
black_spots(fubby).
dog(figaro).
white_spots(figaro).

owns(mary, Pet):- cat(Pet), black_spots(Pet).
loves(Who, What):- owns(Who, What).
