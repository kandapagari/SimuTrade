import time
import pandas as pd
from simutrade.strategies import Strategy

from simutrade.utils import download_historical_data
import matplotlib.pyplot as plt


class Backtester:

    def __init__(
        self,
        data: pd.DataFrame = None,
        data_path: str = None,
        strategy: Strategy = None,
        ticker: str = None,
        start_date: str = None,
        end_date: str = None,
        use_api: bool = False,
        position_size: int = 100,
    ):
        self.data = data
        self.data_path = data_path
        self.strategy = strategy
        self.results = pd.DataFrame()
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.use_api = use_api
        self.position_size = position_size

    def load_data(self):
        if self.data is not None:
            return
        elif self.data_path is not None:
            self.data = pd.read_csv(self.data_path, index_col="Date", parse_dates=True)
        elif self.use_api:
            self.data = download_historical_data(
                self.ticker, self.start_date, self.end_date
            )

    def run(self):
        self.load_data()  # Ensure data is loaded before backtesting

        signals = self.strategy.generate_signals(self.data)
        self.data["Signals"] = signals

        positions = []
        portfolio_value = []

        previous_position = (
            0  # Initialize previous position (0 for neutral/no position)
        )

        for index, row in self.data.iterrows():
            signal = row["Signals"]
            price = row["Close"]

            if signal != previous_position:
                if signal == 1 and previous_position == 0:  # Buy signal
                    positions.append((index, "Buy", price * self.position_size))
                elif signal == -1 and previous_position == 0:  # Sell signal
                    positions.append((index, "Sell", price * self.position_size))

            previous_position = signal

            # Calculate portfolio value based on open positions and prices
            current_value = 0
            for entry in positions:
                if entry[1] == "Buy":
                    current_value += entry[2]
                elif entry[1] == "Sell":
                    current_value -= entry[2]

            portfolio_value.append(current_value)
        self.data["PortfolioValue"] = portfolio_value

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data["Close"], label="Price")
        plt.plot(self.data["PortfolioValue"], label="Portfolio Value")
        plt.title("Backtest Results")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
        plt.savefig(
            f"output/{self.ticker}_{self.strategy.name}_{time.strftime('%m_%d_%H_%M_%S')}.png"
        )

    def print_results(self):
        total_return = (
            self.data["PortfolioValue"].iloc[-1] - self.data["PortfolioValue"].iloc[0]
        )
        print(f"Total Return: $ {total_return:.2f}")
