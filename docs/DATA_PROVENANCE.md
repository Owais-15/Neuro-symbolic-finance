
# Data Provenance & Methodology

## 1. Data Source
*   **Primary Source**: [Yahoo Finance](https://pypi.org/project/yfinance/) via the `yfinance` Python library.
*   **Universe**: S&P 500 components (approx 500 stocks) + Specific "Zombie" companies for stress testing.
*   **Resolution**: Daily OHLCV (Open, High, Low, Close, Volume).

## 2. Temporal Splitting (The "Time Travel" Fix)
To prevent look-ahead bias (a common flaw in financial AI), we implement a strict **Hard Cutoff**:

*   **Decision Date (Cutoff)**: `2024-01-01`
*   **Input Data**: `2020-01-01` to `2023-12-31` (Strictly observed).
*   **Target Data**: `2024-01-02` to `2024-12-01` (Strictly hidden during feature calculation).

**Verified By**: `scripts/generation/generate_temporal_dataset.py` logic:
```python
hist_features = hist[hist.index < cutoff_date]  # Input
hist_future = hist[hist.index >= cutoff_date]   # Verification Target
```

## 3. Preprocessing & Feature Engineering
All features are point-in-time metrics calculated relative to the `Close` price at the Cutoff Date.

| Feature | Description | Calculation |
| :--- | :--- | :--- |
| **RSI** | Relative Strength Index (14-day) | Momentum oscillator to detect overbought/oversold. |
| **Trend Strength** | ADX / SMA Slope | Measures the robustness of the current price trend. |
| **Volatility** | Annualized Std Dev | `std(daily_returns) * sqrt(252)` |
| **Price vs SMA200** | Deviation from Long-Term Mean | `(Price - SMA200) / SMA200` |
| **Volume Ratio** | Relative Volume | `Current Volume / 30-Day Avg Volume` |

## 4. Handling Missing Data
*   **Method**: Strict Drop.
*   **Rule**: Any stock with < 200 days of history prior to Cutoff or < 20 days of history after Cutoff is excluded.
*   **Imputation**: None. No synthetic data is used to fill gaps to ensure realistic testing.

## 5. Target Variable
*   **Actual Return**: Percentage change from `Close` at Cutoff (`2024-01-01`) to `Close` at Target (`2024-12-01` or latest available).

## 6. Reproducibility
To regenerate the exact dataset used in the thesis:
```bash
python scripts/generation/generate_temporal_dataset.py
```
This will produce `results/datasets/dataset_temporal_valid.csv`.
