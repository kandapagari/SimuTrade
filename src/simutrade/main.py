from simutrade.backtester import Backtester
from simutrade.strategies import (
    RSIStrategy,
    MACrossoverStrategy,
    BollingerBandStrategy,
    AIBasedStrategy,
)
import typer


def main(
    ticker: str = "GOOG", start_date: str = "2024-01-01", end_date: str = "2024-07-01"
):
    strategy = RSIStrategy(period=14, overbought=70, oversold=30)
    strategy = MACrossoverStrategy(short_window=50, long_window=200)
    strategy = BollingerBandStrategy(window=20, std_dev=2)
    strategy = AIBasedStrategy(api_url="http://10.3.2.50:11434")

    backtester = Backtester(
        strategy=strategy,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        use_api=True,
        position_size=1,
    )

    backtester.run()
    backtester.plot_results()
    backtester.print_results()


if __name__ == "__main__":
    typer.run(main)
