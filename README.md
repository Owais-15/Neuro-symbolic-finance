# 🧠 Neuro-Symbolic Stock Predictor

> **"Financial AI that prioritizes explainability & risk control."**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Defense](https://img.shields.io/badge/Defense-Verified-green)](docs/defense_report.md)
[![Correlation](https://img.shields.io/badge/Correlation-r%3D0.25-orange)](results/figures/01_predictive_power.png)
[![Structure](https://img.shields.io/badge/Layout-Open%20Source-blueviolet)](scripts/verify_project_integrity.py)

A hybrid AI system combining **Machine Learning (XGBoost)** with **Symbolic Reasoning (Financial Rules)** to predict stock returns. We aim to mitigate "black box" risks by implementing a **transparent filtering layer** validated against historical solvency failures.

---

| Model | Mean Return | Std Dev | Sharpe | 95% CI (Mean) |
|-------|-------------|---------|--------|---------------|
| **Market (Buy & Hold)** | **21.2%** | 51.4% | 0.41 | [16.9%, 25.9%] |
| **Random Guesser** | **19.7%** | 41.5% | 0.47 | [14.8%, 25.4%] |
| **Heuristic (RSI)** | **18.0%** | 45.6% | 0.40 | [12.3%, 23.9%] |
| **Neuro-Symbolic (Proj)**| **44.6%** | 72.4% | 0.62 | [30.4%, 60.1%] |

*Note: N=1000 Bootstrap Samples. "Neuro-Symbolic" is a projected estimate based on XGBoost top-decile performance.*

### 1. Predictive Power
![Predictive Power](results/figures/01_predictive_power.png)
*Figure 1: Actual vs Predicted Returns (N=461 Stocks). A clear, positive trend confirms the signal is real.*

### 2. Model Comparison
![Model Comparison](results/figures/03_model_comparison.png)
*Figure 2: Our Neuro-Symbolic Approach (r=0.28) outperforms Pure Rules, Heuristics, and Pure LLMs.*
*See [Baselines Methodology](docs/BASELINES.md) for model details.*

---

## 🛠️ Installation & Usage

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/neuro-symbolic-finance
cd neuro-symbolic-finance
pip install -r requirements.txt
```

### 2. Reproduction Guide (Manual verification)
Follow these steps to reproduce our results from scratch, similar to verifying a scientific paper.

**Step A: Generate the Dataset**
Validate the sourcing and temporal splitting logic.
```bash
# Sourcing: Yahoo Finance | Cutoff: 2024-01-01
python scripts/generation/generate_temporal_dataset.py
```
*See [Data Provenance](docs/DATA_PROVENANCE.md) for details on splits and feature engineering.*

**Step B: Run Safety Validation (The Graveyard Test)**
Verify the system correctly rejects historical failures (SVB, WeWork).
```bash
python scripts/validation/validate_tier2.py
```
*Expected Output: `🏆 GRAVEYARD RESULT: 4/4 Threats Neutralized`*

**Step C: Generate Thesis Artifacts**
Reproduce the r=0.25 correlation and model comparison charts.
```bash
python scripts/generation/generate_thesis_charts.py
```
*Artifacts saved to `results/figures/`.*

### 3. Quick Start (Inference Demo)
See the prediction pipeline (Data -> Rules -> ML -> Verdict) in action:
```bash
python scripts/demo_inference.py
```

### 4. Interactive Dashboard
Explore the verified results visually:
```bash
streamlit run app/dashboard.py
```

---

## 📂 Open-Source Structure

Professional layout designed for reproducibility:

```
Neuro_Symbolic_Thesis/
├── app/                  # Streamlit Web Dashboard
├── src/                  # Core Engine (ML + Rules)
├── scripts/              
│   ├── generation/       # Dataset Generation
│   ├── validation/       # Rigorous Testing (Graveyard)
│   └── analysis/         # Model Comparison
├── results/              
│   ├── figures/          # Publication Charts (01-05)
│   └── datasets/         # Validated Temporal Data
└── docs/                 # Methodology & Defense
```

---

## 🔬 Methodology

1.  **Strict Temporal Split**: Training on pre-2023 data, testing on post-Jan 2024. **Zero data leakage.**
2.  **Hybrid Engine**: 
    - **Symbolic**: Rejects high-risk stocks (e.g., Debt/Equity > 2.0).
    - **Neural**: Ranks remaining stocks by upside potential.
3.  **Graveyard Test**: System explicitly validated on bankrupt companies to ensure safety.

---

## ⚠️ Limitations & Constraints

To ensure rigorous transparency, we disclose the following limitations:

1.  **Market Regime Dependence**: Validation data (2024) represents a Bull Market. Performance in Bear Markets (e.g., 2008, 2022) remains unverified.
2.  **Transaction Costs**: Returns reported are gross returns. Real-world implementation must account for spread, slippage, and fees.
3.  **Universe Bias**: Tested primarily on S&P 500. Small-cap liquidity risks are not modeled.
4.  **Inference Latency**: The Symbolic+LLM pipeline introduces ~2s latency per stock.

---

## � License & Citation

**MIT License** - Free for research and commercial use.

**Author**: Admin
**Thesis**: "Neuro-Symbolic AI for Financial Time-Series Prediction"
