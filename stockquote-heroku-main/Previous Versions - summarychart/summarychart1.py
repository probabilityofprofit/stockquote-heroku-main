import yfinance as yf
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Streamlit app
st.title('Stock Data Visualization')

# User input for stock ticker
ticker = st.text_input('Enter Stock Ticker:', 'AAPL')

# Radio buttons for time period
time_period_options = {
    '1d': {'interval': '1m', 'period': '1d'},
    '5d': {'interval': '15m', 'period': '5d'},
    '1mo': {'interval': '30m', 'period': '1mo'},
    '6mo': {'interval': '1d', 'period': '6mo'},
    'ytd': {'interval': '30m', 'period': 'ytd'},
    '1y': {'interval': '1d', 'period': '1y'},
    '5y': {'interval': '1wk', 'period': '5y'},
    'max': {'interval': '3mo', 'period': 'max'}
}

selected_option = st.radio('Select Time Period:', list(time_period_options.keys()))

# Fetch historical stock data based on selected time period
interval = time_period_options[selected_option]['interval']
period = time_period_options[selected_option]['period']

stock_data = yf.download(ticker, interval=interval, period=period)

# Display stock data
st.write(f'### Historical Stock Data ({selected_option} period)')
st.write(stock_data)

# Format date based on selected time period
if selected_option == '1d':
    formatted_dates = stock_data.index.strftime('%I:%M %p')
    hover_format = '%I:%M %p'
elif selected_option in ['5d']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%a, %b %d, %I:%M %p'
elif selected_option in ['1mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%b %#d, %y'
elif selected_option in ['6mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%b %#d, %y'    
elif selected_option in ['ytd']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%b %#d, %y' 
elif selected_option in ['1y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%b %#d, %y'
elif selected_option in ['5y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    hover_format = '%b %#d, %y'    
else: # Max
    formatted_dates = stock_data.index.strftime('%Y-%m-%d')
    hover_format = '%b %#d, %y'


# Plot historical stock data using plotly with formatted dates
fig = px.line(stock_data, x=formatted_dates, y='Close', title=f'{ticker} Stock Price Over Time ({selected_option} period)')
fig.update_xaxes(title_text='', type='category', nticks=5, spikethickness=1)  # Set x-axis type to 'category'
fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=1)
fig.update_layout(hovermode='closest', hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial", bordercolor="black"))
fig.update_traces(hovertemplate='%{text}<br> $%{y:.2f}', hoverinfo='x', text=stock_data.index.strftime(hover_format), selector=dict(type='scatter'))
fig.update_xaxes(hoverformat=hover_format, showspikes=True, spikemode="across")  # Set hover format
st.plotly_chart(fig)
# import yfinance as yf
# import streamlit as st
# import plotly.express as px
# from datetime import datetime, timedelta

# # Streamlit app
# st.title('Stock Data Visualization')

# # User input for stock ticker
# ticker = st.text_input('Enter Stock Ticker:', 'AAPL')

# # Radio buttons for time period
# time_period_options = {
#     '1d': {'interval': '1m', 'period': '1d'},
#     '5d': {'interval': '15m', 'period': '5d'},
#     '1mo': {'interval': '30m', 'period': '1mo'},
#     '6mo': {'interval': '1d', 'period': '6mo'},
#     'ytd': {'interval': '30m', 'period': 'ytd'},
#     '1y': {'interval': '1d', 'period': '1y'},
#     '5y': {'interval': '1wk', 'period': '5y'},
#     'max': {'interval': '3mo', 'period': 'max'}
# }

# selected_option = st.radio('Select Time Period:', list(time_period_options.keys()))

# # Fetch historical stock data based on selected time period
# interval = time_period_options[selected_option]['interval']
# period = time_period_options[selected_option]['period']

# stock_data = yf.download(ticker, interval=interval, period=period)

# # Display stock data
# st.write(f'### Historical Stock Data ({selected_option} period)')
# st.write(stock_data)

# if selected_option == '1d':
#     formatted_dates = stock_data.index.strftime('%I:%M %p')
#     formatted_labels = stock_data.index.strftime('%I %p')
#     hover_format = '%I:%M %p'
#     tickvals = formatted_dates[::60]  # Display every 10th date
#     ticktext = formatted_labels[::60]
# elif selected_option in ['5d']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%a, %b %d, %I:%M %p'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['1mo']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['6mo']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['ytd']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['1yr']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['5y']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# elif selected_option in ['max']:
#     formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
#     formatted_labels = stock_data.index.strftime('%Y-%m-%d %I %p')
#     hover_format = '%b %#d, %y'
#     tickvals = formatted_dates[::10]  # Display every 10th date
#     ticktext = formatted_labels[::10]
# # Add similar blocks for other time periods...

# # Plot historical stock data using plotly with formatted labels
# fig = px.line(stock_data, x=formatted_dates, y='Close', title=f'{ticker} Stock Price Over Time ({selected_option} period)')
# fig.update_xaxes(title_text='', type='category', nticks=5, spikethickness=1)  # Set x-axis type to 'category'
# fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=1)
# fig.update_layout(hovermode='closest', hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial", bordercolor="black"))
# fig.update_traces(hovertemplate='%{text}<br> $%{y:.2f}', hoverinfo='x', text=stock_data.index.strftime(hover_format), selector=dict(type='scatter'))
# fig.update_xaxes(hoverformat=hover_format, showspikes=True, spikemode="across", ticktext=ticktext, tickvals=tickvals)  # Set hover format and use formatted_labels for ticktext
# st.plotly_chart(fig)