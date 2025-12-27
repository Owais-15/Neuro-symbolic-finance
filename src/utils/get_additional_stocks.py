"""
Expand Dataset to N=600+ with Additional Stocks

Adds Russell 2000 and international stocks to reach N=600+.
"""

# Additional high-quality stocks beyond S&P 500
ADDITIONAL_STOCKS = [
    # Russell 2000 Large Caps (50 stocks)
    "SMCI", "CELH", "IONQ", "HIMS", "RKLB", "BROS", "CAVA", "ARM", "RDDT", "HOOD",
    "KVUE", "FSLR", "ENPH", "SEDG", "RUN", "NOVA", "WOLF", "SPWR", "CSIQ", "JKS",
    "DQ", "SOL", "MAXN", "ARRY", "AMPS", "SHLS", "VVNT", "CWEN-A", "NEP", "BEP",
    "AY", "CWEN", "PEGI", "CAPL", "GPRE", "REX", "BIOX", "GEVO", "AMTX", "REGI",
    "RDUS", "NEXT", "CLNE", "WPRT", "HYLN", "WKHS", "ARVL", "MULN", "ELMS", "HYZN",
    
    # International Tech (30 stocks)
    "TSM", "BABA", "TCEHY", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "BILI",
    "SE", "GRAB", "MELI", "NU", "CPNG", "SHOP", "SPOT", "ASML", "SAP", "ADYEN",
    "TEAM", "WDAY", "ZM", "DOCU", "OKTA", "DDOG", "SNOW", "MDB", "NET", "CRWD",
    
    # Emerging Markets (20 stocks)
    "VALE", "ITUB", "PBR", "ABEV", "BBD", "SBS", "BRFS", "CIG", "ERJ", "GOL",
    "AZUL", "STNE", "PAGS", "MOMO", "IQ", "VIPS", "ATHM", "TIGR", "FUTU", "LEGN",
    
    # Biotech & Healthcare (30 stocks)
    "MRNA", "BNTX", "NVAX", "VXRT", "INO", "OCGN", "SAVA", "AVXL", "ATNF", "PROG",
    "ATOS", "CTXR", "BNGO", "PACB", "ILMN", "TWST", "BEAM", "CRSP", "EDIT", "NTLA",
    "BLUE", "FATE", "SGMO", "CRBU", "VERV", "PRME", "ABCL", "ALNY", "IONS", "ARWR",
    
    # Fintech & Crypto (20 stocks)
    "SQ", "PYPL", "AFRM", "UPST", "LC", "SOFI", "COIN", "MARA", "RIOT", "CLSK",
    "HUT", "BITF", "ARBK", "CIFR", "WULF", "IREN", "CORZ", "BTBT", "CAN", "SOS"
]

print(f"Additional stocks to process: {len(ADDITIONAL_STOCKS)}")
print(f"Current dataset: 462 stocks")
print(f"Target after expansion: {462 + len(ADDITIONAL_STOCKS)} = {462 + len(ADDITIONAL_STOCKS)} stocks")
print(f"\nWith 3 API keys (90 req/min), estimated time: {len(ADDITIONAL_STOCKS) * 0.1 / 60:.1f} minutes")

# Save to file
import pandas as pd
df = pd.DataFrame({'ticker': ADDITIONAL_STOCKS})
df.to_csv('data/additional_stocks.csv', index=False)
print(f"\n💾 Saved to: data/additional_stocks.csv")
