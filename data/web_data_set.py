import requests
import pandas as pd
from io import StringIO
from baseComponentRetrieval import baseComponentRetrieval

class PCComponentFetcher(baseComponentRetrieval):
    def get_best_options(self, url, budget=None, manufacturer=None, columns=None):
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {url}. Status code: {response.status_code}")

        csv_data = response.content.decode('utf-8')

        df = pd.read_csv(StringIO(csv_data))
        
        # Filter by budget
        if budget is not None:
            if 'price' in df.columns:
                if budget < df['price'].min():
                    raise ValueError(f"No options found within the budget of ${budget}")
                else:
                    df = df[df['price'] <= budget]
            else:
                raise KeyError("The 'price' column is not present in the DataFrame")

        # Filter by manufacturer keyword in the name
        if manufacturer:
            df = df[df['name'].str.contains(manufacturer, case=False, na=False)]

        # Sort by price to get the top options within budget
        top_options = df.sort_values(by='price').tail(20)

        if columns:
            top_options = top_options[columns]

        return top_options

    def get_component(self, component_type, budget, manufacturer):
        if component_type == 'CPU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
            columns = ['name', 'price', 'core_count']
        elif component_type == 'GPU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/video-card.csv'
            columns = ['name', 'price', 'chipset']
        elif component_type == 'motherboard':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/motherboard.csv'
            columns = ['name', 'price', 'socket']
        elif component_type == 'PSU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/power-supply.csv'
            columns = ['name', 'price', 'efficiency', 'wattage', 'modular']
        elif component_type == 'RAM':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/memory.csv'
            columns = ['name', 'price', 'speed', 'modules', 'first_word_latency', 'cas_latency']
        else:
            raise ValueError(f"Unknown component type: {component_type}")
        
        return self.get_best_options(url, budget, manufacturer, columns)

# Display the results
fetcher = PCComponentFetcher()
try:
    print(fetcher.get_component('RAM', budget=30, manufacturer=''))
    print(fetcher.get_component('CPU', budget=100, manufacturer=''))    
    print(fetcher.get_component('GPU', budget=2000000, manufacturer=''))
    print(fetcher.get_component('motherboard', budget=170, manufacturer=''))
    print(fetcher.get_component('PSU', budget=50, manufacturer=''))
except ValueError as e:
    print(e)

