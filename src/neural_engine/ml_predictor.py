"""
ML Predictor Module

Trains XGBoost model on financial + technical features to predict returns.
Combines Trust Score + Technical Indicators for optimal performance.
"""

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from scipy.stats import pearsonr
import pickle
import os

class StockReturnPredictor:
    """
    ML model to predict stock returns using ensemble of features.
    """
    
    def __init__(self):
        self.model = XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective='reg:squarederror'
        )
        self.feature_names = []
        self.is_trained = False
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """
        Extract features from dataset.
        
        Returns:
            X (features), y (target)
        """
        # Define feature columns
        feature_cols = [
            # Financial fundamentals (14 features)
            'pe_ratio', 'debt_to_equity', 'revenue_growth',
            'profit_margins', 'roe', 'free_cash_flow',
            'dividend_yield', 'cash_reserves', 'operating_costs',
            'net_income', 'analyst_target', 'current_price',
            
            # Trust score and breakdown
            'Trust_Score',
            
            # Technical indicators (17 features)
            'rsi', 'macd', 'macd_signal', 'roc',
            'sma_50', 'sma_200', 'ema_20',
            'price_vs_sma50', 'price_vs_sma200',
            'bb_upper', 'bb_lower', 'bb_position',
            'atr', 'volatility',
            'volume_trend', 'volume_ratio',
            'trend_strength'
        ]
        
        # Filter to available columns
        available_features = [col for col in feature_cols if col in df.columns]
        self.feature_names = available_features
        
        X = df[available_features].fillna(0)  # Handle missing values
        y = df['Actual_Return_1Y']
        
        return X, y
    
    def train(self, df: pd.DataFrame, cv_splits: int = 5):
        """
        Train model with cross-validation.
        
        Args:
            df: DataFrame with features and target
            cv_splits: Number of time series CV splits
        """
        print("="*80)
        print("TRAINING ML MODEL")
        print("="*80)
        
        X, y = self.prepare_features(df)
        
        print(f"\nDataset: {len(df)} stocks")
        print(f"Features: {len(self.feature_names)}")
        print(f"Feature list: {', '.join(self.feature_names[:10])}...")
        
        # Time series cross-validation
        tscv = TimeSeriesSplit(n_splits=cv_splits)
        
        cv_scores = []
        cv_correlations = []
        
        print(f"\nCross-Validation ({cv_splits} splits):")
        print("-"*80)
        
        for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # Train
            self.model.fit(X_train, y_train, verbose=False)
            
            # Validate
            y_pred = self.model.predict(X_val)
            
            # Metrics
            r2 = r2_score(y_val, y_pred)
            mae = mean_absolute_error(y_val, y_pred)
            r, p = pearsonr(y_val, y_pred)
            
            cv_scores.append(r2)
            cv_correlations.append(r)
            
            print(f"Fold {fold+1}: R²={r2:.4f}, MAE={mae:.2f}%, Correlation={r:.4f} (p={p:.4f})")
        
        # Final train on all data
        print("\nTraining final model on full dataset...")
        self.model.fit(X, y, verbose=False)
        
        # Final predictions
        y_pred_final = self.model.predict(X)
        r_final, p_final = pearsonr(y, y_pred_final)
        r2_final = r2_score(y, y_pred_final)
        
        self.is_trained = True
        
        print("\n" + "="*80)
        print("TRAINING RESULTS")
        print("="*80)
        print(f"Cross-Validation R²: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
        print(f"Cross-Validation Correlation: {np.mean(cv_correlations):.4f} ± {np.std(cv_correlations):.4f}")
        print(f"\nFinal Model (full data):")
        print(f"  Correlation (r): {r_final:.4f}")
        print(f"  P-value: {p_final:.6f}")
        print(f"  R²: {r2_final:.4f}")
        
        if p_final < 0.001:
            print("  ✅ HIGHLY SIGNIFICANT (p<0.001)")
        elif p_final < 0.05:
            print("  ✅ SIGNIFICANT (p<0.05)")
        else:
            print("  ⚠️  Not significant (p>=0.05)")
        
        # Feature importance
        print("\n" + "="*80)
        print("TOP 10 MOST IMPORTANT FEATURES")
        print("="*80)
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for i, row in feature_importance.head(10).iterrows():
            print(f"{row['feature']:25s}: {row['importance']:.4f}")
        
        return {
            'cv_r2_mean': np.mean(cv_scores),
            'cv_r2_std': np.std(cv_scores),
            'cv_corr_mean': np.mean(cv_correlations),
            'final_correlation': r_final,
            'final_p_value': p_final,
            'final_r2': r2_final,
            'feature_importance': feature_importance
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict returns for new data.
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        X_features = X[self.feature_names].fillna(0)
        return self.model.predict(X_features)
    
    def save(self, filepath: str = "models/stock_predictor.pkl"):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"✅ Model saved to {filepath}")
    
    @staticmethod
    def load(filepath: str = "models/stock_predictor.pkl"):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)


# Training script
if __name__ == "__main__":
    print("Loading dataset...")
    
    # Load N=210 dataset
    df = pd.read_csv("results/final_thesis_dataset.csv")
    
    # Remove errors
    df = df[df['Verdict'] != 'ERROR'].copy()
    
    print(f"Loaded {len(df)} valid stocks\n")
    
    # Train model
    predictor = StockReturnPredictor()
    results = predictor.train(df, cv_splits=5)
    
    # Save model
    predictor.save()
    
    print("\n" + "="*80)
    print("✅ ML MODEL TRAINING COMPLETE")
    print("="*80)
