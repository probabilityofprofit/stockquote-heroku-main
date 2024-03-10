import streamlit as st
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Add this line
from datetime import datetime, timedelta
from fuzzywuzzy import process
import os

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
from summarychart10 import format_volume, has_minute_data_in_last_day 
from statistics_tab_utils import display_valuation_measures
from historicaldata_tab_utils import get_historical_data, display_historical_data
from profile_tab_utils import display_key_executives
from financials_tab_utils import get_financials_data, display_financials_data
from holdings_tab_utils import get_position_weightings, display_position_info, get_sector_weightings, display_sector_info, get_equity_weightings, display_equity_info, get_bond_holdings_data, display_bond_holdings_data, get_bond_ratings, display_bond_ratings, get_fund_holding_info, display_fund_holding_info
from analysis_tab_utils import get_earnings_trend_data, display_earnings_trend_data
from option_tab_utils import display_option_chain
from stock_options1 import stock_options
from st_keyup import st_keyup

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def get_current_price(symbol):
    stock_info = Ticker(symbol).summary_detail
    ask_price = stock_info.get(symbol, {}).get('ask', 'N/A')
    previous_close = stock_info.get(symbol, {}).get('previousClose', 'N/A')
    regular_open = stock_info.get(symbol, {}).get('regularMarketOpen', 'N/A')
    
    # If ask price N/A or ask price 0 use the previous close instead
    if ask_price == 'N/A' or ask_price == 0:
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

def find_related_options(user_input):
    user_input = user_input.upper()
    first_char = user_input[0] if user_input else ''

    folder_path = 'Listofsymbols'
    filename = os.path.join(folder_path, f"{first_char}.py")
    
    try:
        with open(filename, 'r') as file:
            options = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in file.readlines()}
    except FileNotFoundError:
        options = {}

    options_with_scores = process.extract(user_input, options.keys(), limit=5)
    related_options = [(option, options[option]) for option, score in options_with_scores]
    return related_options

