from yahooquery import Ticker

t = Ticker('AAPL')

# sector weightings, returns pandas DataFrame
valuation_measures = t.valuation_measures
print(valuation_measures)