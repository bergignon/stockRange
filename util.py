import math
import numpy as np
from scipy.stats import norm

def call_price(asset, sigma, strike, expiry, interest):
    d1 = (math.log(asset / strike) + 
          (interest + .5 * sigma**2) * expiry) / (sigma * expiry**.5)
    d2 = d1 - sigma * expiry**0.5
    n1 = norm.cdf(d1)
    n2 = norm.cdf(d2)
    DF = math.exp(-interest * expiry)
    price = asset * n1 - strike * DF * n2
    return price

# Initial guess of volatility value
def inflexion_point(asset, strike, expiry, r):
    m = asset / (strike * math.exp(-r * expiry))
    return math.sqrt(2 * np.abs(math.log(m)) / expiry)

def compute_vega(asset, sigma, strike, expiry, interest):
    d1 = (math.log(asset / strike) + (interest + .5 * sigma**2) * expiry) / (sigma * expiry**.5)
    vega = asset * expiry**0.5 * norm.pdf(d1)
    return vega

def volatility(premium, asset, strike, interest, expiry, tolerance):
    guess = inflexion_point(asset, strike, expiry, interest)
    call = call_price(asset, guess, strike, expiry, interest)
    vega = compute_vega(asset, guess, strike, expiry, interest)
    while (abs((call - premium) / vega) > tolerance):
        guess = guess - (call - premium) / vega
        print("Price difference : ", call - premium)
        call = call_price(asset, guess, strike, expiry, interest)
        vega = compute_vega(asset, guess, strike, expiry, interest)
    return guess

