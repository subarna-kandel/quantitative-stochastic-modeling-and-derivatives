"""Option pricing lattice and stochastic volatility models (CRR, Trinomial, Heston, Merton)."""

import numpy as np


def binomial_american_option(S0, K, r, sigma, T, n_steps=100, option_type='call'):
    """Price American option using Cox-Ross-Rubinstein (CRR) binomial tree."""
    dt = T / n_steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    q = (np.exp(r * dt) - d) / (u - d)
    df = np.exp(-r * dt)

    stock_prices = S0 * (u ** np.arange(n_steps, -1, -1)) * (d ** np.arange(0, n_steps + 1))
    if option_type == 'call':
        option_values = np.maximum(stock_prices - K, 0.0)
    else:
        option_values = np.maximum(K - stock_prices, 0.0)

    for i in range(n_steps - 1, -1, -1):
        stock_prices = S0 * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1))
        continuation = df * (q * option_values[:-1] + (1.0 - q) * option_values[1:])
        if option_type == 'call':
            exercise = np.maximum(stock_prices - K, 0.0)
        else:
            exercise = np.maximum(K - stock_prices, 0.0)
        option_values = np.maximum(exercise, continuation)

    return float(option_values[0])


def trinomial_european_option(S0, K, r, sigma, T, n_steps=100, option_type='call'):
    """Price European option using Boyle trinomial lattice."""
    dt = T / n_steps
    u = np.exp(sigma * np.sqrt(2.0 * dt))
    d = 1.0 / u
    pu = ((np.exp(r * dt / 2.0) - np.exp(-sigma * np.sqrt(dt / 2.0))) /
          (np.exp(sigma * np.sqrt(dt / 2.0)) - np.exp(-sigma * np.sqrt(dt / 2.0)))) ** 2
    pd = ((np.exp(sigma * np.sqrt(dt / 2.0)) - np.exp(r * dt / 2.0)) /
          (np.exp(sigma * np.sqrt(dt / 2.0)) - np.exp(-sigma * np.sqrt(dt / 2.0)))) ** 2
    pm = 1.0 - pu - pd

    j_indices = np.arange(-n_steps, n_steps + 1)
    stock_prices = S0 * (u ** j_indices)
    if option_type == 'call':
        option_values = np.maximum(stock_prices - K, 0.0)
    else:
        option_values = np.maximum(K - stock_prices, 0.0)

    for i in range(n_steps - 1, -1, -1):
        option_values = np.exp(-r * dt) * (pu * option_values[2:] + pm * option_values[1:-1] + pd * option_values[:-2])

    return float(option_values[0])


def heston_characteristic_function(u, S0, T, r, kappa, theta, sigma, rho, v0):
    """Heston (1993) log-price characteristic function E[exp(i u ln S_T)]."""
    x0 = np.log(S0)
    d = np.sqrt((rho * sigma * 1j * u - kappa)**2 + sigma**2 * (1j * u + u**2))
    g = (kappa - rho * sigma * 1j * u - d) / (kappa - rho * sigma * 1j * u + d)
    C = r * 1j * u * T + (kappa * theta / sigma**2) * ((kappa - rho * sigma * 1j * u - d) * T - 2.0 * np.log((1.0 - g * np.exp(-d * T)) / (1.0 - g)))
    D = ((kappa - rho * sigma * 1j * u - d) / sigma**2) * ((1.0 - np.exp(-d * T)) / (1.0 - g * np.exp(-d * T)))
    return np.exp(C + D * v0 + 1j * u * x0)


def heston_lewis_call(S0, K, T, r, kappa, theta, sigma, rho, v0, alpha=1.5):
    """Heston European call price via Carr-Madan Fourier damped transform."""
    u_grid = np.linspace(1e-4, 50.0, 3000)
    du = u_grid[1] - u_grid[0]
    denom = alpha**2 + alpha - u_grid**2 + 1j * (2.0 * alpha + 1.0) * u_grid
    cf_vals = np.array([heston_characteristic_function(u - (alpha + 1.0) * 1j, S0, T, r, kappa, theta, sigma, rho, v0) for u in u_grid])
    integrand = (np.exp(-r * T) * np.exp(-1j * u_grid * np.log(K)) * cf_vals / denom).real
    call_price = (np.exp(-alpha * np.log(K)) / np.pi) * np.sum(integrand) * du
    return float(np.maximum(call_price, 0.0))
