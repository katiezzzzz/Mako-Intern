import numpy as np
from Services.Intern.Simulation import simTrades


class simulationData():
    def __init__(self, aParams):
        self.transactTime = np.int64(0)
        self.prevTransactTimeBidValuation = np.nan
        self.prevTransactTimeAskValuation = np.nan
        self.prevTransactTime = np.int64(0)
        self.lastTransactTime = np.int64(0)
        self.lastTradePrice = np.nan

        self.simTrades = simTrades.simTrades(aParams)
        self.simNetDelta = 0
        self.simNetPnL = 0
        self.simTradingPnL = 0
        self.simTotalFees = 0
        self.simTradingVolume = 0
