"""Unit tests for option lattice pricers, Fourier engines, and Greeks."""

import sys
import os
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models import binomial_american_option, trinomial_european_option, heston_lewis_call
from src.evaluation import compute_finite_difference_greeks, check_put_call_parity


class TestOptionPricingModels(unittest.TestCase):

    def setUp(self):
        self.S0 = 100.0
        self.K = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0

    def test_binomial_american_call_bounds(self):
        call_price = binomial_american_option(self.S0, self.K, self.r, self.sigma, self.T, n_steps=50, option_type='call')
        # Non-dividend paying American call should be approximately Black-Scholes price (~10.45)
        self.assertGreater(call_price, 9.5)
        self.assertLess(call_price, 11.5)

    def test_binomial_american_put_early_exercise(self):
        # Deep ITM American put should be >= intrinsic value S0 - K
        deep_itm_k = 150.0
        put_price = binomial_american_option(self.S0, deep_itm_k, self.r, self.sigma, self.T, n_steps=50, option_type='put')
        intrinsic = deep_itm_k - self.S0
        self.assertGreaterEqual(put_price, intrinsic - 1e-4)

    def test_trinomial_european_convergence(self):
        call_tri = trinomial_european_option(self.S0, self.K, self.r, self.sigma, self.T, n_steps=50, option_type='call')
        call_bi = binomial_american_option(self.S0, self.K, self.r, self.sigma, self.T, n_steps=50, option_type='call')
        # For non-dividend call, European trinomial and American binomial converge
        self.assertAlmostEqual(call_tri, call_bi, delta=0.5)

    def test_heston_lewis_pricing(self):
        # Known standard benchmark parameters: kappa=2.0, theta=0.04, sigma=0.3, rho=-0.7, v0=0.04
        price = heston_lewis_call(self.S0, self.K, self.T, self.r, kappa=2.0, theta=0.04, sigma=0.3, rho=-0.7, v0=0.04)
        self.assertGreater(price, 8.0)
        self.assertLess(price, 12.0)

    def test_finite_difference_greeks(self):
        def dummy_pricer(S):
            return binomial_american_option(S, self.K, self.r, self.sigma, self.T, n_steps=30, option_type='call')
        res = compute_finite_difference_greeks(dummy_pricer, self.S0, h=0.5)
        # ATM Call delta should be around 0.5 - 0.7
        self.assertGreater(res['Delta'], 0.4)
        self.assertLess(res['Delta'], 0.8)
        self.assertGreater(res['Gamma'], 0.0)

    def test_put_call_parity_checker(self):
        # Artificial consistent prices
        call_p = 10.45
        put_p = call_p - self.S0 + self.K * np.exp(-self.r * self.T)
        parity = check_put_call_parity(call_p, put_p, self.S0, self.K, self.r, self.T)
        self.assertTrue(parity['Holds'])
        self.assertLess(parity['Discrepancy'], 1e-4)


if __name__ == '__main__':
    unittest.main()
