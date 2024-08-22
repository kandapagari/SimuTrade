from simutrade.strategies import Strategy
import numpy as np


class BollingerBandStrategy(Strategy):
    def __init__(self, window=20, std_dev=2):
        super().__init__("BollingerBand")
        self.window = window
        self.std_dev = std_dev

    def generate_signals(self, data):
        data["MiddleBand"] = data["Close"].rolling(window=self.window).mean()
        data["StdDev"] = data["Close"].rolling(window=self.window).std()
        data["UpperBand"] = data["MiddleBand"] + (data["StdDev"] * self.std_dev)
        data["LowerBand"] = data["MiddleBand"] - (data["StdDev"] * self.std_dev)
        data["Signal"] = 0.0
        data["Signal"][self.window :] = np.where(
            data["Close"][self.window :] > data["UpperBand"][self.window :],
            1.0,  # Sell Signal
            np.where(
                data["Close"][self.window :] < data["LowerBand"][self.window :],
                -1.0,
                0.0,
            ),  # Buy Signal
        )
        return data["Signal"]
