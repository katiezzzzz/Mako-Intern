from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import matplotlib.pyplot as plt
import numpy as np

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

factorlist = np.array([1, 0.1, (0.1 ** 2)])

def main1():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190711_B.dat.gz', 'rb')

    myStatus = None
    book = []
    timestamp = []
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        BookValue = (np.dot(np.array(myMarketEvent.askDepth.prices[:3]), factorlist * np.array(myMarketEvent.bidDepth.volumes[:3]))
         + np.dot(np.array(myMarketEvent.bidDepth.prices[:3]), factorlist * np.array(myMarketEvent.askDepth.volumes[:3]))) / np.sum(
            factorlist * (np.array(myMarketEvent.askDepth.volumes[:3]) + np.array(myMarketEvent.bidDepth.volumes[:3])))
        book.append(BookValue)
        timestamp.append(myMarketEvent.timestamp)
    book.reverse()
    timestamp.reverse()
    return (book),(timestamp)

def main2():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190711_D.dat.gz', 'rb')

    myStatus = None
    book = []
    timestamp = []
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        BookValue = (np.dot(np.array(myMarketEvent.askDepth.prices[:3]),
                            factorlist * np.array(myMarketEvent.bidDepth.volumes[:3]))
                     + np.dot(np.array(myMarketEvent.bidDepth.prices[:3]),
                              factorlist * np.array(myMarketEvent.askDepth.volumes[:3]))) / np.sum(
            factorlist * (np.array(myMarketEvent.askDepth.volumes[:3]) + np.array(myMarketEvent.bidDepth.volumes[:3])))
        book.append(BookValue)
        timestamp.append(myMarketEvent.timestamp)
    book.reverse()
    timestamp.reverse()
    return (book),(timestamp)


if __name__ == '__main__':
    Data1 = main1()
    Data2 = main2()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(Data1[1], Data1[0],color='blue')
    ax1.set_ylabel('Nasdaq Book Values')

    ax2 = ax1.twinx()
    ax2.plot(Data2[1], Data2[0],'r-',color='purple')
    ax2.set_ylabel('S&P Book Values',color='purple')
    for t1 in ax2.get_yticklabels():
        t1.set_color('purple')

    plt.savefig('0711 B,D Compare')
    plt.show()
