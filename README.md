## Binance Cryptocurrency Data Analysis, Plotting, and Prediction Script

This repository contains a Python script to fetch, process, analyze, and predict cryptocurrency data from Binance. It
retrieves historical price data and funding rates, calculates the Relative Strength Index (RSI), visualizes data trends
with plots, and uses the processed data for predictions. The processed data and results are saved as CSV files for
further use.

### Features

* Fetch historical price data from Binance.
* Fetch funding rate data for futures trading pairs.
* Calculate the Relative Strength Index (RSI) for price data.
* Merge historical price data and funding rate data into a unified dataset.
* Convert timestamps to German timezone (Europe/Berlin) in the format YYYY-MM-DD HH:MM.
* Save the combined data and other results into CSV files.
* Create plots for price and RSI development.
* Make predictions based on the processed data.

### Requirements

Before running the script, ensure you have the following installed:

* Python 3.8+
* Required Python packages (see below)

### Docker Environment

    docker compose up -d
    docker compose logs -f
    docker compose exec -it python bash

### Usage

Get Data and create CSV
python app/main.py
Create plots from CSV
python app/plot.py
Make predictions after running
python app/predict.py
This repository contains a Python script to fetch, process, and analyze cryptocurrency data from Binance. It retrieves historical price data and funding rates, calculates the Relative Strength Index (RSI), and merges the data into a single dataset for analysis. The processed data is then saved as a CSV file.

### Features
* Fetch historical price data from Binance.
* Fetch funding rate data for futures trading pairs.
* Calculate the Relative Strength Index (RSI) for price data.
* Merge historical price data and funding rate data into a unified dataset.
* Convert timestamps to German timezone (Europe/Berlin) in the format YYYY-MM-DD HH:MM.
* Save the combined data into a CSV file.
* **Plot for Price and RSI Development**
* **make predictions using the gained data**

### Requirements
Before running the script, ensure you have the following installed:
* Python 3.8+
* Required Python packages (see below)

### Docker Enviroment

    docker compose up -d
    docker compose logs -f
    docker compose exec -it python bash

### Usage

Get Requirements
    
    pip install -r requirements.txt
    
Get Data and create CSV

    python app/main.py <currency> #e.g SOLUSDT

create plot from CSV

    python app/plot.py
    
