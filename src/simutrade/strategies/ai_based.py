import requests
import pandas as pd
from simutrade.strategies import Strategy
import json
import tqdm


class AIBasedStrategy(Strategy):
    def __init__(self, api_url="http://10.3.2.50:11434"):
        self.name = "AI Based Strategy"
        self.api_url = api_url

    def generate_signals(self, data):
        signals = []
        example = """
        Here is an example that you can use,

        Previous Close Prices: 150.50, 152.25, 151.75 
        Current Price: $153.00

        and you would reply with "UP"
        """
        for i in tqdm.tqdm(range(len(data) - 1)):  # Leave last row for prediction
            date = data.index[i].strftime("%Y-%m-%d")
            price = data["Close"].iloc[i]
            previous_prices = data["Close"].iloc[:-i].to_list()
            prompt = f"""
                        Analyze the following stock price history and predict the direction for {date}:

                        Previous Close Prices: {', '.join(map(str, previous_prices))} 
                        Current Price: ${price:.2f},

                        Predict whether the stock price will go "UP", "DOWN", or "STAY THE SAME" on {date}.
                        If you dont have enough previous prices, you can return "STAY THE SAME"
                        DO NOT Provide any explanation for your prediction.
                        """
            payload = {
                "model": "llama3.1:latest",
                "prompt": prompt + example,
                "stream": False,
            }
            response = requests.post(f"{self.api_url}/api/generate", json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                prediction = json.loads(response.text)["response"]

                if "UP" in prediction:
                    signals.append(1)  # Buy signal
                elif "DOWN" in prediction or "decrease" in prediction:
                    signals.append(-1)  # Sell Signal
                else:
                    signals.append(0)  # Neutral

            else:
                print(
                    f"Error: API request failed with status code {response.status_code}"
                )
                signals.append(0)  # Append neutral signal on error

        signals.append(0)  # Append a neutral signal for the last data point

        return pd.Series(signals, index=data.index)
