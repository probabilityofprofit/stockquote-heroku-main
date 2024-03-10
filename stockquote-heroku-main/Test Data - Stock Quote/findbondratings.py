from yahooquery import Ticker

# Replace 'hasgx' with your actual fund symbol
fund_symbol = 'VBTLX'

# Create a Ticker instance for the fund
fund = Ticker(fund_symbol)

# Get fund holding information
fund_holding_info = fund.fund_holding_info

# Extract bond ratings data
bond_ratings = fund_holding_info[fund_symbol]['bondRatings']

# Display bond ratings data
print("Bond Ratings Data:")
print(bond_ratings)
