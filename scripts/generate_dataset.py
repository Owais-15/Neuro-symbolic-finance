"""
N=500+ Dataset Generator with Parallel Processing

Efficiently fetches data for 500+ stocks using parallel processing
with rate limiting and error handling.
"""

import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from orchestrator.data_loader import get_real_stock_data, get_historical_price
from orchestrator.main import run_analysis

# Load stock list
STOCK_LIST_FILE = "data/sp500_tickers.csv"
RESULTS_FILE = "results/dataset_n500_enhanced.csv"
MAX_WORKERS = 10  # Parallel threads
RATE_LIMIT_DELAY = 0.2  # Seconds between requests

def load_stock_list():
    """Load stock tickers from CSV"""
    try:
        df = pd.read_csv(STOCK_LIST_FILE)
        tickers = df['ticker'].tolist()
        print(f"✅ Loaded {len(tickers)} tickers from {STOCK_LIST_FILE}")
        return tickers
    except Exception as e:
        print(f"❌ Error loading stock list: {e}")
        return []

def process_single_stock(symbol, index, total):
    """
    Process a single stock: fetch data, run analysis, calculate returns.
    
    Args:
        symbol: Stock ticker
        index: Current index (for progress tracking)
        total: Total number of stocks
    
    Returns:
        dict: Stock data with all features and analysis
    """
    try:
        print(f"[{index}/{total}] Processing {symbol}...", end=" ")
        
        # Get enhanced data (includes technical indicators)
        raw_data = get_real_stock_data(symbol)
        
        if raw_data["current_price"] == 0.0:
            print("⚠️  SKIP (no data)")
            return None
        
        # Run analysis
        analysis = run_analysis(symbol)
        
        # Get historical price
        hist_price = get_historical_price(symbol, days_ago=365)
        current_price = raw_data["current_price"]
        
        if hist_price > 0:
            actual_return = ((current_price - hist_price) / hist_price) * 100
        else:
            actual_return = 0.0
        
        # Combine all data
        result = {
            'Symbol': symbol,
            'Trust_Score': analysis['trust_score'],
            'Verdict': analysis['verdict'],
            'Current_Price': current_price,
            'Actual_Return_1Y': actual_return,
            
            # Financial metrics (14)
            'pe_ratio': raw_data.get('pe_ratio', 0),
            'debt_to_equity': raw_data.get('debt_to_equity', 0),
            'revenue_growth': raw_data.get('revenue_growth', 0),
            'profit_margins': raw_data.get('profit_margins', 0),
            'roe': raw_data.get('roe', 0),
            'free_cash_flow': raw_data.get('free_cash_flow', 0),
            'dividend_yield': raw_data.get('dividend_yield', 0),
            'cash_reserves': raw_data.get('cash_reserves', 0),
            'operating_costs': raw_data.get('operating_costs', 0),
            'net_income': raw_data.get('net_income', 0),
            'analyst_target': raw_data.get('analyst_target', 0),
            'current_price': raw_data.get('current_price', 0),
            'sector': raw_data.get('sector', 'Unknown'),
            
            # Technical indicators (17)
            'rsi': raw_data.get('rsi', 50),
            'macd': raw_data.get('macd', 0),
            'macd_signal': raw_data.get('macd_signal', 0),
            'roc': raw_data.get('roc', 0),
            'sma_50': raw_data.get('sma_50', 0),
            'sma_200': raw_data.get('sma_200', 0),
            'ema_20': raw_data.get('ema_20', 0),
            'price_vs_sma50': raw_data.get('price_vs_sma50', 0),
            'price_vs_sma200': raw_data.get('price_vs_sma200', 0),
            'bb_upper': raw_data.get('bb_upper', 0),
            'bb_lower': raw_data.get('bb_lower', 0),
            'bb_position': raw_data.get('bb_position', 0.5),
            'atr': raw_data.get('atr', 0),
            'volatility': raw_data.get('volatility', 0),
            'volume_trend': raw_data.get('volume_trend', 0),
            'volume_ratio': raw_data.get('volume_ratio', 1.0),
            'trend_strength': raw_data.get('trend_strength', 0)
        }
        
        print(f"✅ Trust:{analysis['trust_score']:.0f}, Return:{actual_return:.1f}%, RSI:{raw_data.get('rsi', 0):.0f}")
        
        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def process_stocks_parallel(symbols, max_workers=MAX_WORKERS):
    """
    Process multiple stocks in parallel with progress tracking.
    
    Args:
        symbols: List of stock tickers
        max_workers: Number of parallel threads
    
    Returns:
        list: List of processed stock data
    """
    results = []
    total = len(symbols)
    
    print(f"\n🚀 Starting parallel processing of {total} stocks...")
    print(f"Workers: {max_workers}, Rate limit: {RATE_LIMIT_DELAY}s")
    print("="*80)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_symbol = {
            executor.submit(process_single_stock, symbol, i+1, total): symbol
            for i, symbol in enumerate(symbols)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"❌ Exception for {symbol}: {e}")
    
    elapsed_time = time.time() - start_time
    
    print("="*80)
    print(f"✅ Processing complete!")
    print(f"Time elapsed: {elapsed_time/60:.1f} minutes")
    print(f"Successful: {len(results)}/{total} stocks ({len(results)/total*100:.1f}%)")
    print(f"Average: {elapsed_time/total:.1f} seconds per stock")
    
    return results

def save_dataset(results, filename=RESULTS_FILE):
    """
    Save processed data to CSV.
    
    Args:
        results: List of stock data dictionaries
        filename: Output filename
    """
    df = pd.DataFrame(results)
    
    # Sort by Trust_Score descending
    df = df.sort_values('Trust_Score', ascending=False)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"\n💾 Dataset saved to: {filename}")
    print(f"Total stocks: {len(df)}")
    print(f"Features: {len(df.columns)} columns")
    
    # Quick statistics
    print(f"\n📊 Quick Statistics:")
    print(f"  Average Return: {df['Actual_Return_1Y'].mean():.2f}%")
    print(f"  Median Return: {df['Actual_Return_1Y'].median():.2f}%")
    print(f"  Std Dev: {df['Actual_Return_1Y'].std():.2f}%")
    print(f"  Win Rate: {(df['Actual_Return_1Y'] > 0).sum() / len(df) * 100:.1f}%")
    
    # Verdict distribution
    print(f"\n📋 Verdict Distribution:")
    print(df['Verdict'].value_counts())
    
    return df

def main():
    """Main execution function"""
    print("="*80)
    print("N=500+ DATASET GENERATION")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load stock list
    symbols = load_stock_list()
    
    if not symbols:
        print("❌ No stocks to process. Exiting.")
        return
    
    print(f"\nTarget: {len(symbols)} stocks")
    print(f"Estimated time: {len(symbols) * RATE_LIMIT_DELAY / 60 / MAX_WORKERS:.1f} minutes")
    
    # Process stocks in parallel
    results = process_stocks_parallel(symbols, max_workers=MAX_WORKERS)
    
    if not results:
        print("❌ No results to save. Exiting.")
        return
    
    # Save dataset
    df = save_dataset(results)
    
    print(f"\n✅ Dataset generation complete!")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return df

if __name__ == "__main__":
    df = main()
