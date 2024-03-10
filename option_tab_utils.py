# option_chain_utils.py
import streamlit as st
import yfinance as yf
import pandas as pd

def display_option_chain(symbol, expiration_dates, selected_expiration_date):
    try:
        stock = yf.Ticker(symbol)
        if not expiration_dates:
            st.warning("No option chain data available for this stock.")
            return

        # Allow the user to select an expiration date
        selected_expiration_date = st.selectbox("Select Expiration Date:", expiration_dates, index=expiration_dates.index(selected_expiration_date))

        # Fetch option chain data for the selected expiration date
        option_chain = stock.option_chain(selected_expiration_date)
        calls = option_chain.calls
        puts = option_chain.puts

        # Columns to display for both calls and puts
        columns_to_display = ["lastPrice", "change", "percentChange", "volume", "openInterest", "strike"]

        # Merge calls and puts on the 'strike' column
        option_chain_combined = pd.merge(calls[columns_to_display], puts[columns_to_display], on="strike", how='outer', suffixes=('_Call', '_Put'))

        # Add a new column to store in-the-money information
        option_chain_combined["In the Money Call"] = option_chain_combined["strike"] <= stock.info["ask"]
        option_chain_combined["In the Money Put"] = option_chain_combined["strike"] >= stock.info["ask"]

        # Sort the DataFrame by the 'strike' column
        option_chain_combined = option_chain_combined.sort_values(by='strike')

        # Define the desired column order
        desired_column_order = [
            "In the Money Call",
            "lastPrice_Call", "change_Call", "percentChange_Call", "volume_Call", "openInterest_Call", "strike",
            "lastPrice_Put", "change_Put", "percentChange_Put", "volume_Put", "openInterest_Put", "In the Money Put"
        ]

        # Reorder columns dynamically based on the desired order
        option_chain_combined = option_chain_combined[desired_column_order]

        # Define a dictionary for mapping original column names to display names
        column_name_mapping = {
            "In the Money Call": "ITM",
            "lastPrice_Call": "Price",
            "change_Call": "Chg",
            "percentChange_Call": "% Chg",
            "volume_Call": "Vol",
            "openInterest_Call": "Intrest",
            "strike": "Strike",
            "lastPrice_Put": "Price ",
            "change_Put": "Chg ",
            "percentChange_Put": "% Chg ",
            "volume_Put": "Vol ",
            "openInterest_Put": "Interest",
            "In the Money Put": "ITM "
        }

        # Rename columns using the mapping dictionary
        option_chain_combined.rename(columns=column_name_mapping, inplace=True)

        # Update formatting for percentChange_Call and percentChange_Put columns
        option_chain_combined["% Chg"] = option_chain_combined["% Chg"].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else None)
        option_chain_combined["% Chg "] = option_chain_combined["% Chg "].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else None)

        # Display the DataFrame with the selected column order and updated column names
        if not option_chain_combined.empty:
            # Set a fixed height for the DataFrame display
            fixed_height = 700  # Set your desired fixed height
            st.dataframe(option_chain_combined, height=fixed_height, width=1000, hide_index=True)
        else:
            st.info("No option chain data available.")

    except Exception as e:
        st.error(f"Error fetching option chain data: {str(e)}")