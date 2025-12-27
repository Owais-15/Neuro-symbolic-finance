"""
Portfolio Backtesting & Performance Analysis

Simulates actual portfolio performance using ML predictions.
Calculates Sharpe ratio, alpha, and compares to baselines.
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.ml_predictor import StockReturnPredictor

# Load data and model
df = pd.read_csv("results/enhanced_dataset_v3_full.csv")
predictor = StockReturnPredictor.load("models/final_model_v3.pkl")

print("="*80)
print("PORTFOLIO BACKTESTING & PERFORMANCE ANALYSIS")
print("="*80)

# Get ML predictions
X = df[predictor.feature_names].fillna(0)
df['ML_Prediction'] = predictor.predict(X)

print(f"\nDataset: {len(df)} stocks")
print(f"Features used: {len(predictor.feature_names)}")

# === STRATEGY 1: TOP 20 STOCKS BY ML PREDICTION ===
print("\n" + "="*80)
print("STRATEGY 1: TOP 20 STOCKS (ML PREDICTIONS)")
print("="*80)

top_20 = df.nlargest(20, 'ML_Prediction')
portfolio_return = top_20['Actual_Return_1Y'].mean()
portfolio_std = top_20['Actual_Return_1Y'].std()
sharpe_ratio = (portfolio_return / portfolio_std) * np.sqrt(1) if portfolio_std > 0 else 0

print(f"\nPortfolio Performance:")
print(f"  Average Return: {portfolio_return:.2f}%")
print(f"  Std Deviation: {portfolio_std:.2f}%")
print(f"  Sharpe Ratio: {sharpe_ratio:.4f}")
print(f"  Win Rate: {(top_20['Actual_Return_1Y'] > 0).sum() / len(top_20) * 100:.1f}%")
print(f"  Max Return: {top_20['Actual_Return_1Y'].max():.2f}%")
print(f"  Min Return: {top_20['Actual_Return_1Y'].min():.2f}%")

# === STRATEGY 2: TOP 20 STOCKS BY TRUST SCORE ===
print("\n" + "="*80)
print("STRATEGY 2: TOP 20 STOCKS (TRUST SCORE)")
print("="*80)

top_20_trust = df.nlargest(20, 'Trust_Score')
trust_return = top_20_trust['Actual_Return_1Y'].mean()
trust_std = top_20_trust['Actual_Return_1Y'].std()
trust_sharpe = (trust_return / trust_std) * np.sqrt(1) if trust_std > 0 else 0

print(f"\nPortfolio Performance:")
print(f"  Average Return: {trust_return:.2f}%")
print(f"  Std Deviation: {trust_std:.2f}%")
print(f"  Sharpe Ratio: {trust_sharpe:.4f}")
print(f"  Win Rate: {(top_20_trust['Actual_Return_1Y'] > 0).sum() / len(top_20_trust) * 100:.1f}%")

# === BASELINE: RANDOM 20 STOCKS ===
print("\n" + "="*80)
print("BASELINE: RANDOM 20 STOCKS (MARKET)")
print("="*80)

np.random.seed(42)
random_20 = df.sample(20)
random_return = random_20['Actual_Return_1Y'].mean()
random_std = random_20['Actual_Return_1Y'].std()
random_sharpe = (random_return / random_std) * np.sqrt(1) if random_std > 0 else 0

print(f"\nPortfolio Performance:")
print(f"  Average Return: {random_return:.2f}%")
print(f"  Std Deviation: {random_std:.2f}%")
print(f"  Sharpe Ratio: {random_sharpe:.4f}")
print(f"  Win Rate: {(random_20['Actual_Return_1Y'] > 0).sum() / len(random_20) * 100:.1f}%")

# === BASELINE: EQUAL WEIGHT ALL STOCKS ===
print("\n" + "="*80)
print("BASELINE: EQUAL WEIGHT ALL STOCKS")
print("="*80)

market_return = df['Actual_Return_1Y'].mean()
market_std = df['Actual_Return_1Y'].std()
market_sharpe = (market_return / market_std) * np.sqrt(1) if market_std > 0 else 0

print(f"\nMarket Performance:")
print(f"  Average Return: {market_return:.2f}%")
print(f"  Std Deviation: {market_std:.2f}%")
print(f"  Sharpe Ratio: {market_sharpe:.4f}")
print(f"  Win Rate: {(df['Actual_Return_1Y'] > 0).sum() / len(df) * 100:.1f}%")

# === COMPARISON & STATISTICAL TESTING ===
print("\n" + "="*80)
print("PERFORMANCE COMPARISON")
print("="*80)

comparison = pd.DataFrame({
    'Strategy': ['ML Top 20', 'Trust Top 20', 'Random 20', 'Market (All)'],
    'Return (%)': [portfolio_return, trust_return, random_return, market_return],
    'Sharpe Ratio': [sharpe_ratio, trust_sharpe, random_sharpe, market_sharpe],
    'Std Dev (%)': [portfolio_std, trust_std, random_std, market_std]
})

print("\n", comparison.to_string(index=False))

# Statistical significance test
t_stat, p_value = ttest_ind(top_20['Actual_Return_1Y'], random_20['Actual_Return_1Y'])

print("\n" + "="*80)
print("STATISTICAL SIGNIFICANCE")
print("="*80)
print(f"\nML Top 20 vs Random 20:")
print(f"  T-statistic: {t_stat:.4f}")
print(f"  P-value: {p_value:.4f}")

if p_value < 0.05:
    print("  ✅ STATISTICALLY SIGNIFICANT (p<0.05)")
    print("  → ML strategy significantly outperforms random selection")
else:
    print("  ⚠️  Not statistically significant (p>=0.05)")

# Alpha calculation
alpha_ml = portfolio_return - market_return
alpha_trust = trust_return - market_return

print("\n" + "="*80)
print("ALPHA GENERATION")
print("="*80)
print(f"\nML Strategy Alpha: {alpha_ml:+.2f}% vs Market")
print(f"Trust Strategy Alpha: {alpha_trust:+.2f}% vs Market")

if alpha_ml > 5:
    print("✅ ML strategy generates significant alpha (>5%)")
elif alpha_ml > 0:
    print("✅ ML strategy generates positive alpha")
else:
    print("⚠️  ML strategy underperforms market")

# === FINAL VERDICT ===
print("\n" + "="*80)
print("FINAL VERDICT")
print("="*80)

print(f"\n✅ Sharpe Ratio: {sharpe_ratio:.4f}", end="")
if sharpe_ratio > 1.5:
    print(" (EXCEEDS TARGET >1.5)")
elif sharpe_ratio > 1.0:
    print(" (GOOD, >1.0)")
elif sharpe_ratio > 0.5:
    print(" (MODERATE)")
else:
    print(" (NEEDS IMPROVEMENT)")

print(f"✅ Alpha: {alpha_ml:+.2f}%", end="")
if alpha_ml > 10:
    print(" (EXCELLENT)")
elif alpha_ml > 5:
    print(" (GOOD)")
elif alpha_ml > 0:
    print(" (POSITIVE)")
else:
    print(" (NEGATIVE)")

print(f"✅ Statistical Significance: p={p_value:.4f}", end="")
if p_value < 0.05:
    print(" (SIGNIFICANT)")
else:
    print(" (NOT SIGNIFICANT)")

# Save results
comparison.to_csv("results/portfolio_backtest_results.csv", index=False)
print(f"\n💾 Results saved to results/portfolio_backtest_results.csv")

print("\n" + "="*80)
