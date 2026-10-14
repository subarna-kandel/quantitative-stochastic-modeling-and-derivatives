"""Visualizations for option prices, Greeks profiles, and calibration surfaces."""

import matplotlib.pyplot as plt
import numpy as np


def plot_price_vs_strike(strikes, call_prices, put_prices, title="Option Price Profile"):
    """Plot European call and put price curves against strike."""
    plt.figure(figsize=(8, 5))
    plt.plot(strikes, call_prices, 'b-o', label='Call Price')
    plt.plot(strikes, put_prices, 'r-s', label='Put Price')
    plt.xlabel('Strike (K)')
    plt.ylabel('Option Premium')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    return plt.gcf()
