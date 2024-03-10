import streamlit as st
import yfinance as yf
from yahooquery import Ticker
import pandas as pd

from timestamp import convert_unix_timestamp_to_date, convert_unix_to_date
from attribute_mapping import (
    profile1_info_mapping, profile2_info_mapping, profile4_info_mapping,
    financial_info_mapping, financial_fiscal_mapping, financial_profitability_mapping,
    financial_management_mapping, financial_income_mapping, financial_balance_mapping,
    financial_cash_mapping, financial_price_mapping, financial_stock_mapping,
    financial_share_mapping, financial_dividends_mapping, summary1_info_mapping,
    summary2_info_mapping, finance_statements_mapping,
)

from summary_tab_utils import get_fund_weightings, display_fund_info, get_profile_weightings, display_profile_info, get_category_weightings, display_category_info, get_performance_weightings, display_performance_info
from statistics_tab_utils import display_valuation_measures
from historicaldata_tab_utils import get_historical_data, display_historical_data
from profile_tab_utils import display_key_executives
from financials_tab_utils import get_financials_data, display_financials_data
from holdings_tab_utils import get_position_weightings, display_position_info, get_sector_weightings, display_sector_info, get_equity_weightings, display_equity_info, get_bond_holdings_data, display_bond_holdings_data, get_bond_ratings, display_bond_ratings, get_fund_holding_info, display_fund_holding_info
from analysis_tab_utils import get_earnings_trend_data, display_earnings_trend_data
from option_tab_utils import display_option_chain

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def get_current_price(symbol):
    stock_info = Ticker(symbol).summary_detail
    ask_price = stock_info.get(symbol, {}).get('ask', 'N/A')
    previous_close = stock_info.get(symbol, {}).get('previousClose', 'N/A')

    if ask_price == 'N/A':
        return previous_close
    else:
        return ask_price

def display_stock_info(info, mapping):
    data = {}
    for attribute, (alternative_name, format_specifier) in mapping.items():
        if attribute == 'averageVolume' and info.get(attribute, 0) == 0.00:
            continue
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
        
        if attribute == 'bid_bidSize':
            bid = info.get('bid', 'N/A')
            bidSize = info.get('bidSize', 'N/A')

            # Check if bid and bidSize are not 'N/A' before formatting
            if bid != 'N/A' and bidSize != 'N/A':
                value = f"{bid} x {bidSize}"
            else:
                # If either bid or bidSize is 'N/A', skip this attribute
                continue

        elif attribute == 'ask_askSize':
            ask = info.get('ask', 'N/A')
            askSize = info.get('askSize', 'N/A')

            # Check if ask and askSize are not 'N/A' before formatting
            if ask != 'N/A' and askSize != 'N/A':
                value = f"{ask} x {askSize}"
            else:
                # If either ask or askSize is 'N/A', skip this attribute
                continue

        elif attribute == 'dayLow_dayHigh':
            dayLow = info.get('dayLow', 'N/A')
            dayHigh = info.get('dayHigh', 'N/A')

            # Check if dayLow and dayHigh are not 'N/A' before formatting
            if dayLow != 'N/A' and dayHigh != 'N/A':
                value = f"{dayLow} - {dayHigh}"
            else:
                # If either dayLow or dayHigh is 'N/A', skip this attribute
                continue
        
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

        elif attribute == 'fundInceptionDate':
            inception_date_unix = info.get(attribute, 'N/A')

            # Check if fiscal_date_unix is not 'N/A' before formatting
            if inception_date_unix != 'N/A':
                # Convert Unix timestamp to formatted date
                inception_date_formatted = convert_unix_timestamp_to_date(inception_date_unix)
            else:
                inception_date_formatted = 'N/A'

            value = inception_date_formatted
        
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

        # Format values in millions or billions (excluding 'Full-Time Employees')
        if isinstance(value, (int, float)) and attribute != 'fullTimeEmployees':
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
            elif magnitude == 4:
                formatted_value = '{:,.2f}T'.format(value)
            else:
                formatted_value = '{:,.2f}'.format(value)

            if magnitude in [2, 3, 4]:  # Apply the custom format only for millions and billions
                value = formatted_value


        if format_specifier is not None and isinstance(value, (int, float)):
            value = format_specifier.format(value)

        # Check if the attribute is in summary1_info_mapping
        if attribute in summary1_info_mapping:
            label = f"{alternative_name.capitalize()}: " if alternative_name != '' else ''
            st.write(f"<div style='display: flex; justify-content: space-between;'><div>{label}</div><div style='text-align: right;'>{value}</div></div>", unsafe_allow_html=True)

        # Check if the attribute is in summary2_info_mapping
        elif attribute in summary2_info_mapping:
            label = f"{alternative_name.capitalize()}: " if alternative_name != '' else ''
            st.write(f"<div style='display: flex; justify-content: space-between;'><div>{label}</div><div style='text-align: right;'>{value}</div></div>", unsafe_allow_html=True)

        # Check if the attribute is in any of the financial dictionaries
        elif attribute in financial_fiscal_mapping or attribute in financial_profitability_mapping or attribute in financial_management_mapping or attribute in financial_income_mapping or attribute in financial_balance_mapping or attribute in financial_cash_mapping or attribute in financial_price_mapping or attribute in financial_stock_mapping or attribute in financial_share_mapping or attribute in financial_dividends_mapping:
            label = f"{alternative_name.capitalize()}: " if alternative_name != '' else ''
            st.write(f"<div style='display: flex; justify-content: space-between;'><div>{label}</div><div style='text-align: right;'>{value}</div></div>", unsafe_allow_html=True)

        # Check if the attribute is in profile2_info_mapping
        elif attribute in profile2_info_mapping:
            label = f"{alternative_name.capitalize()}: " if alternative_name != '' else ''
            st.write(f"<div style='display: flex; justify-content: space-between;'><div>{label}</div><div style='text-align: right;'>{value}</div></div>", unsafe_allow_html=True)

        # For other attributes, display normally without alignment
        else:
            st.write(f"{alternative_name.capitalize()} {value}")

        data[attribute] = value

    return data

