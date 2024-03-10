import yfinance as yf
import streamlit as st

def get_financials_data(symbol, statement_type='income', period='annual'):
    stock = yf.Ticker(symbol)
    
    if statement_type == 'income':
        if period == 'annual':
            data = stock.income_stmt
        elif period == 'quarterly':
            data = stock.quarterly_income_stmt
    elif statement_type == 'balance':
        if period == 'annual':
            data = stock.balance_sheet
        elif period == 'quarterly':
            data = stock.quarterly_balance_sheet
    elif statement_type == 'cashflow':
        if period == 'annual':
            data = stock.cashflow
        elif period == 'quarterly':
            data = stock.quarterly_cashflow
    else:
        raise ValueError("Invalid statement_type. Use 'income', 'balance', or 'cashflow'")
    
    return data

def display_financials_data(data):
    # Display financials data in a DataFrame
    if data is not None and not data.empty:
        # Reverse the order of the DataFrame rows
        reversed_data = data.iloc[::-1]
        st.dataframe(reversed_data)
    else:
        st.warning("No financials data available.")