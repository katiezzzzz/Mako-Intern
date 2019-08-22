from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

scaler = MinMaxScaler(feature_range=(0,1))

# Generate data
def main():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190705_B.dat.gz', 'rb')

    myStatus = None
    askprice = np.array([])
    timestamp = np.array([])
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.timestamp < 1562332500000000000:
            askprice = np.append(askprice,myMarketEvent.askDepth.prices[0])
            timestamp = np.append(timestamp,myMarketEvent.timestamp)
        else:
            break
    return (askprice,timestamp)

# Plots to demonstrate stationarity
def test_stationarity(x,y):
    # Determing rolling statistics
    rolmean = y.rolling(window=12).mean()
    rolstd = y.rolling(window=12).std()

    # Plot rolling statistics:
    orig = plt.plot(x,y, color='blue', label='Original')
    mean = plt.plot(x,rolmean, color='red', label='Rolling Mean')
    std = plt.plot(x,rolstd, color='black', label='Rolling Std')

    plt.ylim(-0.0002,0.0002)
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

data = main()
askprice = data[0]
askprice = pd.DataFrame(askprice)
timestamp = data[1]
askprice_log = np.log(askprice)
moving_avg = askprice_log.rolling(200).mean()                       # moving average

# exponentially weighted moving average
expwighted_avg = askprice_log.ewm(halflife=200).mean()                      # halflife defines the amount of exponential decay

askprice_log_moving_avg_diff = askprice_log - moving_avg
askprice_log_moving_avg_diff = askprice_log_moving_avg_diff.iloc[200:]
askprice_log_ewm_diff = askprice_log - expwighted_avg
askprice_log_ewm_diff = askprice_log_ewm_diff.iloc[:,0].values

d = {'AskPrice':askprice_log_ewm_diff,'TimeStamp':timestamp}
df = pd.DataFrame(data=d)
df.dropna()
df = df[df.AskPrice != 0]

timestamp_model = df['TimeStamp']
askprice_model = df['AskPrice']
timestamp_model = timestamp_model.values
askprice_model = askprice_model.values
askprice_model = askprice_model**2

print('Results of Dickey-Fuller Test:')
dftest = adfuller(askprice_model, autolag='AIC')
dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
print(dfoutput)
