import numpy as np
import pandas as pd


def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):

    Info = aValuationData.memoryData

    ImChris = aParameters
    prev_data = aValuationData.memoryData.RegressionData

    if ImChris.params == 0:
        ImChris.data_col()
        ImChris.regression_testing()
        ImChris.params=1



    new_event=False
    # TKAP: aEventBook is either 'baseBook' or 'corrBook'
    if aEventBook == 'baseBook':
        # Info.UpdateDataB(aMarketEvent.askDepth.prices[0], aMarketEvent.bidDepth.prices[0], aMarketEvent.eventType,
        # aMarketEvent.eventSide, aMarketEvent.timestamp, aMarketEvent.eventVolume, aMarketEvent.aggressorSide)
        if aMarketEvent.eventType.lower() == 'trade':
            prev_data.data[aMarketEvent.timestamp] = [aMarketEvent.eventPrice, prev_data.last_price_d,
                                                      aMarketEvent.askDepth.prices[0] - aMarketEvent.bidDepth.prices[0],
                                                      aMarketEvent.aggressorSide * aMarketEvent.eventVolume]
            if len(prev_data.data.keys()) > 20:
                print(prev_data.data.pop(min(prev_data.data.keys())))
                new_event = True
    if aEventBook == 'corrBook':
        # Info.UpdateDataD(aMarketEvent.askDepth.prices[0], aMarketEvent.bidDepth.prices[0], aMarketEvent.eventType,
        # aMarketEvent.eventSide, aMarketEvent.timestamp)
        if aMarketEvent.eventType.lower() == 'trade':
            prev_data.last_price_d = aMarketEvent.eventPrice

    if len(prev_data.data.keys()) >= 15:
        ImChris.data.index = pd.to_numeric(ImChris.data.index)
        last_index = ImChris.data.index[-1]
        prev_data.dataframe = pd.DataFrame(prev_data.data).transpose()
        prev_data.dataframe.columns = ['B', 'D', 'B_spread', 'Dir_vol']
        prev_data.dataframe['B_fd'] = prev_data.dataframe['B'] - prev_data.dataframe['B'].shift(1)
        prev_data.dataframe['D_fd'] = prev_data.dataframe['D'] - prev_data.dataframe['D'].shift(1)
        prev_data.dataframe['B_prev'] = prev_data.dataframe['B']
        prev_data.dataframe['D_fd_prev'] = prev_data.dataframe['D_fd'].shift(1)
        prev_data.dataframe['D_prev'] = prev_data.dataframe['D'] - prev_data.dataframe['D'].shift(1)
        prev_data.dataframe['dir_vol_roll_prev'] = prev_data.dataframe['Dir_vol'].rolling(5).sum()
        prev_data.dataframe.dropna(inplace=True)
        prev_data.dataframe['index'] = 0
        for x in range(len(prev_data.dataframe)):
            prev_data.dataframe['index'].iloc[x] = last_index-10+x+1
        prev_data.dataframe.set_index('index',inplace=True,drop=True)
        prev_data.dataframe.index = pd.to_datetime(prev_data.dataframe.index)
        for col in prev_data.dataframe.columns:
            if col not in ['B_fd','D','B_spread','dir_vol_roll_prev','B_prev','B']:
                prev_data.dataframe.drop(col, axis=1, inplace=True)
        for x in range(1,6):
            for y in ['B_prev','D_fd','B_spread','dir_vol_roll_prev']:
                prev_data.dataframe[y + ' shift '+str(x)] = prev_data.dataframe[y].shift(x)
        prev_data.dataframe.dropna(inplace=True)
        ImChris.dataUpdate(prev_data.dataframe)
        ImChris.data.index = pd.to_datetime(ImChris.data.index)
        ImChris.prediction()
        valuation = ImChris.data['prediction'][-1]
        Info.next_valuation(valuation)

        aValuationData.bidValuation = Info.valuation_bid
        aValuationData.askValuation = Info.valuation_ask

        print(Info.valuation_ask)
        print(Info.valuation_bid)
    else:
        aValuationData.bidValuation = Info.B_BidPrices[0] - 1
        aValuationData.askValuation = Info.B_AskPrices[0] + 1

    aValuationData.memoryData.testParam = aValuationData.askValuation

    return aValuationData


import numpy as np
import pandas as pd
import warnings


