"""
Train Model on N=462 Dataset

Tests performance improvement with larger dataset.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.ml_predictor import StockReturnPredictor
import pandas as pd

print("="*80)
print("TRAINING MODEL ON N=462 DATASET")
print("="*80)

# Load dataset
print("\nLoading N=462 dataset...")
df = pd.read_csv('results/dataset_n500_enhanced.csv')
print(f"Dataset: {len(df)} stocks, {len(df.columns)} features")

# Train model
print("\nTraining XGBoost model with 5-fold cross-validation...")
predictor = StockReturnPredictor()
results = predictor.train(df, cv_splits=5)

# Save model
predictor.save('models/final_model_n462.pkl')

# Print final results
print("\n" + "="*80)
print("FINAL RESULTS - N=462 DATASET")
print("="*80)
print(f"\nCorrelation (r): {results['final_correlation']:.4f}")
print(f"P-value: {results['final_p_value']:.6f}")
print(f"R²: {results['final_r2']:.4f}")

# Compare to N=202
print("\n" + "="*80)
print("COMPARISON: N=462 vs N=202")
print("="*80)
print(f"N=202 (previous): r=0.9998 (training, overfitted)")
print(f"N=202 (validated): r=0.59 (out-of-sample)")
print(f"N=462 (current):   r={results['final_correlation']:.4f} (training)")

if results['final_correlation'] > 0.60:
    print("\n✅ IMPROVEMENT! Larger dataset improved performance!")
elif results['final_correlation'] > 0.55:
    print("\n✅ GOOD! Performance maintained with larger dataset!")
else:
    print("\n⚠️  Performance similar - need walk-forward validation")

print("\n" + "="*80)
