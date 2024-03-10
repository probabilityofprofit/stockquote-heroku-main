import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Add this line
from datetime import datetime, timedelta

def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    else:
        return f"{volume}"

# User input for stock ticker
ticker = st.text_input('Enter Stock Ticker:', 'AAPL')

# Create two columns
col1, col2 = st.columns([1, 1])

# Fetch historical stock data
stock_data = yf.download(ticker, period='1mo')

# Check if 'Volume' column is present and contains non-zero values
if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():
    time_period_options = {
        '1d': {'interval': '2m', 'period': '1d'},
        '5d': {'interval': '15m', 'period': '5d'},
        '1mo': {'interval': '30m', 'period': '1mo'},
        '6mo': {'interval': '1d', 'period': '6mo'},
        'ytd': {'interval': '30m', 'period': 'ytd'},
        '1y': {'interval': '1d', 'period': '1y'},
        '5y': {'interval': '1wk', 'period': '5y'},
        'max': {'interval': '1mo', 'period': 'max'}
    }
    selected_option = col1.selectbox('Select Time Period:', list(time_period_options.keys()))
else:
    time_period_options = {
        '1mo': {'interval': '30m', 'period': '1mo'},
        'ytd': {'interval': '30m', 'period': 'ytd'},
        '1y': {'interval': '1d', 'period': '1y'},
        '5y': {'interval': '1wk', 'period': '5y'},
        'max': {'interval': '1mo', 'period': 'max'}
    }
    selected_option = col1.selectbox('Select Time Period:', list(time_period_options.keys()))

# Option for selecting chart type
chart_type_options = ['Line', 'Area', 'Candlestick']
selected_chart_type = col2.selectbox('Select Chart Type:', chart_type_options, index=0)

# Fetch historical stock data based on selected time period
interval = time_period_options[selected_option]['interval']
period = time_period_options[selected_option]['period']
stock_data = yf.download(ticker, interval=interval, period=period)

# Calculate percentage change
start_price = stock_data['Close'].iloc[0]
end_price = stock_data['Close'].iloc[-1]
percentage_change = ((end_price - start_price) / start_price) * 100

# Display stock data
st.write(f'### Historical Stock Data ({selected_option} period)')
# st.write(stock_data)

if selected_option == '1d':
    formatted_dates = stock_data.index.strftime('%I:%M %p')
    formatted_labels = stock_data.index.strftime('%I %p')
    hover_format = stock_data.index.strftime('%I:%M %p')
    tickvals = formatted_dates[::64]  # Display every 125th date
    ticktext = formatted_labels[::64]
elif selected_option in ['5d']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%a')
    hover_format = stock_data.index.strftime('%a, %b %d, %I:%M %p')
    tickvals = formatted_dates[::30]
    ticktext = formatted_labels[::30]
elif selected_option in ['1mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::90]
    ticktext = formatted_labels[::90]
elif selected_option in ['6mo']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::65]
    ticktext = formatted_labels[::65]
elif selected_option in ['ytd']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::125]
    ticktext = formatted_labels[::125]
elif selected_option in ['1y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::126]
    ticktext = formatted_labels[::126]
elif selected_option in ['5y']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::131]
    ticktext = formatted_labels[::131]
elif selected_option in ['max']:
    formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
    formatted_labels = stock_data.index.strftime('%b %#d, %y')
    hover_format = stock_data.index.strftime('%b %#d, %y')
    tickvals = formatted_dates[::79]
    ticktext = formatted_labels[::79]

# Create subplot with two y-axes
fig = make_subplots(specs=[[{"secondary_y": True}]])

#Add shaded areas for every other tick on the x-axis
for i in range(0, len(tickvals), 2):
    fig.add_shape(
        type="rect",
        x0=tickvals[i],
        x1=tickvals[i + 1] if i + 1 < len(tickvals) else formatted_dates[-1],
        y0=-1e9,
        y1=1e9,
        fillcolor="rgba(245,245,245,1.000)",
        opacity=1,
        layer="below",
        line=dict(width=0),
    )

# Default chart type is 'line'
chart_type = selected_chart_type

# Add trace based on chart type
if chart_type == 'Line':
    trace = go.Scatter(x=formatted_dates, y=stock_data['Close'], mode='lines', name=f'')
elif chart_type == 'Area':
    trace = go.Scatter(x=formatted_dates, y=stock_data['Close'], mode='lines', fill='tozeroy', name=f'', fillcolor='rgba(0, 104, 201, 1)')
