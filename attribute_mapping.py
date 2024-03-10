profile1_info_mapping = {
    'shortName': ('', None),
    'address1': ('', None),
    'city_state_zip': ('', None),
    'country': ('', None),
    'phone': ('', None),
    'website': ('', None),
}

profile2_info_mapping = {
    'sector': ('Sector(s)', None),
    'industry': ('Industry', None),
    'fullTimeEmployees': ('Full-Time Employees', '{:,.0f}'),
    'category': ('Category', '{:,.2f}'),
    'fundFamily': ('Fund Family', '{:,.2f}'),
    'totalAssets': ('Net Assets', '{:,.2f}'),
    'ytdReturn': ('YTD Daily Total Return', '{:,.2%}'),
    'yield': ('Yield', '{:,.2%}'),
    'legalType': ('Legal Type', '{:,.2f}'),
}

profile3_info_mapping = {
    'companyOfficers': ('Company Officers', None),
}

profile4_info_mapping = {
    'longBusinessSummary': ('', None),
}

summary1_info_mapping = {
    'regularMarketPreviousClose': ('Previous Close', '{:,.2f}'),
    'regularMarketOpen': ('Open', '{:,.2f}'),
    'bid_bidSize': ('Bid', '{:,.2f}'),
    'ask_askSize': ('Ask', '{:,.2f}'),
    'dayLow_dayHigh': ('Daily Range', '{:,.2f}'),
    'fiftyTwoWeekLow_fiftyTwoWeekHigh': ('52 Week Range', '{:,.2f}'),
    'fiftyDayAverage': ('50 Day Average', '{:,.2f}'),
    'twoHundredDayAverage': ('200 Day Average', '{:,.2f}'),
    'lastCapGain': ('Last Cap Gain', '{:,.2f}'),
    'morningStarOverallRating': ('Morningstar Rating', '{:,.2f}'),
    'morningStarRiskRating': ('Morningstar Risk Rating', '{:,.2f}'),

}

summary2_info_mapping = {
    'volume': ('Volume', '{:,.2f}'),
    'averageVolume': ('Average Volume', '{:,.2f}'),
    'totalAssets': ('Net Assets', '{:,.2f}'),
    'marketCap': ('Market Cap', '{:,.2f}'),
    'navPrice': ('NAV', '{:,.2f}'),
    'beta': ('Beta (5Y Monthly)', '{:,.2f}'),
    'trailingPE': ('PE Ratio (TTM)', '{:,.2f}'),
    'trailingEps': ('EPS (TTM)', '{:,.2f}'),
    'dividendRate_dividendYield': ('Forward Dividend & Yield', '{:,.2f}'),
    'exDividendDate': ('Ex Dividend Date)', '{:,.2f}'),
    'yield': ('Yield', '{:.2%}'),
    'ytdReturn': ('YTD Daily Total Return', '{:,.2%}'),
    'beta3Year': ('Beta (5Y Monthly)', '{:,.2f}'),
    'targetMeanPrice': ('1y Target Est', '{:,.2f}'),
    'annualHoldingsTurnover': ('Holdings Turnover', '{:,.2%}'),
    'lastDividendValue': ('Last Dividend', '{:,.2f}'),
    'fundInceptionDate': ('Inception Date', '{:,.2f}'),


}

financial_info_mapping = {
    'marketCap': ('Market Cap', '{:,.2f}'),
    'enterpriseValue': ('Enterprise Value', '{:,.2f}'),
    'trailingPE': ('Trailing Pe', '{:.2f}'),
    'forwardPE': ('Forward Pe', '{:.2f}'),
    'pegRatio': ('Peg_Ratio', '{:.2f}'),
    'priceToSalesTrailing12Months': ('Price To Sales Trailing 12 Months', '{:.2f}'),
    'priceToBook': ('Price To Book', '{:.2f}'),
}

financial_fiscal_mapping = {
    'lastFiscalYearEnd': ('Fiscal Year Ends', '{:,.2f}'),
    'mostRecentQuarter': ('Most Recent Quarter (mrq)', '{:,.2f}'),
}

financial_profitability_mapping = {
    'profitMargins': ('Profit Margin', '{:,.2%}'),
    'operatingMargins': ('Operating Margin (ttm)', '{:,.2%}'),
}

