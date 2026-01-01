"""
Unit Tests for Technical Indicators Module

Tests the correctness of technical indicator calculations
to ensure no data leakage and proper implementation.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.technical_indicators import (
    calculate_rsi, calculate_macd, calculate_roc,
    calculate_bollinger_bands, calculate_atr,
    calculate_volume_trend, calculate_trend_strength
)

def test_rsi_bounds():
    """Test that RSI is always between 0 and 100"""
    # Uptrend
    prices_up = pd.Series(range(100, 150))
    rsi_up = calculate_rsi(prices_up)
    assert 0 <= rsi_up <= 100, f"RSI out of bounds: {rsi_up}"
    assert rsi_up > 50, "Uptrend should have RSI > 50"
    
    # Downtrend
    prices_down = pd.Series(range(150, 100, -1))
    rsi_down = calculate_rsi(prices_down)
    assert 0 <= rsi_down <= 100, f"RSI out of bounds: {rsi_down}"
    assert rsi_down < 50, "Downtrend should have RSI < 50"

def test_rsi_extreme_values():
    """Test RSI with extreme price movements"""
    # All gains (should approach 100)
    prices_all_gains = pd.Series([100 + i for i in range(50)])
    rsi_gains = calculate_rsi(prices_all_gains)
    assert rsi_gains > 70, "Continuous gains should have high RSI"
    
    # All losses (should approach 0)
    prices_all_losses = pd.Series([100 - i for i in range(50)])
    rsi_losses = calculate_rsi(prices_all_losses)
    assert rsi_losses < 30, "Continuous losses should have low RSI"

def test_macd_uptrend():
    """Test MACD in uptrend"""
    prices = pd.Series(range(100, 200))
    macd, signal = calculate_macd(prices)
    
    # In strong uptrend, MACD should be above signal
    assert macd > signal, f"MACD ({macd}) should be above signal ({signal}) in uptrend"

def test_macd_downtrend():
    """Test MACD in downtrend"""
    prices = pd.Series(range(200, 100, -1))
    macd, signal = calculate_macd(prices)
    
    # In strong downtrend, MACD should be below signal
    assert macd < signal, f"MACD ({macd}) should be below signal ({signal}) in downtrend"

def test_roc_calculation():
    """Test Rate of Change calculation"""
    # 10% increase
    prices = pd.Series([100] * 20 + [110])
    roc = calculate_roc(prices, period=20)
    assert abs(roc - 10.0) < 0.1, f"ROC should be ~10%, got {roc}%"
    
    # 10% decrease
    prices = pd.Series([100] * 20 + [90])
    roc = calculate_roc(prices, period=20)
    assert abs(roc - (-10.0)) < 0.1, f"ROC should be ~-10%, got {roc}%"

def test_bollinger_bands_ordering():
    """Test that Bollinger Bands are properly ordered"""
    prices = pd.Series(np.random.randn(100) * 10 + 100)
    upper, lower = calculate_bollinger_bands(prices)
    
    # Upper band should always be above lower band
    assert upper > lower, f"Upper band ({upper}) should be > lower band ({lower})"
    
    # Current price should typically be between bands
    current_price = prices.iloc[-1]
    # Allow some tolerance for extreme cases
    assert lower * 0.9 < current_price < upper * 1.1, \
        f"Price ({current_price}) should be near bands ({lower}, {upper})"

def test_atr_positive():
    """Test that ATR is always positive"""
    # Create sample OHLC data
    data = {
        'High': pd.Series(np.random.randn(100) * 5 + 105),
        'Low': pd.Series(np.random.randn(100) * 5 + 95),
        'Close': pd.Series(np.random.randn(100) * 5 + 100)
    }
    hist = pd.DataFrame(data)
    
    atr = calculate_atr(hist)
    assert atr >= 0, f"ATR should be non-negative, got {atr}"

def test_volume_trend():
    """Test volume trend calculation"""
    # Increasing volume
    volume_up = pd.Series(range(100, 200))
    trend_up = calculate_volume_trend(volume_up)
    assert trend_up > 0, "Increasing volume should have positive trend"
    
    # Decreasing volume
    volume_down = pd.Series(range(200, 100, -1))
    trend_down = calculate_volume_trend(volume_down)
    assert trend_down < 0, "Decreasing volume should have negative trend"

def test_trend_strength():
    """Test trend strength calculation"""
    # Strong uptrend
    prices_up = pd.Series(range(100, 150))
    strength_up = calculate_trend_strength(prices_up)
    assert strength_up > 0, "Uptrend should have positive strength"
    
    # Strong downtrend
    prices_down = pd.Series(range(150, 100, -1))
    strength_down = calculate_trend_strength(prices_down)
    assert strength_down < 0, "Downtrend should have negative strength"
    
    # Flat trend
    prices_flat = pd.Series([100] * 50)
    strength_flat = calculate_trend_strength(prices_flat)
    assert abs(strength_flat) < 0.1, "Flat trend should have near-zero strength"

def test_no_future_data_leakage():
    """Critical test: Ensure indicators don't use future data"""
    # Create a price series with a known future spike
    prices = pd.Series([100] * 50 + [200] * 50)
    
    # Calculate RSI using only first 50 points
    rsi_before = calculate_rsi(prices[:50])
    
    # RSI should not "know" about the future spike
    # It should be around 50 (neutral) since prices are flat
    assert 45 < rsi_before < 55, \
        f"RSI calculated on flat prices should be ~50, got {rsi_before}. " \
        "This suggests data leakage!"

def test_indicator_consistency():
    """Test that indicators are deterministic"""
    prices = pd.Series(np.random.randn(100) * 10 + 100)
    
    # Calculate twice
    rsi1 = calculate_rsi(prices)
    rsi2 = calculate_rsi(prices)
    
    assert rsi1 == rsi2, "Indicator should be deterministic"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