def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):
    Info = aValuationData.memoryData
    warnings.simplefilter('ignore', np.RankWarning)
    Info.UpdateData(10 ** 5, 10 ** 8, 200, aEventBook, aMarketEvent.askDepth.prices[0:3],
                    aMarketEvent.bidDepth.prices[0:3],
                    aMarketEvent.eventType, aMarketEvent.timestamp,
                    aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                    aSimulationData.simNetPnL, 0.5)

    if Info.counter != 10000:
        if Info.counter > 1:
            Info.counter = 1
        elif Info.counter < -1:
            Info.counter = -1

        if Info.counter != 0 and Info.cheese_amount != aSimulationData.simNetDelta:
            Info.counter = 0
        elif Info.counter < 1 and Info.counter > -1:
            Info.counter = 0
        elif Info.counter >= 1 and Info.book_amount == 5:
            Info.counter = 0
        elif Info.counter <= -1 and Info.book_amount == -5:
            Info.counter = 0
        elif Info.counter == 0 and Info.counter1 != 0 and Info.book_amount != aSimulationData.simNetDelta:
            Info.counter1 = 0

        #if Info.Ind == 1:
        #    Info.Ind = 2
        #elif Info.Ind == -1:
        #    Info.Ind = -2
        #elif Info.Ind == 2 or Info.Ind == -2:
        #    Info.Ind = 0

    Info.UpdateBookAmounts(aSimulationData.simNetDelta, Info.book_amount, aMarketEvent.askDepth.prices[0],
                           aMarketEvent.bidDepth.prices[0])
    Info.cheese_amount = Info.book_amount
    Info.book_amount = aSimulationData.simNetDelta

    #Info.TrackBGrad(length1=10, length2=300)
    #Info.TrackDGrad(length1=10, length2=300)

    length = 100
    if aEventBook == 'baseBook' and len(Info.BValList) > length and len(Info.DValList) > length:
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
            if abs(m) > 5 and max(Info.prev_n) < 1 and min(Info.prev_n) > -1:
                Info.counter = 0

        if Info.counter == 0:
            if len(Info.BValList) > length and len(Info.DValList) > length:
                k = 2
                if len(Info.prev_n) >= length:
                    Info.prev_n = Info.prev_n[0:length]

                if len(Info.prev_m) >= length:
                    Info.prev_m = Info.prev_m[0:length]

                if m >= k:  #buy
                    if sum(np.array(Info.prev_n) > 2 * m / 3) == 0:
                        Info.counter += 1
                        Info.prev_m = []
                        Info.prev_n = []
                elif m <= -k:    #sell
                    if sum(np.array(Info.prev_n) < 2 * m / 3) == 0:
                        Info.counter -= 1
                        Info.prev_m = []
                        Info.prev_n = []

    #if aEventBook == 'baseBook':
        #if Info.counter == 0 and Info.counter1 == 0:
        #    if n >= 5:
        #        Info.counter -= 1
        #        Info.counter1 = 1
        #    elif n <= 5:
        #        Info.counter += 1
        #        Info.counter1 = 1

    if Info.counter != 10000:
        #Info.DShortTrend(factor = 0.5, width=80)    # 0.08 seconds of data

        # Info.BLongTrend(frequency=10000, length=20, factor=5, width=3)    # 10 seconds of data, takes the last 3

        # Info.StayClosetoZero(saferange=2, factor = 0.3)

        # if aEventBook == 'baseBook':
        # Info.AppleV1(maxGain = 5, maxLoss = 5, AskPrice = aMarketEvent.askDepth.prices[0], BidPrice = aMarketEvent.bidDepth.prices[0])
        #Info.AppleV2(maxGain = 1000, maxLoss = 300, TimeFrame = 5000)

        #Info.MovingAverage(length = 200, bidprice = aMarketEvent.bidDepth.prices[0],
         #                    askprice = aMarketEvent.askDepth.prices[0], eventbook = aEventBook)
        if Info.stopcounter == 0:
            Info.AppleV3(maxGain=250, maxLoss=1000, PnL=aSimulationData.simNetPnL)
        elif Info.stopcounter == 1:
            Info.AppleV3(maxGain = 200, maxLoss = 1000, PnL = aSimulationData.simNetPnL)
        elif Info.stopcounter == 2:
            Info.AppleV3(maxGain = 150, maxLoss = 1000, PnL = aSimulationData.simNetPnL)
        elif Info.stopcounter >= 3:
            Info.AppleV3(maxGain = 100, maxLoss = 100, PnL = aSimulationData.simNetPnL)

        if aEventBook == 'baseBook':
            if Info.counter < 1 and Info.counter > 0:   #maybe buy
                Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
                Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 0.15 * Info.counter
            elif Info.counter > -1 and Info.counter < 0:    #maybe sell
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
        if Info.book_amount > 0:    #sell
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] - 10
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 5
        if Info.book_amount < 0:    #buy
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 5
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] + 10
        if Info.book_amount == 0:   #dont do anything
            Info.valuation_bid = aMarketEvent.bidDepth.prices[0] - 10
            Info.valuation_ask = aMarketEvent.askDepth.prices[0] + 10

    aValuationData.askValuation = Info.valuation_ask
    aValuationData.bidValuation = Info.valuation_bid

    if aEventBook == 'corrBook' :
        aValuationData.memoryData.testParam = aMarketEvent.askDepth.prices[0]

    return aValuationData
