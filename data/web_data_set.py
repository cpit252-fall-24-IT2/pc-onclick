import requests
import pandas as pd
from io import StringIO

def get_best_options(url, budget=None, manufacturer=None, columns=None):
    # Fetch the content from the URL
    response = requests.get(url)
    csv_data = response.content.decode('utf-8')
    
    # Convert the CSV data into a DataFrame
    df = pd.read_csv(StringIO(csv_data))
    # Apply filters only if parameters are provided
    if budget is not None:
        df = df[df['price'] <= budget]
    if manufacturer:
        df = df[df['name'].str.contains(manufacturer, case=False, na=False)]
        
    
    # Sort the DataFrame by price and select the top 10 options
    top_options = df.sort_values(by='price').tail(20)
    
    # Select specified columns if provided, else return all columns
    if columns:
        top_options = top_options[columns]
    
    return top_options

# Example usage for CPU
def get_CPU(budget, manufacturer):
    CPU_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
    CPU_budget = budget
    CPU_manufacturer = manufacturer
    CPU_columns = ['name', 'price', 'core_count']
    return get_best_options(CPU_url, CPU_budget, CPU_manufacturer, CPU_columns)

# Example usage for GPU
def get_GPU(budget, manufacturer):
    GPU_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
    GPU_budget = budget
    GPU_manufacturer = manufacturer
    GPU_columns = ['name', 'price', 'core_count']
    return get_best_options(GPU_url, GPU_budget, GPU_manufacturer, GPU_columns)



# Display the results

print(get_CPU(budget=500, manufacturer='amd'))
