import requests
import pandas as pd
import pytz
from datetime import datetime
from ta.momentum import RSIIndicator


# Abstract API Service
class ApiService:
    def fetch_data(self, url, params):
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


# Concrete Binance API Service
class BinanceApiService(ApiService):
    BASE_URL = "https://api.binance.com/api/v3"
    FUTURES_URL = "https://fapi.binance.com/fapi/v1"

    def fetch_historical_data(self, symbol, interval, limit):
        url = f"{self.BASE_URL}/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        data = self.fetch_data(url, params)

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]

        # Convert timestamp to German timezone (CET/CEST) and format it
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["timestamp"] = df["timestamp"].dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
        df["timestamp"] = df["timestamp"].dt.strftime('%Y-%m-%d %H:%M')

        df["close"] = df["close"].astype(float)
        return df

    def fetch_funding_rate(self, symbol):
        url = f"{self.FUTURES_URL}/fundingRate"
        params = {"symbol": symbol}
        data = self.fetch_data(url, params)

        df = pd.DataFrame(data)
        df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms")

        # Convert funding time to German timezone (CET/CEST) and format it
        df["fundingTime"] = df["fundingTime"].dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
        df["fundingTime"] = df["fundingTime"].dt.strftime('%Y-%m-%d %H:%M')

        df["fundingRate"] = df["fundingRate"].astype(float)
        return df

# RSI Calculator (SRP)
class RsiCalculator:
    def calculate(self, df, window):
        rsi = RSIIndicator(df["close"], window=window)
        df["RSI"] = rsi.rsi()
        return df


# Data Merger (SRP)
class DataMerger:
    def merge(self, *dataframes, on, how="left"):
        merged_df = dataframes[0]
        for df in dataframes[1:]:
            merged_df = merged_df.join(df, on=on, how=how)
        return merged_df


# Application Layer
class DataAnalysisApp:
    def __init__(self, api_service, rsi_calculator, data_merger):
        self.api_service = api_service
        self.rsi_calculator = rsi_calculator
        self.data_merger = data_merger

    def run(self, symbol, interval, limit, rsi_window, output_file):
        print("Fetching historical data...")
        price_data = self.api_service.fetch_historical_data(symbol, interval, limit)

        print("Calculating RSI...")
        price_data = self.rsi_calculator.calculate(price_data, rsi_window)

        print("Fetching funding rate data...")
        funding_data = self.api_service.fetch_funding_rate(symbol)

        print("Merging data...")
        price_data.set_index("timestamp", inplace=True)
        funding_data.set_index("fundingTime", inplace=True)
        combined_data = self.data_merger.merge(price_data, funding_data, on="timestamp")

        print("Saving data to CSV...")
        combined_data.to_csv(output_file)
        print(f"Data saved to {output_file}")


# Main Execution
if __name__ == "__main__":
    symbol = "SOLUSDT"
    interval = "30m"
    limit = 240
    rsi_window = 14
    output_file = "solana_data.csv"

    # Instantiate dependencies
    api_service = BinanceApiService()
    rsi_calculator = RsiCalculator()
    data_merger = DataMerger()

    # Run the application
    app = DataAnalysisApp(api_service, rsi_calculator, data_merger)
    app.run(symbol, interval, limit, rsi_window, output_file)
