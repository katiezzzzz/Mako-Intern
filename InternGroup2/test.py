self.ScalpMin = None
self.ScalpMax = None
def Test2(self, maxGain, maxLoss, TimeFrame, length):  # scalps in terms of overall pnl instead of individual futures
    if len(self.pnlStore) >= TimeFrame:
        self.pnlStore = self.pnlStore[0:TimeFrame]
    if len(self.pnlStore) >= TimeFrame / 2:
        if len(self.pnlStore) >= TimeFrame and self.book_amount > 0:  # sell
            Min = np.min(self.pnlStore[1:TimeFrame])
            Max = np.max(self.pnlStore[1:TimeFrame])
            if not self.ScalpMin or not self.ScalpMax:
                self.ScalpMin = Min
                self.ScalpMax = Max
            if self.n % length == 0:
                self.ScalpMin = Min
                self.ScalpMax = Max
            if Max - self.pnlStore[0] > maxLoss or self.pnlStore[0] - Min > maxGain:
                self.valuation_ask = self.B_BidPrices[0] - 5
                self.valuation_bid = self.B_BidPrices[0] - 10
            self.counter = 1
        elif len(self.pnlStore) >= TimeFrame and self.book_amount < 0:
            Min = np.min(self.pnlStore[1:TimeFrame])
            Max = np.max(self.pnlStore[1:TimeFrame])
            if self.pnlStore[0] - Min > maxGain or Max - self.pnlStore[0] > maxLoss:
                self.valuation_bid = self.B_AskPrices[0] + 5
                self.valuation_ask = self.B_AskPrices[0] + 10
            self.counter = 1