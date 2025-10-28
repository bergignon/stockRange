import yfinance as yf
import os
import time
from datetime import datetime
from util import *
import numpy as np

# Get ticker

while True:
    ticker = input("Enter the ticker of the stock : ")
    if any(not char.isupper() for char in ticker):
        print("Enter a valid ticker\r")
        time.sleep(0.5)
        os.system('clear')
    else:
        break

data = yf.Ticker(ticker)

print("Available days to forecast : ")
for index, date in enumerate(data.options):
    index += 1
    print(f"Number #{index} : {date}  |   ", end='')

date_choice = int(input("Select forecast day : "))
date_choice = data.options[date_choice-1]

# Param 1
price = data.info['regularMarketPrice']

option = data.option_chain(date_choice)
print(len(option.calls))
call = option.calls.iloc[int(len(option.calls) / 2)]

# Param 2 3 & 4
premium = call["lastPrice"]
strike = call["strike"]
interest_rate = 0.04

exp_date = datetime.strptime(date_choice, "%Y-%m-%d")
today = datetime.today()

# Param 5

time_to_expiration = (exp_date - today).days / 365

IV = volatility(premium, price, strike, interest_rate, time_to_expiration, 10**-8)
print(IV)

small_iv = IV * np.sqrt(time_to_expiration)

U = price * 2
L = price * 1.5
days = (exp_date - today).days

z_upper = (np.log(U/price) + 0.5 * small_iv**2) / small_iv
z_lower = (np.log(L/price) + 0.5 * small_iv**2) / small_iv

prob = norm.cdf(z_upper) - norm.cdf(z_lower)
print(f"Probability of stock ending between {L} and {U} in {days} days: {prob:.2%}")