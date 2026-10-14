# Data Documentation: Derivatives Pricing & Stochastic Volatility

## Directory Structure
- `raw/`: Raw market option chains, Euribor discount curves, and underlying historical price data.
- `processed/`: Calibrated parameter logs, volatility surface meshes, and generated Monte Carlo price matrices.
- `heston_calibration/`: Contains the reference market option quote chain `option_data.xlsx`.

## Data Sources & Acquisition
- **Reference Market Options Chain**: `data/heston_calibration/option_data.xlsx` provides real-market European call quotes across various strikes and maturities.
- **Underlying Calibration Data**:
  - Underlying asset reference price: $S_0 = 232.90$
  - Risk-free term structure: Annualized risk-free rates calibrated against Euribor term structures.
- **Preprocessing Pipeline**:
  Options are filtered by strike, maturity ($T$), and moneyness. Out-of-the-money options are isolated to minimize liquidity premia before non-linear least squares calibration using Lewis and Carr-Madan Fourier transform methods.
