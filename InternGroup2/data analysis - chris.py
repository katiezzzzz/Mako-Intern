from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import pandas as pd
import pickle
import statsmodels.tsa.stattools as ts
import numpy as np

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto


def producing_dataframe():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()
    data = []
    #
    myFileStream = gzip.open('InternData/20190710_B.dat.gz', 'rb')
    myStatus = None
    while not myStatus and myMarketEvent.timestamp < 1562765000000000000:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.eventType.lower() == 'trade':
            data.append([myMarketEvent.timestamp, myMarketEvent.eventPrice])
            #print([myMarketEvent.timestamp, myMarketEvent.eventPrice])
    df = pd.DataFrame(data, columns=['Time', 'B'])
    df.set_index('Time',inplace=True)
    df.index = pd.to_numeric(df.index)
    for x in ['A', 'C', 'D', 'E', 'F', 'G', 'H']:
        myFileStream = gzip.open('InternData/20190710_' + x + '.dat.gz', 'rb')
        last_price = {'A':1400 ,'B':7780 ,'C':15 ,'D': 2970,'E':2.39 ,'F': 57.7,'G':1.25 ,'H':1.127 }
        last_time = {'A': 0,'B':0 ,'C':0 ,'D':0 ,'E':0 ,'F':0 ,'G':0 ,'H':0 }
        df[x] = last_price[x]
        myStatus = None
        while not myStatus and myMarketEvent.timestamp < 1562765000000000000:
            myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
            if myMarketEvent.eventType.lower()=='trade':
                df_temp = df[(df.index>=last_time[x])&(df.index<=myMarketEvent.timestamp)]
                for times in df_temp.index:
                    time_gap_lower = times - last_time[x]
                    time_gap_upper = myMarketEvent.timestamp-times
                    if time_gap_upper+time_gap_lower>0:
                        df.at[times,x] = (1-((time_gap_lower)/(myMarketEvent.timestamp-last_time[x])))*last_price[x]+((time_gap_lower)/(myMarketEvent.timestamp-last_time[x]))*myMarketEvent.eventPrice
                        df_temp.at[times,x] =(1-((time_gap_lower)/(myMarketEvent.timestamp-last_time[x])))*last_price[x]+((time_gap_lower)/(myMarketEvent.timestamp-last_time[x]))*myMarketEvent.eventPrice
                        #print(df[x].loc[times])
                    else:
                        df.at[times,x] = myMarketEvent.eventPrice
                        df_temp.at[times, x] = myMarketEvent.eventPrice
                last_price[x] = int(myMarketEvent.eventPrice)
                last_time[x] = int(myMarketEvent.timestamp)
    print(df.head())
    print(df.tail())
    print(df.corr(method='pearson'))
    ts.grangercausalitytests(df[['A','C']],maxlag=100,verbose=True)
    #print(gr_a_c)
    ts.grangercausalitytests(df[['B','D']],maxlag=100,verbose=True)
    #print(gr_b_d)
    ts.grangercausalitytests(df[['A','F']],maxlag=100,verbose=True)
    #print(gr_a_f)
    with open('chris_data.pickle', 'wb') as f:
        pickle.dump(df, f)
    print(df.index.max())
    print(df.index.min())


def correlation():
    df = pd.read_pickle('chris_data.pickle')
    df.set_index('Time')
    df.corr()

if __name__ == '__main__':
    producing_dataframe()
    #correlation()