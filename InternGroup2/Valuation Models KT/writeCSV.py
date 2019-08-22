from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import csv

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto

with open('0711D2.csv','a') as csvFile:
    writer = csv.writer(csvFile)
    def main():
        myMarketEvent = internMarketData.marketEvent()
        myPurePythonInternMarketData = internData_pb2.MarketData()
        myInternMarketData = internData_proto.MarketData()

        myFileStream = gzip.open('InternData/20190711_D.dat.gz', 'rb')

        myStatus = None
        while not myStatus:
            myStatus = myMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myFileStream)
            if myMarketEvent.eventType != 'MatchEventEnd':
                data = [myMarketEvent.timestamp,myMarketEvent.askDepth.prices[0],myMarketEvent.askDepth.volumes[0],
                        myMarketEvent.bidDepth.prices[0],myMarketEvent.bidDepth.volumes[0],myMarketEvent.eventPrice,
                        myMarketEvent.eventType]
                writer.writerow(data)
    main()

with open('0711D2.csv') as input, open('0711D.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    for row in csv.reader(input):
        if any(field.strip() for field in row):
            writer.writerow(row)

#if __name__ == '__main__':
