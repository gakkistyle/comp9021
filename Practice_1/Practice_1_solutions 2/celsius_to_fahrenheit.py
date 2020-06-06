# COMP9021 Practice 1 - Solutions


'''
Prints out a conversion table of temperatures from Celsius to Fahrenheit degrees,
the former ranging from 0 to 100 in steps of 10.
'''


min_temperature = 0
max_temperature = 100
step = 10

print('Celsius\tFahrenheit')
for celsius in range(min_temperature, max_temperature + step, step):
    fahrenheit = celsius // 5 * 9 + 32
    print(f'{celsius:7}\t{fahrenheit:10}')
