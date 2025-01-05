import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

# Load the CSV file
data = pd.read_csv("/usr/src/data/solusdt_data.csv")

# Convert timestamp column to datetime format
data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S", utc=True)

# Filter data for SOLUSDT and 30-minute intervals until Friday at 18 p.m.
data_solusdt = data[data['symbol'] == 'SOLUSDT'].sort_values(by='timestamp')
intervals = np.arange(0, 20 * 60 + 1, 30)  # 30-minute intervals from now until Friday at 18 p.m.

# Initialize predictions and RAG scores
predictions = [None] * len(intervals)
rag_scores = [None] * len(intervals)

for i in range(len(intervals)):
    # Filter data for the current interval
    filtered_data = data_solusdt[data_solusdt['timestamp'] <= data_solusdt['timestamp'].iloc[i * 30]]

    # Calculate daily returns
    filtered_data['returns'] = np.log(filtered_data['close'] / filtered_data['open'])

    # Fit a linear regression model to predict close price
    X = filtered_data['RSI'].values.reshape(-1, 1)
    y = filtered_data['close'].values
    fit = LinearRegression().fit(X, y)

    # Make predictions for this interval using the model
    if i == 0:
        predictions[i] = np.exp(fit.predict([[filtered_data['RSI'].iloc[-1]]]))
    else:
        predictions[i] = np.exp(fit.predict([[filtered_data['RSI'].iloc[-1]]]))

    # Calculate RAG score for this interval
    if i > 0:
        rag_score = np.sqrt(np.sum((predictions[i] - predictions[i - 1]) ** 2)) / np.sqrt(
            np.sum((filtered_data['close'].iloc[-30:] - filtered_data['close'].iloc[-60:-30]) ** 2))
        if rag_scores[i] is None or rag_score > rag_scores[i]:
            rag_scores[i] = rag_score

# Print predictions and RAG scores for each interval
for i in range(len(intervals)):
    print(f"Interval: {intervals[i]}")
    print("Prediction:", predictions[i])
    print("RAG Score:", rag_scores[i])
    print()