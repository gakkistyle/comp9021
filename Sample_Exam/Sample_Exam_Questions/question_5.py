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
    with open('cpiai.csv') as csvfile:
        file = csv.reader(csvfile)
        infla = []
        for line in file:
            if line[0][:4] == str(year):
                infla.append(float(line[2]))
        max_infla = max(infla)
        max_month = []
    with open('cpiai.csv') as csvfile:
        file = csv.reader(csvfile)
        for line in file:
            if line[0][:4] == str(year):
                if float(line[2]) == max_infla:
                    max_month.append(months[int(line[0].split('/')[0].split('-')[1])-1])
        print(f'In {year}, maximum inflation was: {max_infla}')
        print(f'It was achieved in the following months:',', '.join(num for num in max_month))




if __name__ == '__main__':
    import doctest
    doctest.testmod()
