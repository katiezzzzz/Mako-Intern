import numpy as np


class simTrades():
    def __init__(self, aParams):
        self.tradeTimestamp = np.zeros(0, dtype='int64')
        self.tradeTransactTime = np.zeros(0, dtype='int64')
        self.tradePrice = np.zeros(0)
        self.tradeVolume = np.zeros(0, dtype=int)
        self.tradeSide = np.zeros(0, dtype=int)
        self.tradeDelta = np.zeros(0)
        self.tradeTrigger = np.empty(0, dtype='<U50')
        self.tradeFees = np.zeros(0)

        if aParams.memoryDataFieldsToRecordIntoTradeList:
            myFieldList = aParams.memoryDataFieldsToRecordIntoTradeList.split(';')
            for field in myFieldList:
                myFieldToRecord = field.replace('.', '_')
                setattr(self, myFieldToRecord, np.zeros(0))

    def addNewTrade(self, aTradeItem, aMemoryData, aParams):

        # TKAP: Add all trade fields
        self.tradeTimestamp = np.append(self.tradeTimestamp, np.int64(aTradeItem['timestamp']))
        self.tradeTransactTime = np.append(self.tradeTransactTime, np.int64(aTradeItem['transactTime']))
        self.tradePrice = np.append(self.tradePrice, aTradeItem['price'])
        self.tradeVolume = np.append(self.tradeVolume, aTradeItem['volume'])
        self.tradeSide = np.append(self.tradeSide, aTradeItem['side'])
        self.tradeDelta = np.append(self.tradeDelta, aTradeItem['side'] * aTradeItem['volume'])
        self.tradeTrigger = np.append(self.tradeTrigger, aTradeItem['trigger'])
        self.tradeFees = np.append(self.tradeFees, aTradeItem['fees'])

        if aParams.memoryDataFieldsToRecordIntoTradeList:
            myFieldList = aParams.memoryDataFieldsToRecordIntoTradeList.split(';')
            for field in myFieldList:
                myFieldToRecord = field.replace('.', '_')
                mySplitFields = field.split('.')

                myResult = aMemoryData
                myFoundField = False
                for splitfield in mySplitFields:
                    if hasattr(myResult, splitfield):
                        myFoundField = True
                    else:
                        myFoundField = False
                        break
                    if myFoundField:
                        myResult = getattr(myResult, splitfield)
                if myFoundField:
                    setattr(self, myFieldToRecord, np.append(getattr(self, myFieldToRecord), myResult))

    def calculateTotalVolume(self):
        return np.sum(self.tradeVolume)

    def calculateNetDelta(self):
        return np.sum(self.tradeDelta)

    def calculateTradingPnL(self, aCurrentVal, aContractSize):
        return np.sum(self.tradeDelta * (aCurrentVal - self.tradePrice)) * aContractSize

    def calculateFees(self):
        return np.sum(self.tradeFees) * -1

    def calculateOverallPnL(self, aCurrentVal, aContractSize):
        myTradingPnL = self.calculateTradingPnL(aCurrentVal, aContractSize)
        myFees = self.calculateFees()
        return myTradingPnL + myFees

    def getLastTradeTimesForSide(self, aSide):
        theLastTime = np.int64(0)
        theLastTransactTime = np.int64(0)
        myFilter = self.tradeSide == aSide
        if np.any(myFilter):
            theLastTime = self.tradeTimestamp[myFilter][-1]
            theLastTransactTime = self.tradeTransactTime[myFilter][-1]
        return theLastTime, theLastTransactTime
