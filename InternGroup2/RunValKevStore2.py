import numpy as np


def runValuation(aValuationData, aSimulationData, aMarketEvent, aEventBook, aBaseTickSize, aCorrTickSize, aParameters):
    Info = aValuationData.memoryData

    # TKAP: aEventBook is either 'baseBook' or 'corrBook'
    if aEventBook == 'baseBook':
        Info.UpdateDataB(10000, AskPrice=aMarketEvent.askDepth.prices[0], BidPrice=aMarketEvent.bidDepth.prices[0],
                         eventType=aMarketEvent.eventType,
                         eventSide=aMarketEvent.eventSide, eventTime=aMarketEvent.transactTime,
                         eventVolume=aMarketEvent.eventVolume)

        Info.BookValB(aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                      aMarketEvent.askDepth.prices[0:3], aMarketEvent.bidDepth.prices[0:3], aMarketEvent.eventType, 0.25)
        # To call the book depth valuation, use Info.BookDepthVal

        np.insert(Info.pnlStore, 0, aSimulationData.simNetPnL, axis=0)
        # updates the pnl for Scalp V2

        Info.UpdateBookAmounts(aSimulationData.simNetDelta, Info.book_amount, Info.valuation_bid, Info.valuation_ask)
        Info.book_amount = aSimulationData.simNetDelta
        # updates the amounts for ScalpV1

    if aEventBook == 'corrBook':
        Info.UpdateDataD(aMarketEvent.askDepth.prices[0], aMarketEvent.bidDepth.prices[0], aMarketEvent.eventType,
                         aMarketEvent.eventSide, aMarketEvent.timestamp)

        Info.BookValD(aMarketEvent.askDepth.volumes[0:3], aMarketEvent.bidDepth.volumes[0:3],
                      aMarketEvent.askDepth.prices[0:3], aMarketEvent.bidDepth.prices[0:3], aMarketEvent.eventType, 0.25)

    if len(Info.BValatTrade) > 500:
        Info.UpdateTime()
        RegLength = 500
        x = Info.newtimes[0:RegLength]
        y = Info.BValList[0:RegLength]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        next_time = Info.newtimes[0] * 2 - Info.newtimes[1]  # input the next time required here
        Info.valuation = p(next_time)
        # adjust the ask and bid below

        # Info.nSDfromMean(length=50, factor=0.12) #puts pressure based on the no. of standard deviations out from the mean
        # Info.vol is the variance of the prices
        # Info.TrackGrad(length = 100)
        # Info.GradVol()                  #Info.gradvar is an estimate of how shaky the gradients are

        # factor = (1 - np.exp(-Info.gradvar)) * 0.25         #as vol increases, we want to stay closer to zero

        # Info.DontDoAnything()
        Info.StayClosetoZero(factor=0.1, saferange=2,
                             adjust=1.2)  # If position is too long/short, drags it back in to stay safer
        # Info.DTrend(length=5, factor=0.1)  # If there is a trend in D, checks if same trend is in B
        # Info.TrackBTrend(factor=0.05, howpositive=5, length=6)  # If B is increasing, chances are that it will increase again
        # Info.ScalpV1(maxLoss = 2, maxGain = 5)  # Buys/Sells once we've reached maxLoss/maxGain
        Info.ScalpV2(maxLoss = 50, maxGain = 100, TimeFrame = 30)  #Buys/sells once we've had enough of a pnlChange

        Info.FinalValuation()  # Round the ask and the bid

        aValuationData.bidValuation = Info.valuation_bid
        aValuationData.askValuation = Info.valuation_ask

        Info.EventNo += 1

    else:
        aValuationData.bidValuation = Info.B_BidPrices[0] - 1
        aValuationData.askValuation = Info.B_AskPrices[0] + 1

    aValuationData.memoryData.testParam1 = Info.EventNo
    return aValuationData
