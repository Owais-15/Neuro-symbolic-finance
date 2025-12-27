"""
Train Final ML Model on Enhanced Dataset
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.ml_predictor import StockReturnPredictor
import pandas as pd

# Load enhanced dataset
df = pd.read_csv('results/enhanced_dataset_v3_full.csv')

print(f"Dataset: {len(df)} stocks, {len(df.columns)} features\n")

# Train model
predictor = StockReturnPredictor()
results = predictor.train(df, cv_splits=5)

# Save model
predictor.save('models/final_model_v3.pkl')

# Print final results
print("\n" + "="*80)
print("FINAL ML MODEL RESULTS")
print("="*80)
print(f"Correlation (r): {results['final_correlation']:.4f}")
print(f"P-value: {results['final_p_value']:.6f}")
print(f"R²: {results['final_r2']:.4f}")
print("="*80)
