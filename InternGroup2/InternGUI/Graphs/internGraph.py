from Shared.DateTime import convertUnixToString
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pytz


class internGraph(QtWidgets.QDialog):
    def __init__(self, aResultDataDict, aInternSimParams, aInternGraphParams):
        QtWidgets.QDialog.__init__(self)

        self.resultDataDict = aResultDataDict
        self.groupName = aResultDataDict['overallResult']['group']
        self.dateStr = aResultDataDict['overallResult']['tradeDate']
        self.bookName = aResultDataDict['overallResult']['baseBook']
        self.recordingLabel = aResultDataDict['overallResult']['recordingLabel']
        self.timestamp = aResultDataDict['overallResult']['timestamp']
        self.overallPnL = aResultDataDict['overallResult']['overallPnL']

        self.dualColorList = [['#FF0000', '#0070C0']]
        self.MAColorList = ['m', 'g', 'c']

        self.internSimParams = aInternSimParams
        self.internGraphParams = aInternGraphParams
        self.pytzTimeZone = pytz.timezone(self.internSimParams.timezone)

        self.extraAxisDict = {}

        self.extraFieldDict = {}
        if self.internSimParams.memoryDataFieldsToGraph:
            mySplitList = self.internSimParams.memoryDataFieldsToGraph.split(';')
            for splitfield in mySplitList:
                if splitfield.find('+') != -1:
                    self.extraFieldDict[splitfield] = []
                    myDoubleSplitList = splitfield.split('+')
                    for doublesplitfield in myDoubleSplitList:
                        self.extraFieldDict[splitfield].append(doublesplitfield)
                else:
                    self.extraFieldDict[splitfield] = [splitfield]

        self.graphTitle = self.groupName + ' - ' + self.recordingLabel + ' | ' + self.bookName + ' - ' + self.dateStr + \
                          '\n' + \
                          convertUnixToString.convertUnixToDateAndTime(self.timestamp, self.internSimParams.timezone)\
                          + '\n' + 'PnL: ' + '{:0.1f}'.format(self.overallPnL)

        self.setGeometry(100, 100, 800, 900)
        self.center()
        self.setWindowTitle('Intern Graph')

        self.figure = plt.figure()
        self.figure.suptitle(self.graphTitle, fontweight ='bold', fontsize=12)
        self.figure.set_facecolor('0.75')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        myLayout = QtWidgets.QVBoxLayout()
        myLayout.addWidget(self.toolbar)
        myLayout.addWidget(self.canvas)
        self.setLayout(myLayout)

        self.updateGraph()

    def updateGraph(self):

        self.figure.clf()

        myExtraRows = 0
        if self.internGraphParams.numShowMemoryDataFields:
            for field in self.extraFieldDict:
                if field.find('mvgAvg_') == -1:
                    myExtraRows += 1
        myExtraRows += self.internGraphParams.numShowPnL + self.internGraphParams.numShowPosition
        if myExtraRows:
            myExtraRows += 1

        myHeightRatios = [10]
        myTotalRows = 1
        myNextRow = 2

        if myExtraRows:
            # TKAP: Add gap
            myHeightRatios.append(4)
            myTotalRows +=1

            for extrarowidx in range(myExtraRows):
                myHeightRatios.append(3)
                myTotalRows += 1

        myGridSpec = gridspec.GridSpec(myTotalRows, 1, height_ratios=myHeightRatios)

        self.underlyingAxis = self.figure.add_subplot(myGridSpec[0,0])
        self.underlyingAxis.set_xticklabels(self.underlyingAxis.get_xticks(), rotation=35, ha='right', size=8)
        self.underlyingAxis.xaxis.grid(True)
        self.underlyingAxis.yaxis.grid(True)
        self.underlyingAxis.xaxis_date()
        self.underlyingAxis.xaxis.set_major_formatter(mdates.DateFormatter(fmt='%H:%M:%S.%f', tz=self.pytzTimeZone))
        self.underlyingAxis.grid(linestyle=':', linewidth=1)

        # TKAP: Show bid/ask
        if self.internGraphParams.numShowBidAskForBaseBook:
            self.underlyingAxis.step(self.resultDataDict['graphPointMDates'], self.resultDataDict['graphPointBids'],
                                     c='b', linewidth=0.5, where='post')
            self.underlyingAxis.step(self.resultDataDict['graphPointMDates'], self.resultDataDict['graphPointAsks'],
                                     c='b', linewidth=0.5, where='post')

        # TKAP: Show underlying valuations
            self.underlyingAxis.step(self.resultDataDict['valuationMDates'], self.resultDataDict['bidValuation'],
                                     c='r', linewidth=0.5, where='post')
            self.underlyingAxis.step(self.resultDataDict['valuationMDates'], self.resultDataDict['askValuation'],
                                     c='r', linewidth=0.5, where='post')

        # TKAP: Show trades
        if self.internGraphParams.numShowTrades:
            myBuys = np.sign(self.resultDataDict['tradeDeltas']) == 1
            mySells = ~myBuys

            myMarkerStyle = {'markerfacecolor': 'None', 'markeredgewidth': 1, 'markeredgecolor':'g'}
            self.underlyingAxis.plot(self.resultDataDict['tradeMDates'][myBuys], self.resultDataDict['tradePrices'][
                myBuys], marker='^', markersize=4, c='None', **myMarkerStyle)
            myMarkerStyle = {'markerfacecolor': 'None', 'markeredgewidth': 1, 'markeredgecolor':'g'}
            self.underlyingAxis.plot(self.resultDataDict['tradeMDates'][mySells], self.resultDataDict['tradePrices'][
                mySells], marker='v', markersize=4, c='None', **myMarkerStyle)

        # TKAP: Show extra fields
        myMAIndex = 0
        if self.internGraphParams.numShowMemoryDataFields:
            for field in self.internSimParams.memoryDataFieldsToGraph.split(';'):
                if field in self.resultDataDict:
                    if field.find('mvgAvg_') == -1:
                        self.extraAxisDict[field] = self.figure.add_subplot(myGridSpec[myNextRow], sharex=self.underlyingAxis)
                        self.extraAxisDict[field].step(self.resultDataDict['valuationMDates'], self.resultDataDict[field],
                                                       c='b', linewidth=0.5, where='post')

                        self.extraAxisDict[field].xaxis.grid(True)
                        self.extraAxisDict[field].yaxis.grid(True)
                        self.extraAxisDict[field].set_title(field, fontsize=6)
                        self.extraAxisDict[field].grid(linestyle=':', linewidth=1)
                        for label in self.extraAxisDict[field].get_xticklabels():
                            label.set_visible(False)
                        myNextRow += 1
                    else:
                        myColorIndex = min(len(self.MAColorList), myMAIndex)
                        self.underlyingAxis.step(self.resultDataDict['valuationMDates'], self.resultDataDict[field],
                                                 c=self.MAColorList[myColorIndex], linewidth=0.5, where='post')
                        myMAIndex += 1

        # TKAP: Show PnL
        if self.internGraphParams.numShowPnL:
            field = 'simNetPnL'
            self.extraAxisDict[field] = self.figure.add_subplot(myGridSpec[myNextRow], sharex=self.underlyingAxis)
            self.extraAxisDict[field].step(self.resultDataDict['valuationMDates'], self.resultDataDict[field],
                                           c='b', linewidth=0.5, where='post')
            self.extraAxisDict[field].xaxis.grid(True)
            self.extraAxisDict[field].yaxis.grid(True)
            self.extraAxisDict[field].set_title(field, fontsize=6)
            self.extraAxisDict[field].grid(linestyle=':', linewidth=1)
            for label in self.extraAxisDict[field].get_xticklabels():
                label.set_visible(False)
            myNextRow += 1

        # TKAP: Show Position
        if self.internGraphParams.numShowPosition:
            field = 'simNetDelta'
            self.extraAxisDict[field] = self.figure.add_subplot(myGridSpec[myNextRow], sharex=self.underlyingAxis)
            self.extraAxisDict[field].step(self.resultDataDict['valuationMDates'], self.resultDataDict[field],
                                           c='b', linewidth=0.5, where='post')
            self.extraAxisDict[field].xaxis.grid(True)
            self.extraAxisDict[field].yaxis.grid(True)
            self.extraAxisDict[field].set_title(field, fontsize=6)
            self.extraAxisDict[field].grid(linestyle=':', linewidth=1)
            for label in self.extraAxisDict[field].get_xticklabels():
                label.set_visible(False)
            myNextRow += 1

        # TKAP: Make axes less annoying
        for ax in self.figure.axes:
            ax.ticklabel_format(useOffset=False, axis='y')
        self.underlyingAxis.set_xlim(self.resultDataDict['valuationStartPythonTime'],
                                     self.resultDataDict['valuationEndPythonTime'])

        self.figure.suptitle(self.graphTitle, fontweight ='bold', fontsize=12)
        self.canvas.draw()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerpoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerpoint)
        self.move(frameGm.topLeft())
