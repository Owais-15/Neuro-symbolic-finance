import yfinance as yf
import pandas as pd
from orchestrator.technical_indicators import get_technical_indicators

def get_real_stock_data(symbol: str) -> dict:
    """
    Fetches comprehensive financial data from Yahoo Finance.
    Returns 0.0 for missing values to prevent Pydantic crashes.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Helper to safely get float values
        def get_float(key, default=0.0):
            val = info.get(key)
            return float(val) if val is not None else default

        # Helper to safely get string values
        def get_str(key, default="Unknown"):
            val = info.get(key)
            return str(val) if val is not None else default

        data = {
            "symbol": symbol,
            "sector": get_str("sector"),
            "current_price": get_float("currentPrice"),
            "pe_ratio": get_float("trailingPE"),
            "debt_to_equity": get_float("debtToEquity"),
            "revenue_growth": get_float("revenueGrowth"),
            "cash_reserves": get_float("totalCash"),
            "operating_costs": get_float("totalOperatingExpenses"),
            "net_income": get_float("netIncomeToCommon"),
            
            # V2.0 METRICS
            "profit_margins": get_float("profitMargins"),
            "roe": get_float("returnOnEquity"),
            "free_cash_flow": get_float("freeCashflow"),
            "dividend_yield": get_float("dividendYield"),
            "analyst_target": get_float("targetMeanPrice")
        }
        
        # V3.0: ADD TECHNICAL INDICATORS
        try:
            tech_indicators = get_technical_indicators(symbol)
            data.update(tech_indicators)
        except Exception as e:
            print(f"Warning: Could not fetch technical indicators for {symbol}: {e}")
            # Add default technical indicators
            data.update({
                'rsi': 50.0,
                'macd': 0.0,
                'price_vs_sma50': 0.0,
                'price_vs_sma200': 0.0,
                'bb_position': 0.5,
                'volatility': 0.0,
                'trend_strength': 0.0
            })

        return data

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Return zombie object with defaults
        return {
            "symbol": symbol,
            "sector": "Unknown",
            "current_price": 0.0,
            "pe_ratio": 0.0,
            "debt_to_equity": 0.0,
            "revenue_growth": 0.0,
            "cash_reserves": 0.0,
            "operating_costs": 0.0,
            "net_income": 0.0,
            "profit_margins": 0.0,
            "roe": 0.0,
            "free_cash_flow": 0.0,
            "dividend_yield": 0.0,
            "analyst_target": 0.0,
            # Technical indicators defaults
            'rsi': 50.0,
            'macd': 0.0,
            'price_vs_sma50': 0.0,
            'price_vs_sma200': 0.0,
            'bb_position': 0.5,
            'volatility': 0.0,
            'trend_strength': 0.0
        }

def get_historical_price(symbol: str, days_ago: int = 365) -> float:
    """
    Fetch historical stock price from N days ago.
    Used for backtesting and calculating actual returns.
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=f"{days_ago+30}d")  # Extra buffer
        
        if len(hist) < days_ago:
            print(f"Warning: Insufficient history for {symbol}")
            return 0.0
        
        # Get price from approximately N days ago
        target_date = hist.index[-days_ago] if len(hist) >= days_ago else hist.index[0]
        historical_price = hist.loc[target_date, 'Close']
        
        return float(historical_price)
    
    except Exception as e:
        print(f"Error fetching historical price for {symbol}: {e}")
        return 0.0
