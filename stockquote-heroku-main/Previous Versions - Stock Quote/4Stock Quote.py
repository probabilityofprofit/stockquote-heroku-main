import streamlit as st
import yfinance as yf
from timestamp import convert_unix_timestamp_to_date
from attribute_mapping import (
    company1_info_mapping,
    company2_info_mapping,
    financial_info_mapping,
    market_info_mapping,
    risk_info_mapping,
    summary1_info_mapping,
    summary2_info_mapping,
    target_price_mapping,
    finance_statements_mapping,
    additional_information_mapping
)

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def display_stock_info(info, mapping):
    for attribute, (alternative_name, format_specifier) in mapping.items():
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
        else:
            value = info.get(attribute, 'N/A')

        # Skip attributes with 'N/A' value
        if value == 'N/A':
            continue

        if format_specifier is not None and isinstance(value, (int, float)):
            value = format_specifier.format(value)

        # Check if alternative_name is not empty before displaying the label
        label = f"**{alternative_name.capitalize()}:** " if alternative_name != '' else ''
        st.write(f"{label}{value}")

def main():
    st.title("Stock Quote Web Application")

    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):").upper()

    if st.button("Get Stock Information"):
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
                        pass

                with tabs[1]:
                    st.write("#### Chart")
                    display_stock_info(stock_info, financial_info_mapping)

                with tabs[2]:
                    st.write("#### Statistics")
                    display_stock_info(stock_info, market_info_mapping)

                with tabs[3]:
                    st.write("#### Historical Data")
                    display_stock_info(stock_info, risk_info_mapping)

                with tabs[4]:
                    st.write("#### Profile")

                    # Separate content into two columns
                    col1, col2 = st.columns(2)
                    with col1:
                        display_stock_info(stock_info, company1_info_mapping)
                    with col2:
                        display_stock_info(stock_info, company2_info_mapping)

                    st.write("#### Key Executives")

                    # Display a table for the key executives
                    key_executives_data = stock_info.get('companyOfficers', [])
                    key_executives_columns = ['Name', 'Title', 'Pay', 'Exercised', 'Year Born']
                    key_executives_table = [key_executives_columns]  # Include headers in the first row

                    for executive in key_executives_data:
                        name = executive.get('name', 'N/A')
                        title = executive.get('title', 'N/A')
                        pay = executive.get('totalPay', 'N/A')
                        exercised = executive.get('exercisedValue', 'N/A')
                        year_born = executive.get('yearBorn', 'N/A')

                        key_executives_table.append([name, title, pay, exercised, year_born])

                    st.table(data=key_executives_table)

                with tabs[5]:
                    st.write("#### Financials")
                    display_stock_info(stock_info, target_price_mapping)

                with tabs[6]:
                    st.write("#### Analysis")
                    display_stock_info(stock_info, finance_statements_mapping)

                with tabs[7]:
                    st.write("#### Options")
                    display_stock_info(stock_info, additional_information_mapping)

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a stock symbol.")

if __name__ == "__main__":
    main()