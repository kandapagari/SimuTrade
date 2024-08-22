from simutrade.strategies import Strategy
import talib


class RSIStrategy(Strategy):

    def __init__(self, period=14, overbought=70, oversold=30):
        super().__init__("RSI")
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def generate_signals(self, data):
        data["RSI"] = talib.RSI(
            data["Close"], timeperiod=self.period
        )  # Requires 'talib' library
        data["Signals"] = 0.0
        data.loc[data["RSI"] < self.oversold, "Signals"] = 1.0
        data.loc[data["RSI"] > self.overbought, "Signals"] = -1.0

        return data["Signals"].values.astype(int)
