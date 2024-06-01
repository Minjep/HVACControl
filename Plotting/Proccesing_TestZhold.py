import pandas as pd

# Assuming you have a list of row dictionaries like row = {'unix time': unixTime[index], 'real time': formatted_date, 'value': dataValues[index]}
# Example data
rows = [
    {'unix time': 1616188800, 'real time': '2021-03-20 00:00:00', 'value': 400},
    {'unix time': 1616275200, 'real time': '2021-03-21 00:00:00', 'value': 410},
    # Add more data as needed
]

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(rows)

# Convert 'real time' column to datetime
df['real time'] = pd.to_datetime(df['real time'])

# Set 'real time' as the index
df.set_index('real time', inplace=True)

# Assuming you have a date range for your data, you can use it to reindex the DataFrame
# Assuming start_date and end_date are the start and end dates of your data
start_date = df.index.min()
end_date = df.index.max()
date_range = pd.date_range(start=start_date, end=end_date, freq='D')  # Daily frequency, adjust as needed

# Reindex the DataFrame to include all dates in the range
df = df.reindex(date_range)

# Forward fill missing values (zero-order hold)
df['value'] = df['value'].fillna(method='ffill')

print(df)
print("test")