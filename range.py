import yfinance as yf
import os
import time
import scipy
from datetime import datetime
import math
import numpy as np


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

def call_price(asset, sigma, strike, expiry, interest):
    d1 = (math.log(asset / strike) + 
          (interest + .5 * sigma**2) * expiry) / (sigma * expiry**.5)
    d2 = d1 - sigma * expiry**0.5
    n1 = math.norm.cdf(d1)
    n2 = math.norm.cdf(d2)
    DF = math.exp(-interest * expiry)
    price = asset * n1 - strike * DF * n2
    return price

# Initial guess of volatility value
def inflexion_point(asset, strike, expiry, r):
    m = asset / (strike * math.exp(-r * expiry))
    return math.sqrt(2 * np.abs(math.log(m)) / expiry)

def vega(asset, sigma, strike, expiry, interest):
    d1 = (math.log(asset / strike) + (interest + .5 * sigma**2) * expiry) / (sigma * expiry**.5)
    vega = asset * expiry**0.5 * math.norm.pdf(d1)
    return vega

def volatility(premium, asset, strike, interest, expiry, tolerance):
    guess = inflexion_point(asset, strike, expiry, interest)
    call = call_price(asset, guess, strike, expiry, interest)
    vega = vega(asset, guess, strike, expiry, interest)
    while (abs((price - premium) / vega) > tolerance):
        guess = guess - (call - premium) / vega
        call = call_price(asset, guess, strike, expiry, interest)
        vega = vega(asset, guess, strike, expiry, interest)
    return guess

print(price, premium)
