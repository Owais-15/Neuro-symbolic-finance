"""
GRAVEYARD STRESS TEST (Survivorship Bias Defense)

The "Safety Catch" Protocol:
This script tests the Symbolic Engine against "Zombie Profiles" - synthetic data
reconstructing the financial state of famous bankruptcies right before they crashed.

Goal: Prove that even if these companies were in our dataset, 
the Rule-Based Safety Catch would have rejected them (Verdict: SELL/TRIM).
"""

import sys
import os
import pandas as pd

# Add project root AND src to path to ensure imports work
# We need to go up one level from 'scripts' to get to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')

sys.path.append(project_root)
sys.path.append(src_path)

# Try import
try:
    from symbolic_engine.rule_checker import RuleChecker
except ImportError:
    from src.symbolic_engine.rule_checker import RuleChecker

def run_graveyard_test():
    print("💀 RUNNING GRAVEYARD STRESS TEST")
    print("==================================================")
    print("Testing if Symbolic Rules catch famous bankruptcies...\n")

    # Define Zombie Profiles (Pre-Crash Metrics)
    # Data approximated from financial reports ~3-6 months before failure
    zombies = [
        {
            "name": "Silicon Valley Bank (SVB) - 2023",
            "context": "Liquidity Crisis",
            "data": {
                "pe_ratio": 8.0,              # Looked "cheap"
                "debt_to_equity": 2.5,        # High leverage
                "free_cash_flow": -100000,    # Massive cash burn
                "cash_reserves": 5000,        # Dwindling relative to liabilities
                "roe": 12.0,                  # Looked okay
                "current_price": 200.0,
                "sector": "Financial Services"
            }
        },
        {
            "name": "Bed Bath & Beyond (BBBY) - 2022",
            "context": "Retail Apocalypse",
            "data": {
                "pe_ratio": 0.0,              # Negative earnings
                "debt_to_equity": 5.0,        # Massive debt load
                "revenue_growth": -0.25,      # Revenue collapsing
                "profit_margins": -0.15,      # Losing money 
                "current_price": 15.0,
                "sector": "Consumer Cyclical"
            }
        },
        {
            "name": "WeWork (Pre-IPO) - 2019",
            "context": "Valuation Bubble",
            "data": {
                "pe_ratio": -50.0,            # Massive losses
                "debt_to_equity": 8.0,        # Insane leverage
                "free_cash_flow": -5000000,   # Incinerating cash
                "profit_margins": -0.80,      # -80% margins
                "current_price": 100.0,
                "sector": "Real Estate"
            }
        },
        {
            "name": "Typical 'Dotcom' Zombie",
            "context": "No Earnings, High Hype",
            "data": {
                "pe_ratio": 500.0,            # Sky high valuation
                "revenue_growth": 2.0,        # Growing fast
                "net_income": -50000,         # But losing money
                "cash_reserves": 1000,        # Low runway
                "current_price": 50.0,
                "sector": "Technology"
            }
        }
    ]

    engine = RuleChecker()
    passed = 0
    
    results_data = []

    for zombie in zombies:
        print(f"🧟 Testing: {zombie['name']}")
        print(f"   Context: {zombie['context']}")
        
        # Run Symbolic Engine
        score, verdict, reasons = engine.evaluate_stock(zombie['data'])
        
        print(f"   🛡️ Score: {score}/100")
        print(f"   ⚖️ Verdict: {verdict}")
        print(f"   🚨 Flags: {reasons[:2]}...") # Show top 2 flags
        
        # Verify Safety Catch
        # A "Success" here means the engine REJECTED the bad company (Score < 60)
        is_safe = score < 60
        
        if is_safe:
            print("   ✅ SUCCESS: Safety mechanism triggered!")
            passed += 1
            status = "CAUGHT"
        else:
            print("   ❌ FAILURE: Zombie skipped through!")
            status = "MISSED"
            
        results_data.append({
            "Company": zombie['name'],
            "Verdict": verdict,
            "Score": score,
            "Status": status
        })
        print("-" * 50)

    print(f"\n🏆 TEST RESULTS: {passed}/{len(zombies)} Threats Neutralized")
    
    if passed == len(zombies):
        print("\n✅ DEFENSE VERIFIED: The Graveyard Test proves survivorship bias mitigation.")
        print("   Even if these companies were in the dataset, they would be filtered out.")
    else:
        print("\n⚠️ DEFENSE WEAK: Some risky profiles slipped through.")
        
    return results_data

if __name__ == "__main__":
    run_graveyard_test()
