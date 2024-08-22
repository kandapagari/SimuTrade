from simutrade.strategies import Strategy
import numpy as np


class MACrossoverStrategy(Strategy):

    def __init__(self, short_window=50, long_window=200):
        super().__init__("MACrossover")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        df["SMA_Short"] = df["Close"].rolling(window=self.short_window).mean()
        df["SMA_Long"] = df["Close"].rolling(window=self.long_window).mean()
        df["Signal"] = 0.0  # Initialize signal column

        # Buy when short MA crosses above long MA, sell the reverse

        df["Signal"][self.short_window :] = np.where(
            df["SMA_Short"][self.short_window :] > df["SMA_Long"][self.short_window :],
            1.0,
            np.where(
                df["SMA_Short"][self.short_window :]
                < df["SMA_Long"][self.short_window :],
                -1.0,
                0.0,
            ),
        )
        return df["Signal"]
