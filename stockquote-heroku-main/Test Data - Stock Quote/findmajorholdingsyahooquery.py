from yahooquery import Ticker

# Define the fund ticker symbol
fund_ticker = 'DIA'

# Create a Ticker object
fund = Ticker(fund_ticker)

# Get the fund holding information
holding_info = fund.fund_holding_info

# Extract relevant data
holdings_data = holding_info[fund_ticker]['holdings']

# Print the holdings information
print("Holdings:")
for holding in holdings_data:
    symbol = holding.get("symbol", "")
    holding_name = holding.get("holdingName", "")
    holding_percent = holding.get("holdingPercent", "")
    print(f"Symbol: {symbol}, Holding Name: {holding_name}, Holding Percent: {holding_percent}")


