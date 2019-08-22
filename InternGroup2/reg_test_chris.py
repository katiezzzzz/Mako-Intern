from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import linear_model as lm


try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

class Regression:

    def __init__(self):
        self.results = 0
        self.data = 0
        self.model = 0
        self.params = 0

    def dataUpdate(self, Input):
        #for x in range(len(Input)):
        #    self.data.drop(self.data.index[-(x+1)], inplace=True)
        self.data = Input

    def data_col(self):
        times = {}
        # last_price_b = np.nan
        last_price_d = -1
        for future in ['D', 'B']:
            myMarketEvent = internMarketData.marketEvent()
            myPurePythonInternMarketData = internData_pb2.MarketData()
            myInternMarketData = internData_proto.MarketData()
            myFileStream = gzip.open(
                'H:\InternGroup2\InternData/20190710_' + str(future) + '.dat.gz', 'rb')
            myStatus = None
            while not myStatus and myMarketEvent.timestamp < 1562765000000000000:
                myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData,
                                                          myFileStream)
                if myMarketEvent.eventType.lower() == 'trade':
                    if future == 'D':
                        times[myMarketEvent.timestamp] = [-1, myMarketEvent.eventPrice, 0, 0]
                        if last_price_d == -1:
                            last_price_d = myMarketEvent.eventPrice
                    if future == 'B':
                        times[myMarketEvent.timestamp] = [myMarketEvent.eventPrice, -1,
                                                          myMarketEvent.askDepth.prices[0] -
                                                          myMarketEvent.bidDepth.prices[0],
                                                          myMarketEvent.aggressorSide * myMarketEvent.eventVolume]
                        if myMarketEvent.eventPrice < 7000 or myMarketEvent.eventPrice > 8500:
                            print(myMarketEvent.eventPrice)
                        # if last_price_b == -1:
                        #   last_price_b = myMarketEvent.eventPrice
                    # print([myMarketEvent.timestamp, myMarketEvent.eventPrice])
        l = list(times.keys())
        l.sort()
        for time in l:
            if times[time][0] == -1:
                times[time][0] = np.nan
                last_price_d = times[time][1]
            if times[time][1] == -1:
                times[time][1] = last_price_d
                # last_price_b = times[time][0]
        df = pd.DataFrame(times).transpose()
        df.columns = ['B', 'D', 'B_spread', 'Dir_vol']
        df = df.dropna()
        df['B_fd'] = df['B'] - df['B'].shift(1)
        df['D_fd'] = df['D'] - df['D'].shift(1)
        df['B_prev'] = df['B'].shift(1)
        df['D_fd_prev'] = df['D_fd'].shift(1)
        df['D_prev'] = df['D'] - df['D'].shift(1)
        df['dir_vol_roll_prev'] = df['Dir_vol'].rolling(5).sum()
        df['next_5_prices'] = df['B'].shift(-5).rolling(5).mean()
        df = df.dropna()
        for col in df.columns:
            if col not in ['B_prev','D_fd','B_spread','dir_vol_roll_prev','next_5_prices']:
                df.drop(col,axis=1,inplace=True)
        df['index'] = 0
        for x in range(len(df)):
            df.at[df.index[x],'index'] = x
        df.set_index('index',inplace=True,drop=True)
        df.index = pd.to_datetime(df.index)
        for x in range(1,6):
            for y in ['B_prev','D_fd','B_spread','dir_vol_roll_prev']:
                df[y + ' shift '+str(x)] = df[y].shift(x)
        df.dropna(inplace=True)
        self.data = df

    def regression_testing(self):

        n_min = 0
        aic_min = 99999
        #for n in range(1,10):
        #    model = sm.tsa.statespace.SARIMAX(df['next_5_prices'],order=(n,1,n),exog=df[['D_prev','B_spread','dir_vol_roll_prev']],enforce_invertibility=False,enforce_stationarity=False,trend='c')
        #    results = model.fit()
        #    aic = results.aic
        #    if aic<aic_min:
        #        n_min = n
        #        aic_min = aic
        X = self.data
        y = X['next_5_prices']
        X.drop('next_5_prices',axis=1,inplace=True)
        self.model = lm.LinearRegression()
        self.results = self.model.fit(X,y)

        print(self.results.coef_)


    def graph_compare(self):
        self.data['prediction'] = self.results.predict()
        for x in range(5):
            self.data['prediction'].iloc[x] = self.data['B_prev'].iloc[x]
        plt.scatter(self.data['next_5_prices'],self.data['prediction'])
        plt.show()

    def results_sum(self):
        pass

    def prediction(self):
        try:
            self.data.drop('next_5_prices',inplace = True,axis = 1)
        except:
            pass
        self.data['prediction'] = self.results.predict(self.data)



if __name__ == '__main__':
    my_reg = Regression()
    my_reg.data_col()
    my_reg.regression_testing()
    my_reg.results_sum()
    #my_reg.graph_compare()
    my_reg.prediction()

    my_reg.prediction()
