import numpy as np


class testSampleData():
    def __init__(self, aNumPoints = 0):

        self.timestamp = np.zeros(aNumPoints, dtype='int64')
        self.prices = np.zeros(aNumPoints) * np.nan
        self.corrPrices = np.zeros(aNumPoints) * np.nan
        self.blahPrices = np.zeros(aNumPoints) * np.nan

    def insertValue(self, aTimestamp, aPrice, aCorrPrice, aBlahPrices):

        for key in self.__dict__:
            myCurrentArray = getattr(self, key)
            myCurrentArray[1:] = myCurrentArray[0:-1]

        self.timestamp[0] = aTimestamp
        self.prices[0] = aPrice
        self.corrPrices[0] = aCorrPrice
        self.blahPrices[0] = aBlahPrices

    def getActualData(self):
        theSlicedData = testSampleData()

        myFilter = self.timestamp != 0

        for key in theSlicedData.__dict__:
            setattr(theSlicedData, key, getattr(self, key)[myFilter])

        return theSlicedData
