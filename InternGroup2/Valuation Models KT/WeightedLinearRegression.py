import numpy as np
import matplotlib.pyplot as plt
from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import statsmodels.api as sm


try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

from memoryData import memoryData

def main():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()
    Info = memoryData()

    myFileStream = gzip.open('InternData/20190705_B.dat.gz', 'rb')

    myStatus = None
    AllAskPrice = np.array([])
    AllTimeStamp = np.array([])
    PredTime = np.array([])
    PredPrice = np.array([])
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.eventType != 'MatchEventEnd':
            if myMarketEvent.timestamp < 1562332500000000000:
                Info.UpdateDataB(10, myMarketEvent.askDepth.prices[0], myMarketEvent.bidDepth.prices[0],
                                 myMarketEvent.eventType, myMarketEvent.eventSide, myMarketEvent.timestamp,
                                 myMarketEvent.eventVolume)
                Info.BookValB(myMarketEvent.askDepth.volumes[0:3], myMarketEvent.bidDepth.volumes[0:3],
                              myMarketEvent.askDepth.prices[0:3], myMarketEvent.bidDepth.prices[0:3],
                              myMarketEvent.eventType, 0.2)
                AllAskPrice = np.append(AllAskPrice, myMarketEvent.askDepth.prices[0])
                AllTimeStamp = np.append(AllTimeStamp, myMarketEvent.timestamp)
            else:
                break

        if len(Info.B_times) == 10:
            x = Info.B_times
            y = Info.B_AskPrices
            w = np.ones(10)
            if np.isnan(x).any() or np.isnan(y).any():
                pass
            else:
                mod_wls = sm.WLS(y,x,weights=1/(w**2))
                res_wls = mod_wls.fit()
                TestTime = 2*Info.B_times[0] - Info.B_times[1]
                PredTime = np.append(PredTime,TestTime)
                TestPrice = res_wls.predict(TestTime)
                PredPrice = np.append(PredPrice,TestPrice)

    plt.plot(AllTimeStamp, AllAskPrice)
    plt.plot(PredTime, PredPrice, color='g')
    plt.show()

if __name__ == '__main__':
    main()

