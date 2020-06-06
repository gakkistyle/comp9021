# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 5


'''
Will be tested with year between 1913 and 2013.
You might find the reader() function of the csv module useful,
but you can also use the split() method of the str class.
'''

import csv

def f(year):
    '''
    >>> f(1914)
    In 1914, maximum inflation was: 2.0
    It was achieved in the following months: Aug
    >>> f(1922)
    In 1922, maximum inflation was: 0.6
    It was achieved in the following months: Jul, Oct, Nov, Dec
    >>> f(1995)
    In 1995, maximum inflation was: 0.4
    It was achieved in the following months: Jan, Feb
    >>> f(2013)
    In 2013, maximum inflation was: 0.82
    It was achieved in the following months: Feb
    '''
    months = 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    # Insert your code here
    
    max_inf= -1000
    inflation= []
    with open('cpiai.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=",")
        row_count=0
        for row in csv_reader:
            if row_count==0:
                row_count=1
            else:
                if row[0].split('-')[0]==str(year):
                    if float(row[2])>max_inf:
                        max_inf=float(row[2])
                    inflation.append(float(row[2]))
    maxMonths=''
    for i in range(len(inflation)):
        if inflation[i]==max_inf:
            maxMonths+=months[i]+', '
            
    print('In '+str(year)+', maximum inflation was:', max_inf)
    print('It was achieved in the following months: '+maxMonths[:-2])
        
                
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()

#f(1922)