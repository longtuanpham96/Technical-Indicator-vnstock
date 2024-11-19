import numpy as np
import pandas as pd
from vnstock3 import Vnstock

# Fetch historical stock data
stock = Vnstock().stock(symbol='MBB', source='VCI')
df = stock.quote.history(start='2014-01-01', end='2024-06-30', interval='1D')

# Ensure column names are correct
df.rename(columns={'time': 'date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format

# Define period
period = 14

# Extract High, Low, and Close prices
high = df['High'].values
low = df['Low'].values
close = df['Close'].values
previous_close = df['Close'].shift().values  # Previous Close

# Calculate True Range (TR)
tr1 = high - low
tr2 = np.abs(high - previous_close)
tr3 = np.abs(low - previous_close)
true_range = np.maximum.reduce([tr1, tr2, tr3])  # Element-wise max
true_range[0] = tr1[0]  # Initialize first TR value

# Calculate ATR using 14-day period Exponential Weighted Average (EWA)
atr = np.zeros_like(high)
atr[period] = np.mean(true_range[1:period+1])  # Initial ATR value as a simple mean

# Calculate the ATR for subsequent days using EMA
for i in range(period + 1, len(atr)):
    atr[i] = (true_range[i] * (1 / period)) + (atr[i - 1] * (1 - 1 / period))

# Add ATR to the DataFrame
df['ATR'] = atr

# Print message and display the first few rows
print(df[['date', 'High', 'Low', 'Close', 'ATR']].head(20))
