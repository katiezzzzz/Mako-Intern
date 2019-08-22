import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):
    Info = aValuationData.memoryData
    # TKAP: aEventBook is either 'baseBook' or 'corrBook'
    if aEventBook == 'baseBook':
        Info.UpdateDataB(10, aMarketEvent.askDepth.prices[0], aMarketEvent.bidDepth.prices[0], aMarketEvent.eventType,
                              aMarketEvent.eventSide, aMarketEvent.timestamp, aMarketEvent.eventVolume)
        Info.BookVal(aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                    aMarketEvent.askDepth.prices[0:3], aMarketEvent.bidDepth.prices[0:3], 0.5)

        Info.UpdateBookAmounts(aSimulationData.simNetDelta, Info.book_amount, Info.valuation_bid, Info.valuation_ask)
        Info.book_amount = aSimulationData.simNetDelta

    if aEventBook == 'corrBook':
        Info.UpdateDataD(aMarketEvent.askDepth.prices[0], aMarketEvent.bidDepth.prices[0], aMarketEvent.eventType,
                              aMarketEvent.eventSide, aMarketEvent.timestamp)


    if len(Info.B_AskPrices) == 10:
        Info.valuation_ask = np.mean(Info.B_AskPrices)
        Info.valuation_bid = np.mean(Info.B_BidPrices)
        aValuationData.askValuation = min(Info.valuation_ask, Info.B_AskPrices[0] + 0.25)
        aValuationData.bidValuation = max(Info.valuation_bid, Info.B_BidPrices[0] - 0.25)
    else:
        aValuationData.bidValuation = Info.B_BidPrices[0] - 1
        aValuationData.askValuation = Info.B_AskPrices[0] + 1

    return aValuationData
