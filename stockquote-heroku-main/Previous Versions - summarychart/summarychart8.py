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

# Used as a conditional check for assets that do not have minute intraday data.
def has_minute_data_in_last_day(ticker):
    # Fetch historical stock data with '1m' interval for the last day
    stock_data = yf.download(ticker, interval='1m', period='1d')
    return not stock_data.empty and len(stock_data) >= 2

# User input for stock ticker
ticker = st.text_input('Enter Stock Ticker:', 'AAPL')

# Check if the ticker is provided
if not ticker:
    st.error("Please enter a valid stock ticker.")
    st.stop()  # Stop further execution of the code

# Fetch historical stock data
try:
    stock_data = yf.download(ticker, period='1mo')
    
    # Check if stock_data is empty
    if stock_data.empty:
        st.error(f"No data available for the stock with ticker '{ticker}'. Please enter a valid ticker.")
        st.stop()  # Stop further execution of the code

except IndexError:
    st.error(f"Stock with ticker '{ticker}' does not exist. Please enter a valid ticker.")
    st.stop()  # Stop further execution of the code

# Create two columns
col1, col2 = st.columns([1, 1])

# Check if 'Volume' column is present and contains non-zero values
if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():
    # If there is minute data available for the most recent day, include intraday options
    if has_minute_data_in_last_day(ticker): 
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
    else:
        # If there is no minute data for the most recent day, exclude intraday options
        time_period_options = {
            '6mo': {'interval': '1d', 'period': '6mo'},
            '1y': {'interval': '1d', 'period': '1y'},
            '5y': {'interval': '1wk', 'period': '5y'},
            'max': {'interval': '1wk', 'period': 'max'}
        }
