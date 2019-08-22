from GUIs.Shared.Tables import tableWithCopyPaste
from PyQt5 import QtWidgets, QtCore, QtGui
from Shared.DateTime import convertUnixToString


class internSimTradesTable(tableWithCopyPaste.TableWidgetCustom):
    def __init__(self, aSimTrades, aTimeZone, aTickSize):
        tableWithCopyPaste.TableWidgetCustom.__init__(self)
        self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.setGeometry(QtCore.QRect(400, 400, 1000, 600))
        self.center()

        self.horizontalHeaderLabels = list(aSimTrades.__dict__)

        myStrTickSize = '{:0.15f}'.format(round(aTickSize, 14)).rstrip('0')
        myRoundingDigits = len(myStrTickSize.split('.')[1])
        myRoundingString = '{:0.' + str(myRoundingDigits) + 'f}'

        myRowCount = len(aSimTrades.tradeTimestamp)
        myColumnCount = len(self.horizontalHeaderLabels)

        self.clear()
        self.setRowCount(myRowCount)
        self.setColumnCount(myColumnCount)
        self.setWindowTitle('SimTrades')

        self.setHorizontalHeaderLabels(self.horizontalHeaderLabels)

        for fieldidx, field in enumerate(self.horizontalHeaderLabels):
            myArray = getattr(aSimTrades, field)
            for valueidx, value in enumerate(myArray):
                myItem = value
                if field in ['tradeTimestamp', 'tradeTransactTime']:
                    myItem = convertUnixToString.convertUnixToTimeWithMicros(myItem, aTimeZone)
                elif field == 'tradePrice':
                    myItem = myRoundingString.format(myItem)

                self.setItemProperties(myItem, valueidx, fieldidx)

        myFont = QtGui.QFont()
        myFont.setPointSize(8)
        self.horizontalHeader().setFont(myFont)
        self.horizontalHeader().setStretchLastSection(False)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeRowsToContents()

        myTableWidth = 200 + 60 * myColumnCount

        self.setGeometry(QtCore.QRect(400, 400, myTableWidth, 400))
        self.center()
