import yfinance as yf
import pandas as pd

class MarketFeed:
    def __init__(self, ticker, interval='1d'):
        self.ticker = ticker
        self.interval = interval

    def fetch_latest_data(self, period="7d"):
        """Fetch recent OHLCV data."""
        stock = yf.Ticker(self.ticker)
        data = stock.history(period=period, interval=self.interval)
        data.reset_index(inplace=True)
        return data
