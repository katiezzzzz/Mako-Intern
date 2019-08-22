from GUIs.Shared.Tables import tableWithCopyPaste
from PyQt5 import QtWidgets, QtCore, QtGui
from Shared.DateTime import convertUnixToString


class internPnLTable(tableWithCopyPaste.TableWidgetCustom):
    def __init__(self, aCollection, aGroup, aTimeZone):
        tableWithCopyPaste.TableWidgetCustom.__init__(self)
        self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.setGeometry(QtCore.QRect(400, 400, 1000, 600))
        self.center()

        self.horizontalHeaderLabels = ['group', 'recordingLabel', 'timestamp', 'baseBook',
                                       'tradeDate', 'startTimestamp', 'endTimestamp', 'overallPnL',
                                       'tradingPnL', 'fees', 'totalVolume']

        myTotalEntries = aCollection.count_documents({'group': aGroup})
        myCursor = aCollection.find({'group': aGroup}).sort([('timestamp', -1)]).hint('intern')

        myRowCount = myTotalEntries
        myColumnCount = len(self.horizontalHeaderLabels)

        self.clear()
        self.setRowCount(myRowCount)
        self.setColumnCount(myColumnCount)
        self.setWindowTitle('SimTrades')

        self.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        self.verticalHeader().hide()

        for entryidx, entry in enumerate(myCursor):
            for fieldidx, field in enumerate(self.horizontalHeaderLabels):
                myItem = entry[field]
                if field in ['timestamp']:
                    myItem = convertUnixToString.convertUnixToDateAndTime(myItem, aTimeZone)
                elif field in ['startTimestamp', 'endTimestamp']:
                    myItem = convertUnixToString.convertUnixToTime(myItem, aTimeZone)
                elif field in ['overallPnL', 'tradingPnL', 'fees']:
                    myItem = '{:0.2f}'.format(myItem)
                self.setItemProperties(myItem, entryidx, fieldidx)

        myFont = QtGui.QFont()
        myFont.setPointSize(8)
        self.horizontalHeader().setFont(myFont)
        self.horizontalHeader().setStretchLastSection(False)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeRowsToContents()

        myTableWidth = 100 + 70 * myColumnCount

        self.setGeometry(QtCore.QRect(400, 400, myTableWidth, 400))
        self.center()
