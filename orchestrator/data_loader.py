import yfinance as yf

def get_real_stock_data(symbol: str) -> dict:
    """
    Fetch real-time financial data for a given symbol using Yahoo Finance.
    
    Args:
        symbol (str): Stock ticker symbol (e.g., "TSLA").
        
    Returns:
        dict: Dictionary containing financial metrics matching StockData fields.
    """
    print(f"Fetching real data for {symbol}...")
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Extract metrics with safe defaults for missing data
        data = {
            "symbol": symbol,
            "current_price": info.get("currentPrice", 0.0),
            "pe_ratio": info.get("trailingPE", 0.0),
            "debt_to_equity": info.get("debtToEquity", 0.0) / 100.0 if info.get("debtToEquity") else 0.0, # yfinance returns percentage
            "revenue_growth": info.get("revenueGrowth", 0.0),
            "cash_reserves": info.get("totalCash", 0.0),
            "operating_costs": info.get("totalOperatingExpenses", 0.0),
            "net_income": info.get("netIncomeToCommon") or info.get("netIncome") or 0.0
        }
        
        # Fallback for operating costs if not explicitly available (common in some yf datasets)
        if data["operating_costs"] == 0.0:
             # Rough proxy: Total Revenue - Operating Income
             revenue = info.get("totalRevenue", 0.0)
             op_income = info.get("operatingMargins", 0.0) * revenue
             data["operating_costs"] = revenue - op_income

        return data
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        # Return safe defaults to prevent crash, but will likely trigger rules
        return {
            "symbol": symbol,
            "current_price": 0.0,
            "pe_ratio": 0.0,
            "debt_to_equity": 0.0,
            "revenue_growth": 0.0,
            "cash_reserves": 0.0,
            "operating_costs": 0.0
        }
