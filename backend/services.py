import yfinance as yf
import pandas as pd
import csv

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
           (stock_info.get('marketCap') < min_market_cap):
            continue
        # If all conditions are met append the data directly
        filtered_stocks.append(stock_info)
    return filtered_stocks

def nomralize_data(stock_data):
    pass

stock_symbols = get_stock_symbols('stock_symbols_short.csv')
stock_data = fetch_stocks(stock_symbols)
stock_data = filter_stocks(stock_data, exchange='NMS', sector='Technology')

print(stock_data)
