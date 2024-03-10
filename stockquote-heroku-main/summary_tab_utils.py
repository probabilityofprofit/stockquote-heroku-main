from yahooquery import Ticker
import streamlit as st

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

def get_category_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_profile[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Access the 'categoryName' value
    category_name = fund_info.get('categoryName', None)

    return category_name

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
