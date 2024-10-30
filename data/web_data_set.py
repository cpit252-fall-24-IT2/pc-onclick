import requests
import pandas as pd
from io import StringIO


def get_best_options(url, budget=None, manufacturer=None, columns=None):
    response = requests.get(url)
    csv_data = response.content.decode('utf-8')

    df = pd.read_csv(StringIO(csv_data))

    if budget is not None:
        df = df[df['price'] <= budget]

    # Filter by manufacturer keyword in the name
    if manufacturer:
        df = df[df['name'].str.contains(manufacturer, case=False, na=False)]

    # Sort by price to get the top options within budget
    top_options = df.sort_values(by='price').tail(20)

    if columns:
        top_options = top_options[columns]

    return top_options


def get_CPU(budget, manufacturer):
    CPU_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/cpu.csv'
    CPU_columns = ['name', 'price', 'core_count']
    return get_best_options(CPU_url, budget, manufacturer, CPU_columns)


def get_GPU(budget, manufacturer):
    GPU_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/video-card.csv'
    GPU_columns = ['name', 'price', 'chipset']
    return get_best_options(GPU_url, budget, manufacturer, GPU_columns)


def get_motherboard(budget, manufacturer):
    motherboard_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/motherboard.csv'
    motherboard_columns = ['name', 'price', 'socket']
    return get_best_options(motherboard_url, budget, manufacturer, motherboard_columns)


def get_power_supply(budget, manufacturer):
    psu_url = 'https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/csv/power-supply.csv'
    psu_columns = ['name', 'price', 'efficiency', 'wattage', 'modular']
    return get_best_options(psu_url, budget, manufacturer, psu_columns)



