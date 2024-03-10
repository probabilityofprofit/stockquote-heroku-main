# historical_data_utils.py
import yfinance as yf
import pandas as pd
import streamlit as st

def get_historical_data(symbol, start_date=None, end_date=None, period=None):
    stock = yf.Ticker(symbol)

    if start_date and end_date:
        historical_data = stock.history(start=start_date, end=end_date, actions=True)
    elif period:
        historical_data = stock.history(period=period, actions=True)
    else:
        historical_data = stock.history(period="1y", actions=True)  # Default to 1 year if no start_date, end_date, or period provided

    return historical_data

def display_historical_data(symbol, historical_data):
    # Add an option to select time period
    time_period_options = ["1D", "5D", "1M", "3M", "6M", "YTD", "1Y", "5Y", "Max", "Custom"]
    selected_time_period = st.selectbox("Select Time Period", time_period_options, index=time_period_options.index("1M"))

    if selected_time_period == "Custom":
        # Allow users to input custom start and end dates
        start_date = st.date_input("Select Start Date")
        end_date = st.date_input("Select End Date")

        if start_date >= end_date:
            st.error("End date must be after start date. Please select valid dates.")
            return

        historical_data = get_historical_data(symbol, start_date=start_date, end_date=end_date)
    else:
        # Convert time period to corresponding yfinance period string
        if selected_time_period == "1D":
            period = "1d"
        elif selected_time_period == "5D":
            period = "5d"
        elif selected_time_period == "1M":
            period = "1mo"
        elif selected_time_period == "3M":
            period = "3mo"
        elif selected_time_period == "6M":
            period = "6mo"
        elif selected_time_period == "YTD":
            period = "ytd"
        elif selected_time_period == "1Y":
            period = "1y"
        elif selected_time_period == "5Y":
            period = "5y"
        elif selected_time_period == "Max":
            period = "max"

        # Fetch historical data based on the selected time period
        historical_data = get_historical_data(symbol, period=period)

    # Add an option to select frequency
    frequency_options = ["Daily", "Weekly", "Monthly"]
    selected_frequency = st.selectbox("Select Frequency", frequency_options)

    # Convert frequency to corresponding pandas resample string
    if selected_frequency == "Daily":
        resample_string = 'D'
    elif selected_frequency == "Weekly":
        resample_string = 'W'
    elif selected_frequency == "Monthly":
        resample_string = 'M'

    # Resample historical data based on the selected frequency
    selected_columns = ['Volume', 'Open', 'High', 'Low', 'Close', 'Dividends', 'Stock Splits']

    if all(col in historical_data.columns for col in selected_columns):
        resampled_data = historical_data[selected_columns].resample(resample_string).agg({
            'Volume': 'sum',  # Use sum instead of last for volume
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Dividends': 'sum',
            'Stock Splits': 'sum'
        })

        # Fill missing values in Close with the previous available close
        resampled_data['Close'] = resampled_data['Close'].ffill()

        # Calculate % Change and Change based on Close
        resampled_data['% Change'] = (resampled_data['Close'].pct_change() * 100).map(lambda x: "{:.2f}%".format(x) if not pd.isna(x) else None)
        resampled_data['Change'] = resampled_data['Close'].diff()

        # Reorder columns to move 'Change' and '% Change' to desired positions
        resampled_data = resampled_data[['Volume', 'Open', 'High', 'Low', 'Close', 'Change', '% Change', 'Dividends', 'Stock Splits']]

        # Filter out rows where any of the specified columns have None values
        resampled_data = resampled_data.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'])

        # Reverse the order of the resampled data to have the most recent date first
        resampled_data = resampled_data[::-1]

        # Convert the index (date) to the desired format
        resampled_data.index = resampled_data.index.strftime('%b %d, %Y')

        # Set the height of the DataTable to 700
        st.dataframe(resampled_data, height=700, width=1000)
    else:
        st.warning("Historical Data is not present in selected time period. Please choose a different time period")
