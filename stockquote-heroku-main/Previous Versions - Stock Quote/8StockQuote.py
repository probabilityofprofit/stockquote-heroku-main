import streamlit as st
import yfinance as yf
from yahooquery import Ticker
import pandas as pd
from timestamp import convert_unix_timestamp_to_date
from option_chain_utils import display_option_chain
from historical_data_utils import get_historical_data, display_historical_data
from attribute_mapping import (
    profile1_info_mapping, profile2_info_mapping, profile4_info_mapping,
    financial_info_mapping, financial_fiscal_mapping, financial_profitability_mapping, financial_management_mapping, financial_income_mapping, financial_balance_mapping, financial_cash_mapping, financial_price_mapping, financial_stock_mapping, financial_share_mapping, financial_dividends_mapping,
    summary1_info_mapping, summary2_info_mapping,
    finance_statements_mapping,
)

# Function to convert Unix timestamp to date
def convert_unix_to_date(unix_timestamp):
    if unix_timestamp == 'N/A':
        return 'N/A'
    else:
        return convert_unix_timestamp_to_date(unix_timestamp)


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def get_position_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]
    
    # Extract position weightings for cash, stock, bond, other, preferred, and convertible
    cash_position = fund_info.get('cashPosition', None)
    stock_position = fund_info.get('stockPosition', None)
    bond_position = fund_info.get('bondPosition', None)
    other_position = fund_info.get('otherPosition', None)
    preferred_position = fund_info.get('preferredPosition', None)
    convertible_position = fund_info.get('convertiblePosition', None)
    
    position_weightings = {
        'cashPosition': cash_position,
        'stockPosition': stock_position,
        'bondPosition': bond_position,
        'otherPosition': other_position,
        'preferredPosition': preferred_position,
        'convertiblePosition': convertible_position,
    }
    
    return position_weightings

def get_sector_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]
    sector_weightings = fund_info.get('sectorWeightings', None)
    return sector_weightings

def get_equity_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]
    
    # Access the 'equityHoldings' dictionary
    equity_holdings = fund_info.get('equityHoldings', {})
    
    # Extract equity weightings for priceToEarnings, priceToBook, priceToSales, priceToCashflow, medianMarketCap, and threeYearEarningsGrowth
    price_To_earnings = equity_holdings.get('priceToEarnings', None)
    price_To_Book = equity_holdings.get('priceToBook', None)
    price_To_Sales = equity_holdings.get('priceToSales', None)
    price_To_Cashflow = equity_holdings.get('priceToCashflow', None)
    median_Market_Cap = equity_holdings.get('medianMarketCap', None)
    three_Year_Earnings_Growth = equity_holdings.get('threeYearEarningsGrowth', None)
    
    equity_weightings = {
        'priceToEarnings': price_To_earnings,
        'priceToBook': price_To_Book,
        'priceToSales': price_To_Sales,
        'priceToCashflow': price_To_Cashflow,
        'medianMarketCap': median_Market_Cap,
        'threeYearEarningsGrowth': three_Year_Earnings_Growth,
    }
    
    return equity_weightings

def get_bond_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]
    
    # Access the 'bondRatings' dictionary
    bond_holdings = fund_info.get('bondRatings', None)
    
    # Check if bond_holdings is a non-empty dictionary
    if isinstance(bond_holdings, dict):
        # Extract Bond Ratings for us_government, aaa, aa, a, bbb, bb, b, below_b, other
        us_government_ = bond_holdings.get('us_government', None)
        a_a_a = bond_holdings.get('aaa', None)
        a_a = bond_holdings.get('aa', None)
        a_ = bond_holdings.get('a', None)
        b_b_b = bond_holdings.get('bbb', None)
        b_b = bond_holdings.get('bb', None)
        b_ = bond_holdings.get('b', None)
        below_b_ = bond_holdings.get('below_b', None)
        other_ = bond_holdings.get('other', None)

        bond_weightings = {
            'us_government': us_government_,
            'aaa': a_a_a,
            'aa': a_a,
            'a': a_,
            'bbb': b_b_b,
            'bb': b_b,
            'b': b_,
            'below_b': below_b_,
            'other': other_,
        }
        
        return bond_weightings

