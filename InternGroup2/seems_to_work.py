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

    if Info.counter != 0 and Info.book_amount != aSimulationData.simNetDelta:  # waits 50 steps to make sure the trade is done
        Info.counter = 0
        if Info.shortInd == 1:
            Info.shortInd = 2
        if Info.avgInd == 1:
            Info.avgInd = 2
        if Info.avgInd == -1:
            Info.avgInd = -2
        if Info.avgInd == 2 or Info.avgInd == -2:
            Info.avgInd = 0
    elif Info.counter >= 1000:
        Info.counter = 0
        Info.avgInd = 0
        Info.shortInd = 0
    else:
        Info.counter += 1

    Info.UpdateBookAmounts(aSimulationData.simNetDelta, Info.book_amount, Info.valuation_ask, Info.valuation_bid)
    Info.book_amount = aSimulationData.simNetDelta

    Info.TrackBGrad(length1 = 10, length2 = 300)
    Info.TrackDGrad(length1 = 10, length2 = 300)
    length = 300
    if Info.counter == 0:
        Info.valuation_bid = Info.B_BidPrices[0] - 2
        Info.valuation_ask = Info.B_AskPrices[0] + 2

    if Info.counter != 0 and Info.book_amount != aSimulationData.simNetDelta:  #locks in a trade
        Info.counter = 0

    if Info.counter == 0 and len(Info.Bgrad) > 2 and aEventBook=='baseBook':
        if len(Info.Bgrad) > 5 and len(Info.Dgrad) > 5:
            Baverage = np.mean(Info.BValList[0: length], dtype=np.float64)
            Bstd = np.std(Info.BValList[0: length], dtype=np.float64)
            Daverage = np.mean(Info.DValList[0: length], dtype=np.float64)
            Dstd = np.std(Info.DValList[0: length], dtype=np.float64)
            n = ((Info.BValList[0] - Baverage) / Bstd)
            m = ((Info.DValList[0] - Daverage) / Dstd)

            if len(Info.prev_n) >= 20:
                Info.prev_n.pop(0)
                Info.prev_n.append(n)
            else:
                Info.prev_n.append(n)

            if len(Info.prev_m) >= 20:
                Info.prev_m.pop(0)
                Info.prev_m.append(m)
            else:
                Info.prev_m.append(m)

            m_greater = False
            if m >= 1.5:
                m_greater = True
                for x in Info.prev_n:
                    if x > 2*m / 3:
                        m_greater = False
            else:
                if m <= -1.5:
                    m_greater = True
                    for x in Info.prev_n:
                        if x < 2*m / 3:
                            m_greater = False

            if m_greater == True:
                if m < 0:
                    Info.valuation_ask = aMarketEvent.bidDepth.prices[0]
                    Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 1
                    set_value = True
                    Info.counter=1
                elif m > 0:
                    Info.valuation_bid = aMarketEvent.askDepth.prices[0]
                    Info.valuation_ask = aMarketEvent.askDepth.prices[0]
                    set_value = True
                    Info.counter=1
    if max(Info.prev_m)>1.5 and max(Info.prev_n)<1 and Info.counter!=0:
        Info.valuation_ask += 0.25
        Info.valuation_bid -= 0.25
        set_value = True
    if min(Info.prev_m)<-1.5 and min(Info.prev_n)>-1 and Info.counter!=0:
        Info.valuation_ask += 0.25
        Info.valuation_bid -= 0.25
        set_value = True


    #Info.DShortTrend(frequency=10, length=8, factor=0.3)    # 0.08 seconds of data
    #Info.DLongTrend(frequency=100000, length=50, factor=12)    # 10 seconds of data, takes the last 3
    #Info.nSDfromMean(length = 300, factor = 0.05)
    #Info.GradVol()
    #Info.StayClosetoZero(factor=0.1, saferange=2, adjust=1.2)
    #Info.ScalpV1(maxGain = 15, maxLoss = 10)
    Info.AppleV2(maxGain=100, maxLoss=50, TimeFrame=10000)
    #extremevol = 25

    #if Info.gradvar / 10 ** 9 > extremevol:       #If it is too volatile, we exit the market
        #Info.valuation_ask = Info.B_AskPrices[0] - 10
        #Info.valuation_bid = Info.B_BidPrices[0] + 10

    #Info.MovingAverage(length = 200, bidprice = aMarketEvent.bidDepth.prices[0],
                       #askprice = aMarketEvent.askDepth.prices[0], eventbook = aEventBook)

    if len(Info.times) > 0:
        Info.FinalValuation()

    aValuationData.askValuation = Info.valuation_ask
    aValuationData.bidValuation = Info.valuation_bid
    aValuationData.memoryData.testParam1 = len(Info.SellFuture)
    aValuationData.memoryData.testParam2 = len(Info.BuyFuture)

    return aValuationData