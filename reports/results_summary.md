# Research & Methodology Summary: Derivatives Pricing & Stochastic Volatility

## 1. Executive Overview
This project investigates numerical valuation engines and stochastic volatility calibration for complex derivative contracts. We examine discrete lattice methods (Cox-Ross-Rubinstein and Boyle trinomial trees), jump-diffusion processes (Merton 1976), and Fourier transform calibration for the Heston (1993) and Bates (1996) stochastic volatility models.

## 2. Mathematical Engines & Methods
- **Lattice Pricing**:
  - Binomial and Trinomial lattices implemented with dynamic backward induction to value American early-exercise opportunities.
  - Greeks estimation (Delta, Gamma, Vega) derived from internal node differences.
- **Continuous Stochastic Volatility**:
  - Heston model dynamics: $dS_t = r S_t dt + \sqrt{v_t} S_t dW_t^S$, $dv_t = \kappa(	heta - v_t)dt + \sigma_v \sqrt{v_t} dW_t^v$ with $d\langle W^S, W^v angle_t = ho dt$.
  - Exact characteristic function integration via Lewis (2001) and Carr-Madan (1999) dampened Fourier transforms.
- **Jump-Diffusion**: Compound Poisson jumps with log-normal jump magnitudes calibrated alongside diffusion vol.

## 3. Empirical Calibration Results
- **Model Fit**: Calibration to market call chains demonstrated that the Heston model successfully replicates the observed volatility skew/smile that constant-volatility Black-Scholes fails to capture.
- **Feller Condition**: Calibrated parameters ($2\kappa	heta > \sigma_v^2$) confirmed that the variance process remains strictly positive, preventing artificial absorption at zero.
- **Exotic Derivatives**: Longstaff-Schwartz Least Squares Monte Carlo (LSM) reliably priced American and path-dependent barrier options under stochastic volatility.

## 4. Limitations & Practical Remarks
- Optimization landscape exhibits local minima during calibration; robust global optimizers (differential evolution) are required.
- High-frequency Greek re-hedging induces discrete transaction cost drag in practical deployment.