else:
    # If there is no minute data and no volume data, exclude intraday options
    time_period_options = {
        '1mo': {'interval': '1d', 'period': '1mo'},
        'ytd': {'interval': '1d', 'period': 'ytd'},
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

# Display stock dataframe
st.write(stock_data)

if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():

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
else:
    
    if selected_option in ['1mo']:
        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
        formatted_labels = stock_data.index.strftime('%b %#d')
        hover_format = stock_data.index.strftime('%b %#d, %y')
        tickvals = formatted_dates[::7]
        ticktext = formatted_labels[::7]
    elif selected_option in ['ytd']:
        formatted_dates = stock_data.index.strftime('%Y-%m-%d %I:%M %p')
        formatted_labels = stock_data.index.strftime('%b %#d, %y')
        hover_format = stock_data.index.strftime('%b %#d, %y')
        tickvals = formatted_dates[::9]
        ticktext = formatted_labels[::9]
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

#Add shaded areas for every other tick on the x-axis for background
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
if 'Volume' in stock_data.columns and not stock_data['Volume'].eq(0).all():
    # Add bar trace for volume
    volume_colors = ['red' if close_price < open_price else 'green' for open_price, close_price in zip(stock_data['Open'], stock_data['Close'])]

    if chart_type in ['Line', 'Candlestick']:
        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color=volume_colors, hoverinfo='skip'))
    else:
        fig.add_trace(go.Bar(x=formatted_dates, y=stock_data['Volume'], yaxis='y2', name='Volume', marker_color='rgba(160, 198, 255, 1)', hoverinfo='skip'))

    # Update axis labels and layout for volume data available
    fig.update_yaxes(title_text='', showspikes=True, nticks=5, spikemode="across", spikethickness=-2, side='right')
    fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=-2, side='right', secondary_y=True, showticklabels=False)

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
    # Update axis labels and layout for no volume data available
    fig.update_yaxes(title_text='', showspikes=True, nticks=5, spikemode="across", spikethickness=-2, side='right')
    fig.update_yaxes(title_text='', showspikes=True, spikemode="across", spikethickness=-2, side='right', secondary_y=True, showticklabels=False)

    # Add this section to dynamically set the y-axis ranges based on selected_option
    if selected_option in ['1mo']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = None
    elif selected_option in ['ytd']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = None
    elif selected_option in ['1y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = None    
    elif selected_option in ['5y']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = None
    elif selected_option in ['max']:
        yaxis_range = [stock_data['Close'].min() * 0.99, stock_data['Close'].max() * 1.01]
        yaxis2_range = None

fig.update_layout(
    hovermode='closest',
    hoverlabel=dict(bgcolor="white", font_color="black", font_size=14, font_family="Arial", bordercolor="black"),
    xaxis=dict(showspikes=True, spikemode="across", ticktext=ticktext, tickvals=tickvals, spikethickness=-2, fixedrange=True),
    yaxis=dict(side='right', range=yaxis_range, fixedrange=True),
    yaxis2=dict(showticklabels=False, overlaying='y', showgrid=False, range=yaxis2_range, fixedrange=True),
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

# Find the most recent closing price
most_recent_close = stock_data['Close'].iloc[-1]

# Add a scatter trace so annotation can find y-axis of the most recent price
fig.add_trace(go.Scatter(
    x=[formatted_dates[-1]],
    y=[most_recent_close],
    mode='markers',
    marker=dict(color='red', size=10),
    showlegend=False,
    hoverinfo='none',
    visible=False
))

# Update the layout to ensure the annotation stays on the y-axis
fig.update_layout(
    annotations=[
        dict(
            x=1,  # Adjust this value to control the x-position of the annotation
            y=most_recent_close,
            xref='paper',
            yref='y',
            text=f'${most_recent_close:.2f}',  # Display the price value
            showarrow=False,
            font=dict(color='White', size=12),
            align='left',
            # bordercolor='red',
            # borderwidth=1,
            # borderpad=4,
            bgcolor='rgba(0, 104, 201, 1)'
        )
    ]
)

# Trace for Line & Area
fig.update_traces(
    hovertemplate=hover_template,
    hoverinfo='x',
    text=[f'{ticker}<br>{hover_format[i]}<br>${open_price:.2f} Open<br>${high_price:.2f} High<br>${low_price:.2f} Low<br>${close_price:.2f} Close<br>{format_volume(volume)} Volume'
          for i, (open_price, high_price, low_price, close_price, volume) in enumerate(
              zip(stock_data['Open'], stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume']))],
    selector=dict(type='scatter')
)

# Get the 52-week high and low
fifty_two_week_high = stock_data['Close'].max()
fifty_two_week_low = stock_data['Close'].min()

# Calculate the percentage from the 52-week low and high
percent_from_low = ((most_recent_close - fifty_two_week_low) / fifty_two_week_low) * 100
percent_from_high = ((most_recent_close - fifty_two_week_high) / fifty_two_week_high) * 100

# Buy or Sell recommendations based on percentage from 52-week low/high
buy_sell_recommendation_low = "Buy" if percent_from_low > 10 else "Hold" if 0 <= percent_from_low <= 10 else "Sell"
buy_sell_recommendation_high = "Buy" if percent_from_high > -10 else "Hold" if -10 <= percent_from_high <= 0 else "Sell"


# Percent Change of ticker
bgcolor = "green" if percentage_change >= 0 else "red"
fig.add_annotation(
    text=f'({selected_option}) {ticker} {percentage_change:.2f}%',
    xref='paper', yref='paper',
    x=0.00, y=1.10,
    showarrow=False,
    font=dict(size=13, color="black", family="Arial Black"),
    bgcolor=bgcolor,  # Set bgcolor based on the sign of percentage_change
)

fig.add_annotation(
    text=f'52WK-L {fifty_two_week_low:.2f}\n {percent_from_low:.2f}%\n {buy_sell_recommendation_low}',
    xref='paper', yref='paper',
    x=0.00, y=1.30,
    showarrow=False,
    font=dict(size=13, color="black", family="Arial Black"),
    bgcolor='rgba(245,245,245,1.000)',
)

fig.add_annotation(
    text=f'52WK-H {fifty_two_week_high:.2f}\n {percent_from_high:.2f}%\n {buy_sell_recommendation_high}',
    xref='paper', yref='paper',
    x=0.00, y=1.20,
    showarrow=False,
    font=dict(size=13, color="black", family="Arial Black"),
    bgcolor='rgba(245,245,245,1.000)',
)

# Border top-side
fig.add_shape(
            type="line",
            xref="paper",
            yref="paper",
            x0=0,
            y0=1.12,
            x1=.94,
            y1=1.12,
            line=dict(
                color="white",
                width=2,
            )
        )

# Border bot-side
fig.add_shape(
            type="line",
            xref="paper",
            yref="paper",
            x0=0,
            y0=0,
            x1=.94,
            y1=0,
            line=dict(
                color="rgba(245,245,245,1.000)",
                width=2,
            )
        )

# Border right-side
fig.add_shape(
            type="line",
            xref="paper",
            yref="paper",
            x0=.94,
            y0=1.12,
            x1=.94,
            y1=0,
            line=dict(
                color="rgba(245,245,245,1.000)",
                width=3,
            )
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
st.plotly_chart(fig, config=config, use_container_width=True)
