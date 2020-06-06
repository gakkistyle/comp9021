# COMP9021 Practice 6 - Solutions


'''
Data downloaded from http://www.bom.gov.au/climate/averages/tables/cw_066062.shtml
'''


import csv
import sys
from math import floor, ceil
from calendar import month_name

from matplotlib import pyplot as plt


datafile = 'IDCJCM0037_066062.csv'
try:
    with open(datafile) as csvfile:
        file = csv.reader(csvfile)
        for _ in range(12):
            next(file)
        mean_max_temperatures = [float(i) for i in next(file)[1: 13]]
        for _ in range(9):
            next(file)
        mean_min_temperatures = [float(i) for i in next(file)[1: 13]]
except FileNotFoundError:
    print(f'Could not open {datafile}, giving up.')
    sys.exit()

min_temperature = floor(min(mean_min_temperatures))
max_temperature = ceil(max(mean_max_temperatures))
min_dec_jan = (mean_min_temperatures[0] + mean_min_temperatures[-1]) / 2
max_dec_jan = (mean_max_temperatures[0] + mean_max_temperatures[-1]) / 2
mean_min_temperatures = [min_dec_jan] + mean_min_temperatures + [min_dec_jan]
mean_max_temperatures = [max_dec_jan] + mean_max_temperatures + [max_dec_jan]

temperatures = plt.figure(dpi = 220, figsize = (5, 3.5))
plt.axis([0.5, 12.5, min_temperature - 1, max_temperature + 1])
plt.xticks(range(1, 13), [month_name[i] for i in range(1, 13)], fontsize = 8)
plt.yticks([i / 2 for i in range(min_temperature * 2, max_temperature * 2 + 1)], fontsize = 4)
xrange = [0.5] + list(range(1, 13)) + [12.5]
plt.plot(xrange, mean_max_temperatures, c = 'red')
plt.plot(xrange, mean_min_temperatures, c = 'blue')
plt.fill_between(xrange, mean_min_temperatures, mean_max_temperatures, facecolor = 'grey',
                                                                                         alpha = 0.1
                )
plt.title('Mean min and max temperatures in Sydney', fontsize = 10)
plt.grid(True)
temperatures.autofmt_xdate()
plt.show()

