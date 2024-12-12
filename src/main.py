import requests
import pandas as pd
import numpy as np
from datetime import datetime
from ta.momentum import RSIIndicator


# Function to fetch historical price data from Binance API
def fetch_historical_data(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Parse the data into a DataFrame
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])

    # Keep only relevant columns
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df


# Function to fetch funding rate data from Binance API
def fetch_funding_rate(symbol):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": symbol
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Parse the data into a DataFrame
    df = pd.DataFrame(data)
    df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms")
    df["fundingRate"] = df["fundingRate"].astype(float)
    return df


# Placeholder function to fetch liquidation map data (requires specific API access)
def fetch_liquidation_data(symbol):
    # Example: Replace with actual API call to a service like Coinglass or Glassnode
    url = f"https://api.example.com/liquidationData"
    params = {
        "symbol": symbol
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Parse the data into a DataFrame
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


# Function to calculate RSI
def calculate_rsi(df, window):
    rsi = RSIIndicator(df["close"], window=window)
    df["RSI"] = rsi.rsi()
    return df


# Fetch historical price data for Solana (SOLUSDT)
symbol = "SOLUSDT"
interval = "1h"  # Adjust as needed (e.g., "1d" for daily data)
limit = 500  # Number of data points to fetch

print("Fetching historical data...")
price_data = fetch_historical_data(symbol, interval, limit)

# Calculate RSI with a 14-period window
print("Calculating RSI...")
price_data = calculate_rsi(price_data, window=14)

# Fetch funding rate data
print("Fetching funding rate data...")
funding_data = fetch_funding_rate(symbol)

# Fetch liquidation map data (if available)
# print("Fetching liquidation data...")
# liquidation_data = fetch_liquidation_data(symbol)

# Merge price, funding, and liquidation data on timestamps (if close enough in time)
print("Merging data...")
price_data.set_index("timestamp", inplace=True)
funding_data.set_index("fundingTime", inplace=True)
# liquidation_data.set_index("timestamp", inplace=True)

combined_data = price_data.join(funding_data, how="left")

# Display the final DataFrame
print("Combined data:")
print(combined_data.head())

# Save data to CSV for further analysis
combined_data.to_csv("solana_data.csv")
print("Data saved to solana_data.csv")
