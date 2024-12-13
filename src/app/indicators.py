import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
try:
    df = pd.read_csv('solana_data.csv')
except FileNotFoundError:
    print("The file 'solana_data.csv' was not found. Please check the file path.")
    exit()

# Check if necessary columns exist
required_columns = ['timestamp', 'close', 'RSI']
if not all(col in df.columns for col in required_columns):
    print(f"The CSV file must contain the following columns: {', '.join(required_columns)}")
    exit()

# Convert the timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Handle potential missing or invalid timestamps
if df['timestamp'].isnull().any():
    print("Warning: Some timestamps were invalid and have been converted to NaT.")
    df = df.dropna(subset=['timestamp'])

# Basic analysis: Calculate average closing price and RSI
avg_close = df['close'].mean()
avg_rsi = df['RSI'].mean()

# Plotting closing prices and RSI
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot the closing prices
ax1.plot(df['timestamp'], df['close'], color='tab:blue', label='Close Price', marker='o')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Close Price', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis for RSI
ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['RSI'], color='tab:red', label='RSI', marker='x')
ax2.set_ylabel('RSI', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Title and save the plot
plt.title(f"Closing Prices and RSI (Avg Close: {avg_close:.2f}, Avg RSI: {avg_rsi:.2f})")
plt.tight_layout()

# Save plot to file (instead of showing it)
plt.savefig('solana_plot.png')

# Optionally, print a success message
print("Plot saved as 'solana_plot.png'.")
