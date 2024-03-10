from datetime import datetime

def convert_unix_timestamp_to_date(unix_timestamp):
    try:
        # Convert Unix timestamp to datetime object
        date_object = datetime.utcfromtimestamp(unix_timestamp)
        # Format the datetime object as a string
        formatted_date = date_object.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        return 'Invalid Date'

# Function to convert Unix timestamp to date
def convert_unix_to_date(unix_timestamp):
    if unix_timestamp == 'N/A':
        return 'N/A'
    else:
        return convert_unix_timestamp_to_date(unix_timestamp)

