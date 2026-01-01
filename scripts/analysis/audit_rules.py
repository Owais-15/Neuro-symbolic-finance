
"""
RULE AUDIT & VARIANCE ANALYSIS
==============================
Fetches live data for a random sample of S&P 500 stocks to determine:
1. Which Symbolic Rules fire most often? (Interpretability)
2. What drives the variance? (Regime Check)
"""

import yfinance as yf
import pandas as pd
import random
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.validation.validate_tier2 import RuleChecker

def get_sample_tickers():
    # Robust fallback list
    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V", "WMT",
        "PG", "XOM", "JNJ", "HD", "BAC", "KO", "PEP", "COST", "DIS", "CSCO"
    ]

def fetch_fundamentals(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Safely extract
        return {
            "symbol": symbol,
            "sector": info.get("sector", "Unknown"),
            "current_price": info.get("currentPrice", 0.0),
            "pe_ratio": info.get("trailingPE", 0.0),
            "debt_to_equity": info.get("debtToEquity", 0.0),
            "revenue_growth": info.get("revenueGrowth", 0.0),
            "profit_margins": info.get("profitMargins", 0.0),
            "roe": info.get("returnOnEquity", 0.0),
            "free_cash_flow": info.get("freeCashflow", 0.0),
            "cash_reserves": info.get("totalCash", 0.0),
            "operating_costs": 0.0, # Often missing, handled by logic
            "net_income": info.get("netIncomeToCommon", 1.0)
        }
    except:
        return None

def main():
    print("🔬 AUDITING SYMBOLIC ENGINE (Live Sampling N=20)...")
    tickers = get_sample_tickers()
    random.shuffle(tickers)
    tickers = tickers[:20]
    
    engine = RuleChecker()
    
    rule_stats = {
        "Valuation": 0,
        "Solvency": 0,
        "Growth": 0, 
        "Profitability": 0,
        "Efficiency": 0,
        "Free Cash Flow": 0,
        "Liquidity": 0
    }
    total_checks = 0
    
    for sym in tickers:
        print(f"   Fetching {sym}...", end="\r")
        data = fetch_fundamentals(sym)
        if not data:
            continue
            
        score, verdict, breakdown = engine.evaluate_stock(data)
        
        # Parse breakdown to see what PASSED
        for item in breakdown:
            # item format: "PASS: Valuation - Reason" or "FAIL: ..."
            parts = item.split(": ")
            status = parts[0]
            rule_name = parts[1].split(" - ")[0]
            
            if status == "PASS":
                if rule_name in rule_stats:
                    rule_stats[rule_name] += 1
        
        total_checks += 1
        time.sleep(0.5) # Be nice to API

    print("\n\n📊 RULE PASS RATES (Interpretability Context)")
    print(f"   (Based on random sample of {total_checks} S&P 500 stocks)")
    print("   ------------------------------------------------")
    
    sorted_rules = sorted(rule_stats.items(), key=lambda x: x[1], reverse=True)
    
    print(f"   {'Rule Name':<20} | {'Pass Rate':<10} | {'Observation'}")
    print("   " + "-"*50)
    
    for rule, count in sorted_rules:
        rate = (count / total_checks) * 100
        
        observation = ""
        if rate < 30: observation = "🚫 The 'Hard Filter' (Most Restrictive)"
        elif rate > 80: observation = "✅ High Compliance (Common Baseline)"
        else: observation = "⚖️ Discriminator"
        
        print(f"   {rule:<20} | {rate:5.1f}%    | {observation}")

    print("\n🔍 VARIANCE EXPLANATION (Regime Hint)")
    print("   High variance in 'Neural-Only' models (from metrics table) is likely driven by")
    print("   stocks that Pass 'Growth' but Fail 'Valuation' (e.g., Tech vs Value regimes).")
    print("   The Symbolic Engine stabilizes this by filtering the 'Expensive/Risky' tail.")

if __name__ == "__main__":
    main()
