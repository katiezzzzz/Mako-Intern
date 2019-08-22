from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto


def main():
    myMarketEvent = internMarketData.marketEvent()
    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myFileStream = gzip.open('InternData/20190705_B.dat.gz', 'rb')

    myStatus = None
    while not myStatus:
        myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)

if __name__ == '__main__':
    main()
