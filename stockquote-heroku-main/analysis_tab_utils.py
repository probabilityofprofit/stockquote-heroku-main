from yahooquery import Ticker
import streamlit as st
import pandas as pd

def get_earnings_trend_data(symbol):
    stock_ticker = Ticker(symbol)
    earnings_trend_data = stock_ticker.earnings_trend
    
    periods_data = {}
    
    # Check if earnings_trend_data is not empty and has the necessary structure
    if earnings_trend_data and symbol in earnings_trend_data and 'trend' in earnings_trend_data[symbol]:
        for trend_data in earnings_trend_data[symbol]['trend']:
            period = trend_data.get('period', '')
            if period not in ['+5y', '-5y']:
                periods_data[period] = {
                    'endDate': trend_data.get('endDate', ''),
                    'growth': trend_data.get('growth', ''),
                    'earningsEstimate': trend_data.get('earningsEstimate', ''),
                    'revenueEstimate': trend_data.get('revenueEstimate', ''),
                    'epsTrend': trend_data.get('epsTrend', ''),
                    'epsRevisions': trend_data.get('epsRevisions', '')
                }

    return periods_data

def display_earnings_trend_data(earnings_trend_data):
    # Set custom names for indices
    index_names = {
        '0q': 'Current Quarter',
        '+1q': 'Next Quarter',
        '0y': 'Current Year',
        '+1y': 'Next Year'
    }

    # Check if earnings_trend_data is not empty
    if earnings_trend_data:
        # Create DataFrames for each attribute
        earnings_estimate_df = pd.DataFrame({index_names.get(period, period): data['earningsEstimate'] for period, data in earnings_trend_data.items()}).T
        revenue_estimate_df = pd.DataFrame({index_names.get(period, period): data['revenueEstimate'] for period, data in earnings_trend_data.items()}).T
        eps_trend_df = pd.DataFrame({index_names.get(period, period): data['epsTrend'] for period, data in earnings_trend_data.items()}).T
        eps_revisions_df = pd.DataFrame({index_names.get(period, period): data['epsRevisions'] for period, data in earnings_trend_data.items()}).T

        # Explicitly set data types for each column
        earnings_estimate_df = earnings_estimate_df.apply(pd.to_numeric, errors='coerce')
        revenue_estimate_df = revenue_estimate_df.apply(pd.to_numeric, errors='coerce')
        eps_trend_df = eps_trend_df.apply(pd.to_numeric, errors='coerce')
        eps_revisions_df = eps_revisions_df.apply(pd.to_numeric, errors='coerce')

        # Display transposed DataFrames within tabs[7] with width set to a large value
        st.write("#### Earnings Estimate")
        st.dataframe(earnings_estimate_df.T, width=1000)
        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.write("#### Revenue Estimate")
        st.dataframe(revenue_estimate_df.T, width=1000)
        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.write("#### EPS Trend")
        st.dataframe(eps_trend_df.T, width=1000)
        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.write("#### EPS Revisions")
        st.dataframe(eps_revisions_df.T, width=1000)
    else:
        st.warning("No earnings trend data is available.")