def display_sector_info(sector_weightings):
    sector_dict = {}

    # Populate the dictionary with sector weightings
    for sector in sector_weightings:
        for key, value in sector.items():
            sector_dict[key] = value

    # Define custom names for each sector
    sector_names = {
        'realestate': 'Real Estate',
        'consumer_cyclical': 'Consumer Cyclical',
        'basic_materials': 'Basic Materials',
        'consumer_defensive': 'Consumer Defensive',
        'technology': 'Technology',
        'communication_services': 'Communication Services',
        'financial_services': 'Financial Services',
        'utilities': 'Utilities',
        'industrials': 'Industrials',
        'energy': 'Energy',
        'healthcare': 'Healthcare',
    }

    # Access sector weightings from realestate through healthcare
    for sector_name, sector_weight in sector_dict.items():
        label = f"{sector_names.get(sector_name, sector_name.capitalize())}: " if sector_name != '' else ''
       
        # Check if equity information is available
        if sector_weight is not None:
            sector_weight_formatted = '{:.2%}'.format(sector_weight)
        else:
            sector_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{sector_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_position_info(position_weightings):
    # Define custom names for each position
    position_names = {
        'cashPosition': 'Cash',
        'stockPosition': 'Stock',
        'bondPosition': 'Bond',
        'otherPosition': 'Other',
        'preferredPosition': 'Preferred',
        'convertiblePosition': 'Convertible',
    }

    # Access position weightings for each position
    for position_name, position_weight in position_weightings.items():
        label = f"{position_names.get(position_name, position_name.capitalize())}: " if position_name != '' else ''
        
        # Check if equity information is available
        if position_weight is not None:
            position_weight_formatted = '{:.2%}'.format(position_weight)
        else:
            position_weight_formatted = 'N/A'        
        
        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{position_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_equity_info(equity_weightings):
    # Define custom names for each position
    equity_names = {
        'priceToEarnings': 'Price/Earnings',
        'priceToBook': 'Price/Book',
        'priceToSales': 'Price/Sales',
        'priceToCashflow': 'Price/Cashflow',
        'medianMarketCap': 'Median Market Cap',
        'threeYearEarningsGrowth': '3 Year Earnings Growth',
    }

    # Access equity weightings for each position
    for equity_name, equity_weight in equity_weightings.items():
        label = f"{equity_names.get(equity_name, equity_name.capitalize())}: " if equity_name != '' else ''
        
        # Check if equity information is available
        if equity_weight is not None:
            equity_weight_formatted = '{:.2f}'.format(equity_weight)
        else:
            equity_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{equity_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_bond_info(bond_weightings):
    # Define custom names for each position
    bond_names = {
        'us_government': 'US Government',
        'aaa': 'AAA',
        'aa': 'AA',
        'a': 'A',
        'bbb': 'BBB',
        'bb': 'BB',
        'b': 'B',
        'below_b': 'Below B',
        'other': 'Others',        
    }

    # Access bond weightings for each position
    for bond_name, bond_weight in bond_weightings.items():
        label = f"{bond_names.get(bond_name, bond_name.capitalize())}: " if bond_name != '' else ''
        
        # Check if equity information is available
        if bond_weight is not None:
            bond_weight_formatted = '{:.2f}'.format(bond_weight)
        else:
            bond_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{bond_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_valuation_measures(symbol):
    t = Ticker(symbol)
    valuation_measures = t.valuation_measures
    
    # Check if valuation_measures is a DataFrame
    if not isinstance(valuation_measures, pd.DataFrame):
        st.warning("No valuation data available.")
    else:
        st.dataframe(valuation_measures)

def display_stock_info(info, mapping):
    data = {}
    for attribute, (alternative_name, format_specifier) in mapping.items():
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
        
        elif attribute == 'bid_bidSize':
            bid = info.get('bid', 'N/A')
            bidSize = info.get('bidSize', 'N/A')
            value = f"{bid} x {bidSize}"
        
        elif attribute == 'ask_askSize':
            ask = info.get('ask', 'N/A')
            askSize = info.get('askSize', 'N/A')
            value = f"{ask} x {askSize}"
        
        elif attribute == 'dayLow_dayHigh':
            dayLow = info.get('dayLow', 'N/A')
            dayHigh = info.get('dayHigh', 'N/A')
            value = f"{dayLow} - {dayHigh}"
        
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
            else:
                formatted_value = '{:,.2f}'.format(value)

            if magnitude in [2, 3]:  # Apply the custom format only for millions and billions
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
            current_price = stock_info.get('ask', 'N/A')
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
                with col2:
                    display_stock_info(stock_info, summary2_info_mapping)
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

            with tabs[1]:
                st.write("#### Chart")
                display_stock_info(stock_info, financial_info_mapping)

            with tabs[2]:
                st.write("#### Valuation Measures")
                st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                # Display the valuation measures
                display_valuation_measures(symbol)

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
                    
                    # Separate content into two columns
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("#### Overall Portfolio Composition (%)")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get position weightings
                        position_weightings = get_position_weightings(symbol)

                        # Display position weightings
                        if position_weightings:
                            display_position_info(position_weightings)
                        else:
                            st.warning("No position weightings data available.")
                                               
                    with col1:
                        st.write("#### Sector Weightings (%)")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get sector weightings
                        sector_weightings = get_sector_weightings(symbol)

                        # Display sector weightings
                        if sector_weightings:
                            display_sector_info(sector_weightings)
                        else:
                            st.warning("No sector weightings data available.")

                    with col2:
                        st.write("#### Equity Holdings")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get sector weightings
                        equity_weightings = get_equity_weightings(symbol)

                        # Display equity weightings
                        if equity_weightings:
                            display_equity_info(equity_weightings)
                        else:
                            st.warning("No Equity Holdings data available.")
                        st.write("#### Bond Ratings")
                        st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

                        # Call the function to get sector weightings
                        bond_weightings = get_bond_weightings(symbol)

                        # Display equity weightings
                        if bond_weightings:
                            display_bond_info(bond_weightings)
                        else:
                            st.warning("No Bond Ratings data available.")

            with tabs[7]:
                st.write("#### Analysis")
                display_stock_info(stock_info, finance_statements_mapping)

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
    else:
        st.warning("Please enter a stock symbol.")

if __name__ == "__main__":
    main()