from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

# Generate data
def main():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190705_B.dat.gz', 'rb')

    myStatus = None
    AllAskPrice = np.array([])
    AllTimeStamp = np.array([])
    askprice = np.array([])
    timestamp = np.array([])
    model = LinearRegression()
    n = 0
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.eventType != 'MatchEventEnd':
            askprice = np.append(askprice,myMarketEvent.askDepth.prices[0])
            AllAskPrice = np.append(AllAskPrice, myMarketEvent.askDepth.prices[0])
            timestamp = np.append(timestamp,myMarketEvent.timestamp)
            AllTimeStamp = np.append(AllTimeStamp,myMarketEvent.timestamp)
        if len(askprice) == 1000 and n == 1:
            d = {'AskPrice': askprice, 'TimeStamp': timestamp}
            df = pd.DataFrame(data=d)
            df = df.dropna()
            train = df[:900]
            valid = df[900:]
            x_train = train.drop('AskPrice', axis=1)
            y_train = train['AskPrice']
            x_valid = valid.drop('AskPrice', axis=1)
            model.fit(x_train, y_train)
            print(x_valid)
            preds = model.predict(x_valid)
            valid.insert(2, 'Predictions', preds)
            plt.plot(valid['TimeStamp'], valid['Predictions'], color='g')
            n = 0
        if len(askprice) > 1000:
            askprice = np.delete(askprice, range(0,101))
            timestamp = np.delete(timestamp, range(0,101))
            n += 1


    print(len(AllTimeStamp))
    plt.plot(AllTimeStamp,AllAskPrice)
    plt.show()

main()
'''
d = {'AskPrice':data[0],'TimeStamp':data[1]}
df = pd.DataFrame(data=d)
df = df.dropna()
df = df[df.AskPrice != 0]
train = df[:14000]
valid = df[14000:]

x_train = train.drop('AskPrice',axis=1)
y_train = train['AskPrice']
x_valid = valid.drop('AskPrice',axis=1)
y_valid = valid['AskPrice']

model = LinearRegression()
model.fit(x_train,y_train)

# plot
preds = model.predict(x_valid)
valid.insert(2,'Predictions',preds)
plt.plot(df['TimeStamp'],df['AskPrice'])
plt.plot(valid['TimeStamp'],valid['Predictions'])
plt.show()
'''