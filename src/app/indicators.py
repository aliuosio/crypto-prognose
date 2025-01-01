import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Load data from CSV file
data_folder = 'data'
csv_files = glob.glob(os.path.join(data_folder, '*.csv'))

if not csv_files:
    print(f"No CSV files found in the '{data_folder}' folder. Please check the folder path or add CSV files.")
    exit()

df_list = []
for file in csv_files:
    try:
        temp_df = pd.read_csv(file)
        df_list.append(temp_df)
    except Exception as e:
        print(f"Error reading file {file}: {e}")

if not df_list:
    print("No valid data could be loaded from the CSV files.")
    exit()

df = pd.concat(df_list, ignore_index=True)

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
plot_folder = 'plots'
os.makedirs(plot_folder, exist_ok=True)
plot_filename = os.path.join(plot_folder, os.path.splitext(os.path.basename(file))[0] + '.png')
plt.savefig(plot_filename)

# Output the name of the file created
print(f"Plot saved as '{plot_filename}'.")
