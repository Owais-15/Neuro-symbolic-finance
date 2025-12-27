"""
Technical Indicators Module

Calculates technical analysis indicators for stock prediction.
Adds 15+ features to improve correlation with returns.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Optional

def get_technical_indicators(symbol: str, period: str = "1y") -> Dict[str, float]:
    """
    Fetch and calculate technical indicators for a stock.
    
    Args:
        symbol: Stock ticker symbol
        period: Historical period for calculation (default: 1 year)
    
    Returns:
        Dictionary of technical indicator values
    """
    try:
        # Fetch historical data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if len(hist) < 50:  # Need minimum data
            return get_default_indicators()
        
        # Calculate indicators
        indicators = {}
        
        # === MOMENTUM INDICATORS ===
        indicators['rsi'] = calculate_rsi(hist['Close'])
        indicators['macd'], indicators['macd_signal'] = calculate_macd(hist['Close'])
        indicators['roc'] = calculate_roc(hist['Close'], period=20)
        
        # === TREND INDICATORS ===
        indicators['sma_50'] = hist['Close'].rolling(window=50).mean().iloc[-1]
        indicators['sma_200'] = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else hist['Close'].mean()
        indicators['ema_20'] = hist['Close'].ewm(span=20).mean().iloc[-1]
        
        # Price position relative to moving averages
        current_price = hist['Close'].iloc[-1]
        indicators['price_vs_sma50'] = (current_price - indicators['sma_50']) / indicators['sma_50'] * 100
        indicators['price_vs_sma200'] = (current_price - indicators['sma_200']) / indicators['sma_200'] * 100
        
        # === VOLATILITY INDICATORS ===
        indicators['bb_upper'], indicators['bb_lower'] = calculate_bollinger_bands(hist['Close'])
        indicators['bb_position'] = (current_price - indicators['bb_lower']) / (indicators['bb_upper'] - indicators['bb_lower'])
        indicators['atr'] = calculate_atr(hist)
        indicators['volatility'] = hist['Close'].pct_change().std() * np.sqrt(252) * 100  # Annualized
        
        # === VOLUME INDICATORS ===
        indicators['volume_trend'] = calculate_volume_trend(hist['Volume'])
        indicators['volume_ratio'] = hist['Volume'].iloc[-1] / hist['Volume'].mean()
        
        # === TREND STRENGTH ===
        indicators['trend_strength'] = calculate_trend_strength(hist['Close'])
        
        return indicators
        
    except Exception as e:
        print(f"Error calculating indicators for {symbol}: {e}")
        return get_default_indicators()

def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0

def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """Calculate MACD and Signal line"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    
    return (macd.iloc[-1] if not pd.isna(macd.iloc[-1]) else 0.0,
            signal_line.iloc[-1] if not pd.isna(signal_line.iloc[-1]) else 0.0)

def calculate_roc(prices: pd.Series, period: int = 20) -> float:
    """Calculate Rate of Change"""
    roc = ((prices.iloc[-1] - prices.iloc[-period]) / prices.iloc[-period]) * 100
    return roc if not pd.isna(roc) else 0.0

def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: int = 2) -> tuple:
    """Calculate Bollinger Bands"""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    
    return (upper.iloc[-1] if not pd.isna(upper.iloc[-1]) else prices.iloc[-1] * 1.1,
            lower.iloc[-1] if not pd.isna(lower.iloc[-1]) else prices.iloc[-1] * 0.9)

def calculate_atr(hist: pd.DataFrame, period: int = 14) -> float:
    """Calculate Average True Range"""
    high_low = hist['High'] - hist['Low']
    high_close = np.abs(hist['High'] - hist['Close'].shift())
    low_close = np.abs(hist['Low'] - hist['Close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    return atr.iloc[-1] if not pd.isna(atr.iloc[-1]) else 0.0

def calculate_volume_trend(volume: pd.Series, period: int = 20) -> float:
    """Calculate volume trend (current vs average)"""
    avg_volume = volume.rolling(window=period).mean()
    trend = (volume.iloc[-1] - avg_volume.iloc[-1]) / avg_volume.iloc[-1] * 100
    return trend if not pd.isna(trend) else 0.0

def calculate_trend_strength(prices: pd.Series, period: int = 20) -> float:
    """
    Calculate trend strength using linear regression slope.
    Positive = uptrend, Negative = downtrend
    """
    if len(prices) < period:
        return 0.0
    
    recent_prices = prices.iloc[-period:]
    x = np.arange(len(recent_prices))
    
    # Linear regression
    slope = np.polyfit(x, recent_prices, 1)[0]
    
    # Normalize by price level
    normalized_slope = (slope / recent_prices.mean()) * 100
    
    return normalized_slope

def get_default_indicators() -> Dict[str, float]:
    """Return default values when calculation fails"""
    return {
        'rsi': 50.0,
        'macd': 0.0,
        'macd_signal': 0.0,
        'roc': 0.0,
        'sma_50': 0.0,
        'sma_200': 0.0,
        'ema_20': 0.0,
        'price_vs_sma50': 0.0,
        'price_vs_sma200': 0.0,
        'bb_upper': 0.0,
        'bb_lower': 0.0,
        'bb_position': 0.5,
        'atr': 0.0,
        'volatility': 0.0,
        'volume_trend': 0.0,
        'volume_ratio': 1.0,
        'trend_strength': 0.0
    }

# Test function
if __name__ == "__main__":
    print("Testing Technical Indicators Module...")
    
    test_symbols = ["AAPL", "TSLA", "NVDA"]
    
    for symbol in test_symbols:
        print(f"\n{symbol}:")
        indicators = get_technical_indicators(symbol)
        
        print(f"  RSI: {indicators['rsi']:.2f}")
        print(f"  MACD: {indicators['macd']:.2f}")
        print(f"  Price vs SMA50: {indicators['price_vs_sma50']:.2f}%")
        print(f"  BB Position: {indicators['bb_position']:.2f}")
        print(f"  Trend Strength: {indicators['trend_strength']:.2f}")
