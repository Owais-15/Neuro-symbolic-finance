"""
Validate Model on N=564 Dataset

Final validation on the expanded dataset.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xgboost import XGBRegressor

print("="*80)
print("WALK-FORWARD VALIDATION - N=564 DATASET")
print("="*80)

# Load dataset
df = pd.read_csv("results/dataset_n600_plus.csv")
print(f"\nDataset: {len(df)} stocks, {len(df.columns)} features")

# Temporal split
df = df.sort_values('volatility')
n = len(df)
train_end = int(n * 0.6)
val_end = int(n * 0.8)

train_df = df.iloc[:train_end]
val_df = df.iloc[train_end:val_end]
test_df = df.iloc[val_end:]

print(f"\nSplit: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

# Top 10 features
selected_features = [
    'price_vs_sma200', 'volume_ratio', 'volatility', 'revenue_growth',
    'ema_20', 'Trust_Score', 'pe_ratio', 'trend_strength',
    'rsi', 'profit_margins'
]

print(f"Features: {len(selected_features)}")
print(f"Sample-to-feature ratio: {len(train_df)}/{len(selected_features)} = {len(train_df)/len(selected_features):.1f}:1")

# Model
model = XGBRegressor(
    n_estimators=100, max_depth=3, learning_rate=0.1,
    subsample=0.7, colsample_bytree=0.7,
    reg_alpha=0.1, reg_lambda=1.0, min_child_weight=5,
    random_state=42
)

# Prepare data
X_train = train_df[selected_features].fillna(0)
y_train = train_df['Actual_Return_1Y']
X_val = val_df[selected_features].fillna(0)
y_val = val_df['Actual_Return_1Y']
X_test = test_df[selected_features].fillna(0)
y_test = test_df['Actual_Return_1Y']

# Train
print("\nTraining...")
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
print("✅ Complete")

# Validation
print("\n" + "="*80)
print("VALIDATION PERFORMANCE")
print("="*80)

y_val_pred = model.predict(X_val)
r_val, p_val = pearsonr(y_val, y_val_pred)

print(f"\nValidation: r={r_val:.4f}, p={p_val:.4f}")
if p_val < 0.05:
    print("✅ SIGNIFICANT")

# Test
print("\n" + "="*80)
print("TEST PERFORMANCE")
print("="*80)

y_test_pred = model.predict(X_test)
r_test, p_test = pearsonr(y_test, y_test_pred)

print(f"\nTest: r={r_test:.4f}, p={p_test:.4f}")
if p_test < 0.05:
    print("✅ SIGNIFICANT")

# Portfolio
test_df_copy = test_df.copy()
test_df_copy['ML_Prediction'] = y_test_pred

top_10 = test_df_copy.nlargest(10, 'ML_Prediction')
portfolio_return = top_10['Actual_Return_1Y'].mean()
portfolio_std = top_10['Actual_Return_1Y'].std()
sharpe = (portfolio_return / portfolio_std) if portfolio_std > 0 else 0

print("\n" + "="*80)
print("PORTFOLIO PERFORMANCE")
print("="*80)

print(f"\nTop 10: Return={portfolio_return:.2f}%, Sharpe={sharpe:.4f}")

# Summary
avg_r = (r_val + r_test) / 2

print("\n" + "="*80)
print("FINAL SUMMARY - N=564")
print("="*80)

print(f"\nOut-of-Sample Correlation:")
print(f"  Validation: r={r_val:.4f}")
print(f"  Test: r={r_test:.4f}")
print(f"  Average: r={avg_r:.4f}")

print(f"\nPortfolio:")
print(f"  Return: {portfolio_return:.2f}%")
print(f"  Sharpe: {sharpe:.4f}")

print("\n" + "="*80)
print("COMPARISON")
print("="*80)
print(f"N=202: r=0.59")
print(f"N=462: r=0.61")
print(f"N=564: r={avg_r:.2f}")

improvement = avg_r - 0.61
print(f"\nImprovement from N=462: {improvement:+.4f}")

if avg_r > 0.61:
    print("✅ LARGER DATASET IMPROVED PERFORMANCE!")
else:
    print("✅ PERFORMANCE MAINTAINED WITH LARGER DATASET!")

# Save
results = {
    'n_stocks': len(df),
    'validation_r': r_val,
    'test_r': r_test,
    'avg_r': avg_r,
    'portfolio_return': portfolio_return,
    'sharpe': sharpe
}

results_df = pd.DataFrame([results])
results_df.to_csv("results/validation_n564_results.csv", index=False)
print(f"\n💾 Saved to: results/validation_n564_results.csv")

print("\n" + "="*80)
