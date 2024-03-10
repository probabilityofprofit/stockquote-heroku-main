import streamlit as st
import yfinance as yf
import pandas as pd
from timestamp import convert_unix_timestamp_to_date
from option_chain_utils import display_option_chain
from historical_data_utils import get_historical_data, display_historical_data
from attribute_mapping import (
    profile1_info_mapping, profile2_info_mapping, profile4_info_mapping,
    financial_info_mapping, financial_fiscal_mapping, financial_profitability_mapping, financial_management_mapping, financial_income_mapping, financial_balance_mapping, financial_cash_mapping, financial_stock_mapping, financial_share_mapping, financial_dividends_mapping,
    summary1_info_mapping, summary2_info_mapping,
    target_price_mapping,
    finance_statements_mapping,
)

# Function to convert Unix timestamp to date
def convert_unix_to_date(unix_timestamp):
    if unix_timestamp == 'N/A':
        return 'N/A'
    else:
        return convert_unix_timestamp_to_date(unix_timestamp)


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def display_stock_info(info, mapping):
    data = {}
    for attribute, (alternative_name, format_specifier) in mapping.items():
        if attribute == 'sharesShort' or attribute == 'shortRatio' or attribute == 'shortPercentOfFloat' or attribute == 'sharesPercentSharesOut':
            date_short_interest = info.get('dateShortInterest', 'N/A')
            alternative_name = alternative_name.format(dateShortInterest=convert_unix_to_date(date_short_interest))
        
        if attribute == 'sharesShortPriorMonth':
            date_short_prior = info.get('sharesShortPreviousMonthDate', 'N/A')
            alternative_name = alternative_name.format(sharesShortPreviousMonthDate=convert_unix_to_date(date_short_prior))

        if attribute == 'dateShortInterest':
            date_short_interest = info.get('dateShortInterest', 'N/A')
            alternative_name = alternative_name.format(dateShortInterest=convert_unix_to_date(date_short_interest))

        if attribute == 'city_state_zip':
            city = info.get('city', 'N/A')
            state = info.get('state', 'N/A')
            zip_code = info.get('zip', 'N/A')
            # Check if any component is 'N/A'; if so, skip this attribute
            if city == 'N/A' or state == 'N/A' or zip_code == 'N/A':
                continue
            value = f"{city}, {state} {zip_code}"
        
        elif attribute == 'bid_bidSize':
            bid = info.get('bid', 'N/A')
            bidSize = info.get('bidSize', 'N/A')
            value = f"{bid} x {bidSize}"
        
        elif attribute == 'ask_askSize':
            ask = info.get('ask', 'N/A')
            askSize = info.get('askSize', 'N/A')
            value = f"{ask} x {askSize}"
        
        elif attribute == 'dayLow_dayHigh':
            dayLow = info.get('dayLow', 'N/A')
            dayHigh = info.get('dayHigh', 'N/A')
            value = f"{dayLow} - {dayHigh}"
        
        elif attribute == 'fiftyTwoWeekLow_fiftyTwoWeekHigh':
            fiftyTwoWeekLow = info.get('fiftyTwoWeekLow', 'N/A')
            fiftyTwoWeekHigh = info.get('fiftyTwoWeekHigh', 'N/A')
            value = f"{fiftyTwoWeekLow} - {fiftyTwoWeekHigh}"
        
        elif attribute == 'dividendRate_dividendYield':
            dividendRate = info.get('dividendRate', 'N/A')
            dividendYield = info.get('dividendYield', 'N/A')
            # Check if both dividendRate and dividendYield are not 'N/A' before formatting
            if dividendRate != 'N/A' and dividendYield != 'N/A':
                # Format dividendYield as a percentage
                dividendYield_formatted = f"{dividendYield * 100:.2f}%"
                value = f"{dividendRate} ({dividendYield_formatted})"
            else:
                # If either dividendRate or dividendYield is 'N/A', skip this attribute
                continue
        
        elif attribute == 'exDividendDate':
            ex_dividend_date_unix = info.get('exDividendDate', 'N/A')
            # Check if ex_dividend_date_unix is not 'N/A' before formatting
            if ex_dividend_date_unix != 'N/A':
                # Convert Unix timestamp to formatted date
                ex_dividend_date_formatted = convert_unix_timestamp_to_date(ex_dividend_date_unix)
            else:
                ex_dividend_date_formatted = 'N/A'

            value = ex_dividend_date_formatted
        
        elif attribute == 'lastSplitDate':
            ex_dividend_date_unix = info.get('lastSplitDate', 'N/A')

            # Check if ex_dividend_date_unix is not 'N/A' before formatting
            if ex_dividend_date_unix != 'N/A':
                # Convert Unix timestamp to formatted date
                ex_dividend_date_formatted = convert_unix_timestamp_to_date(ex_dividend_date_unix)
            else:
                ex_dividend_date_formatted = 'N/A'

            value = ex_dividend_date_formatted
        
        elif attribute == 'lastFiscalYearEnd' or attribute == 'mostRecentQuarter':
            fiscal_date_unix = info.get(attribute, 'N/A')

            # Check if fiscal_date_unix is not 'N/A' before formatting
            if fiscal_date_unix != 'N/A':
                # Convert Unix timestamp to formatted date
                fiscal_date_formatted = convert_unix_timestamp_to_date(fiscal_date_unix)
            else:
                fiscal_date_formatted = 'N/A'

            value = fiscal_date_formatted
        
        elif attribute == 'debtToEquity':
            debt_to_equity = info.get(attribute, 'N/A')
            # Check if debt_to_equity is not 'N/A' before formatting
            if debt_to_equity != 'N/A':
                # Divide the value by 100 and format it as a percentage
                value = '{:.2%}'.format(debt_to_equity / 100)

        else:
            value = info.get(attribute, 'N/A')

        
        # Skip attributes with 'N/A' value
        if value == 'N/A':
            continue

        # Format values in millions or billions
        if isinstance(value, (int, float)):
            magnitude = 0
            while abs(value) >= 1000:
                magnitude += 1
                value /= 1000.0

            # Choose the appropriate format specifier based on magnitude
            if magnitude == 1:
                formatted_value = '{:,.2f}K'.format(value)
            elif magnitude == 2:
                formatted_value = '{:,.2f}M'.format(value)
            elif magnitude == 3:
                formatted_value = '{:,.2f}B'.format(value)
            else:
                formatted_value = '{:,.2f}'.format(value)

            if magnitude in [2, 3]:  # Apply the custom format only for millions and billions
                value = formatted_value

        if format_specifier is not None and isinstance(value, (int, float)):
            value = format_specifier.format(value)

        # Check if alternative_name is not empty before displaying the label
        label = f"**{alternative_name.capitalize()}:** " if alternative_name != '' else ''
        st.write(f"{label}{value}")

        data[attribute] = value

    return data

