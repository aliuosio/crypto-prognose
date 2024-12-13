## Binance Data Analysis Script
This repository contains a Python script to fetch, process, and analyze cryptocurrency data from Binance. It retrieves historical price data and funding rates, calculates the Relative Strength Index (RSI), and merges the data into a single dataset for analysis. The processed data is then saved as a CSV file.

### Features
* Fetch historical price data from Binance.
* Fetch funding rate data for futures trading pairs.
* Calculate the Relative Strength Index (RSI) for price data.
* Merge historical price data and funding rate data into a unified dataset.
* Convert timestamps to German timezone (Europe/Berlin) in the format YYYY-MM-DD HH:MM.
* Save the combined data into a CSV file.
* **Plot for Price and RSI Development**

### Requirements
Before running the script, ensure you have the following installed:
* Python 3.8+
* Required Python packages (see below)

### Docker Enviroment

    docker compose up -d
    docker compose logs -f
    docker compose exec -it python bash

### Usage
    
    # create CSV
    python app/main.py 

    # create plot from CSV
    python app/indicators.py
    