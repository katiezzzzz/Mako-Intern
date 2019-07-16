import pandas as pd
import numpy as np
import math
import csv

class Input:

    species = "data"

    def __init__(self, TimeStamp, Symbol, Quantity, Price):
        self.TimeStamp = TimeStamp
        self.Symbol = Symbol
        self.Quantity = Quantity
        self.Price = Price

    def instrument(self, Symbol):
        instrument_array = np.array(Symbol)
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