import numpy as np
import importlib
from Shared.MongoDB import mongoDBObject


class internValuationData(mongoDBObject.mongoDBObject):
    def __init__(self, aAlgorithm = '', aMemoryData = None):

        self.timestamp = np.int64(0)
        self.bidValuation = np.nan
        self.askValuation = np.nan

        if aAlgorithm:
            myMemoryClass = importlib.import_module('Services.Intern.Algos.' + aAlgorithm + '.memoryData')
            self.memoryData = myMemoryClass.memoryData()

        if aMemoryData:
            self.memoryData = aMemoryData
