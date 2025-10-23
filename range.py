import yfinance as yf
import os
import time
import scipy
from datetime import datetime
import math


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

date_str = "2025-10-31"
today = datetime.today()
exp_date = datetime.strptime(date_str, "%Y-%m-%d")
time_to_expiration = (exp_date - today).days / 365


ticker = "AAPL"
data = yf.Ticker(ticker)
interest_rate = 0.04

price = data.info['regularMarketPrice']
expiration_dates = data.options
option = data.option_chain(date_str)
call = option.calls.iloc[0]
premium = call["lastPrice"]

def CallPrice(S, sigma, K, T, r):
    d1 = (math.log(S / K) + (r + .5 * sigma**2) * T) / (sigma * T**.5)
    d2 = d1 - sigma * T**0.5
    n1 = math.norm.cdf(d1)
    n2 = math.norm.cdf(d2)
    DF = math.exp(-r * T)
    price=S * n1 - K * DF * n2
    return price


print(price, premium)
