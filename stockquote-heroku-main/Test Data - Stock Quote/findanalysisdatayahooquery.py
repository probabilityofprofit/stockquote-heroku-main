from yahooquery import Ticker

def get_earnings_trend_data(symbol):
    # Create Ticker object
    stock_ticker = Ticker(symbol)
    
    # Get earnings trend data
    earnings_trend_data = stock_ticker.earnings_trend
    
    # Extract data for each period
    periods_data = {}
    
    for trend_data in earnings_trend_data[symbol]['trend']:
        period = trend_data['period']
        periods_data[period] = {
            'endDate': trend_data['endDate'],
            'growth': trend_data['growth'],
            'earningsEstimate': trend_data['earningsEstimate'],
            'revenueEstimate': trend_data['revenueEstimate'],
            'epsTrend': trend_data['epsTrend'],
            'epsRevisions': trend_data['epsRevisions']
        }
    
    return periods_data

# Example usage for "aapl" symbol
symbol = 'aapl'
earnings_trend_data = get_earnings_trend_data(symbol)

# Print data for each period
for period, data in earnings_trend_data.items():
    print(f"\nPeriod: {period}")
    print(f"End Date: {data['endDate']}")
    print(f"Growth: {data['growth']}")
    print(f"Earnings Estimate: {data['earningsEstimate']}")
    print(f"Revenue Estimate: {data['revenueEstimate']}")
    print(f"EPS Trend: {data['epsTrend']}")
    print(f"EPS Revisions: {data['epsRevisions']}")