financial_management_mapping = {
    'returnOnAssets': ('Profit Margin', '{:,.2%}'),
    'returnOnEquity': ('Operating Margin (ttm)', '{:,.2%}'),
}

financial_income_mapping = {
    'totalRevenue': ('Revenue (ttm)', '{:,.2f}'),
    'revenuePerShare': ('Revenue Per Share (ttm)', '{:,.2f}'),
    'revenueGrowth': ('Quarterly Revenue Growth (yoy)', '{:,.2%}'),
    'grossProfits': ('Gross Profit (ttm)', '{:,.2f}'),
    'ebitda': ('EBITDA', '{:,.2f}'),
    'netIncomeToCommon': ('Net Income Avi to Common (ttm)', '{:,.2f}'),
    'trailingEps': ('Diluted EPS (ttm)', '{:,.2f}'),
    'earningsQuarterlyGrowth': ('Quarterly Earnings Growth (yoy)', '{:,.2%}'),
}

financial_balance_mapping = {
    'totalCash': ('Total Cash (mrq)', '{:,.2f}'),
    'totalCashPerShare': ('Total Cash Per Share (mrq)', '{:,.2f}'),
    'totalDebt': ('Total Debt (mrq)', '{:,.2f}'),
    'debtToEquity': ('Total Debt/Equity (mrq)', '{:.2%}'),
    'currentRatio': ('Current Ratio (mrq)', '{:,.2f}'),
    'bookValue': ('Book Value Per Share (mrq)', '{:,.2f}'),
}

financial_cash_mapping = {
    'operatingCashflow': ('Operating Cash Flow (ttm)	', '{:,.2f}'),
    'freeCashflow': ('Levered Free Cash Flow (ttm)	', '{:,.2f}'),
}

financial_price_mapping = {
    'operatingCashflow': ('Operating Cash Flow (ttm)	', '{:,.2f}'),
    'freeCashflow': ('Levered Free Cash Flow (ttm)	', '{:,.2f}'),
}

financial_stock_mapping = {
    'beta': ('Beta (5Y Monthly)', '{:,.2f}'),
    '52WeekChange': ('52-Week Change', '{:,.2%}'),
    'SandP52WeekChange': ('S&P500 52-Week Change', '{:,.2%}'),
    'fiftyTwoWeekHigh': ('52 Week High', '{:,.2f}'),
    'fiftyTwoWeekLow': ('52 Week Low', '{:,.2f}'),
    'fiftyDayAverage': ('50-Day Moving Average', '{:,.2f}'),
    'twoHundredDayAverage': ('200-Day Moving Average ', '{:,.2f}'),
}

financial_share_mapping = {
    'averageVolume': ('Avg Vol (3 month)', '{:,.2f}'),
    'averageVolume10days': ('Avg Vol (10 day)', '{:,.2f}'),
    'sharesOutstanding': ('Shares Outstanding', '{:,.2f}'),
    'impliedSharesOutstanding': ('Shares Outstanding', '{:,.2f}'),
    'impliedSharesOutstanding': ('Implied Shares Outstanding ', '{:,.2f}'),
    'floatShares': ('Float', '{:,.2f}'),
    'heldPercentInsiders': ('% Held by Insiders', '{:,.2%}'),
    'heldPercentInstitutions': ('% Held by Institutions', '{:,.2%}'),
    'sharesShort': ('Shares Short ({dateShortInterest})', '{:,.2f}'),
    'shortRatio': ('Short Ratio ({dateShortInterest})', '{:,.2f}'),
    'shortPercentOfFloat': ('Short % of Float ({dateShortInterest})', '{:,.2%}'),
    'sharesPercentSharesOut': ('Short % of Shares Outstanding ({dateShortInterest})', '{:,.2%}'),
    'sharesShortPriorMonth': ('Short Short (prior month {sharesShortPreviousMonthDate})', '{:,.2f}'),
}

financial_dividends_mapping = {
    'dividendRate': ('Forward Annual Dividend Rate', '{:,.2f}'),
    'dividendYield': ('Forward Annual Dividend Yield', '{:,.2%}'),
    'trailingAnnualDividendRate': ('Trailing Annual Dividend Rate', '{:,.2f}'),
    'trailingAnnualDividendYield': ('Trailing Annual Dividend Yield', '{:,.2%}'),
    'fiveYearAvgDividendYield': ('5 Year Average Dividend Yield', '{:,.2f}'),
    'payoutRatio': ('Payout Ratio', '{:,.2%}'),
    'exDividendDate': ('Ex-Dividend Date', '{:,.2f}'),
    'lastSplitFactor': ('Last Split Factor', None),
    'lastSplitDate': ('Last Split Date', None),
}

