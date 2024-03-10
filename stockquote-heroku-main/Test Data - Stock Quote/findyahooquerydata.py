from yahooquery import Ticker

def get_ask(ticker_symbol):
    # Create a Ticker object with the specified symbol
    ticker = Ticker(ticker_symbol)

    try:
        # Get the summary_detail data for the specified ticker
        summary_detail = ticker.summary_detail[ticker_symbol]

        # Extract the 'ask' value from the summary_detail data
        ask_price = summary_detail.get('previousClose')

        if ask_price is not None:
            return f"The 'ask' price for {ticker_symbol} is: {ask_price}"
        else:
            return f"Ask price not available for {ticker_symbol}"

    except KeyError:
        return f"Invalid ticker symbol: {ticker_symbol}"

# Example usage
ticker_symbol = 'VTSAX'
result = get_ask(ticker_symbol)
print(result)