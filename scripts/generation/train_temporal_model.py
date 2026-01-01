"""
Train Temporal Model (Strict Validation)

Trains an XGBoost model on the temporally valid dataset (dataset_temporal_valid.csv).
Uses only technical indicators (no fundamentals) to ensure zero leakage.
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import sys
import os

# Configuration
DATASET_FILE = "results/datasets/dataset_temporal_valid.csv"

def train_temporal_model():
    print("🚀 TRAINING STRICT TEMPORAL MODEL")
    
    # Load data
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Dataset not found: {DATASET_FILE}")
        return
        
    df = pd.read_csv(DATASET_FILE)
    print(f"Loaded {len(df)} samples")
    
    # Features
    feature_cols = [
        'rsi', 'macd', 'macd_signal', 'roc', 
        'price_vs_sma50', 'price_vs_sma200', 
        'volatility', 'trend_strength'
    ]
    
    X = df[feature_cols]
    y = df['Actual_Return']
    
    # XGBoost Regressor
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    
    # Cross Validation (5-Fold)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    # Metrics: R2 (Coefficient of Determination) - proxies for "explained variance"
    # Note: R2 is related to correlation squared, but can be negative for bad models
    r2_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
    
    print("\n📊 CV RESULTS (5-Fold):")
    print(f"  Mean R²: {r2_scores.mean():.4f}")
    print(f"  Std R²:  {r2_scores.std():.4f}")
    
    # Train final model to get feature importance
    model.fit(X, y)
    
    # Calculate Correlation on Training Set (Upper Bound)
    preds = model.predict(X)
    corr = np.corrcoef(y, preds)[0, 1]
    
    print(f"\n📈 TRAINING FIT:")
    print(f"  Correlation (In-Sample): {corr:.4f}")
    
    if corr < 0.2:
        print("\n⚠️  WARNING: Even in-sample correlation is low.")
        print("    This suggests technicals alone have very little 1-year predictive power.")
    
    # Feature Importance
    print("\n🔑 FEATURE IMPORTANCE:")
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(importances)
    
    return r2_scores.mean(), corr

if __name__ == "__main__":
    train_temporal_model()