@st.cache_resource(show_spinner=False)
def get_fund_weightings_cached(symbol):
    return get_fund_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_profile_weightings_cached(symbol):
    return get_profile_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_category_weightings_cached(symbol):
    return get_category_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_performance_weightings_cached(symbol):
    return get_performance_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_bond_ratings_cached(symbol):
    return get_bond_ratings(symbol)

@st.cache_resource(show_spinner=False)
def get_bond_holdings_data_cached(symbol):
    return get_bond_holdings_data(symbol)

@st.cache_resource(show_spinner=False)
def get_equity_weightings_cached(symbol):
    return get_equity_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_sector_weightings_cached(symbol):
    return get_sector_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_position_weightings_cached(symbol):
    return get_position_weightings(symbol)

@st.cache_resource(show_spinner=False)
def get_fund_holding_info_cached(symbol):
    return get_fund_holding_info(symbol)

@st.cache_resource(show_spinner=False)
def display_valuation_measures_cached(symbol):
    return display_valuation_measures(symbol)

@st.cache_resource(show_spinner=False)
def get_earnings_trend_data_cached(symbol):
    return get_earnings_trend_data(symbol)

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
            current_price = get_current_price(symbol)
            previous_close = stock_info.get('regularMarketPreviousClose', 'N/A')
            price_change = round(current_price - previous_close, 4)
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
                "Holdings",
                "Analysis",
                "Options"
            ])

            with tabs[0]:
                st.write("#### Summary")
                
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                # Separate content into two columns
                col1, col2 = st.columns(2)
            with col1:
                display_stock_info(stock_info, summary1_info_mapping)

                # Call the function to get fund weightings
                fund_weightings = get_fund_weightings_cached(symbol)

                # Display fund weightings if available
                if fund_weightings:
                    display_fund_info(fund_weightings)
                else:
                    # Instead of displaying a warning, simply don't display anything
                    pass
                
                # Call the function to get profile weightings
                profile_weightings = get_profile_weightings_cached(symbol)

                # Display fund weightings if available
                if profile_weightings:
                    display_profile_info(profile_weightings)
                else:
                    # Instead of displaying a warning, simply don't display anything
                    pass

                # Call the function to get category weightings
                category_weightings = get_category_weightings_cached(symbol)

                # Display fund weightings if available
                if category_weightings:
                    display_category_info(category_weightings)
                else:
                    # Instead of displaying a warning, simply don't display anything
                    pass
            
            with col2:
                display_stock_info(stock_info, summary2_info_mapping)
                
                # Call the function to get performance weightings
                performance_weightings = get_performance_weightings_cached(symbol)

                # Display performance weightings if available
                if performance_weightings:
                    display_performance_info(performance_weightings)
                else:
                    # Instead of displaying a warning, simply don't display anything
                    pass

            st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

            with tabs[1]:
                st.write("#### Chart")
                display_stock_info(stock_info, financial_info_mapping)
                
            with tabs[2]:
                st.write("#### Valuation Measures")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Display the valuation measures
                display_valuation_measures_cached(symbol)

                col1, col2 = st.columns(2)

                with col1:
                    st.write("#### Trading Information")
                    st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                    st.write("##### Stock Price History")
                    display_stock_info(stock_info, financial_stock_mapping)
                    st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                    st.write("##### Share Statistics")
                    display_stock_info(stock_info, financial_share_mapping)
                    st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                    st.write("##### Dividends & Splits")
                    display_stock_info(stock_info, financial_dividends_mapping)

                with col2:
                    # Check if there is any data from financial_fiscal_mapping, financial_profitability_mapping, and financial_management_mapping
                    if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_fiscal_mapping) \
                            or any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_profitability_mapping) \
                            or any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_management_mapping) \
                            or any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_income_mapping) \
                            or any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_balance_mapping) \
                            or any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_cash_mapping):
                        st.write("#### Financial Highlights")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                
                        # Check if there is any data from financial_fiscal_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_fiscal_mapping):
                            st.write("##### Fiscal Year")
                            display_stock_info(stock_info, financial_fiscal_mapping)
                            st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                        
                        # Check if there is any data from financial_profitability_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_profitability_mapping):
                            st.write("##### Profitability")
                            display_stock_info(stock_info, financial_profitability_mapping)
                            st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                        
                        # Check if there is any data from financial_management_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_management_mapping):
                            st.write("##### Management effectiveness")
                            display_stock_info(stock_info, financial_management_mapping)
                            st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                        
                        # Check if there is any data from financial_income_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_income_mapping):
                            st.write("##### Income Statement")
                            display_stock_info(stock_info, financial_income_mapping)
                            st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                        
                        # Check if there is any data from financial_balance_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_balance_mapping):
                            st.write("##### Balance Sheet")
                            display_stock_info(stock_info, financial_balance_mapping)
                            st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Check if there is any data from financial_cash_mapping
                        if any(stock_info.get(attribute, 'N/A') != 'N/A' for attribute in financial_cash_mapping):
                            st.write("##### Cash Flow Statement")
                            display_stock_info(stock_info, financial_cash_mapping)

            with tabs[3]:
                st.write("#### Historical Data")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Fetch historical data
                historical_data = get_historical_data(symbol)

                # Display historical data in a datatable
                display_historical_data(symbol, historical_data)

            with tabs[4]:
                st.write("#### Profile")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Separate content into two columns
                col1, col2 = st.columns(2)
                with col1:
                    display_stock_info(stock_info, profile1_info_mapping)
                with col2:
                    display_stock_info(stock_info, profile2_info_mapping)
                    pass

                st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                st.write("##### Description")
                display_stock_info(stock_info, profile4_info_mapping)
                st.markdown("""<hr style="height:2px; margin-top: 5px; margin-bottom: 5px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Call the new display_key_executives function
                display_key_executives(stock_info)


                with tabs[5]:
                    st.write("#### Financials")
                    st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    # Separate content into two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Add a button to select statement type
                        statement_type = st.radio("Select Financial Statement:", ('Income Statement', 'Balance Sheet', 'Cash Flow'))

                    with col2:
                        # Add a button to select the period (annual or quarterly)
                        period = st.radio("Select Period:", ('Annual', 'Quarterly'))
                        selected_period = 'annual' if period == 'Annual' else 'quarterly'
                    
                    # Map the user-friendly names to the corresponding API names
                    statement_type_mapping = {
                        'Income Statement': 'income',
                        'Balance Sheet': 'balance',
                        'Cash Flow': 'cashflow'
                    }

                    selected_statement_type = statement_type_mapping.get(statement_type)
                    
                    st.write(f"#### {selected_statement_type.capitalize()} ({selected_period.capitalize()}) Financials")
                    
                    # Fetch financials data
                    financials_data = get_financials_data(symbol, selected_statement_type, selected_period)
                    
                    # Display financials data
                    display_financials_data(financials_data)

            with tabs[6]:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("#### Overall Portfolio Composition (%)")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get position weightings
                        position_weightings = get_position_weightings_cached(symbol)

                        # Display position weightings
                        if position_weightings:
                            display_position_info(position_weightings)
                        else:
                            st.warning("No position weightings data available.")
                                               
                    with col1:
                        st.write("#### Sector Weightings (%)")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get sector weightings
                        sector_weightings = get_sector_weightings_cached(symbol)

                        # Display sector weightings
                        if sector_weightings:
                            display_sector_info(sector_weightings)
                        else:
                            st.warning("No sector weightings data available.")

                    with col2:
                        st.write("#### Equity Holdings")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get sector weightings
                        equity_weightings = get_equity_weightings_cached(symbol)

                        # Display equity weightings
                        if equity_weightings:
                            display_equity_info(equity_weightings)
                        else:
                            st.warning("No Equity Holdings data available.")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                        st.write("#### Bond Holdings Data")
            
                        # Call the function to get bond holdings data
                        bond_holdings_data = get_bond_holdings_data_cached(symbol)
            
                        # Display bond holdings data
                        display_bond_holdings_data(bond_holdings_data)

                        st.write("#### Bond Ratings")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get bond ratings
                        bond_ratings = get_bond_ratings_cached(symbol)

                        # Display bond ratings
                        display_bond_ratings(bond_ratings)

                    
                    st.write("#### Top 10 Holdings")
                    st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                    # Call the function to get fund holding information
                    fund_holding_info = get_fund_holding_info_cached(symbol)

                    # Display fund holding information in a DataFrame
                    display_fund_holding_info(fund_holding_info)
                    # Separate content into two columns

            with tabs[7]:
                st.write("#### Analysis")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Fetch earnings trend data
                earnings_trend_data = get_earnings_trend_data_cached(symbol)

                # Display earnings trend data
                display_earnings_trend_data(earnings_trend_data)

            with tabs[8]:
                st.write("#### Options")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

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
            st.exception(e) # <- Remove this later 

    else:
        st.warning("Please enter a stock symbol.")

if __name__ == "__main__":
    main()