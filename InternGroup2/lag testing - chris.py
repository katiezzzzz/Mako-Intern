from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import pandas as pd
import pickle
import statsmodels.tsa.stattools as ts
import numpy as np
from statsmodels.tsa.arima_model import ARIMA,ARIMAResults
from datetime import datetime

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto


def causality_testing():
    times = {}
    last_price_b = -1
    last_price_d = -1
    for future in ['B','D']:
        myMarketEvent = internMarketData.marketEvent()
        myPurePythonInternMarketData = internData_pb2.MarketData()
        myInternMarketData = internData_proto.MarketData()
        myFileStream = gzip.open('InternData/20190710_'+str(future)+'.dat.gz', 'rb')
        myStatus = None
        while not myStatus and myMarketEvent.timestamp < 1562765000000000000:
            myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
            if myMarketEvent.eventType.lower() == 'trade':
                if future == 'D':
                    times[myMarketEvent.timestamp] = [-1,myMarketEvent.eventPrice]
                    if last_price_d == -1:
                        last_price_d = myMarketEvent.eventPrice
                if future == 'B':
                    times[myMarketEvent.timestamp] = [myMarketEvent.eventPrice, -1]
                    if last_price_b == -1:
                        last_price_b = myMarketEvent.eventPrice
                #print([myMarketEvent.timestamp, myMarketEvent.eventPrice])
    for time in times.keys():
        if times[time][0] == -1:
            times[time][0] = last_price_b
            last_price_d = times[time][1]
        if times[time][1]==-1:
            times[time][1] = last_price_d
            last_price_b = times[time][0]
    df = pd.DataFrame(times).transpose()
    df.columns = ['B','D']
    df.index = pd.to_datetime(df.index)
    #ts.grangercausalitytests(df[['D','B']],maxlag=100,verbose=True)
    model = ARIMA(endog=df['D'],order = (10,1,10),exog=df['B'])
    results = model.fit()
    #ARIMAResults

if __name__ == '__main__':
    causality_testing()