"""
Expand Dataset to N=600+ 

Processes 150 additional stocks to reach N=612.
Uses multi-key system for fast processing.
"""

import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.data_loader import get_real_stock_data, get_historical_price
from orchestrator.main import run_analysis

# Configuration
MAX_WORKERS = 15  # Increased for 3 API keys
RATE_LIMIT_DELAY = 0.05  # Very fast with 3 keys

def process_single_stock(symbol, index, total):
    """Process a single stock"""
    try:
        print(f"[{index}/{total}] {symbol}...", end=" ")
        
        raw_data = get_real_stock_data(symbol)
        
        if raw_data["current_price"] == 0.0:
            print("SKIP")
            return None
        
        analysis = run_analysis(symbol)
        hist_price = get_historical_price(symbol, days_ago=365)
        current_price = raw_data["current_price"]
        
        if hist_price > 0:
            actual_return = ((current_price - hist_price) / hist_price) * 100
        else:
            actual_return = 0.0
        
        result = {
            'Symbol': symbol,
            'Trust_Score': analysis['trust_score'],
            'Verdict': analysis['verdict'],
            'Current_Price': current_price,
            'Actual_Return_1Y': actual_return,
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
        
        print(f"✅ T:{analysis['trust_score']:.0f}, R:{actual_return:.1f}%")
        time.sleep(RATE_LIMIT_DELAY)
        
        return result
        
    except Exception as e:
        print(f"ERR: {str(e)[:30]}")
        return None

def main():
    print("="*80)
    print("EXPANDING DATASET TO N=600+")
    print("="*80)
    print(f"Start: {datetime.now().strftime('%H:%M:%S')}\n")
    
    # Load existing and additional stocks
    existing_df = pd.read_csv("results/dataset_n500_enhanced.csv")
    additional_df = pd.read_csv("data/additional_stocks.csv")
    
    existing_symbols = set(existing_df['Symbol'].tolist())
    additional_symbols = [s for s in additional_df['ticker'].tolist() 
                         if s not in existing_symbols]
    
    print(f"Existing: {len(existing_symbols)} stocks")
    print(f"Additional: {len(additional_symbols)} stocks")
    print(f"Target: {len(existing_symbols) + len(additional_symbols)} stocks")
    print(f"Est. time: ~15-20 minutes\n")
    
    # Process additional stocks
    new_results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_stock, symbol, i+1, len(additional_symbols)): symbol
            for i, symbol in enumerate(additional_symbols)
        }
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                new_results.append(result)
    
    elapsed = time.time() - start_time
    
    # Combine datasets
    if new_results:
        new_df = pd.DataFrame(new_results)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df = combined_df.sort_values('Trust_Score', ascending=False)
        
        # Save
        combined_df.to_csv("results/dataset_n600_plus.csv", index=False)
        
        print("\n" + "="*80)
        print("DATASET EXPANSION COMPLETE!")
        print("="*80)
        print(f"\nTotal stocks: {len(combined_df)}")
        print(f"New stocks added: {len(new_results)}")
        print(f"Processing time: {elapsed/60:.1f} minutes")
        print(f"Features: {len(combined_df.columns)}")
        
        print(f"\n📊 Statistics:")
        print(f"  Average Return: {combined_df['Actual_Return_1Y'].mean():.2f}%")
        print(f"  Median Return: {combined_df['Actual_Return_1Y'].median():.2f}%")
        print(f"  Win Rate: {(combined_df['Actual_Return_1Y'] > 0).sum() / len(combined_df) * 100:.1f}%")
        
        print(f"\n📋 Verdict Distribution:")
        print(combined_df['Verdict'].value_counts())
        
        print(f"\n💾 Saved to: results/dataset_n600_plus.csv")
    else:
        print("\n❌ No new stocks processed")
    
    print(f"\nEnd: {datetime.now().strftime('%H:%M:%S')}")
    print("="*80)

if __name__ == "__main__":
    main()
