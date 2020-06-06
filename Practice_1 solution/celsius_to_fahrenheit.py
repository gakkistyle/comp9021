'''
Prints out a conversion table of temperatures from Celsius to Fahrenheit degrees,
with the former ranging from 0 to 100 in steps of 10.
'''


min_temperature = 0
max_temperature = 100
step = 10
# \t: A tab
print('Celsius\tFahrenheit')
# We let celsius take the values
# - min_temperature
# - min_temperature + step
# - min_temperature + 2 * step
# - min_temperature + 3 * step
# ...
# up to the largest value smaller than max_temperature + step
for celsius in range(min_temperature, max_temperature + step, step):
    fahrenheit = int(32+(9 * (celsius) / 5))
    # {:10d} or {:10}:  fahrenheit as a decimal number in a field of width 10
    # {:7.1f}: celsius as a floating point number in a field of width 7
    #          with 1 digit after the decimal point
    print(f'{celsius:7}\t{fahrenheit:10}')
