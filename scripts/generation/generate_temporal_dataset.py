"""
STRICT TEMPORAL DATASET GENERATOR

Addresses Gemini's "Time Travel" critique.
Generates a dataset where:
1. Features are calculated strictly BEFORE the cutoff date.
2. Targets are calculated strictly AFTER the cutoff date.

Usage:
    python scripts/generate_temporal_dataset.py
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.technical_indicators import (
    calculate_rsi, calculate_macd, calculate_roc, 
    calculate_bollinger_bands, calculate_atr, 
    calculate_volume_trend, calculate_trend_strength
)

# Configuration
CUTOFF_DATE = "2024-01-01"
TARGET_END_DATE = "2024-12-01"  # 11 months later for return
STOCK_LIST_FILE = "data/sp500_tickers.csv"
OUTPUT_FILE = "results/datasets/dataset_temporal_valid.csv"

def get_temporal_data(symbol, cutoff_date):
    """
    Fetch data and calculate features strictly at the cutoff date.
    Returns: (features_dict, actual_return)
    """
    try:
        # Fetch data: 1 year before cutoff (for indicators) to 1 year after (for target)
        start_date = (datetime.strptime(cutoff_date, "%Y-%m-%d") - timedelta(days=400)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Download OHLCV
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=end_date)
        
        if len(hist) < 200:
            return None, None
            
        # --- SPLIT DATA ---
        # Data available for decision making (Up to Cutoff)
        hist_features = hist[hist.index < cutoff_date].copy()
        
        # Data for verification (After Cutoff)
        hist_future = hist[hist.index >= cutoff_date].copy()
        
        if len(hist_features) < 50 or len(hist_future) < 20:
            return None, None
            
        # --- CALCULATE FEATURES (Strictly Past Data) ---
        features = {}
        
        # Price at decision time (Cutoff)
        price_at_cutoff = hist_features['Close'].iloc[-1]
        
        # Valid Technicals
        features['rsi'] = calculate_rsi(hist_features['Close'])
        features['macd'], features['macd_signal'] = calculate_macd(hist_features['Close'])
        features['roc'] = calculate_roc(hist_features['Close'])
        
        # Moving Averages relative to Cutoff Price
        sma50 = hist_features['Close'].rolling(50).mean().iloc[-1]
        sma200 = hist_features['Close'].rolling(200).mean().iloc[-1]
        
        features['price_vs_sma50'] = (price_at_cutoff - sma50) / sma50 * 100
        features['price_vs_sma200'] = (price_at_cutoff - sma200) / sma200 * 100
        
        # Volatility
        features['volatility'] = hist_features['Close'].pct_change().std() * np.sqrt(252) * 100
        
        # Trend
        features['trend_strength'] = calculate_trend_strength(hist_features['Close'])
        
        # --- CALCULATE TARGET (Strictly Future Data) ---
        # Return from Cutoff to Target End Date (or latest available)
        # We find the price closest to TARGET_END_DATE
        future_mask = hist_future.index <= TARGET_END_DATE
        if not future_mask.any():
            return None, None
            
        price_future = hist_future.loc[future_mask, 'Close'].iloc[-1]
        
        actual_return = ((price_future - price_at_cutoff) / price_at_cutoff) * 100
        
        # Metadata
        features['Symbol'] = symbol
        features['Close_Cutoff'] = price_at_cutoff
        features['Close_Future'] = price_future
        features['Actual_Return'] = actual_return
        
        return features, actual_return

    except Exception as e:
        # print(f"Error {symbol}: {e}")
        return None, None

def main():
    print(f"🚀 GENERATING TEMPORAL DATASET")
    print(f"📅 Cutoff Date (Decision Time): {CUTOFF_DATE}")
    print(f"📅 Target Date (Outcome Time):  {TARGET_END_DATE}")
    print("="*60)
    
    # Load tickers
    try:
        df_tickers = pd.read_csv(STOCK_LIST_FILE)
        tickers = df_tickers['ticker'].tolist() 
    except:
        print("Using limited ticker list for test...")
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AMD", "INTC", "IBM"]
    
    dataset = []
    
    print(f"Processing {len(tickers)} stocks...")
    
    for i, symbol in enumerate(tickers):
        if i % 10 == 0:
            print(f"Processing {i}/{len(tickers)}...", end="\r")
            
        features, target = get_temporal_data(symbol, CUTOFF_DATE)
        
        if features:
            dataset.append(features)
            
    print(f"\n✅ Completed. Valid samples: {len(dataset)}")
    
    if len(dataset) > 0:
        df_out = pd.DataFrame(dataset)
        df_out.to_csv(OUTPUT_FILE, index=False)
        print(f"💾 Saved to {OUTPUT_FILE}")
        
        # Quick Stats
        print("\n📊 DATASET STATS (REALITY CHECK)")
        print(f"Mean Return: {df_out['Actual_Return'].mean():.2f}%")
        print(f"Corr (RSI vs Return): {df_out['rsi'].corr(df_out['Actual_Return']):.4f}")
        print(f"Corr (Trend vs Return): {df_out['trend_strength'].corr(df_out['Actual_Return']):.4f}")
        
    else:
        print("❌ No valid data generated.")

if __name__ == "__main__":
    main()
