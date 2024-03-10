from yahooquery import Ticker

def get_bond_holdings_data(ticker):
    try:
        fund = Ticker(ticker)
        bond_holdings = fund.fund_bond_holdings

        maturity = bond_holdings[ticker]['maturity']
        duration = bond_holdings[ticker]['duration']
        maturity_cat = bond_holdings[ticker]['maturityCat']
        duration_cat = bond_holdings[ticker]['durationCat']

        return {
            "maturity": maturity,
            "duration": duration,
            "maturityCat": maturity_cat,
            "durationCat": duration_cat
        }
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
ticker_data = get_bond_holdings_data('VBTLX')
print(ticker_data)
