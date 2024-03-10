import yfinance as yf
import streamlit as st
import pandas as pd

def display_key_executives(stock_info):
    st.write("##### Key Executives")

    # Columns to display
    columns_to_display = ["name", "title", "totalPay", "exercisedValue", "yearBorn"]

    # Display Key Executives information using DataTable
    key_executives_data = stock_info.get('companyOfficers', [])

    # Check if there is at least one name present in the data
    if any(executive.get("name") for executive in key_executives_data):
        key_executives_df = pd.DataFrame(key_executives_data)

        # Ensure 'totalPay' is present in the DataFrame
        if 'totalPay' not in key_executives_df.columns:
            key_executives_df['totalPay'] = 'N/A'

        # Ensure 'exercisedValue' is present in the DataFrame
        if 'exercisedValue' not in key_executives_df.columns:
            key_executives_df['exercisedValue'] = 'N/A'

        # Ensure 'yearBorn' is present in the DataFrame
        if 'yearBorn' not in key_executives_df.columns:
            key_executives_df['yearBorn'] = 'N/A'

        # Filter and rename columns for better display
        key_executives_df_display = key_executives_df[columns_to_display].rename(columns={
            "name": "Name",
            "title": "Title",
            "totalPay": "Total Pay",
            "exercisedValue": "Exercised Value",
            "yearBorn": "Year Born"
        })

        # Display the DataFrame with updated column names and only the specified columns
        st.dataframe(key_executives_df_display, hide_index=True)
    else:
        st.info("No Key Executive information available.")
