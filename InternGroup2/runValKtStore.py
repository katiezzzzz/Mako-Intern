import numpy as np
import warnings


def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):
    Info = aValuationData.memoryData
    warnings.simplefilter('ignore', np.RankWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    Info.UpdateData(10 ** 5, aEventBook, aMarketEvent.askDepth.prices[0:3],
                    aMarketEvent.bidDepth.prices[0:3],
                    aMarketEvent.eventType, aMarketEvent.timestamp,
                    aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                    aSimulationData.simNetPnL, 0.1, 100, aSimulationData.simNetDelta)

    if aEventBook == 'baseBook' and Info.counter2 != 0:
        if Info.counter2 > 0:
            if aMarketEvent.askDepth.prices[0] < Info.PastAsk and aMarketEvent.bidDepth.volumes[0] < Info.PastBid:
                # sell
                Info.counter = -1
        if Info.counter2 < 0:
            if aMarketEvent.askDepth.prices[0] > Info.PastAsk and aMarketEvent.bidDepth.volumes[0] > Info.PastBid:
                Info.counter = 1

    Info.PastAsk = aMarketEvent.askDepth.volumes[0]
    Info.PastBid = aMarketEvent.bidDepth.volumes[0]

    if Info.counter != 10000:
        if Info.counter > 1:
            Info.counter = 1
        elif Info.counter < -1:
            Info.counter = -1

        if Info.counter != 0 and Info.book_amount[-1] != aSimulationData.simNetDelta:
            Info.counter = 0
            if Info.counter1 == 1:
                Info.counter1 = 2
            elif Info.counter1 == -1:
                Info.counter1 = -2
            elif Info.counter1 == 2 or Info.counter1 == -2:
                Info.counter1 = 0
        elif Info.counter < 1 and Info.counter > -1:
            Info.counter = 0
        elif Info.counter >= 1 and aSimulationData.simNetDelta == 5:
            Info.counter = 0
        elif Info.counter <= -1 and aSimulationData.simNetDelta == -5:
            Info.counter = 0


        #if Info.Ind == 1:
        #    Info.Ind = 2
        #elif Info.Ind == -1:
        #    Info.Ind = -2
        #elif Info.Ind == 2 or Info.Ind == -2:
        #    Info.Ind = 0

    #Info.TrackBGrad(length1=10, length2=300)
    #Info.TrackDGrad(length1=10, length2=300)
    length = 50

    if aEventBook == 'baseBook' and len(Info.BValList[Info.BValList != 0]) > length and len(Info.DValList[Info.DValList != 0]) > length:
        chris = 0.1
        Baverage = np.mean(Info.BValList[0: length], dtype=np.float64)
        Bstd = max(np.std(Info.BValList[0: length], dtype=np.float64), chris)
        Daverage = np.mean(Info.DValList[0: length], dtype=np.float64)
        Dstd = max(np.std(Info.DValList[0: length], dtype=np.float64), chris)
        n = ((Info.BValList[0] - Baverage) / Bstd)
        m = ((Info.DValList[0] - Daverage) / Dstd)

        Info.prev_n.insert(0, n)
        Info.prev_m.insert(0, m)

        if Info.counter == 10000:
            if abs(m) > 4 and max(Info.prev_n) < 1.5 and min(Info.prev_n) > -1.5:
                Info.counter = 0

        if Info.counter == 0:
            if len(Info.BValList) > length and len(Info.DValList) > length:
                k = 3

                if len(Info.prev_n) >= length:
                    Info.prev_n = Info.prev_n[0:length]

                if len(Info.prev_m) >= length:
                    Info.prev_m = Info.prev_m[0:length]

                if len(Info.prev_n) >= length / 2 and len(Info.prev_m) >= length / 2:
                    if m >= k:  #buy
                        if sum(np.array(Info.prev_n) > m) == 0:
                            Info.counter += 1
                            Info.prev_m = []
                            Info.prev_n = []
                    elif m <= -k:    #sell
                        if sum(np.array(Info.prev_n) < m) == 0:
                            Info.counter -= 1
                            Info.prev_m = []
                            Info.prev_n = []

                    elif sum(Info.prev_m) / len(Info.prev_m) > 1: #tracking trends
                        Info.counter = 1       #seems to revert more often than not
                        Info.counter1 = 1
                        Info.prev_m = []
                        Info.prev_n = []
                    elif sum(Info.prev_m) / len(Info.prev_m) < - 1: #trending down a lot
                        Info.counter = -1
                        Info.counter1 = -1
                        Info.prev_m = []
                        Info.prev_n = []

                #elif Info.counter1 == 0:    #trial mean reversion
                    #if n >= 4:  #sell and wait for a drop

                     #   Info.counter = -1
                     #   Info.counter1 = -1
                    #if n <= -4:  #buy and wait for a rise

                     #   Info.counter = 1
                      #  Info.counter1 = 1

    if Info.counter != 10000:
        #Info.DShortTrend(factor = 0.5, width=20)

        # Info.StayClosetoZero(saferange=2, factor = 0.3)

        # if aEventBook == 'baseBook':
        # Info.AppleV1(maxGain = 5, maxLoss = 5, AskPrice = aMarketEvent.askDepth.prices[0], BidPrice = aMarketEvent.bidDepth.prices[0])
        #Info.AppleV2(maxGain = 1000, maxLoss = 300, TimeFrame = 5000)

        #Info.MovingAverage(length = 200, eventbook = aEventBook)

        Info.AppleV4(maxGain = 25, maxLoss = 100, timespan = 10 ** 5,
                        PnL = aSimulationData.simNetPnL, time = aMarketEvent.timestamp)

        if Info.stopcounter == 0:
            Info.AppleV3(maxGain=250, maxLoss=1000, PnL=aSimulationData.simNetPnL)
        elif Info.stopcounter == 1:
            Info.AppleV3(maxGain = 200, maxLoss = 500, PnL = aSimulationData.simNetPnL)
        elif Info.stopcounter == 2:
            Info.AppleV3(maxGain = 150, maxLoss = 250, PnL = aSimulationData.simNetPnL)
        elif Info.stopcounter >= 3:
            Info.AppleV3(maxGain = 100, maxLoss = 100, PnL = aSimulationData.simNetPnL)

        if aEventBook == 'baseBook':
            if 1 > Info.counter > 0:   #maybe buy
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 0.15 * Info.counter
            elif -1 < Info.counter < 0:    #maybe sell
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] - 0.15 * Info.counter
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 5
            elif Info.counter >= 1:   #buy
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 2
            elif Info.counter <= -1:    #sell
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] - 2
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 5
            elif Info.counter == 0: #dont do anything
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 10
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 10

    if aEventBook == 'baseBook' and Info.counter == 10000:
        if aSimulationData.simNetDelta > 0:    #sell
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] - 10
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 5
        if aSimulationData.simNetDelta < 0:    #buy
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 10
        if aSimulationData.simNetDelta == 0:   #dont do anything
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 10
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 10

    #maybe a volatility measure to stop/limit trading?

    aValuationData.askValuation = Info.valuation_ask
    aValuationData.bidValuation = Info.valuation_bid

    if aEventBook == 'corrBook':
        if len(Info.prev_m) > 10:
            aValuationData.memoryData.testParam = sum(Info.prev_m) / len(Info.prev_m)

    return aValuationData
