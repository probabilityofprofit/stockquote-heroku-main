import yfinance as yf
import streamlit as st
import pandas as pd

def get_stock_data(ticker, start_date, end_date, interval):
    stock_data = yf.download(ticker, start=start_date, end=end_date, period=interval)
    return stock_data

def main():

    # Sidebar for user input
    st.sidebar.header("User Input")
    ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL")
    start_date = st.sidebar.text_input("Enter Start Date (YYYY-MM-DD):", "2021-01-01")
    end_date = st.sidebar.text_input("Enter End Date (YYYY-MM-DD):", "2022-01-01")
    interval = st.sidebar.selectbox("Choose Time Interval", ['1m', '2m', '30m', '1d', '1wk', '1mo'])

    # Fetch stock data
    stock_data = get_stock_data(ticker, start_date, end_date, interval)

    # Display stock data in the main app
    st.subheader(f" {ticker}")
    st.write(stock_data)

if __name__ == "__main__":
    main()
