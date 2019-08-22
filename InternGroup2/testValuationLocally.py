from Shared.MarketData import internMarketData
from Protobufs import internData_pb2
import gzip
import runValuation
import internValuationData
import memoryData
import simulationData
from ParamSet import paramSet
from ParamSets import setInternSimParams

try:
    import internData_proto
except:
    from Protobufs import internData_pb2 as internData_proto


def main():
    myBaseMarketEvent = internMarketData.marketEvent()
    myCorrMarketEvent = internMarketData.marketEvent()

    myPurePythonInternMarketData = internData_pb2.MarketData()
    myInternMarketData = internData_proto.MarketData()

    myMemoryData = memoryData.memoryData()
    myInternSimParams = setInternSimParams.setInternSimParams()
    myInternSimParams.convertStringsToNumbers()

    myValuationData = internValuationData.internValuationData(aMemoryData=myMemoryData)
    mySimulationData = simulationData.simulationData(myInternSimParams)

    myParams = paramSet.paramSet()
    myParams.convertStringsToNumbers()

    myDateStr = '20190709'
    myBaseBook = 'B'
    myCorrBook = 'D'
    myBaseBookTickSize = 0.01
    myCorrBookTickSize = 0.01

    myBaseFileStream = gzip.open('InternData/' + myDateStr + '_' + myBaseBook + '.dat.gz', 'rb')
    myCorrFileStream = gzip.open('InternData/' + myDateStr + '_' + myCorrBook + '.dat.gz', 'rb')

    myBaseStatus = myBaseMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myBaseFileStream)
    myCorrStatus = myCorrMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData, myCorrFileStream)

    while True:
        if myBaseMarketEvent.timestamp <= myCorrMarketEvent.timestamp:
            myNextEvent = 'baseBook'
            myMarketEvent = myBaseMarketEvent
        else:
            myNextEvent = 'corrBook'
            myMarketEvent = myCorrMarketEvent


        runValuation.runValuation(myValuationData, mySimulationData, myMarketEvent, myNextEvent, myBaseBookTickSize,
                                  myCorrBookTickSize, myParams)

        # TKAP: Create any custom recording here

        if myNextEvent == 'baseBook':
            myBaseStatus = myBaseMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData,
                                                              myBaseFileStream)
        else:
            myCorrStatus = myCorrMarketEvent.getEventFromFile(myPurePythonInternMarketData, myInternMarketData,
                                                              myCorrFileStream)

        if myBaseStatus or myCorrStatus:
            break

if __name__ == '__main__':
    main()
