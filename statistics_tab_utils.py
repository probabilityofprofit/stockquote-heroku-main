from yahooquery import Ticker
import streamlit as st
import pandas as pd

def format_market_cap(value):
    if pd.notna(value):
        if value >= 1e12:
            return f'{value/1e12:.2f}T'
        elif value >= 1e9:
            return f'{value/1e9:.2f}B'
        elif value >= 1e6:
            return f'{value/1e6:.2f}M'
        else:
            return f'{value:.2f}'
    else:
        return None

def format_values(valuation_measures):
    for column in valuation_measures.columns:
        valuation_measures[column] = valuation_measures[column].apply(format_market_cap)
    return valuation_measures

def display_valuation_measures(symbol):
    t = Ticker(symbol)
    valuation_measures = t.valuation_measures
    
    # Check if valuation_measures is a DataFrame
    if not isinstance(valuation_measures, pd.DataFrame):
        st.warning("No valuation data available.")
    else:
        if 'EnterprisesValueRevenueRatio' in valuation_measures.columns:
            valuation_measures = valuation_measures.dropna(subset=['EnterprisesValueRevenueRatio', 'MarketCap'])
        else:
            # Drop rows only based on 'MarketCap' if 'EnterprisesValueRevenueRatio' is not present
            valuation_measures = valuation_measures.dropna(subset=['MarketCap'])
        
        # Set 'asOfDate' as the index
        valuation_measures = valuation_measures.set_index('asOfDate')
        
        # Sort DataFrame based on 'asOfDate' in descending order (latest to oldest)
        valuation_measures = valuation_measures.sort_index(ascending=False)
        
        # Format 'asOfDate' index to 'M/D/YYYY' format
        valuation_measures.index = pd.to_datetime(valuation_measures.index).strftime('%m/%d/%Y')
        
        # Specify the desired order of columns
        desired_order = [
            'MarketCap',
            'EnterpriseValue',
            'PeRatio',
            'ForwardPeRatio',
            'PegRatio',
            'PsRatio',
            'PbRatio',
            'EnterprisesValueRevenueRatio',
            'EnterprisesValueEBITDARatio'
        ]
        
        # Fill missing columns with 0
        missing_columns = [col for col in desired_order if col not in valuation_measures.columns]
        for col in missing_columns:
            valuation_measures[col] = 0
        
        # Reorder columns based on the desired order
        valuation_measures = valuation_measures[desired_order]
        
        # Rename the column labels
        column_mapping = {
            'MarketCap': 'Market Cap',
            'EnterpriseValue': 'Enterprise Value',
            'PeRatio': 'Trailing P/E',
            'ForwardPeRatio': 'Forward P/E',
            'PegRatio': 'PEG Ratio (5yr expected)',
            'PsRatio': 'Price/Sales',
            'PbRatio': 'Price/Book',
            'EnterprisesValueRevenueRatio': 'Enterprise Value/Revenue',
            'EnterprisesValueEBITDARatio': 'Enterprise Value/EBITDA'
        }
        valuation_measures = valuation_measures.rename(columns=column_mapping)
        
        # Format values with abbreviations
        valuation_measures = format_values(valuation_measures)
        
        # Transpose the DataFrame
        transposed_data = valuation_measures.T
        
        if transposed_data.empty:
            st.warning("No valuation data available.")
        else:
            st.dataframe(transposed_data, width=1000)
