import pandas as pd
import numpy as np
import math
import csv

# assign each column
cols = ['TimeStamp', 'Symbol', 'Quantity', 'Price']
input = pd.read_csv('input_data.csv', header=None, names=cols)
# define a function to find out the names of different financial instruments
def instrument(arg):
    instrument_array = np.array(arg)
    instruments = np.array([])
    n = 0
    for i in instrument_array:
        for j in instruments:
            if i == j:
                n += 1
        if n == 0:
            instruments = np.append(instruments, i)
        n = 0
    return instruments
symbols = instrument(input['Symbol'])
# put the symbols in alphabetical order
symbols = sorted(symbols)
# number of different instruments
no_symbols = np.arange(0,len(symbols),1)

'''find the maximum time gap'''
# create an array of the difference in time between consecutive rows, then find max
# build a function to find maximum of a column
def column_maximum(arg):
    maxtime = np.array([])
    for i in no_symbols:
        small = np.array(((input.loc[arg == symbols[i]])['TimeStamp']))[0:-1]
        big = np.array(((input.loc[arg == symbols[i]])['TimeStamp']))[1:]
        gap = big - small
        maxtime = np.append(maxtime, np.amax(gap))
    return maxtime
maxtime = (column_maximum(input['Symbol']))
# do a test here


'''find the sum of the quantity for all trades in a symbol'''

# define a function and input one symbol
def total_volume(arg):
    totalvolumes = np.array([])
    for i in no_symbols:
        Sum = sum((input.loc[arg == symbols[i]])['Quantity'])
        totalvolumes = np.append(totalvolumes, Sum)
    return totalvolumes
totalvolumes = total_volume(input['Symbol'])
# add up the quantities
# print the sums out

# find max trade price
def max_tradeprice(arg):
    maxprice = np.array([])
    for i in no_symbols:
        Max = np.amax((input.loc[arg == symbols[i]])['Price'])
        maxprice = np.append(maxprice, Max)
    return maxprice
maxprice = max_tradeprice(input['Symbol'])

def weighted_average_price(arg):
    average_price = np.array([])
    for i in no_symbols:
        quantity = np.array((input.loc[arg == symbols[i]])['Quantity'])
        price = np.array((input.loc[arg == symbols[i]])['Price'])
        weighted_average = sum(quantity * price)/sum(quantity)
        average_price = np.append(average_price, math.trunc(weighted_average))
    return average_price
average_price = weighted_average_price(input['Symbol'])

output_data = {'Symbol': symbols,
               'MaxTimeGap': maxtime,
               'Volume': totalvolumes,
               'WeightedAveragePrice': average_price,
               'Maxprice': maxprice}
df = pd.DataFrame(output_data)
df.to_csv('output.csv')
