# Quantitative Option Pricing and Risk

Numerical methods for option valuation, sensitivities, hedging, stochastic volatility, and jump risk.

## Research modules

- Lattice pricing for European and American options, Greeks, put-call parity, and delta hedging.
- Monte Carlo pricing under Heston and Merton models, including barrier and early-exercise examples.
- Heston parameter calibration using Lewis and Carr?Madan Fourier methods.

## Data and execution

Install dependencies from `requirements.txt` and run notebooks in Jupyter from the repository root. The source calibration workbook is retained at `data/heston_calibration/option_data.xlsx`; the notebook currently uses the market observations embedded in its code. Other modules use specified or simulated inputs.

The notebooks remain separate because they use distinct parameter sets and variable conventions. Review assumptions and attribution before release.
