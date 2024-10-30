import requests
import pandas as pd
from io import StringIO

# GitHub raw URL for the CSV file
url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'

# Fetch the content from the URL
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Convert the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Set budget and manufacturer filter directly
budget = 500  # Set your budget
manufacturer = 'intel'  # Set your desired CPU manufacturer

# Filter the DataFrame based on budget and manufacturer
filtered_df = df[(df['price'] <= budget) & (df['name'].str.contains(manufacturer, case=False))]

# Sort the DataFrame by price and select the top 10 CPUs
top_cpus = filtered_df.sort_values(by='price').tail(10)

# Display the results
print("Top 10 CPU options:")
print(top_cpus[['name', 'price', 'core_count', 'core_clock', 'boost_clock', 'tdp', 'graphics', 'smt']])
