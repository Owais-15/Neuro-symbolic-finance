
import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.validation.validate_tier2 import RuleChecker

def test_graveyard_zombie_detection():
    """Verify that SVB-like profile is rejected"""
    svb_profile = {
        "symbol": "SIVB",
        "sector": "Financial Services",
        "current_price": 200.0,
        "pe_ratio": 8.0,
        "debt_to_equity": 250.0, # HIGH DEBT
        "revenue_growth": 0.0,
        "cash_reserves": 5000,
        "operating_costs": 1000,
        "net_income": 100,
        "profit_margins": 0.1,
        "roe": 12.0,
        "free_cash_flow": -100000, # BURNING CASH
        "dividend_yield": 0.0,
        "analyst_target": 0.0
    }
    
    engine = RuleChecker()
    score, verdict, breakdown = engine.evaluate_stock(svb_profile)
    
    print(f"SVB Score: {score}")
    assert score < 60, f"SVB should be rejected (Score < 60), got {score}"
    assert "FAIL: Solvency" in str(breakdown) or "FAIL: Free Cash Flow" in str(breakdown)

def test_healthy_compounder():
    """Verify that a healthy stock is accepted"""
    aapl_profile = {
        "symbol": "AAPL",
        "sector": "Technology",
        "current_price": 150.0,
        "pe_ratio": 25.0, # Reasonable for tech
        "debt_to_equity": 150.0, 
        "revenue_growth": 0.10,
        "cash_reserves": 50000,
        "operating_costs": 20000,
        "net_income": 10000,
        "profit_margins": 0.25,
        "roe": 100.0,
        "free_cash_flow": 50000,
        "dividend_yield": 0.005,
        "analyst_target": 180.0
    }
    
    engine = RuleChecker()
    score, verdict, breakdown = engine.evaluate_stock(aapl_profile)
    
    print(f"AAPL Score: {score}")
    assert score > 70, f"AAPL should be trusted (Score > 70), got {score}"
    assert verdict == "TRUSTED"
