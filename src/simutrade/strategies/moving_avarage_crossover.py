from simutrade.strategies import Strategy
import numpy as np


class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        data["ShortMA"] = data["Close"].rolling(window=self.short_window).mean()
        data["LongMA"] = data["Close"].rolling(window=self.long_window).mean()
        data["Signal"] = 0.0
        data["Signal"][self.short_window :] = np.where(
            data["ShortMA"][self.short_window :] > data["LongMA"][self.short_window :],
            1.0,
            0.0,
        )
        return data["Signal"]
