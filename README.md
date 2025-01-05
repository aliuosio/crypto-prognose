## Binance Cryptocurrency Data Analysis, Plotting, and Prediction Script

### Features

* Fetch historical price data from Binance.
* Fetch funding rate data for futures trading pairs.
* Calculate the Relative Strength Index (RSI) for price data.
* Merge historical price data and funding rate data into a unified dataset.
* Save the combined data and other results into CSV files.
* Create plots for price and RSI development.

### Docker Environment

    docker compose up -d
    docker compose logs -f
    docker compose exec -it python bash

### Usage

    docker compose up -d
    docker compose logs -f
    docker compose exec -it python bash

### Usage

Get Requirements
    
    pip install -r requirements.txt
    
Get Data and create CSV

    Examples:
    python app/main.py SOLUSDT
    python app/main.py BTCUSDT

create plot from CSV

    python app/plot.py
    