def main():
    # Get query parameters from the URL
    query_params = st.experimental_get_query_params()

    # Extract the symbol from the query parameters
    symbol = query_params.get("symbol", [""])[0].upper()

    # st.title("Stock Quote")

    # Set the initial value of the text input to the extracted symbol
    symbol = st_keyup("Enter Stock Symbol (e.g., AAPL):", key="stock_symbol", value=symbol)

    # Check if the entered symbol is in the list of options
    symbol_valid = symbol.upper() in stock_options
    if symbol_valid:
        st.write(f"Selected Stock Symbol: {symbol} - {stock_options[symbol.upper()]}")
    elif symbol:
        st.warning("Invalid stock symbol. Please choose from the list.")

    # Find related options based on user input
    related_options = find_related_options(symbol)

    # Display related options as buttons
    for option, full_name in related_options:
        if st.button(f"{option} - {full_name}"):
            # Update selected symbol if the button is clicked
            symbol = option.strip("'")  # Remove unwanted characters
            st.write(f"Selected Stock Symbol: {symbol} - {full_name}")
            symbol_valid = True  # Set the flag to indicate a valid symbol
            
    # Placeholder variable for expiration date
    selected_expiration_date = None

    # Continue execution only if the symbol is valid
    if not symbol_valid:
        return

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
                # st.write("#### Summary")
                
                # Fetch historical stock data
                try:
                    stock_data = yf.download(symbol, period='1mo')
                    
                    # Check if stock_data is empty
                    if stock_data.empty:
                        st.error(f"No data available for the stock with symbol '{symbol}'. Please enter a valid symbol.")
                        st.stop()  # Stop further execution of the code

                except IndexError:
                    st.error(f"Stock with symbol '{symbol}' does not exist. Please enter a valid symbol.")
                    st.stop()  # Stop further execution of the code

                # Create two columns
                col1, col2 = st.columns([1, 1])

                # Check if 'Volume' column is present and contains non-zero values
                if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():
                    # If there is minute data available for the most recent day, include intraday options
                    if has_minute_data_in_last_day(symbol): 
                        time_period_options = {
                            '1d': {'interval': '2m', 'period': '1d'},
                            '5d': {'interval': '15m', 'period': '5d'},
                            '1mo': {'interval': '30m', 'period': '1mo'},
                            '6mo': {'interval': '1d', 'period': '6mo'},
                            'ytd': {'interval': '30m', 'period': 'ytd'},
                            '1y': {'interval': '1d', 'period': '1y'},
                            '5y': {'interval': '1wk', 'period': '5y'},
                            'max': {'interval': '1mo', 'period': 'max'}
                        }
                    else:
                        # If there is no minute data for the most recent day, exclude intraday options
                        time_period_options = {
                            '6mo': {'interval': '1d', 'period': '6mo'},
                            '1y': {'interval': '1d', 'period': '1y'},
                            '5y': {'interval': '1wk', 'period': '5y'},
                            'max': {'interval': '1wk', 'period': 'max'}
                        }
                else:
                    # If there is no minute data and no volume data, exclude intraday options
                    time_period_options = {
                        '1mo': {'interval': '1d', 'period': '1mo'},
                        'ytd': {'interval': '1d', 'period': 'ytd'},
                        '1y': {'interval': '1d', 'period': '1y'},
                        '5y': {'interval': '1wk', 'period': '5y'},
                        'max': {'interval': '1mo', 'period': 'max'}
                    }

                selected_option = col1.selectbox('Select Time Period:', list(time_period_options.keys()), key='unique_key_for_selectbox')

                # Option for selecting chart type
                chart_type_options = ['Line', 'Area', 'Candlestick']
                selected_chart_type = col2.selectbox('Select Chart Type:', chart_type_options, index=0, key='unique_key_for_chart_type_selectbox')

                # Fetch historical stock data based on selected time period
                interval = time_period_options[selected_option]['interval']
                period = time_period_options[selected_option]['period']
                stock_data = yf.download(symbol, interval=interval, period=period)

                # Calculate percentage change
                start_price = stock_data['Close'].iloc[0]
                end_price = stock_data['Close'].iloc[-1]
                percentage_change = ((end_price - start_price) / start_price) * 100

                # # Display stock dataframe
                # st.write(stock_data)

                if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():

                    if selected_option == '1d':
                        formatted_dates = stock_data.index.strftime('%I:%M %p')
                        formatted_labels = stock_data.index.strftime('%I %p')
                        hover_format = stock_data.index.strftime('%I:%M %p')
                        tickvals = formatted_dates[::64]  # Display every 125th date
                        ticktext = formatted_labels[::64]
                    elif selected_option in ['5d']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%a')
                        hover_format = stock_data.index.strftime('%a, %b %d, %I:%M %p')
                        tickvals = formatted_dates[::30]
                        ticktext = formatted_labels[::30]
                    elif selected_option in ['1mo']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::90]
                        ticktext = formatted_labels[::90]
                    elif selected_option in ['6mo']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::65]
                        ticktext = formatted_labels[::65]
                    elif selected_option in ['ytd']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::125]
                        ticktext = formatted_labels[::125]
                    elif selected_option in ['1y']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::126]
                        ticktext = formatted_labels[::126]
                    elif selected_option in ['5y']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::131]
                        ticktext = formatted_labels[::131]
                    elif selected_option in ['max']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::79]
                        ticktext = formatted_labels[::79]
                else:
                    
                    if selected_option in ['1mo']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::7]
                        ticktext = formatted_labels[::7]
                    elif selected_option in ['ytd']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::9]
                        ticktext = formatted_labels[::9]
                    elif selected_option in ['1y']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::126]
                        ticktext = formatted_labels[::126]
                    elif selected_option in ['5y']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::131]
                        ticktext = formatted_labels[::131]
                    elif selected_option in ['max']:
                        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
                        formatted_labels = stock_data.index.strftime('%b %#d, %y')
                        hover_format = stock_data.index.strftime('%b %#d, %y')
                        tickvals = formatted_dates[::79]
                        ticktext = formatted_labels[::79]

                # Create subplot with two y-axes
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                #Add shaded areas for every other tick on the x-axis for background
                for i in range(0, len(tickvals), 2):
                    fig.add_shape(
                        type="rect",
                        x0=tickvals[i],
                        x1=tickvals[i + 1] if i + 1 < len(tickvals) else formatted_dates[-1],
                        y0=-1e9,
                        y1=1e9,
                        fillcolor="rgba(245,245,245,1.000)",
                        opacity=1,
                        layer="below",
                        line=dict(width=0),
                    )

                # Default chart type is 'line'
                chart_type = selected_chart_type

                # Add trace based on chart type
                if chart_type == 'Line':
                    trace = go.Scatter(x=formatted_dates, y=stock_data['Close'], mode='lines', name=f'')
                elif chart_type == 'Area':
                    trace = go.Scatter(x=formatted_dates, y=stock_data['Close'], mode='lines', fill='tozeroy', name=f'', fillcolor='rgba(0, 104, 201, 1)')
                elif chart_type == 'Candlestick':
                    trace = go.Candlestick(x=formatted_dates,
                                        open=stock_data['Open'],
                                        high=stock_data['High'],
                                        low=stock_data['Low'],
                                        close=stock_data['Close'],
                                        name=f'{symbol}',
                                        hoverinfo='x+text+name')
                    
                    # Remove range slider for candlestick chart
                    fig.update_xaxes(rangeslider_visible=False)

                # Add trace to the subplot
                fig.add_trace(trace)

                # Check if volume data is available
                if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():
                    # Add bar trace for volume
                    volume_colors = ['red' if close_price < open_price else 'green' for open_price, close_price in zip(stock_data['Open'], stock_data['Close'])]

                    if chart_type in ['Line', 'Candlestick']:
                        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color=volume_colors, hoverinfo='skip'))
                    else:
                        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color='rgba(160, 198, 255, 1)', hoverinfo='skip'))

                    # Update axis labels and layout for volume data available
                    fig.update_yaxes(showspikes=True, nticks=5, spikemode="across", spikethickness=-2, side='right')
                    fig.update_yaxes(showspikes=True, spikemode="across", spikethickness=-2, side='right', secondary_y=True, showticklabels=False)

                    # Add this section to dynamically set the y-axis ranges based on selected_option
                    if selected_option == '1d':
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
                    elif selected_option in ['5d']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 4.01]
                    elif selected_option in ['1mo']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.01]
                    elif selected_option in ['6mo']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
                    elif selected_option in ['ytd']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
                    elif selected_option in ['1y']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
                    elif selected_option in ['5y']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
                    elif selected_option in ['max']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]

                else:
                    # Update axis labels and layout for no volume data available
                    fig.update_yaxes(showspikes=True, nticks=5, spikemode="across", spikethickness=-2, side='right')
                    fig.update_yaxes(showspikes=True, spikemode="across", spikethickness=-2, side='right', secondary_y=True, showticklabels=False)

                    # Add this section to dynamically set the y-axis ranges based on selected_option
                    if selected_option in ['1mo']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = None
                    elif selected_option in ['ytd']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = None
                    elif selected_option in ['1y']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = None    
                    elif selected_option in ['5y']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = None
                    elif selected_option in ['max']:
                        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
                        yaxis2_range = None

                fig.update_layout(
                    height=500,
                    hovermode='closest',
                    hoverlabel=dict(bgcolor="white", font_color="black", font_size=14, font_family="Arial", bordercolor="black"),
                    xaxis=dict(showspikes=True, spikemode="across", ticktext=ticktext, tickvals=tickvals, spikethickness=-2, fixedrange=True),
                    yaxis=dict(side='right', range=yaxis_range, fixedrange=True),
                    yaxis2=dict(showticklabels=False, overlaying='y', showgrid=False, range=yaxis2_range, fixedrange=True),
                    showlegend=False,
                    margin=dict(b=0, t=90)
                )

                # Add this section to dynamically set the hovertemplate and text for update_traces
                if selected_option == '1d':
                    hover_template = '%{text}<br>'
                elif selected_option in ['5d']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['1mo']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['6mo']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['ytd']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['1y']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['5y']:
                    hover_template = '%{text}<br>'
                elif selected_option in ['max']:
                    hover_template = '%{text}<br>'

                # Find the most recent closing price
                most_recent_close = stock_data['Close'].iloc[-1]

                # Add a scatter trace so annotation can find y-axis of the most recent price
                fig.add_trace(go.Scatter(
                    x=[formatted_dates[-1]],
                    y=[most_recent_close],
                    mode='markers',
                    marker=dict(color='red', size=10),
                    showlegend=False,
                    hoverinfo='none',
                    visible=False
                ))

                # Update the layout to ensure the annotation stays on the y-axis
                fig.update_layout(
                    annotations=[
                        dict(
                            x=1,  # Adjust this value to control the x-position of the annotation
                            y=most_recent_close,
                            xref='paper',
                            yref='y',
                            text=f'${most_recent_close:.2f}',  # Display the price value
                            showarrow=False,
                            font=dict(color='White', size=12),
                            align='left',
                            # bordercolor='red',
                            # borderwidth=1,
                            # borderpad=4,
                            bgcolor='rgba(0, 104, 201, 1)'
                        )
                    ]
                )

                # Trace for Line & Area
                fig.update_traces(
                    hovertemplate=hover_template,
                    hoverinfo='x',
                    text=[f'{symbol}<br>{hover_format[i]}<br>${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
                        for i, (open_price, high_price, low_price, close_price, volume) in enumerate(
                            zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume']))],
                    selector=dict(type='scatter')
                )

                # Get the current high and low for the corresponding time period option.
                current_high = stock_data['Close'].max()
                current_low = stock_data['Close'].min()

                # Calculate the percentage from the current low and high
                percent_from_low = ((most_recent_close - current_low) / current_low) * 100
                percent_from_high = ((most_recent_close - current_high) / current_high) * 100

                # Percent Change of symbol
                bgcolor = "green" if percentage_change >= 0 else "red"
                fig.add_annotation(
                    text=f'({selected_option}) {symbol} {stock_data['Close'].iloc[-1]:.2f} {percentage_change:.2f}%',
                    xref='paper', yref='paper',
                    x=0.00, y=1.20,
                    showarrow=False,
                    font=dict(size=13, color="black", family="Arial Black"),
                    bgcolor=bgcolor,  # Set bgcolor based on the sign of percentage_change
                )

                fig.add_annotation(
                    text=f'L {current_low:.2f}\n {percent_from_low:.2f}%\n',
                    xref='paper', yref='paper',
                    x=0.00, y=1.10,
                    showarrow=False,
                    font=dict(size=13, color="black", family="Arial Black"),
                    bgcolor='rgba(245,245,245,1.000)',
                )

                # Get the width of the low value annotation
                low_annotation_width = 0.94  # Adjust this value based on your layout

                fig.add_annotation(
                    text=f'H {current_high:.2f}\n {percent_from_high:.2f}%\n',
                    xref='paper', yref='paper',
                    x=low_annotation_width,  # Set the x-coordinate to be the right edge of the low annotation
                    y=1.10,
                    showarrow=False,
                    font=dict(size=13, color="black", family="Arial Black"),
                    bgcolor='rgba(245,245,245,1.000)',
                )

                # Border top-side
                fig.add_shape(
                            type="line",
                            xref="paper",
                            yref="paper",
                            x0=0,
                            y0=1.12,
                            x1=.94,
                            y1=1.12,
                            line=dict(
                                color="white",
                                width=2,
                            )
                        )

                # Border bot-side
                fig.add_shape(
                            type="line",
                            xref="paper",
                            yref="paper",
                            x0=0,
                            y0=0,
                            x1=.94,
                            y1=0,
                            line=dict(
                                color="rgba(245,245,245,1.000)",
                                width=2,
                            )
                        )

                # Border right-side
                fig.add_shape(
                            type="line",
                            xref="paper",
                            yref="paper",
                            x0=.94,
                            y0=1.12,
                            x1=.94,
                            y1=0,
                            line=dict(
                                color="rgba(245,245,245,1.000)",
                                width=3,
                            )
                        )

                # Set hoverinfo and text for Candlestick
                hoverinfo_candlestick = 'text'
                text_candlestick = [
                    f'${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
                    for open_price, high_price, low_price, close_price, volume in
                    zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume'])
                ]

                # Trace for Candlestick
                fig.update_traces(
                    hoverinfo='text',
                    text=[f'{symbol}<br>{hover_format[i]}<br>${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
                        for i, (open_price, high_price, low_price, close_price, volume) in enumerate(
                            zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume']))],
                    selector=dict(type='candlestick')
                )

                # Hides the tools on the Mode Bar
                config = {'displayModeBar': False}
                st.plotly_chart(fig, config=config, use_container_width=True)

                
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