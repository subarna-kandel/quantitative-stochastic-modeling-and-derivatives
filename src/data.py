"""Option chain data loading, cleaning, and filtering routines."""

import os
import pandas as pd
import numpy as np


def load_heston_market_data(filepath=None):
    """Load reference market option quotes from Excel/CSV source."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'heston_calibration', 'option_data.xlsx')
    if os.path.exists(filepath):
        df = pd.read_excel(filepath)
        return df
    # Fallback to standard mock/reference quotes if file not present
    strikes = np.array([210.0, 220.0, 230.0, 240.0, 250.0])
    market_prices = np.array([25.4, 18.2, 12.1, 7.5, 4.2])
    return pd.DataFrame({'Strike': strikes, 'MarketPrice': market_prices})


def filter_otm_options(options_df, S0, option_type='call'):
    """Filter out-of-the-money options to mitigate liquidity bias during calibration."""
    if option_type == 'call':
        return options_df[options_df['Strike'] >= S0].copy()
    else:
        return options_df[options_df['Strike'] <= S0].copy()
