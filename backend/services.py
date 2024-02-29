import yfinance as yf
import pandas as pd
import csv

metrics = ['trailingPE', 'forwardPE', 'priceToBook', 'debtToEquity', 'dividendYield', 'freeCashflow']
# Metrics for which lower is better
invert_list = set(['trailingPE', 'forwardPE', 'priceToBook', 'debtToEquity'])
weights = {'trailingPE': 0.18, 'forwardPE': 0.12, 'priceToBook': 0.25, 'debtToEquity': 0.2, 'dividendYield': 0.15, 'freeCashflow': 0.1}


# Fetches the stock symbols from the csv file
def get_stock_symbols(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]
    
def fetch_stocks(stock_symbols):
    stock_data =[]

    # Get all stock infos
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        stock_data.append(stock_info)

    return stock_data

def filter_stocks(stock_data, exchange='Any', sector='Any', min_market_cap=0):
    filtered_stocks = []

    # Filter for each stock
    for stock_info in stock_data:
        # Early skip conditions that don't meet the criteria
        if (sector != 'Any' and stock_info.get('sector') != sector) or \
           (exchange != 'Any' and stock_info.get('exchange') != exchange) or \
           (stock_info.get('marketCap', 0) < min_market_cap):
            continue
        # If all conditions are met append the data directly
        filtered_stocks.append(stock_info)
    return filtered_stocks

# Gets min and max value for each metric, needed for normalization
def get_min_max_values(stock_data):

    min_max_values = {metric: {'min': float('inf'), 'max': float('-inf')} for metric in metrics}

    for stock in stock_data:
        for metric in metrics:
            value = stock.get(metric)
            if isinstance(value, float) or isinstance(value, int):
                min_max_values[metric]['min'] = min(min_max_values[metric]['min'], value)
                min_max_values[metric]['max'] = max(min_max_values[metric]['max'], value)
    
    return min_max_values

def normalize_value(value, min_value, max_value, invert=False):
    if max_value - min_value == 0:
        return 1 if invert else 0
    normalized = (value - min_value) / (max_value - min_value)
    return 1 - normalized if invert else normalized

def calculate_undervalue_index(stock, min_max_values):
    undervalue_index = 0
    for metric, weight in weights.items():

        min_value, max_value = min_max_values[metric]['min'], min_max_values[metric]['max']
        metric_value = stock.get(metric)

        if isinstance(metric_value, float) or isinstance(metric_value, int):
            invert = metric in invert_list
            normalized_value = normalize_value(metric_value, min_value, max_value, invert=invert)
            undervalue_index += normalized_value * weight

    return undervalue_index

def get_top_stocks(stock_data, n):
    # Calculate undervalue index for each stock
    min_max_values = get_min_max_values(stock_data)
    for stock in stock_data:
        stock['undervalue_index'] = calculate_undervalue_index(stock, min_max_values)

    # Sort stocks by undervalue index in descending order
    sorted_stocks = sorted(stock_data, key=lambda x: x['undervalue_index'], reverse=True)

    # Return the top n stocks
    return sorted_stocks[:n]

stock_symbols = get_stock_symbols('symbol_list_final.csv')
stock_data = fetch_stocks(stock_symbols)
filtered_stock_data = filter_stocks(stock_data)
top_stocks = get_top_stocks(filtered_stock_data, 120)

#for stock in filtered_stock_data:
 #   for metric in metrics:
  #      print(stock.get('symbol'), type(stock.get(metric)))

for stock in top_stocks:
    print(f"Symbol: {stock['symbol']}, Undervalue Index: {stock['undervalue_index']}")
