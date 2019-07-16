import pandas as pd
import numpy as np
import math
import csv

class Output:
    species = "data"

    def __init__(self, File):
        self.File = File

    def read(self):
        self.File = pd.read_csv(self.File, header=None, names=['TimeStamp', 'Symbol', 'Quantity', 'Price'])
        self.TimeStamp = self.File['TimeStamp']
        self.Symbol = self.File['Symbol']
        self.Quantity = self.File['Quantity']
        self.Price = self.File['Price']

    def instrument(self):
        instrument_array = np.array(self.Symbol)
        self.instruments = np.array([])
        n = 0
        for i in instrument_array:
            for j in self.instruments:
                if i == j:
                    n += 1
            if n == 0:
                self.instruments = np.append(self.instruments, i)
            n = 0
        self.instruments = sorted(self.instruments)
        self.no_symbols = np.arange(0, len(self.instruments), 1)
        return self.instruments

    def max_timegap(self):
        self.maxtime = np.array([])
        for i in self.no_symbols:
            small = np.array(((self.File.loc[self.Symbol == self.instruments[i]])['TimeStamp']))[0:-1]
            big = np.array(((self.File.loc[self.Symbol == self.instruments[i]])['TimeStamp']))[1:]
            gap = big - small
            self.maxtime = np.append(self.maxtime, np.amax(gap))
        return self.maxtime

    def total_volume(self):
        self.totalvolumes = np.array([])
        for i in self.no_symbols:
            Sum = sum((self.File.loc[self.Symbol == self.instruments[i]])['Quantity'])
            self.totalvolumes = np.append(self.totalvolumes, Sum)
        return self.totalvolumes

    def max_tradeprice(self):
        self.maxprice = np.array([])
        for i in self.no_symbols:
            Max = np.amax((self.File.loc[self.Symbol == self.instruments[i]])['Price'])
            self.maxprice = np.append(self.maxprice, Max)
        return self.maxprice

    def weighted_average_price(self):
        self.average_price = np.array([])
        for i in self.no_symbols:
            quantity = np.array((self.File.loc[self.Symbol == self.instruments[i]])['Quantity'])
            price = np.array((self.File.loc[self.Symbol == self.instruments[i]])['Price'])
            weighted_average = sum(quantity * price) / sum(quantity)
            self.average_price = np.append(self.average_price, math.trunc(weighted_average))
        return self.average_price

    def output_csv(self):
        output_data = {'Symbol': self.instruments,
                       'MaxTimeGap': self.maxtime,
                       'Volume': self.totalvolumes,
                       'WeightedAveragePrice': self.average_price,
                       'Maxprice': self.maxprice}
        df = pd.DataFrame(output_data)
        df.to_csv('output.csv')


output = Output('input_data.csv')
output.read()
output.instrument()
output.max_timegap()
output.total_volume()
output.max_tradeprice()
output.weighted_average_price()
output.output_csv()