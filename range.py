import yfinance as yf
import os
import time
import scipy
from datetime import datetime

def is_valid_date_format(date_string):
    try:
        if datetime.strptime(date_string, '%Y-%m-%d') < datetime.now():
            return False
        return True
    except ValueError:
        return False

# Get ticker

# while True:
#     ticker = input("Enter the ticker of the stock : ")
#     if any(not char.isupper() for char in ticker):
#         print("Enter a valid ticker\r")
#         time.sleep(0.5)
#         os.system('clear')
#     else:
#         break

# # Get date of range

# while True:
#     date = input("Enter the date of desired IV expectation (YYYY-MM-DD) : ")
#     if is_valid_date_format(date):
#         break
#     else:
#         print("Enter a valid date\r")
#         time.sleep(0.5)
#         os.system('clear')
ticker = "AAPL"
date = "2025-10-31"
data = yf.Ticker(ticker)

expiration_dates = data.options
print(expiration_dates)
option = data.option_chain(date)
print(option)