market_info_mapping = {
    'exchange': ('Exchange', None),
    'quoteType': ('Quote Type', None),
    'regularMarketOpen': ('Regular Market Open', '{:,.2f}'),
    'regularMarketPreviousClose': ('Regular Market Previous Close', '{:,.2f}'),
    'regularMarketDayHigh': ('Regular Market Day High', '{:,.2f}'),
    'regularMarketDayLow': ('Regular Market Day Low', '{:,.2f}'),
    'regularMarketVolume': ('Regular Market Volume', '{:,.0f}'),
    'marketCap': ('Market Cap', '{:,.2f}'),
}

risk_info_mapping = {
    'auditRisk': ('Audit Risk', '{:.2%}'),
    'boardRisk': ('Board Risk', '{:.2%}'),
    'compensationRisk': ('Compensation Risk', '{:.2%}'),
    'shareHolderRightsRisk': ('Shareholder Rights Risk', '{:.2%}'),
    'overallRisk': ('Overall Risk', '{:.2%}'),
    'governanceEpochDate': ('Governance Epoch Date', None),
    'compensationAsOfEpochDate': ('Compensation As Of Epoch Date', None),
    }

market_performance_mapping = {
    '52WeekChange': ('52 Week Change', '{:.2%}'),
    'SandP52WeekChange': ('SandP 52 Week Change', '{:.2%}'),
    'lastDividendValue': ('Last Dividend Value', '{:,.2f}'),
    'lastDividendDate': ('Last Dividend Date', None),
    }

target_price_mapping = {
    'targetHighPrice': ('Target High Price', '{:,.2f}'),
    'targetLowPrice': ('Target Low Price', '{:,.2f}'),
    'targetMeanPrice': ('Target Mean Price', '{:,.2f}'),
    'targetMedianPrice': ('Target Median Price', '{:,.2f}'),
    'recommendationMean': ('Recommendation Mean', '{:.2f}'),
    'recommendationKey': ('Recommendation Key', None),
    'numberOfAnalystOpinions': ('Number of Analyst Opinions', None),
    }

finance_statements_mapping = {
    'totalCash': ('Total Cash', '{:,.2f}'),
    'totalCashPerShare': ('Total Cash Per Share', '{:,.2f}'),
    'ebitda': ('EBITDA', '{:,.2f}'),
    'totalDebt': ('Total Debt', '{:,.2f}'),
    'quickRatio': ('Quick Ratio', '{:.2f}'),
    'currentRatio': ('Current Ratio', '{:.2f}'),
    'totalRevenue': ('Total Revenue', '{:,.2f}'),
    'debtToEquity': ('Debt to Equity', '{:.2f}'),
    'revenuePerShare': ('Revenue Per Share', '{:,.2f}'),
    'returnOnAssets': ('Return on Assets', '{:.2%}'),
    'returnOnEquity': ('Return on Equity', '{:.2%}'),
    'grossProfits': ('Gross Profits', '{:,.2f}'),
    'freeCashflow': ('Free Cashflow', '{:,.2f}'),
    'operatingCashflow': ('Operating Cashflow', '{:,.2f}'),
    'earningsGrowth': ('Earnings Growth', '{:.2%}'),
    'revenueGrowth': ('Revenue Growth', '{:.2%}'),
    }

additional_information_mapping = {
    'priceHint': ('Price Hint', '{:,.2f}'),
    'maxAge': ('Max Age', '{:,.0f}'),
    'exDividendDate': ('Ex-Dividend Date', None),
    'payoutRatio': ('Payout Ratio', '{:.2%}'),
    'fiveYearAvgDividendYield': ('Five-Year Average Dividend Yield', '{:.2%}'),
    'currency': ('Currency', None),
    'enterpriseToRevenue': ('Enterprise to Revenue', '{:.2f}'),
    'enterpriseToEbitda': ('Enterprise to EBITDA', '{:.2f}'),
    'financialCurrency': ('Financial Currency', None),
    'ask': ('Ask', '{:.2f}'),
    }
