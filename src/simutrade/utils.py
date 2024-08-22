import yfinance as yf

import re


def download_historical_data(ticker, start_date, end_date):
    """Downloads historical price data from Yahoo Finance."""
    return yf.download(ticker, start=start_date, end=end_date)


def get_price_direction(response):
    """Extracts price direction from an OpenAI response."""
    if match := re.search(r'"(.*?)"', response):
        return match[1].upper()
    else:
        return "Direction not found"
