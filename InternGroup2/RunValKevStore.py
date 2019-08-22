import numpy as np
import pandas as pd
import warnings


def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):
    Info = aValuationData.memoryData
    Info.UpdateData(10 ** 5, 10 ** 8, 100, aEventBook, aMarketEvent.askDepth.prices[0:3],
                    aMarketEvent.bidDepth.prices[0:3],
                    aMarketEvent.eventType, aMarketEvent.eventSide, aMarketEvent.timestamp,
                    aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                    aSimulationData.simNetDelta, 0.25)

    if Info.counter != 0 and Info.book_amount != aSimulationData.simNetDelta:
        Info.counter = 0

    if Info.counter == 0 and Info.counter1 != 0 and Info.book_amount != aSimulationData.simNetDelta:
        Info.counter1 = 0
        if Info.Ind == 1:
            Info.Ind = 2
        elif Info.Ind == -1:
            Info.Ind = -2
        elif Info.Ind == 2 or Info.Ind == -2:
            Info.Ind = 0

    Info.UpdateBookAmounts(aSimulationData.simNetDelta, Info.book_amount, Info.valuation_ask, Info.valuation_bid)
    Info.book_amount = aSimulationData.simNetDelta

    #Info.TrackBGrad(length1=10, length2=300)
    #Info.TrackDGrad(length1=10, length2=300)

    if Info.counter == 0 and aEventBook == 'baseBook':
        Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 10
        Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 10

    length = 300
    if Info.counter == 0 and aEventBook == 'baseBook':
        if len(Info.BValList) > length and len(Info.DValList) > length:
            Baverage = np.mean(Info.BValList[0: length], dtype=np.float64)
            Bstd = np.std(Info.BValList[0: length], dtype=np.float64)
            Daverage = np.mean(Info.DValList[0: length], dtype=np.float64)
            Dstd = np.std(Info.DValList[0: length], dtype=np.float64)
            n = ((Info.BValList[0] - Baverage) / Bstd)
            m = ((Info.DValList[0] - Daverage) / Dstd)

            k = 1.5

            Info.prev_n.insert(0, n)
            Info.prev_m.insert(0, m)

            if len(Info.prev_n) >= 50:
                Info.prev_n = Info.prev_n[0:50]

            if len(Info.prev_m) >= 50:
                Info.prev_m = Info.prev_m[0:50]

            if m >= k:
                print('blah1')
                if sum(np.array(Info.prev_n) > 2 * m / 3) == 0:
                    Info.c
                for x in Info.prev_n:
                    if x > 2 * m / 3:
                        Info.counter = 1
            elif m <= -k:
                print('blah2')
                for x in Info.prev_n:
                    if x < 2 * m / 3:
                        Info.counter = 1

            if Info.counter == 1:
                if m < 0:   #buy and wait for reversion
                    Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
                    Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 2
                    print('ayay')
                elif m > 0:   #sell and wait for reversion
                    Info.valuation_ask = aMarketEvent.askDepth.prices[0] - 2
                    Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 5
                    print()

    #Info.DShortTrend(frequency=500, length=50, factor=5, width=10)    # 0.08 seconds of data
    #Info.BLongTrend(frequency=10000, length=20, factor=5, width=3)    # 10 seconds of data, takes the last 3
    #Info.nSDfromMean(length = 300, factor = 0.05)
    #Info.GradVol()
    Info.StayClosetoZero(factor=0.1, saferange=3, adjust=1.2)
    #Info.AppleV1(maxGain = 15, maxLoss = 10)
    Info.AppleV2(maxGain=100, maxLoss=50, TimeFrame=10000)
    # extremevol = 25

    # if Info.gradvar / 10 ** 9 > extremevol:       #If it is too volatile, we exit the market
    # Info.valuation_ask = Info.B_AskPrices[0] - 10
    # Info.valuation_bid = Info.B_BidPrices[0] + 10

    # Info.MovingAverage(length = 200, bidprice = aMarketEvent.bidDepth.prices[0],
    # askprice = aMarketEvent.askDepth.prices[0], eventbook = aEventBook)

    if len(Info.times) > 0:
        Info.FinalValuation()

    aValuationData.askValuation = Info.valuation_ask
    aValuationData.bidValuation = Info.valuation_bid

    return aValuationData
