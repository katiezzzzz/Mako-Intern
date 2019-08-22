from GUIs.Shared import baseGUI
from ParamSets import setInternSimParams, setInternGraphParams
from GUIs.InternGUI.Tables import internPnLTable


class handleGUIEvents(baseGUI.baseGUI):

    def loadAllParams(self):
        self.loadSimulationParams()
        self.loadGraphingParams()

    def loadSimulationParams(self):
        self.simulationParams = setInternSimParams.setInternSimParams()
        self.simulationParams.loadFromMongoDB(self.userName)
        self.retrieveParameterSet(self.tableWidgetSimulation, self.simulationParams, aIgnoreList=[''])

    def updateSimulationParams(self):
        self.updateGUIParams(self.userName, self.tableWidgetSimulation, self.simulationParams, 'Simulation',
                             self.loadSimulationParams, self.updateSimulationParams)

    def loadGraphingParams(self):
        self.graphParams = setInternGraphParams.setInternGraphParams()
        self.graphParams.loadFromMongoDB(self.userName)
        self.retrieveParameterSet(self.tableWidgetGraphing, self.graphParams, aIgnoreList=[''])

    def updateGraphingParams(self):
        self.updateGUIParams(self.userName, self.tableWidgetGraphing, self.graphParams, 'Graphing',
                             self.loadGraphingParams, self.updateGraphingParams)

    def showPnLTable(self):
        self.simulationParams = setInternSimParams.setInternSimParams()
        self.simulationParams.loadFromMongoDB(self.userName)
        myTable = internPnLTable.internPnLTable(self.collections.internResultsCollection, self.algoDict[
            self.userName], self.simulationParams.timezone)
        myTable.show()
        self.tableList.append(myTable)