elif chart_type == 'Candlestick':
    trace = go.Candlestick(x=formatted_dates,
                           open=stock_data['Open'],
                           high=stock_data['High'],
                           low=stock_data['Low'],
                           close=stock_data['Close'],
                           name=f'{ticker}',
                           hoverinfo='x+text+name')
    
    # Remove range slider for candlestick chart
    fig.update_xaxes(rangeslider_visible=False)

# Add trace to the subplot
fig.add_trace(trace)

# Check if volume data is available
if 'Volume' in stock_data.columns:
    # Add bar trace for volume
    volume_colors = ['red' if close_price < open_price else 'green' for open_price, close_price in zip(stock_data['Open'], stock_data['Close'])]

    if chart_type in ['Line', 'Candlestick']:
        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color=volume_colors, hoverinfo='skip'))
    else:
        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color='rgba(160, 198, 255, 1)', hoverinfo='skip'))

    # Update axis labels and layout
    fig.update_yaxes(title_text='', showspikes=True, nticks=5, spikemode="across", spikethickness=.5, side='right')
    fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=.5, side='right', secondary_y=True, showticklabels=False)

    # Add this section to dynamically set the y-axis ranges based on selected_option
    if selected_option == '1d':
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
    elif selected_option in ['5d']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 4.01]
    elif selected_option in ['1mo']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.01]
    elif selected_option in ['6mo']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
    elif selected_option in ['ytd']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
    elif selected_option in ['1y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
    elif selected_option in ['5y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]
    elif selected_option in ['max']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = [stock_data['Volume'].min() * 0.20, stock_data['Volume'].max() * 5.80]

else:
    fig.update_yaxes(title_text='', showspikes=True, nticks=5, spikemode="across", spikethickness=1, side='right')
    fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=1, side='right', secondary_y=True, showticklabels=False)

    # Add this section to dynamically set the y-axis ranges based on selected_option
    if selected_option == '1d':
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['5d']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['1mo']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['6mo']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['ytd']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['1y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['5y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
    elif selected_option in ['max']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]

fig.update_layout(
    hovermode='closest',
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", bordercolor="black"),
    xaxis=dict(showspikes=True, spikemode="across", ticktext=ticktext, tickvals=tickvals),
    yaxis=dict(side='right', range=yaxis_range),
    yaxis2=dict(side='left', showticklabels=False, overlaying='y', showgrid=False, range=yaxis2_range),
    showlegend=False
)

# Add this section to dynamically set the hovertemplate and text for update_traces
if selected_option == '1d':
    hover_template = '%{text}<br>'
elif selected_option in ['5d']:
    hover_template = '%{text}<br>'
elif selected_option in ['1mo']:
    hover_template = '%{text}<br>'
elif selected_option in ['6mo']:
    hover_template = '%{text}<br>'
elif selected_option in ['ytd']:
    hover_template = '%{text}<br>'
elif selected_option in ['1y']:
    hover_template = '%{text}<br>'
elif selected_option in ['5y']:
    hover_template = '%{text}<br>'
elif selected_option in ['max']:
    hover_template = '%{text}<br>'

# Trace for Line & Area
fig.update_traces(
    hovertemplate=hover_template,
    hoverinfo='x',
    text=[f'{ticker}<br>{hover_format[i]}<br>${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
          for i, (open_price, high_price, low_price, close_price, volume) in enumerate(
              zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume']))],
    selector=dict(type='scatter')
)

bgcolor = "green" if percentage_change >= 0 else "red"

fig.add_annotation(
    text=f'Percentage Change: {percentage_change:.2f}%',
    xref='paper', yref='paper',
    x=0.02, y=0.98,
    showarrow=False,
    font=dict(size=12, color="black", family="Balto"),
    bgcolor=bgcolor,  # Set bgcolor based on the sign of percentage_change
)

# Set hoverinfo and text for Candlestick
hoverinfo_candlestick = 'text'
text_candlestick = [
    f'${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
    for open_price, high_price, low_price, close_price, volume in
    zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume'])
]
# Trace for Candlestick
fig.update_traces(
    hoverinfo='text',
    text=[f'{ticker}<br>{hover_format[i]}<br>${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
          for i, (open_price, high_price, low_price, close_price, volume) in enumerate(
              zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume']))],
    selector=dict(type='candlestick')
)

# Hides the tools on the Mode Bar
config = {'displayModeBar': False}
st.plotly_chart(fig, config=config)
