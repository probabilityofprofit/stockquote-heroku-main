import streamlit as st
import yfinance as yf
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
        else:
            value = info.get(attribute, 'N/A')

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
                lighter_color = '#c7e0c4' if color == 'green' else '#f7d1cf'

                additional_header_html = f"""
                    <style>
                    .custom-gap {{
                        margin-bottom: 0rem !important;
                    }}
                    </style>
                    <div class="custom-gap">
                        <span style='font-size:31px;'>{current_price} 
                        <span style='color:{color}; font-size:31px;'>{price_change}</span> 
                        (<span style='color:{lighter_color}; font-size:31px;'>{price_change_percentage}%</span>)
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
                        pass

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
