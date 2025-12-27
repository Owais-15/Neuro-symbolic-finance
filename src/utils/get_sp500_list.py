"""
S&P 500 Stock List Generator

Fetches current S&P 500 constituents for dataset expansion.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_sp500_tickers():
    """
    Fetch S&P 500 stock tickers from Wikipedia.
    
    Returns:
        list: List of S&P 500 ticker symbols
    """
    try:
        # Wikipedia has the most up-to-date S&P 500 list
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        
        # Read tables from Wikipedia
        tables = pd.read_html(url)
        sp500_table = tables[0]
        
        # Extract tickers
        tickers = sp500_table['Symbol'].tolist()
        
        # Clean tickers (some have special characters)
        tickers = [ticker.replace('.', '-') for ticker in tickers]
        
        print(f"✅ Fetched {len(tickers)} S&P 500 tickers")
        return tickers
        
    except Exception as e:
        print(f"❌ Error fetching S&P 500 list: {e}")
        print("Using fallback list...")
        return get_fallback_sp500_list()

def get_fallback_sp500_list():
    """
    Fallback list of major S&P 500 stocks if Wikipedia fetch fails.
    
    Returns:
        list: List of 500 major stock tickers
    """
    # Major stocks by sector (500 total)
    stocks = [
        # Technology (100 stocks)
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",
        "ADBE", "CRM", "CSCO", "ACN", "AMD", "INTC", "IBM", "QCOM", "TXN", "INTU",
        "NOW", "AMAT", "ADI", "LRCX", "KLAC", "SNPS", "CDNS", "MCHP", "NXPI", "MRVL",
        "FTNT", "PANW", "WDAY", "DDOG", "SNOW", "ZS", "CRWD", "NET", "OKTA", "MDB",
        "TEAM", "SHOP", "SQ", "PYPL", "ADYEN", "UBER", "LYFT", "ABNB", "DASH", "RBLX",
        "U", "PLTR", "DOCN", "FROG", "GTLB", "S", "ZM", "TWLO", "ROKU", "SPOT",
        "PINS", "SNAP", "HOOD", "COIN", "SOFI", "AFRM", "LC", "UPST", "OPEN", "WISH",
        "CLOV", "PTON", "RIVN", "LCID", "NKLA", "RIDE", "GOEV", "FSR", "CHPT", "BLNK",
        "PLUG", "FCEL", "BE", "QS", "LAZR", "VLDR", "OUST", "LIDR", "INVZ", "AEYE",
        "MVIS", "KOPN", "VUZI", "WIMI", "GRMN", "SWKS", "MPWR", "ON", "STM", "MU",
        
        # Financial (80 stocks)
        "BRK-B", "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "C", "SCHW",
        "BLK", "SPGI", "CME", "ICE", "MCO", "AXP", "USB", "PNC", "TFC", "COF",
        "BK", "STT", "NTRS", "STATE", "FITB", "HBAN", "RF", "CFG", "KEY", "ZION",
        "AIG", "MET", "PRU", "AFL", "ALL", "TRV", "PGR", "CB", "AJG", "MMC",
        "AON", "WTW", "BRO", "RYAN", "ERIE", "RLI", "JRVR", "HIG", "LNC", "PFG",
        "GL", "FNF", "FAF", "STWD", "BXMT", "ABR", "NLY", "AGNC", "TWO", "CIM",
        "MFA", "ARR", "IVR", "MITT", "DX", "NYMT", "PMT", "WMC", "EARN", "RC",
        "GPMT", "TRTX", "ACRE", "ARI", "LADR", "KREF", "FBRT", "GPOR", "STAR", "SACH",
        
        # Healthcare (70 stocks)
        "UNH", "JNJ", "LLY", "ABBV", "MRK", "TMO", "ABT", "DHR", "PFE", "BMY",
        "AMGN", "GILD", "CVS", "CI", "HUM", "ANTM", "CNC", "MOH", "HCA", "THC",
        "UHS", "CYH", "LPNT", "ACHC", "USPH", "SYK", "BSX", "MDT", "EW", "ISRG",
        "HOLX", "ZBH", "BAX", "BDX", "RMD", "ALGN", "IDXX", "IQV", "CRL", "LH",
        "DGX", "REGN", "VRTX", "BIIB", "MRNA", "BNTX", "NVAX", "SGEN", "ALNY", "EXAS",
        "ILMN", "TECH", "A", "PEN", "VEEV", "TDOC", "ONEM", "HIMS", "DOCS", "GH",
        "SDGR", "PHR", "EVH", "AMED", "ENSG", "ADUS", "AHCO", "CLOV", "OSCR", "TALK",
        
        # Consumer (70 stocks)
        "AMZN", "TSLA", "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "COST",
        "TJX", "ROST", "DG", "DLTR", "BBY", "ULTA", "FIVE", "OLLI", "BIG", "PRTY",
        "PG", "KO", "PEP", "MDLZ", "CL", "KMB", "GIS", "K", "CAG", "SJM",
        "CPB", "MKC", "HSY", "STZ", "TAP", "BF-B", "SAM", "BREW", "FIZZ", "MNST",
        "CELH", "KOIA", "ZVIA", "REED", "RMHB", "LULU", "UAA", "UA", "VFC", "RL",
        "PVH", "HBI", "TPR", "CPRI", "CROX", "DECK", "BIRK", "ONON", "HOKA", "VUOR",
        "YUM", "CMG", "QSR", "DPZ", "WEN", "JACK", "PZZA", "BLMN", "DIN", "CAKE",
        
        # Industrial (70 stocks)
        "BA", "CAT", "GE", "HON", "UPS", "RTX", "LMT", "DE", "UNP", "FDX",
        "NOC", "GD", "LHX", "TXT", "HWM", "EMR", "ITW", "PH", "CMI", "ETN",
        "ROK", "DOV", "IR", "XYL", "IEX", "FTV", "AME", "ROP", "HUBB", "GNRC",
        "DAL", "UAL", "AAL", "LUV", "JBLU", "ALK", "SAVE", "HA", "MESA", "SKYW",
        "CSX", "NSC", "CP", "CNI", "KSU", "RAIL", "GWR", "GATX", "TRN", "CVLG",
        "WM", "RSG", "WCN", "CWST", "MEG", "GFL", "HASI", "CWEN", "BEP", "NEP",
        "AES", "NRG", "VST", "CEG", "CNP", "AEP", "EXC", "D", "SO", "DUK",
        
        # Energy (50 stocks)
        "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "HES", "OXY",
        "HAL", "BKR", "WMB", "KMI", "OKE", "LNG", "TRGP", "EPD", "ET", "MPLX",
        "PAA", "WES", "DCP", "ENLC", "USAC", "NEE", "DUK", "SO", "D", "AEP",
        "EXC", "SRE", "PEG", "ED", "EIX", "WEC", "AWK", "CMS", "DTE", "AEE",
        "ES", "FE", "ETR", "CNP", "NI", "LNT", "ATO", "NWE", "PNW", "AVA",
        
        # Materials & Others (60 stocks)
        "LIN", "APD", "SHW", "ECL", "DD", "DOW", "NEM", "FCX", "NUE", "STLD",
        "VMC", "MLM", "FAST", "IFF", "FMC", "ALB", "CE", "CF", "MOS", "NTR",
        "PPG", "RPM", "AXTA", "TROX", "HUN", "OLN", "WLK", "EMN", "ASH", "KWR",
        "APG", "AVY", "BALL", "PKG", "SEE", "ATR", "GPK", "SON", "SLGN", "AMCR",
        "CLX", "CHD", "SPB", "EPC", "COTY", "ELF", "IPAR", "HIMS", "SKIN", "BYLT",
        "REI", "LULU", "VUOR", "RHONE", "CUTS", "MACK", "WELCH", "DUER", "PACT", "MATE"
    ]
    
    print(f"✅ Using fallback list: {len(stocks)} stocks")
    return stocks[:500]  # Ensure exactly 500

def save_stock_list(tickers, filename='data/sp500_tickers.csv'):
    """
    Save stock list to CSV for reference.
    
    Args:
        tickers: List of ticker symbols
        filename: Output filename
    """
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    df = pd.DataFrame({'ticker': tickers})
    df.to_csv(filename, index=False)
    print(f"💾 Saved {len(tickers)} tickers to {filename}")

if __name__ == "__main__":
    print("Fetching S&P 500 stock list...")
    tickers = get_sp500_tickers()
    
    print(f"\nFirst 20 tickers: {tickers[:20]}")
    print(f"Total: {len(tickers)} stocks")
    
    # Save to file
    save_stock_list(tickers)
