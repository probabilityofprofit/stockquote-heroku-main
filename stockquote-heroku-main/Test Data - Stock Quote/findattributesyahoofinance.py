import yfinance as yf

# Replace 'AAPL' with the ticker symbol of the stock you're interested in
ticker_symbol = 'AGJ.DE'

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Get available attributes
info = ticker.info

# Print the available attributes
for key, value in info.items():
    print(f"{key}: {value}")
