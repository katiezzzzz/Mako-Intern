from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

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
    n = 0
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.eventType != 'MatchEventEnd':
            if myMarketEvent.timestamp < 1562332500000000000:
                askprice = np.append(askprice,myMarketEvent.askDepth.prices[0])
                AllAskPrice = np.append(AllAskPrice, myMarketEvent.askDepth.prices[0])
                timestamp = np.append(timestamp,myMarketEvent.timestamp)
                AllTimeStamp = np.append(AllTimeStamp,myMarketEvent.timestamp)
            else:
                break
        if len(askprice) == 1000 and n == 1:
            d = {'AskPrice': askprice, 'TimeStamp': timestamp}
            df = pd.DataFrame(data=d)
            df = df.dropna()
            train = df[:900]
            valid = df[900:]
            x_train = train.drop('AskPrice', axis=1)
            x_train_scaled = scaler.fit_transform(x_train)
            x_train = pd.DataFrame(x_train_scaled)
            y_train = train['AskPrice']
            x_valid = valid.drop('AskPrice', axis=1)
            x_valid_scaled = scaler.fit_transform(x_valid)
            x_valid = pd.DataFrame(x_valid_scaled)

            params = {'n_neighbors': [2, 7, 4, 2, 6, 7, 8, 9]}
            knn = neighbors.KNeighborsRegressor()
            model = GridSearchCV(knn, params, cv=5)
            model.fit(x_train, y_train)
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