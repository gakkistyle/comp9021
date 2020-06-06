% https://www.cpp.edu/~jrfisher/www/prolog_tutorial/2_1.html


adjacent(region_1, region_2).
adjacent(region_2, region_1). 
adjacent(region_1, region_3).
adjacent(region_3, region_1). 
adjacent(region_1, region_4).
adjacent(region_4, region_1). 
adjacent(region_1, region_5).
adjacent(region_5, region_1). 
adjacent(region_2, region_3).
adjacent(region_3, region_2). 
adjacent(region_2, region_4).
adjacent(region_4, region_2). 
adjacent(region_3, region_4).
adjacent(region_4, region_3). 
adjacent(region_4, region_5).
adjacent(region_5, region_4).

color(region_1, red, a).
color(region_2, blue, a).
color(region_3, green, a).
color(region_4, yellow, a).
color(region_5, blue, a).

color(region_1, red, b). 
color(region_2, blue, b). 
color(region_3, green, b). 
color(region_4, blue, b). 
color(region_5, green, b).

conflict(R1, R2, Coloring) :- adjacent(R1, R2),  color(R1, Color, Coloring),  color(R2, Color, Coloring). 