def main():
    # Get query parameters from the URL
    query_params = st.experimental_get_query_params()

    # Extract the symbol from the query parameters
    symbol = query_params.get("symbol", [""])[0].upper()

    st.title("Stock Quote")

    # Set the initial value of the text input to the extracted symbol
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):", symbol)

    # Placeholder variable for expiration date
    selected_expiration_date = None

    if symbol:
        try:
            stock_info = get_stock_info(symbol)

            # Display shortName as header
            st.header(f"{stock_info.get('shortName', '')} ({symbol})")

            # Additional header for the requested information
            current_price = stock_info.get('ask', 'N/A')
            previous_close = stock_info.get('regularMarketPreviousClose', 'N/A')
            price_change = round(current_price - previous_close, 2)
            price_change_percentage = round((price_change / previous_close) * 100, 2)

            # Determine color based on the price change
            color = 'green' if price_change >= 0 else 'red'
            lighter_color = '#00bf23' if color == 'green' else '#f54242'

            # Add positive or negative sign to price_change and price_change_percentage
            price_change_sign = '+' if price_change >= 0 else ''
            price_change_percentage_sign = '+' if price_change_percentage >= 0 else ''

            additional_header_html = f"""
                <style>
                .custom-gap {{
                    margin-bottom: 0rem !important;
                }}
                </style>
                <div class="custom-gap">
                    <span style='font-size:31px;'>{current_price} 
                    <span style='color:{color}; font-size:31px;'>{price_change_sign}{price_change}</span> 
                    (<span style='color:{color}; font-size:31px;'>{price_change_percentage_sign}{price_change_percentage}%</span>)
                </div>
            """
            additional_header = st.markdown(additional_header_html, unsafe_allow_html=True)

            # Adjust the color of stock_price_at_ask_html
            stock_price_at_ask_html = f"<span style='color:#5B565A; font-size:12px;'>Stock Price at Ask | <span style='color:{lighter_color}; font-size:12px;'>% Change from Previous Close</span>"
            st.markdown(stock_price_at_ask_html, unsafe_allow_html=True)

            # Create tabs for each attribute mapping
            tabs = st.tabs([
                "Summary",
                "Chart",
                "Statistics",
                "Historical Data",
                "Profile",
                "Financials",
                "Analysis",
                "Options"
            ])

            with tabs[0]:
                st.write("#### Summary")

                # Separate content into two columns
                col1, col2 = st.columns(2)
                with col1:
                    display_stock_info(stock_info, summary1_info_mapping)
                with col2:
                    display_stock_info(stock_info, summary2_info_mapping)

            with tabs[1]:
                st.write("#### Chart")
                display_stock_info(stock_info, financial_info_mapping)

            with tabs[2]:
                # st.write("#### Valuation Measures")

                # # Create a DataFrame from financial_info_mapping
                # financial_info_df = pd.DataFrame.from_dict(financial_info_mapping, orient='index', columns=['Label', 'Format'])
                # financial_info_df['Current'] = financial_info_df.index.map(lambda x: stock_info.get(x, 'N/A'))

                # # Display the DataTable without the default index column
                # st.dataframe(financial_info_df[['Current']])

                # Separate content into two columns
                col1, col2 = st.columns(2)
                with col1:
                    st.write("#### Financial Highlights")

                    st.write("##### Fiscal Year")
                    display_stock_info(stock_info, financial_fiscal_mapping)

                    st.write("##### Profitability")
                    display_stock_info(stock_info, financial_profitability_mapping)

                    st.write("##### Management effectiveness")
                    display_stock_info(stock_info, financial_management_mapping)

                    st.write("##### Income Statement")
                    display_stock_info(stock_info, financial_income_mapping)

                    st.write("##### Balance Sheet")
                    display_stock_info(stock_info, financial_balance_mapping)

                    st.write("##### Cash Flow Statement")
                    display_stock_info(stock_info, financial_cash_mapping)

                with col2:
                    st.write("#### Trading Information")
                    
                    st.write("##### Stock Price History")
                    display_stock_info(stock_info, financial_stock_mapping)

                    st.write("##### Share Statistics")
                    display_stock_info(stock_info, financial_share_mapping)

                    st.write("##### Dividends & Splits")
                    display_stock_info(stock_info, financial_dividends_mapping)


            with tabs[3]:
                st.write("#### Historical Data")

                # Fetch historical data
                historical_data = get_historical_data(symbol)

                # Display historical data in a datatable
                display_historical_data(symbol, historical_data)

            with tabs[4]:
                st.write("#### Profile")

                # Separate content into two columns
                col1, col2 = st.columns(2)
                with col1:
                    display_stock_info(stock_info, profile1_info_mapping)
                with col2:
                    display_stock_info(stock_info, profile2_info_mapping)
                    pass

                st.write("#### Description")
                display_stock_info(stock_info, profile4_info_mapping)

                st.write("#### Key Executives")

                # Columns to display
                columns_to_display = ["name", "title", "totalPay", "exercisedValue", "yearBorn"]

                # Display Key Executives information using DataTable
                key_executives_data = stock_info.get('companyOfficers', [])

                # Check if there is at least one name present in the data
                if any(executive.get("name") for executive in key_executives_data):
                    key_executives_df = pd.DataFrame(key_executives_data)

                    # Filter and rename columns for better display
                    key_executives_df_display = key_executives_df[columns_to_display].rename(columns={
                        "name": "Name",
                        "title": "Title",
                        "totalPay": "Total Pay",
                        "exercisedValue": "Exercised Value",
                        "yearBorn": "Year Born"
                    })

                    # Display the DataFrame with updated column names and only the specified columns
                    st.dataframe(key_executives_df_display, hide_index=True)
                else:
                    st.info("No Key Executive information available.")

            with tabs[5]:
                st.write("#### Financials")
                display_stock_info(stock_info, target_price_mapping)

            with tabs[6]:
                st.write("#### Analysis")
                display_stock_info(stock_info, finance_statements_mapping)

            with tabs[7]:
                st.write("#### Option Chain")

                # Fetch expiration dates only once
                if selected_expiration_date is None:
                    expiration_dates = yf.Ticker(symbol).options
                    if not expiration_dates:
                        st.warning("No option chain data available for this stock.")
                    else:
                        selected_expiration_date = expiration_dates[0]

                # Display subheader for Calls and Puts
                st.markdown(
                    """
                    <style>
                    .split-header {
                        display: flex;
                        justify-content: space-between;
                    }
                    </style>
                    <div class="split-header">
                        <div>Calls</div>
                        <div>Puts</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Display option chain using the function from option_chain_utils.py
                selected_expiration_date = display_option_chain(symbol, expiration_dates, selected_expiration_date)


        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a stock symbol.")

if __name__ == "__main__":
    main()