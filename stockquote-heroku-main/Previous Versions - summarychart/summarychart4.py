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

if selected_option == '1d':
    formatted_dates = stock_data.index.strftime('%I:%M %p')
    formatted_labels = stock_data.index.strftime('%I %p')
    hover_format = '%I:%M %p'
    tickvals = formatted_dates[::125]  # Display every 125th date
    ticktext = formatted_labels[::125]
elif selected_option in ['5d']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%a')
    hover_format = '%a, %b %d, %I:%M %p'
    tickvals = formatted_dates[::30]  
    ticktext = formatted_labels[::30]
elif selected_option in ['1mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::92]
    ticktext = formatted_labels[::92]
elif selected_option in ['6mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::65]
    ticktext = formatted_labels[::65]
elif selected_option in ['ytd']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::125]
    ticktext = formatted_labels[::125]
elif selected_option in ['1y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::126]
    ticktext = formatted_labels[::126]
elif selected_option in ['5y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::131]
    ticktext = formatted_labels[::131]
elif selected_option in ['max']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = '%b %#d, %y'
    tickvals = formatted_dates[::79]
    ticktext = formatted_labels[::79]

# Plot historical stock data using plotly with formatted labels
fig = px.line(stock_data, x=formatted_dates, y='Close', title=f'{ticker} Stock Price Over Time ({selected_option} period)')

# Add volume as a bar chart
fig.add_bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color='rgba(0, 0, 255, 0.5)', hoverinfo='skip')

# Update axis labels and layout
fig.update_xaxes(title_text='', type='category', nticks=5, spikethickness=1)
fig.update_yaxes(title_text='', showspikes=True, nticks=5, spikemode="across", spikethickness=1, side='right')
fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=1, side='right', secondary_y=True, showticklabels=False)

# Add this section to dynamically set the y-axis ranges based on selected_option
if selected_option == '1d':
    yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    yaxis2_range = [0, 5 * 10**6]
elif selected_option in ['5d']:
    yaxis_range = [stock_data['Close'].min() * 0.98, stock_data['Close'].max() * 1.02]
    yaxis2_range = [0, 50 * 10**6]
elif selected_option in ['1mo']:
    yaxis_range = [stock_data['Close'].min() * 0.95, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 50 * 10**6]
elif selected_option in ['6mo']:
    yaxis_range = [stock_data['Close'].min() * 0.95, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 750 * 10**6]
elif selected_option in ['ytd']:
    yaxis_range = [stock_data['Close'].min() * 0.95, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 100 * 10**6]
elif selected_option in ['1y']:
    yaxis_range = [stock_data['Close'].min() * 0.95, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 750 * 10**6]
elif selected_option in ['5y']:
    yaxis_range = [stock_data['Close'].min() * 0.55, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 10050 * 10**6]
elif selected_option in ['max']:
    yaxis_range = [stock_data['Close'].min() * 0.95, stock_data['Close'].max() * 1.05]
    yaxis2_range = [0, 750000 * 10**6]

fig.update_layout(
    hovermode='closest',
    hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial", bordercolor="black"),
    xaxis=dict(hoverformat=hover_format, showspikes=True, spikemode="across", ticktext=ticktext, tickvals=tickvals),
    yaxis=dict(side='right', range=yaxis_range),
    yaxis2=dict(side='left', showticklabels=False, overlaying='y', showgrid=False, autorange=True), #range=yaxis2_range
    showlegend=False
)

def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    else:
        return f"{volume}"

# Add this section to dynamically set the hovertemplate and text for update_traces
if selected_option == '1d':
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['5d']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['1mo']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['6mo']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['ytd']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['1y']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['5y']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'
elif selected_option in ['max']:
    hover_template = '%{text}<br> $%{y:.2f} Close<br> %{customdata} Volume'


fig.update_traces(
    hovertemplate=hover_template,
    hoverinfo='x',
    text=stock_data.index.strftime(hover_format),
    customdata=[format_volume(volume) for volume in stock_data['Volume']],
    selector=dict(type='scatter')
)
st.plotly_chart(fig)