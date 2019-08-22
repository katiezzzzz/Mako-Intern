from GUIs.Shared import baseGUI
from GUIs.QT import InternGUI
from GUIs.InternGUI import handleGUIEvents, handleRedisEvents
from PyQt5 import QtCore
import pickle


class InternGUIApp(InternGUI.Ui_MainWindow, handleGUIEvents.handleGUIEvents, handleRedisEvents.handleRedisEvents,
             baseGUI.baseGUI):
    # TKAP: Create signals
    sigHandleInternResults = QtCore.pyqtSignal(dict)
    sigHandleInternStatus = QtCore.pyqtSignal(dict)

    def __init__(self, aConfig):
        InternGUI.Ui_MainWindow.__init__(self)
        baseGUI.baseGUI.__init__(self, aConfig)

        self.serviceList = ['Intern']
        self.graphList = []
        self.tableList = []
        self.internResultDict = {}

        # TKAP: Distinguish between groups here
        self.algoDict = {'tkapadia': 'InternTest', 'iigboaka': 'InternTest', 'aorquin': 'InternTest',
                         'hforty': 'InternGroup1', 'jjiang': 'InternGroup1', 'kraikund': 'InternGroup1',
                         'cjackson': 'InternGroup2', 'kzeng': 'InternGroup2', 'kxian': 'InternGroup2', 
                         'JJiang': 'InternGroup1'}

        # TKAP: Load all params
        self.loadAllParams()

        # TKAP: Item changed for params
        self.tableWidgetSimulation.itemChanged.connect(self.updateSimulationParams)
        self.tableWidgetGraphing.itemChanged.connect(self.updateGraphingParams)

        # TKAP: Connect buttons
        self.pushButtonRunSimulation.clicked.connect(self.startSimulation)
        self.pushButtonStopSimulation.clicked.connect(self.stopSimulation)
        self.pushButtonShowGraph.clicked.connect(self.showGraph)
        self.pushButtonShowTrades.clicked.connect(self.showTradeTable)
        self.pushButtonShowPnL.clicked.connect(self.showPnLTable)
        self.pushButtonPullGIT.clicked.connect(self.pullFromGIT)

        # TKAP: Connect signals to handlers for received data
        self.sigHandleInternResults.connect(self.handleInternResults)
        self.sigHandleInternStatus.connect(self.handleInternMessage)

        self.registerRedis()

    def registerOtherRedis(self):
        self.internResultsChannel = 'InternResults:' + self.userName
        self.callbackDict[self.internResultsChannel] = self.handleInternResultsWrapper

    def handleErrorMessageWrapper(self, aMessage):
        if aMessage['type'] == 'message':
            myData = aMessage['data']
            myDecodedMessage = pickle.loads(myData)
            if myDecodedMessage['label'] == self.userName:
                self.sigHandleErrorUpdate.emit(myDecodedMessage['error'])
