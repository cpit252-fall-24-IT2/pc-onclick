import requests
import pandas as pd
from io import StringIO
from abc import ABC, abstractmethod
import logging

class baseComponentRetrieval(ABC):
    @abstractmethod
    def get_best_options(self, url, budget=None, manufacturer=None, columns=None):
        pass

    @abstractmethod
    def get_component(self, component_type, budget, manufacturer):
        pass

class PCComponentFetcher(baseComponentRetrieval):

    def fetch_data():
        # Your implementation here
        return "Data fetched from web_data_set"
    
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
         
        return top_options , df['price'].min(), df['price'].max()

    def get_url_and_columns(self, component_type):
        if component_type == 'CPU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
            columns = ['name', 'price', 'core_count']
        elif component_type == 'GPU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/video-card.csv'
            columns = ['name', 'price', 'chipset']
        elif component_type == 'Motherboard':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/motherboard.csv'
            columns = ['name', 'price', 'socket']
        elif component_type == 'PSU':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/power-supply.csv'
            columns = ['name', 'price', 'efficiency', 'wattage', 'modular']
        elif component_type == 'RAM':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/memory.csv'
            columns = ['name', 'price', 'speed', 'modules', 'first_word_latency', 'cas_latency']
        elif component_type == 'Storage':
            url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/internal-hard-drive.csv'
            columns = ['name', 'price', 'capacity', 'type', 'form_factor', 'interface']
        else:
            raise ValueError(f"Unknown component type: {component_type}")
        return url, columns

    def get_component(self, component_type, budget, manufacturer):
        url, columns = self.get_url_and_columns(component_type)
        top_options, min_price, max_price = self.get_best_options(url, budget, manufacturer, columns)
        return top_options, min_price, max_price

    def get_price_ranges(self, component_type):
        url, _ = self.get_url_and_columns(component_type)
        _, min_price, max_price = self.get_best_options(url)
        return min_price, max_price

    def get_component_details(self, component_type, component_name):
        url, columns = self.get_url_and_columns(component_type)
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {url}. Status code: {response.status_code}")

        csv_data = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        
        logging.info(f"Searching for component: {component_name} in {component_type} dataset")
        component_details = df[df['name'].str.contains(component_name, case=False, na=False)]
        
        if component_details.empty:
            raise ValueError(f"No details found for component: {component_name}")
        
        return component_details.iloc[0].to_dict()

# Enable logging
logging.basicConfig(level=logging.INFO)

fetcher = PCComponentFetcher()