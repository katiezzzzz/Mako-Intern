from GUIs.Shared import baseGUI
import pickle
from Shared.Messaging import inMessage
from GUIs.InternGUI.Graphs import internGraph
from GUIs.InternGUI.Tables import internSimTradesTable
from ParamSets import setInternSimParams, setInternGraphParams


class handleRedisEvents(baseGUI.baseGUI):
    def handleInternResultsWrapper(self, aMessage):
        if aMessage['type'] == 'message':
            myData = aMessage['data']
            myDecodedMessage = pickle.loads(myData)
            self.sigHandleInternResults.emit(myDecodedMessage)

    def handleInternResults(self, aDecodedMessage):
        self.internResultDict = aDecodedMessage['resultDict']
        self.normalOutputWritten('Simulation Data Received!')
        self.showGraph()
        self.showTradeTable()

    def pullFromGIT(self):
        myRedisMessage = inMessage.returnGUIMessage(aService='Intern', aRequest='PullGIT', aLabel=self.userName)
        self.redisClient.publish(self.inChannelIntern, myRedisMessage)

    def startSimulation(self):
        self.simulationParams = setInternSimParams.setInternSimParams()
        self.simulationParams.loadFromMongoDB(self.userName)
        myRedisMessage = inMessage.returnGUIMessage(aService='Intern', aRequest='Start', aLabel=self.userName,
                                                    params=self.simulationParams.getPickleableVersion())
        self.normalOutputWritten('Simulation Started!')
        self.redisClient.publish(self.inChannelIntern, myRedisMessage)

    def stopSimulation(self):
        myRedisMessage = inMessage.returnGUIMessage(aService='Intern', aRequest='Stop', aLabel=self.userName)
        self.redisClient.publish(self.inChannelIntern, myRedisMessage)

    def handleInternMessageWrapper(self, aMessage):
        if aMessage['type'] == 'message':
            myData = aMessage['data']
            myDecodedMessage = pickle.loads(myData)
            if myDecodedMessage['label'] == self.userName:
                self.sigHandleInternStatus.emit(myDecodedMessage)

    def handleInternMessage(self, aDecodedMessage):
        myValue = int(aDecodedMessage['count'])
        self.progressBar.setValue(myValue)

    def showGraph(self):
        if self.internResultDict:
            self.simulationParams = setInternSimParams.setInternSimParams()
            self.simulationParams.loadFromMongoDB(self.userName)

            self.graphParams = setInternGraphParams.setInternGraphParams()
            self.graphParams.loadFromMongoDB(self.userName)
            self.graphParams.convertStringsToNumbers()

            self.sourceSimDataDict = {}
            myGraph = internGraph.internGraph(self.internResultDict, self.simulationParams, self.graphParams)
            myGraph.show()
            self.graphList.append(myGraph)

    def showTradeTable(self):
        if self.internResultDict:
            myTable = internSimTradesTable.internSimTradesTable(self.internResultDict['tradeList'],
                                                                self.internResultDict['timezone'],
                                                                self.internResultDict['tickSize'])
            myTable.show()
            self.tableList.append(myTable)

    def handleErrorMessageWrapper(self, aMessage):
        if aMessage['type'] == 'message':
            myData = aMessage['data']
            myDecodedMessage = pickle.loads(myData)
            if myDecodedMessage['label'] == self.userName:
                self.sigHandleErrorUpdate.emit(myDecodedMessage['error'])