import math
import numpy as np

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

class memoryData:
    def __init__(self, NumPoints = 10 ** 2):
        self.Boldtime = 0
        self.Doldtime = 0

        self.times = np.zeros(NumPoints, dtype=np.int64)

        self.BValList = np.zeros(NumPoints)

        self.DValList = np.zeros(NumPoints)

        self.vol = 0
        self.Bgrad = np.empty([1])
        self.Dgrad = np.empty([1])

        self.BuyFuture = []
        self.SellFuture = []

        self.D_ShortTime = np.zeros(100, dtype=np.int64)
        self.D_ShortValList = np.zeros(100)
        self.B_ShortTime = np.zeros(100, dtype=np.int64)
        self.B_ShortValList = np.zeros(100)

        self.book_amount = np.zeros(10)
        self.cheese_amount=0
        self.book_value = 0
        self.pnlStore = [0]
        self.StopTimeStamp = 10**11
        self.startPnL = 0

        self.InitialPnL = 0
        self.InitialTime = 0

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
        self.StopList = 0

        self.Ratio = 0
        self.PastAsk = 0
        self.PastBId = 0


    def UpdateData(self, timegap, bookname, AskPrice, BidPrice, eventType, eventTime, AskVolume, BidVolume, PnL, factor, ShortFrequency, book_amount):
        RoundedTime = (math.floor(eventTime /timegap) * timegap)
        factorlist = np.array([1, factor, (factor ** 2)])

        if bookname == 'baseBook':
            if RoundedTime > self.times[0] + timegap / 2:       #if it is a new time, shift by 1
                self.InsertData(bookname, AskPrice, BidPrice, AskVolume, BidVolume, RoundedTime, factor, book_amount)
                self.m += 1
                self.Boldtime = RoundedTime

            elif abs(RoundedTime - self.times[0]) < timegap / 4 and abs(RoundedTime - self.Boldtime) > timegap / 4:   #if B was copied across
                self.Boldtime = RoundedTime
                self.BValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                         + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(factorlist * (np.array(AskVolume) + np.array(BidVolume)))

            elif abs(RoundedTime - self.Boldtime) < timegap / 4 and eventType == 'Trade':       #if event is a trade it takes priority
                self.BValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                    + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                    factorlist * (np.array(AskVolume) + np.array(BidVolume)))

        if bookname == 'corrBook':
            if RoundedTime > self.times[0] + timegap / 2:       #if it is a newtime, shift by one
                self.InsertData(bookname, AskPrice, BidPrice, AskVolume, BidVolume, RoundedTime, factor, book_amount)
                self.m += 1
                self.Doldtime = RoundedTime

            elif abs(RoundedTime - self.times[0]) < timegap / 4 and abs(RoundedTime - self.Doldtime) > timegap / 4: #if D was copied across, replace the D values
                self.Doldtime = RoundedTime
                self.DValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                         + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(factorlist * (np.array(AskVolume) + np.array(BidVolume)))


            elif abs(RoundedTime - self.Doldtime) < timegap / 4 and eventType == 'Trade':   #if event is a trade it takes priority
                self.DValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                    + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                    factorlist * (np.array(AskVolume) + np.array(BidVolume)))

        if self.counter == 10000 and not self.StopList:
            self.StopList = RoundedTime
        if self.StopList:
            if self.times[0] - self.StopList >= self.StopTimeStamp:
                self.counter = 0
                self.StopList = 0

        if self.m % ShortFrequency == 0:
            self.D_ShortTime[1:] = self.D_ShortTime[:-1]        #shift by one
            self.D_ShortValList[1:] = self.D_ShortValList[:-1]
            self.B_ShortTime[1:] = self.B_ShortTime[:-1]
            self.B_ShortValList[1:] = self.B_ShortValList[:-1]

            self.D_ShortTime[0] = self.Doldtime         #update
            self.D_ShortValList[0] = self.DValList[0]
            self.B_ShortTime[0] = self.Boldtime
            self.B_ShortValList[0] = self.BValList[0]

        self.UpdatePnL(PnL)

    def InsertData(self, bookname, AskPrice, BidPrice, AskVolume, BidVolume, RoundedEventTime, factor, book_amount):
        factorlist = np.array([1, factor, (factor ** 2)])

        for key in ['times', 'BValList', 'DValList', 'book_amount']:
            CurrentData = getattr(self,key)
            CurrentData[1:] = CurrentData[0:-1]

        if bookname == 'baseBook':
            self.times[0] = RoundedEventTime
            self.BValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                         + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(factorlist * (np.array(AskVolume) + np.array(BidVolume)))
            self.book_amount[0] = book_amount
            self.DValList[0] = self.DValList[1]

        if bookname == 'corrBook':
            self.times[0] = RoundedEventTime
            self.DValList[0] = (np.dot(np.array(AskPrice), factorlist * np.array(BidVolume))
                                + np.dot(np.array(BidPrice), factorlist * np.array(AskVolume))) / np.sum(
                                factorlist * (np.array(AskVolume) + np.array(BidVolume)))
            self.book_amount[0] = book_amount
            self.BValList[0] = self.BValList[1]

    def UpdatePnL(self, PnL):
        if self.m % 1 == 0:
            self.pnlStore.insert(0, PnL)
            self.m = 0
            self.AltInd = 1

    def TrackBGrad(self, length1, length2):  # if there is a trend in D, then we replicate the trend in B
        while len(self.times) > length1:
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
        while len(self.times) > length1:
            x = self.times[0:length1]
            y = np.array(self.DValList[0:length1])
            z = np.poly1d(np.polyfit(x, y, 1))
            self.Dgrad = np.append(z[1] * (10 ** 12), self.Dgrad)

        while len(self.Dgrad) > length2:
            self.Dgrad = self.Dgrad[0:length2]

    def GradVol(self):
        self.gradvar = np.var(self.Bgrad)

    def StayClosetoZero(self, saferange, factor):

        if self.book_amount[0] > saferange: #add pressure to sell
            self.counter -= (1 + factor) ** (self.book_amount[0] - saferange) - 1

        elif self.book_amount[0] < - saferange: #add pressure to buy
            self.counter += (1 + factor) ** (self.book_amount[0] - saferange) - 1

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
                if self.book_amount[0] > 0:   #sell
                    Min = np.min(self.pnlStore[1:TimeFrame])
                    Max = np.max(self.pnlStore[1:TimeFrame])
                    if Max - self.pnlStore[0] >= maxLoss or self.pnlStore[0] - Min >= maxGain:
                        self.counter -= 1
                        self.pnlStore = []
                elif self.book_amount[0] < 0:     #buy
                    Min = np.min(self.pnlStore[1:TimeFrame])
                    Max = np.max(self.pnlStore[1:TimeFrame])
                    if self.pnlStore[0] - Min >= maxGain or Max - self.pnlStore[0] >= maxLoss:
                        self.counter += 1
                        self.pnlStore = []
                self.AltInd = 0

    def AppleV3(self, maxGain, maxLoss, PnL):
        if not self.startPnL:
            self.startPnL = PnL
        elif self.startPnL:
            if PnL - self.startPnL > maxGain:
                self.counter = 10000
                self.startPnL = 0
                self.stopcounter += 1
            if PnL - self.startPnL < -maxLoss:
                self.counter = 10000
                self.startPnL = 0
                self.stopcounter += 1  #maybe can set this to a -= if this works better

    def AppleV4(self, maxGain, maxLoss, timespan, PnL, time):    #deals with single futures
        if self.counter1 != 0 and not self.InitialPnL:
            self.InitialPnL = PnL
        if self.counter1 != 0 and not self.InitialTime:
            self.InitialTime = time
        if self.counter == 0 and self.counter1 != 0 and self.InitialPnL:
            if PnL - self.InitialPnL > maxGain:
                if self.counter1 == 2:
                    self.counter = -1
                elif self.counter1 == -2:
                    self.counter = 1
                self.InitialPnL = 0
                self.InitialTime = 0

            elif self.InitialPnL - PnL > maxLoss:
                if self.counter1 == 2:
                    self.counter = -1
                elif self.counter1 == -2:
                    self.counter = 1
                self.InitialPnL = 0
                self.InitialTime = 0

        elif self.times[0] - self.InitialTime > timespan:
            if self.counter1 == 2:
                self.counter = -1
            elif self.counter1 == -2:
                self.counter = 1

    def DShortTrend(self, factor, width):  # for relatively short term, E.g. every half a min
        Filter = self.B_ShortTime != 0
        B_ShortTime = self.B_ShortTime[Filter]
        B_ShortValList = self.B_ShortValList[Filter]
        D_ShortTime = self.D_ShortTime[Filter]
        D_ShortValList = self.D_ShortValList[Filter]
        try:
            if len(D_ShortTime) > 1 and len(B_ShortTime) > 1:
                B_grad = np.poly1d(np.polyfit(B_ShortTime[:10], B_ShortValList[:10], 1))[1]
                D_grad = np.poly1d(np.polyfit(D_ShortTime[:10], D_ShortValList[:10], 1))[1]
                if B_grad > 1*10**(-7) and D_grad > 1*10**(-8) or B_grad < -1*10**(-7) and D_grad < -1*10**(-8):
                    B_sd = max(0.1, np.std(B_ShortValList))
                    B_mean = np.mean(B_ShortValList[:width])
                    D_sd = max(0.1, np.std(D_ShortValList))
                    D_mean = np.std(D_ShortValList[:width])
                    if B_grad > 0 and D_grad > 0 and (B_ShortValList[0] - B_mean) > (2.5*B_sd) and (D_ShortValList[0] - D_mean) > (2*D_sd):
                        # buy
                        self.counter += factor
                        self.counter2 += 1
                    elif B_grad < 0 and D_grad < 0 and (B_ShortValList[0] - B_mean) > (2.5*B_sd) and (D_ShortValList[0] - D_mean) > (2*D_sd):
                        # sell
                        self.counter -= factor
                        self.counter2 -= 1
        except:
            pass

    def MovingAverage(self, length,  eventbook):
        if len(self.BValList[self.BValList != 0]) > length:
            self.mvgAvg_ = np.mean(self.BValList[0:length])

            if eventbook == 'baseBook':
                if self.counter == 0 and self.counter1 == 0:
                    if self.Ind == 0:
                        if self.mvgAvg_ > self.BValList[0] + 0.5 and self.Bgrad[0] < -10:  # (i.e. decreasing)
                            self.counter -= 0.5         #sell

                        elif self.mvgAvg_ < self.BValList[0] - 0.5 and self.Bgrad[0] > 10: #(i.e. increasing)
                            self.counter += 0.5         #buy

                    if self.Ind == 2 and self.mvgAvg_ <= self.BValList[0]:
                        self.counter += 0.5             #buy

                        self.counter1 = 1
                    elif self.Ind == -2 and self.mvgAvg_ >= self.BValList[0]:
                        self.counter -= 0.5             #sell

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
