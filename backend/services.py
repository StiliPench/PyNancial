import yfinance as yf
import pandas as pd
import csv

# Fetches the stock symbols from the csv file
def get_stock_symbols():
    with open('stock_symbols_short.csv', 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def fetch_and_filter_stocks(exchange='Any', sector='Any', min_market_cap=0):
    stock_symbols = get_stock_symbols()

    stock_data =[]

    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        stock_info = stock.info

        stock_sector = stock_info.get('sector')
        stock_exchange = stock_info.get('exchange')
        stock_market_cap = stock_info.get('marketCap')

        if stock_sector == sector or sector == 'Any':
            if stock_exchange == exchange or exchange == 'Any':
                if stock_market_cap >= min_market_cap:
                    stock_data.append(stock_info.get('symbol'))

    return stock_data

