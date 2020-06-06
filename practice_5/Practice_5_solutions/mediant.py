# COMP9021 Practice 5 - Solutions

def mediants_to(p, q):
    '''
    >>> mediants_to(1, 2)
    0/1     1/2     1/1
    >>> mediants_to(41, 152)
      0/1    *    1/2         1/1  
      0/1    *    1/3         1/2  
      0/1         1/4    *    1/3  
      1/4    *    2/7         1/3  
      1/4    *    3/11        2/7  
      1/4         4/15   *    3/11 
      4/15        7/26   *    3/11 
      7/26   *   10/37        3/11 
      7/26   *   17/63       10/37 
      7/26       24/89   *   17/63 
     24/89       41/152      17/63 
    >>> mediants_to(71, 83)
     0/1       1/2   *   1/1 
     1/2       2/3   *   1/1 
     2/3       3/4   *   1/1 
     3/4       4/5   *   1/1 
     4/5       5/6   *   1/1 
     5/6   *   6/7       1/1 
     5/6      11/13  *   6/7 
    11/13     17/20  *   6/7 
    17/20     23/27  *   6/7 
    23/27     29/34  *   6/7 
    29/34     35/41  *   6/7 
    35/41     41/48  *   6/7 
    41/48     47/55  *   6/7 
    47/55     53/62  *   6/7 
    53/62     59/69  *   6/7 
    59/69     65/76  *   6/7 
    65/76     71/83      6/7 
    '''
    field_width = max(len(str(p)), len(str(q)))
    left = 0, 1
    right = 1, 1
    target = p, q
    mediant = 1, 2
    while mediant != target:
        if mediant[0] * target[1] < target[0] * mediant[1]:
            left_mark = ' '
            right_mark = '*'
        else:
            left_mark = '*'
            right_mark = ' '
        print_mediant(left, left_mark, mediant, right_mark, right, field_width)
        if left_mark == ' ':
            left = mediant
        else:            
            right = mediant
        mediant = left[0] + right[0], left[1] + right[1]
    print_mediant(left, ' ', mediant, ' ', right, field_width)

def print_mediant(left, left_mark, mediant, right_mark, right, w):
    print(f'{left[0]:{w}}/{left[1]:<{w}}'
          f'  {left_mark}  {mediant[0]:{w}}/{mediant[1]:<{w}}  {right_mark}  '
          f'{right[0]:{w}}/{right[1]:<{w}}'
         )


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    
