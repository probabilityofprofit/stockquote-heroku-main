import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Add this line
from datetime import datetime, timedelta

def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    else:
        return f"{volume}"

# Used as a conditional check for assets that do not have minute intraday data.
def has_minute_data_in_last_day(ticker):
    # Fetch historical stock data with '1m' interval for the last day
    stock_data = yf.download(ticker, interval='1m', period='1d')
    return not stock_data.empty and len(stock_data) >= 5
