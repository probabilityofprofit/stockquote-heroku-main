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

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

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

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Extract sector weightings
    sector_weightings = fund_info.get('sectorWeightings', None)

    return sector_weightings


def get_equity_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'equityHoldings' dictionary
    equity_holdings = fund_info.get('equityHoldings', {})

    # Extract equity weightings
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

def get_bond_ratings(symbol):
    fund = Ticker(symbol)
    fund_holding_info = fund.fund_holding_info

    # Check if symbol is in fund_holding_info and if 'bondRatings' key is present
    if symbol in fund_holding_info and 'bondRatings' in fund_holding_info[symbol]:
        bond_ratings = fund_holding_info[symbol]['bondRatings']
        return bond_ratings
    else:
        return []

def get_fund_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_performance[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'performanceOverview' dictionary
    fund_holdings = fund_info.get('performanceOverview', None)

    # Check if bond_holdings is a non-empty dictionary
    if isinstance(fund_holdings, dict):
        # Extract Bond Ratings for ytdReturnPct
        ytdReturnPct_ = fund_holdings.get('ytdReturnPct', None)

        fund_weightings = {
            'ytdReturnPct': ytdReturnPct_,

        }

        return fund_weightings
    else:
        return None

def get_performance_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_performance[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'performanceOverview' dictionary
    performance_holdings = fund_info.get('performanceOverview', None)

    # Check if performance_holdings is a non-empty dictionary
    if isinstance(performance_holdings, dict):
        # Extract Bond Ratings for fiveYrAvgReturnPct
        fiveYrAvgReturnPct_ = performance_holdings.get('fiveYrAvgReturnPct', None)

        performance_weightings = {
            'fiveYrAvgReturnPct': fiveYrAvgReturnPct_,

        }

        return performance_weightings
    else:
        return None

def get_profile_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_profile[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'feesExpensesInvestment' dictionary
    profile_holdings = fund_info.get('feesExpensesInvestment', None)

    # Check if profile_holdings is a non-empty dictionary
    if isinstance(profile_holdings, dict):
        # Extract Bond Ratings for netExpRatio
        netExpRatio_ = profile_holdings.get('netExpRatio', None)

        profile_weightings = {
            'netExpRatio': netExpRatio_,
            
        }

        return profile_weightings
    else:
        return None

def get_category_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_profile[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'categoryName' value
    category_name = fund_info.get('categoryName', None)

    return category_name
 

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


def display_bond_ratings(bond_ratings):
    if bond_ratings:
        custom_bond_names = {
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

        # Define the order of custom bond names
        bond_order = ['us_government', 'aaa', 'aa', 'a', 'bbb', 'bb', 'b', 'below_b', 'other']

        for rating_name in bond_order:
            custom_label = f"{custom_bond_names.get(rating_name, rating_name.capitalize())}: "
            
            # Find the corresponding bond rating value
            rating_value = next((item[rating_name] for item in bond_ratings if rating_name in item), None)

            # Check if bond rating value is available
            if rating_value is not None:
                rating_value_formatted = '{:.2%}'.format(rating_value)
            else:
                rating_value_formatted = 'N/A'

            st.write(
                f"<div style='display: flex; justify-content: space-between;'>"
                f"<div>{custom_label}</div>"
                f"<div style='text-align: right;'>{rating_value_formatted}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("No Bond Ratings data available.")


def display_fund_info(fund_weightings):
    # Define custom names for each position
    fund_names = {
        'ytdReturnPct': 'YTD Return',
     
    }

    # Access bond weightings for each position
    for fund_name, fund_weight in fund_weightings.items():
        label = f"{fund_names.get(fund_name, fund_name.capitalize())}: " if fund_name != '' else ''
        
        # Check if equity information is available
        if fund_weight is not None:
            fund_weight_formatted = '{:.2%}'.format(fund_weight)
        else:
            fund_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{fund_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_performance_info(performance_weightings):
    # Define custom names for each position
    performance_names = {
        'fiveYrAvgReturnPct': '5y Average Return',
     
    }

    # Access performance weightings for each position
    for performance_name, performance_weight in performance_weightings.items():
        label = f"{performance_names.get(performance_name, performance_name.capitalize())}: " if performance_name != '' else ''
        
        # Check if equity information is available
        if performance_weight is not None:
            performance_weight_formatted = '{:.2%}'.format(performance_weight)
        else:
            performance_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{performance_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

def display_profile_info(profile_weightings):
    # Define custom names for each position
    profile_names = {
        'netExpRatio': 'Expense Ratio (net)',
     
    }

    # Access profile weightings for each position
    for profile_name, profile_weight in profile_weightings.items():
        label = f"{profile_names.get(profile_name, profile_name.capitalize())}: " if profile_name != '' else ''
        
        # Check if equity information is available
        if profile_weight is not None:
            profile_weight_formatted = '{:.2%}'.format(profile_weight)
        else:
            profile_weight_formatted = 'N/A'

        st.write(
            f"<div style='display: flex; justify-content: space-between;'>"
            f"<div>{label}</div>"
            f"<div style='text-align: right;'>{profile_weight_formatted}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
def display_category_info(category_weightings):
    # Define custom names for the category
    category_names = {
        'categoryName': 'Category',
    }

    label = f"{category_names.get('categoryName', 'Category')}: " if category_weightings is not None else ''

    if isinstance(category_weightings, (int, float)):
        category_weight_formatted = '{:.2f}'.format(category_weightings)
    elif isinstance(category_weightings, str):
        category_weight_formatted = category_weightings
    else:
        category_weight_formatted = 'N/A'

    st.write(
        f"<div style='display: flex; justify-content: space-between;'>"
        f"<div>{label}</div>"
        f"<div style='text-align: right;'>{category_weight_formatted}</div>"
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

def get_current_price(symbol):
    stock_info = Ticker(symbol).summary_detail
    ask_price = stock_info.get(symbol, {}).get('ask', 'N/A')
    previous_close = stock_info.get(symbol, {}).get('previousClose', 'N/A')

    if ask_price == 'N/A':
        return previous_close
    else:
        return ask_price

def get_fund_holding_info(symbol):
    # Use Yahooquery or any other suitable method to retrieve fund holding information
    fund = Ticker(symbol)
    holding_info = fund.fund_holding_info

    # Check if the symbol is present in the holding_info dictionary
    if symbol in holding_info:
        # Check if 'holdings' key is present in the dictionary for the given symbol
        if 'holdings' in holding_info[symbol]:
            return holding_info[symbol]['holdings']
        else:
            return None
    else:
        st.warning(f"No information available for {symbol}.")
        return None

def get_bond_holdings_data(ticker):
    try:
        fund = Ticker(ticker)
        bond_holdings = fund.fund_bond_holdings

        maturity = bond_holdings[ticker]['maturity']
        duration = bond_holdings[ticker]['duration']
        maturity_cat = bond_holdings[ticker]['maturityCat']
        duration_cat = bond_holdings[ticker]['durationCat']

        return {
            "maturity": maturity,
            "duration": duration,
            "maturityCat": maturity_cat,
            "durationCat": duration_cat
        }
    except Exception as e:
        return f"Error: {str(e)}"


def display_bond_holdings_data(bond_holdings_data):
    # Define custom names for bond holdings categories
    category_names = {
        'maturity': 'Maturity',
        'duration': 'Duration',
        'maturityCat': 'Maturity Category',
        'durationCat': 'Duration Category',
    }

    # Display bond holdings data in col2 of tabs[6]

    if bond_holdings_data is not None and isinstance(bond_holdings_data, dict):
        for category_key, category_label in category_names.items():
                label = f"{category_label}: " if category_key in bond_holdings_data else 'N/A'

                if isinstance(bond_holdings_data.get(category_key), (int, float)):
                    category_weight_formatted = '{:.2f}'.format(bond_holdings_data[category_key])
                elif isinstance(bond_holdings_data.get(category_key), str):
                    category_weight_formatted = bond_holdings_data[category_key]
                else:
                    category_weight_formatted = 'N/A'

                st.write(
                    f"<div style='display: flex; justify-content: space-between;'>"
                    f"<div>{label}</div>"
                    f"<div style='text-align: right;'>{category_weight_formatted}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    else:
        st.warning("No bond holdings data available.")

    st.markdown("""<hr style="height:2px; margin-top: 10px; margin-bottom: 10px; border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


def display_fund_holding_info(fund_holding_info):
    # Create a DataFrame from the fund holding information
    df = pd.DataFrame(fund_holding_info)

    # Check if the DataFrame has any non-null values
    if not df.isnull().all().all():
        # Set the first column as the index
        df.set_index(df.columns[0], inplace=True)

        # Convert the 'holdingpercent' column to percentages
        df['% Assets'] = df['holdingPercent'].apply(lambda x: f"{x:.2%}")

        # Drop the original 'holdingpercent' column
        df.drop(columns=['holdingPercent'], inplace=True)

        # Rename the 'holdingName' column to 'Name'
        df.rename(columns={'holdingName': 'Name', 'symbol': 'Ticker'}, inplace=True)

        # Display the DataFrame in Streamlit with max width
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No fund holding information available.")

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
                st.write("#### Summary")
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