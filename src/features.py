"""Moneyness transformations, volatility surfaces, and grid construction."""

import numpy as np


def log_moneyness(S, K):
    """Compute log-moneyness ln(K / S)."""
    return np.log(np.asarray(K) / np.asarray(S))


def black_scholes_implied_vol(price, S, K, T, r, option_type='call'):
    """Compute Black-Scholes implied volatility using Brent root finder."""
    from scipy.stats import norm
    from scipy.optimize import brentq

    def bs_price(vol):
        d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
        d2 = d1 - vol * np.sqrt(T)
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    try:
        return brentq(lambda v: bs_price(v) - price, 1e-4, 5.0)
    except Exception:
        return np.nan
