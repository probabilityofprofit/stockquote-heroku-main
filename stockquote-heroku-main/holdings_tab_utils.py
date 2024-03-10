from yahooquery import Ticker
import streamlit as st
import pandas as pd

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

def get_sector_weightings(symbol):
    fund = Ticker(symbol)
    fund_info = fund.fund_holding_info[symbol]

    # Check if fund_info is a dictionary
    if not isinstance(fund_info, dict):
        return None

    # Extract sector weightings
    sector_weightings = fund_info.get('sectorWeightings', None)

    return sector_weightings

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

def get_bond_ratings(symbol):
    fund = Ticker(symbol)
    fund_holding_info = fund.fund_holding_info

    # Check if symbol is in fund_holding_info and if 'bondRatings' key is present
    if symbol in fund_holding_info and 'bondRatings' in fund_holding_info[symbol]:
        bond_ratings = fund_holding_info[symbol]['bondRatings']
        return bond_ratings
    else:
        return []

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