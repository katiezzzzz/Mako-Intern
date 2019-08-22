from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import matplotlib.pyplot as plt
from memoryData import memoryData

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

my_path = 'H:/InternGroup2/Storage/'
'''
n = list(range(8,10))
letters = ['A','B','C','D','E','F','G','H']
for j in letters:

File = 'InternData/20190705_' + j + '.dat.gz'
'''
Info = memoryData

def main1():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190709_B.dat.gz', 'rb')

    myStatus = None
    askprice = []
    timestamp = []
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)

        if myMarketEvent.timestamp < 1562679500000000000:
            Info.UpdateDataB(timespan = 1000, totaltime = 10 ** 9, myMarketEvent.askDepth.prices[0:3], myMarketEvent.bidDepth.prices[0:3]
                             myMarketEvent.eventType, myMarketEvent.eventSide, myMarketEvent.timestamp, myMarketEvent.askDepth.volumes[0:3]
                                myMarketEvent.bidDepth.volumes[0:3], factor = 0.1)
        else:
            break
    askprice.reverse()
    timestamp.reverse()
    return (askprice),(timestamp)

def main2():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190709_D.dat.gz', 'rb')

    myStatus = None
    askprice = []
    timestamp = []
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
        if myMarketEvent.timestamp < 1562679500000000000:
            askprice.append(myMarketEvent.askDepth.prices[0])
            timestamp.append(myMarketEvent.timestamp)
        else:
            break
    askprice.reverse()
    timestamp.reverse()
    return (askprice),(timestamp)


if __name__ == '__main__':
    Data1 = main1()
    Data2 = main2()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(Data1[1], Data1[0],color='blue')
    ax1.set_ylabel('B askprice')

    ax2 = ax1.twinx()
    ax2.plot(Data2[1], Data2[0],'r-',color='purple')
    ax2.set_ylabel('D askprice',color='purple')
    for t1 in ax2.get_yticklabels():
        t1.set_color('purple')

    plt.savefig('0709 B,D Zoom Compare')
    plt.show()
