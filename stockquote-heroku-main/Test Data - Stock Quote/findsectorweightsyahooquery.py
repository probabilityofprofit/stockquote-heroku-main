from yahooquery import Ticker

t = Ticker('DIA')

# sector weightings, returns pandas DataFrame
sector_weightings = t.fund_sector_weightings
print(sector_weightings)