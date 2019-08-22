import numpy as np
import math
import importlib
import pandas as pd
from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model as lm

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

class memoryData:
    def __init__(self):
        self.times = np.zeros([1], dtype = np.int64)
        self.newtimes = np.empty([1])

        self.B_AskPrices = np.array([0])
        self.B_BidPrices = np.array([0])
        self.B_types = ['None']
        self.B_sides = ['None']
        self.B_Volume = np.empty([1])
        self.B_times = np.array([0], dtype = np.int64)

        self.D_AskPrices = np.array([0])
        self.D_BidPrices = np.array([0])
        self.D_types = ['None']
        self.D_sides = ['None']
        self.D_times = np.array([0], dtype = np.int64)

        self.BBookDepthVal = 0
        self.DBookDepthVal = 0
        self.BValList = [0]
        self.DValList = [0]

        self.vol = 0
        self.Bgrad = np.empty([1])
        self.Dgrad = np.empty([1])

        self.BuyFuture = []
        self.SellFuture = []

        self.D_LongTime = np.empty([1])
        self.D_LongValList = np.empty([1])
        self.D_ShortTime = np.empty([1])
        self.D_ShortValList = np.empty([1])
        self.B_LongTime = np.empty([1])
        self.B_LongValList = np.empty([1])
        self.B_ShortTime = np.empty([1])
        self.B_ShortValList = np.empty([1])

        self.book_amount = 0
        self.cheese_amount=0
        self.book_value = 0
        self.pnlStore = [0]
        self.StopTimeStamp = 2 * 10**11
        self.startPnL = 0

        self.valuation = 0
        self.valuation_bid = np.nan
        self.valuation_ask = np.nan

        self.counter = 0
        self.counter1 = 0
        self.counter2 = 0
        self.stopcounter = 0

        self.indicator = 0
        self.Ind = 0
        self.shortInd = 0
        self.AltInd = 0

        self.n = 0
        self.m = 0

        self.prev_n = []
        self.prev_m = []
        self.StopList = []

        self.Ratio = 0

    def AdjustTime(self, times):
        self.newtimes = np.array(times) - times[-1]

    def UpdateData(self, timespan, totaltime, minlength, bookname, AskPrice, BidPrice, eventType, eventSide, eventTime, AskVolume, BidVolume, PnL, factor, shortfrequency, shortlength):
        factorlist = np.array([1, factor, (factor ** 2)])
        roundedTime = (math.floor(eventTime /timespan) * timespan) - 1.56233 * (10 ** 18) - 1.60028 * (10 ** 12)

        self.m += 1

        if self.counter == 10000 and not self.StopList:
            self.StopList.insert(0, roundedTime)
        if self.StopList:
            if roundedTime - self.StopList[0] >= self.StopTimeStamp:
                self.counter = 0
                self.StopList = []

        if len(self.times) == 0:
            self.times = np.insert(self.times, 0, roundedTime, axis=0)
            self.B_times = np.insert(self.B_times, 0, roundedTime, axis=0)
            self.D_times = np.insert(self.D_times, 0, roundedTime, axis=0)

        if ~np.isnan(AskPrice[0]) and ~np.isnan(BidPrice[0]) and ~np.isnan(AskVolume[0]) and ~np.isnan(BidVolume[0]):
            if bookname == 'baseBook':
                if roundedTime != self.times[0]:
                    self.B_AskPrices = np.insert(self.B_AskPrices, 0, AskPrice[0], axis = 0)
                    self.B_BidPrices = np.insert(self.B_BidPrices, 0, BidPrice[0], axis = 0)
                    self.B_types.insert(0, eventType)
                    self.B_sides.insert(0, eventSide)
                    self.times = np.insert(self.times, 0, roundedTime, axis = 0)
                    self.B_times = np.insert(self.B_times, 0, roundedTime, axis = 0)
                    self.BBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                             + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.BValList.insert(0, self.BBookDepthVal)

                    self.D_AskPrices = np.insert(self.D_AskPrices, 0, self.D_AskPrices[0], axis=0)
                    self.D_BidPrices = np.insert(self.D_BidPrices, 0, self.D_BidPrices[0], axis=0)
                    self.D_types.insert(0, 'None')
                    self.D_sides.insert(0, 'None')
                    self.DValList.insert(0, self.DValList[0])

                elif roundedTime != self.B_times[0]:
                    self.B_times = np.insert(self.B_times, 0, roundedTime, axis=0)
                    self.B_AskPrices[0] = AskPrice[0]
                    self.B_BidPrices[0] = BidPrice[0]
                    self.B_sides[0] = eventSide
                    self.B_types[0] = eventType
                    self.BBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                             + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                        factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.BValList.insert(0, self.BBookDepthVal)

                elif roundedTime == self.times[0] and eventType == 'Trade':
                    self.B_AskPrices[0] = AskPrice[0]
                    self.B_BidPrices[0] = BidPrice[0]
                    self.B_types[0] = eventType
                    self.B_sides[0] = eventSide
                    self.BBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                             + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                        factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.BValList[0] = self.BBookDepthVal

            if bookname == 'corrBook':
                self.n += 1

                # TKAP: Initialization
                #x = np.array([0,0,0,0,0]) #timestamp int64
                #y = np.array([np.nan]*5) #price float64

                # TKAP: Insert
                #x[1:] = x[0:-1]
                #x[0] = 3
                #y[1:] = y[0:-1]
                #y[0] = 3000

                #TKAP: Filter before use
                #myFilter = x!=0
                #if np.any(myFilter):
                #    myFilteredTimestamps = x[myFilter]
                #    myFilteredPrices = y[myFilter]


                if roundedTime != self.times[0]:
                    self.D_AskPrices = np.insert(self.D_AskPrices, 0, AskPrice[0], axis=0)
                    self.D_BidPrices = np.insert(self.D_BidPrices, 0, BidPrice[0], axis=0)
                    self.D_types.insert(0, eventType)
                    self.D_sides.insert(0, eventSide)
                    self.times = np.insert(self.times, 0, roundedTime, axis=0)
                    self.D_times = np.insert(self.D_times, 0, roundedTime, axis=0)
                    self.DBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                          + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) /  np.sum(factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.DValList.insert(0, self.DBookDepthVal)

                    self.B_AskPrices = np.insert(self.B_AskPrices, 0, self.B_AskPrices[0], axis=0)
                    self.B_BidPrices = np.insert(self.B_BidPrices, 0, self.B_BidPrices[0], axis=0)
                    self.B_types.insert(0, 'None')
                    self.B_sides.insert(0, 'None')
                    self.BValList.insert(0, self.BValList[0])

                elif roundedTime != self.D_times[0]:
                    self.D_times = np.insert(self.D_times, 0, roundedTime, axis=0)
                    self.D_AskPrices[0] = AskPrice[0]
                    self.D_BidPrices[0] = BidPrice[0]
                    self.D_sides[0] = eventSide
                    self.D_types[0] = eventType
                    self.DBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                          + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                                             factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.DValList.insert(0, self.DBookDepthVal)

                elif roundedTime == self.times[0] and eventType == 'Trade':
                    self.D_AskPrices[0] = AskPrice[0]
                    self.D_BidPrices[0] = BidPrice[0]
                    self.D_types[0] = eventType
                    self.D_sides[0] = eventSide
                    self.DBookDepthVal = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                             + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                        factorlist * (np.array(AskVolume) + np.array(BidVolume)))
                    self.DValList[0] = self.DBookDepthVal

        while self.times[0] - self.times[-1] > totaltime and len(self.times) > minlength:
            self.times = self.times[:-1]

            self.B_AskPrices = self.B_AskPrices[:-1]
            self.B_BidPrices = self.B_BidPrices[:-1]
            self.B_types = self.B_types[:-1]
            self.B_sides = self.B_sides[:-1]
            self.BValList = self.BValList[:-1]

            self.D_AskPrices = self.D_AskPrices[:-1]
            self.D_BidPrices = self.D_BidPrices[:-1]
            self.D_types = self.D_types[:-1]
            self.D_sides = self.D_sides[:-1]
            self.DValList = self.DValList[:-1]

            if bookname == 'baseBook':
                self.B_times = self.B_times[:-1]
            elif bookname == 'corrBook':
                self.D_times = self.D_times[:-1]

        if self.m % 1 == 0:
            self.pnlStore.insert(0, PnL)
            self.m = 0
            self.AltInd = 1

        #if self.n%shortfrequency == 0:
        #    self.D_ShortTime = np.insert(self.D_ShortTime, 0, self.D_times[0], axis=0)
        #    self.D_ShortValList = np.insert(self.D_ShortValList, 0, self.DValList[0], axis=0)
        #    self.B_ShortTime = np.insert(self.B_ShortTime, 0, self.B_times[0], axis=0)
        #    self.B_ShortValList = np.insert(self.B_ShortValList, 0, self.BValList[0], axis=0)
        #    while len(self.B_ShortTime) > shortlength:
        #        self.B_ShortTime = self.B_ShortTime[:shortlength]
        #        self.B_ShortValList = self.B_ShortValList[:shortlength]
        #    while len(self.D_ShortValList) > shortlength:
        #        self.D_ShortTime = self.D_ShortTime[:shortlength]
        #        self.D_ShortValList = self.D_ShortValList[:shortlength]

    def FinalValuation(self):
        if ~np.isnan(self.valuation_ask) and ~np.isnan(self.valuation_bid):
            self.valuation_ask = min(self.valuation_ask, self.B_AskPrices[0] + 2)
            self.valuation_bid = max(self.valuation_bid, self.B_BidPrices[0] - 2)

    def TrackBGrad(self, length1, length2):  # if there is a trend in D, then we replicate the trend in B
        while len(self.B_times) > length1:
            x = self.times[0:length1]
            y = np.array(self.BValList[0:length1])
            #mask = ~np.isnan(x) & ~np.isnan(y)
            #z = np.poly1d(np.polyfit(x[mask], y[mask], 1))
            if ~np.isnan(x).any() and ~np.isnan(y).any():
                z = np.poly1d(np.polyfit(x, y, 1))
                self.Bgrad = np.append(z[1] * (10 ** 12), self.Bgrad)
            else:
                self.Bgrad = np.empty([1])

        while len(self.Bgrad) > length2:
            self.Bgrad = self.Bgrad[0:length2]

    def TrackDGrad(self, length1, length2):  # if there is a trend in D, then we replicate the trend in B
        while len(self.D_times) > length1:
            x = self.times[0:length1]
            y = np.array(self.DValList[0:length1])
            z = np.poly1d(np.polyfit(x, y, 1))
            self.Dgrad = np.append(z[1] * (10 ** 12), self.Dgrad)

        while len(self.Dgrad) > length2:
            self.Dgrad = self.Dgrad[0:length2]

    def GradVol(self):
        self.gradvar = np.var(self.Bgrad)

    def StayClosetoZero(self, saferange, factor):

        if self.book_amount > saferange: #add pressure to sell
            self.counter -= (1 + factor) ** (self.book_amount - saferange) - 1

        elif self.book_amount < - saferange: #add pressure to buy
            self.counter += (1 + factor) ** (self.book_amount - saferange) - 1

    def UpdateBookAmounts(self, newbook, oldbook, bid, ask):
        if newbook == oldbook + 1 and oldbook >= 0:
            self.BuyFuture.append(bid)
        elif newbook == oldbook - 1 and oldbook <= 0:
            self.SellFuture.append(ask)
        elif newbook == oldbook + 1 and oldbook <= 0:
            self.SellFuture.remove(min(self.SellFuture))
        elif newbook == oldbook - 1 and oldbook >= 0:
            self.BuyFuture.remove(max(self.BuyFuture))

    def AppleV1(self, maxGain, maxLoss, AskPrice, BidPrice):   #run this last
        if len(self.BuyFuture) > 0:
            x = min(self.BuyFuture)
            BuyGain = AskPrice - x

            if BuyGain > maxGain or BuyGain < - maxLoss:
                self.counter += -1        #right now this is the wrong way around but it somehow gives profits

        elif len(self.SellFuture) > 0:
            y = max(self.SellFuture)
            SellGain = y - BidPrice

            if SellGain > maxGain or SellGain < - maxLoss:
                self.counter -= 1

    def AppleV2(self, maxGain, maxLoss, TimeFrame):     #Apples in terms of overall pnl instead of individual futures
        if len(self.pnlStore) >= TimeFrame:
            self.pnlStore = self.pnlStore[0:TimeFrame]
        if self.AltInd == 1:
            if len(self.pnlStore) >= 5:
                if self.book_amount > 0:   #sell
                    Min = np.min(self.pnlStore[1:TimeFrame])
                    Max = np.max(self.pnlStore[1:TimeFrame])
                    if Max - self.pnlStore[0] >= maxLoss or self.pnlStore[0] - Min >= maxGain:
                        self.counter -= 1
                        self.pnlStore = []
                elif self.book_amount < 0:     #buy
                    Min = np.min(self.pnlStore[1:TimeFrame])
                    Max = np.max(self.pnlStore[1:TimeFrame])
                    if self.pnlStore[0] - Min >= maxGain or Max - self.pnlStore[0] >= maxLoss:
                        self.counter += 1
                        self.pnlStore = []
                self.AltInd = 0

    def AppleV3(self, maxGain, maxLoss, PnL):
        if self.startPnL == 0:
            self.startPnL = PnL
        elif self.startPnL != 0:
            if PnL - self.startPnL > maxGain:
                self.counter = 10000
                self.startPnL = 0
                self.stopcounter += 1
            if PnL - self.startPnL < -maxLoss:
                self.counter = 10000
                self.startPnL = 0
                self.stopcounter += 1  #maybe can set this to a -= if this works better

    def DShortTrend(self, factor, width):  # for relatively short term, E.g. every half a min
         # moved this earlier part into update data
        try:
            if len(self.D_ShortTime) > 1 and len(self.B_ShortTime) > 1:
                B_m = np.poly1d(np.polyfit(self.B_ShortTime[:6], self.B_ShortValList[:6], 1))[1]
                B_sd = np.std(self.B_ShortValList)
                B_mean = np.mean(self.B_ShortValList[:width])
                D_m = np.poly1d(np.polyfit(self.D_ShortTime[:6], self.D_ShortValList[:6], 1))[1]
                D_sd = np.std(self.D_ShortValList)
                D_mean = np.std(self.D_ShortValList[:width])
                if B_m > 0 and D_m > 0 and (self.B_ShortValList[0] - B_mean) > (2*B_sd) and (self.D_ShortValList[0] - D_mean) > (1*D_sd):
                    # buy
                    self.counter += factor
                elif B_m < 0 and D_m < 0 and (self.B_ShortValList[0] - B_mean) > (2*B_sd) and (self.D_ShortValList[0] - D_mean) > (1*D_sd):
                    # sell
                    self.counter -= factor
        except:
            pass

    def BLongTrend(self, frequency, length, factor, width):
        if self.n%frequency == 0:
            self.D_LongTime = np.insert(self.D_LongTime, 0, self.D_times[0], axis=0)
            self.D_LongValList = np.insert(self.D_LongValList, 0, self.DValList[0], axis=0)
            self.B_LongTime = np.insert(self.B_LongTime, 0, self.B_times[0], axis=0)
            self.B_LongValList = np.insert(self.B_LongValList, 0, self.BValList[0], axis=0)
            if len(self.B_LongTime) > length:
                self.B_LongTime = self.B_LongTime[:length]
                self.B_LongValList = self.B_LongValList[:length]
            if len(self.D_LongValList) > length:
                self.D_LongTime = self.D_LongTime[:length]
                self.D_LongValList = self.D_LongValList[:length]
            try:
                if len(self.D_ShortTime) > 1 and len(self.B_ShortTime) > 1:
                    Bfit = np.polyfit(self.B_LongTime[:3], self.B_LongValList[:3], 1)[0]
                    Bfit = [Bfit]
                    B_m = Bfit[0]
                    B_sd = np.std(self.B_LongValList)
                    B_mean = np.mean(self.B_LongValList[:width])
                    Dfit = np.polyfit(self.D_LongTime[:3], self.D_LongValList[:3], 1)[0]
                    Dfit = [Dfit]
                    D_m = Dfit[0]
                    #D_sd = np.std(self.D_LongValList)
                    #D_mean = np.std(self.D_LongValList[:width])
                    #maybe set a k i.e. B_m > k and D_m > k so that you are more confident when you lock in a trade
                    if B_m > 0 and D_m > 0 and (self.B_LongValList[0] - B_mean) > (1*B_sd):
                        # buy
                        self.valuation_bid += factor
                        self.valuation_ask += factor
                        self.counter1 = 1
                    elif B_m < 0 and D_m < 0 and (self.B_LongValList[width] - B_mean) > (1*B_sd):
                        # sell
                        self.valuation_ask -= factor
                        self.valuation_bid -= factor
                        self.counter1 = 1
            except:
                pass

    def TrackBTrend(self, factor, howpositive, length):
        if len(self.BValList) > 15:
            TradeChange = np.array(self.BValList[0:length]) - np.array(self.BValList[1:1+length])
            TradePos = sum(x > 0 for x in TradeChange)

            if TradePos >= howpositive:
                self.valuation += factor * (1.1 ** (TradePos))
            elif TradePos <= length - howpositive:
                self.valuation -= factor * (1.1 ** (TradePos))

    def nSDfromMean(self, length, factor):       #adds more and more pressure as we go more standard deviations out
        List = self.BValList[0:length]
        self.sd = np.std(List)
        self.mean = np.mean(List)
        k = 1

        while self.B_BidPrices[0] < self.mean - k*self.sd or self.B_AskPrices[0] > self.mean +k*self.sd and self.sd != 0:
            if self.B_BidPrices[0] < self.mean - k*self.sd:
                self.valuation -= (1 + factor) ** k - 1
            if self.B_AskPrices[0] > self.mean + k*self.sd:
                self.valuation += (1 + factor) ** k - 1
            k += 1

    def MovingAverage(self, length, bidprice, askprice, eventbook):
        if len(self.BValList) > length:
            self.mvgAvg_ = np.mean(self.BValList[0:length])

            if eventbook == 'baseBook':
                if self.counter == 0 and self.counter1 == 0:
                    if self.Ind == 0:
                        if self.mvgAvg_ > self.BValList[0] + 0.5 and self.Bgrad[0] < -10:  # (i.e. decreasing)
                            self.valuation_bid = bidprice - 4
                            self.valuation_ask = askprice               #sell
                            self.Ind = 1
                            self.counter1 = -1

                        elif self.mvgAvg_ < self.BValList[0] - 0.5 and self.Bgrad[0] > 10: #(i.e. increasing)
                            self.valuation_bid = bidprice
                            self.valuation_ask = askprice + 5              #buy
                            self.Ind = -1
                            self.counter1 = 1

                    if self.Ind == 2 and self.mvgAvg_ <= self.BValList[0]:
                        self.valuation_bid = bidprice
                        self.valuation_ask = askprice + 5              #buy

                        self.counter1 = 1
                    elif self.Ind == -2 and self.mvgAvg_ >= self.BValList[0]:
                        self.valuation_bid = bidprice - 5
                        self.valuation_ask = askprice              #sell

                        self.counter1 = -1

    def ShortTermStuff(self, bidprice, askprice):
        if self.counter == 0 and self.shortInd == 0:
            if self.indicator == 1:
                self.valuation_bid = askprice + 2
                self.valuation_ask = askprice + 5
            elif self.indicator == -1:
                self.valuation_bid = bidprice - 5
                self.valuation_ask = bidprice - 2
            self.counter = 1
            self.shortInd = 1

        if self.shortInd == 2 and self.counter == 0:
            if self.indicator == 1:
                self.valuation_bid = bidprice
                self.valuation_ask = askprice
            if self.indicator == -1:
                self.valuation_bid = bidprice
                self.valuation_ask = askprice
            self.shortInd = 0
            self.counter = 1

    def Ratio(self, factor):
        if len(self.BValList) > 0 and len(self.DValList) > 0:
            self.Ratio.insert(0, self.BValList[0] / self.DValList[0])

