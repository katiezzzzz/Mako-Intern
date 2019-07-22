import csv
import math
from collections import OrderedDict

class Instrument:

    def __init__(self, symbol):
        self.symbol = symbol
        self.maxtime = 0
        self.totalVolume = 0
        self.maxprice = 0
        self.Weightedaverage = 0
        self.total = 0
        self.time1 = 0

    def findGap(self,time2):
        if self.time1 == 0:
            self.time1 = time2
            return
        gap = time2 - self.time1
        if gap > self.maxtime:
            self.maxtime = gap
        self.time1 = time2

    def addQuantity(self, volume):
        self.totalVolume += volume

    def findPrice(self, price):
        if price > self.maxprice:
            self.maxprice = price

    def findWeightedaverage(self, quantity, price):
        self.total += (quantity*price)
        self.Weightedaverage = math.trunc(self.total/self.totalVolume)

    def getValues(self):
        return [self.symbol,self.maxtime,self.totalVolume,self.maxprice,self.Weightedaverage]

instruments = {}

with open('input_data.csv') as f:
    reader = csv.reader(f)
    time1 = None
    for row in reader:
        time = int(row[0])
        symbol = row[1]
        quantity = int(row[2])
        price = int(row[3])
        if symbol in instruments:
            inst = instruments[symbol]
            inst.findGap(time)
            inst.addQuantity(quantity)
            inst.findPrice(price)
            inst.findWeightedaverage(quantity, price)
        else:
            instruments[symbol] = Instrument(symbol)
            a = instruments[symbol]
            a.findGap(time)
            a.addQuantity(quantity)
            a.findPrice(price)
instruments = OrderedDict(sorted(instruments.items(), key=lambda instruments:instruments[0]))
with open('output.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    for instrument in instruments.values():
        writer.writerow(instrument.getValues())
