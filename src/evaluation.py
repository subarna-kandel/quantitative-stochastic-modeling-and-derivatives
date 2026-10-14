"""Option sensitivity (Greeks) estimation and parity checks."""

import numpy as np


def compute_finite_difference_greeks(pricing_fn, S0, h=1e-3, **kwargs):
    """Compute Delta and Gamma via central finite differences."""
    p_base = pricing_fn(S0, **kwargs)
    p_up = pricing_fn(S0 + h, **kwargs)
    p_down = pricing_fn(S0 - h, **kwargs)

    delta = (p_up - p_down) / (2.0 * h)
    gamma = (p_up - 2.0 * p_base + p_down) / (h ** 2)
    return {'Price': p_base, 'Delta': delta, 'Gamma': gamma}


def check_put_call_parity(call_price, put_price, S0, K, r, T):
    """Verify European put-call parity: C - P = S - K * exp(-r * T)."""
    lhs = call_price - put_price
    rhs = S0 - K * np.exp(-r * T)
    discrepancy = np.abs(lhs - rhs)
    return {'LHS (C - P)': lhs, 'RHS (S - K*e^-rT)': rhs, 'Discrepancy': discrepancy, 'Holds': bool(discrepancy < 0.05)}
