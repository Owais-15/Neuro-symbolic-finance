import pandas as pd
import random
import csv
import sys
import os

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.main import run_analysis

def get_sp500_sample(n=20):
    print("Scraping S&P 500 list...")
    try:
        tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = tables[0]
        symbols = df['Symbol'].tolist()
        return random.sample(symbols, n)
    except Exception as e:
        print(f"Error scraping S&P 500: {e}")
        # Fallback list if scraping fails
        return ["TSLA", "AAPL", "NVDA", "AMZN", "GOOGL", "MSFT", "META", "BRK.B", "LLY", "AVGO", 
                "JPM", "XOM", "UNH", "V", "PG", "MA", "JNJ", "HD", "MRK", "COST"]

def validate_realtime():
    symbols = get_sp500_sample(20)
    results_file = "validation_report.csv"
    
    print(f"Starting Mass Validation on {len(symbols)} stocks...")
    
    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "PE", "Trust_Score", "Validation_Status", "Error_Msg"])
        
        for symbol in symbols:
            print(f"\nAnalyzing {symbol}...")
            try:
                # Run Analysis
                result = run_analysis(symbol)
                
                # Extract Metrics
                metrics = result.get("metrics", {})
                trust_score = result.get("trust_score", 0.0)
                
                current_price = metrics.get("current_price", 0.0)
                pe_ratio = metrics.get("pe_ratio", 0.0)
                net_income = metrics.get("net_income", 0.0)
                cash = metrics.get("cash_reserves", 0.0)
                costs = metrics.get("operating_costs", 0.0)
                
                status = "PASS"
                error_msg = ""
                
                # Check 1: Valuation (Shadow Assertion)
                # IF pe_ratio > 50 AND trust_score == 1.0 -> FAIL (Rule ignored)
                if pe_ratio > 50 and trust_score == 1.0:
                    status = "FAIL"
                    error_msg = f"High PE ({pe_ratio}) but Score is 1.0"
                
                # Check 2: Insolvency (Shadow Assertion)
                # IF net_income < 0 AND cash < costs AND trust_score > 0.5 -> FAIL (Safety catch missed)
                elif (net_income < 0) and (cash < costs) and (trust_score > 0.5):
                    status = "FAIL"
                    error_msg = f"Insolvent (NetInc < 0, Cash < Costs) but Score {trust_score} > 0.5"
                
                # Check 3: Data Integrity
                elif not current_price or current_price == 0:
                    status = "FAIL"
                    error_msg = "Invalid Data (Price is 0 or None)"
                
                # Console Output
                if status == "PASS":
                    print(f"\033[92m✅ PASS: {symbol}\033[0m")
                else:
                    print(f"\033[91m❌ FAIL: {symbol} ({error_msg})\033[0m")
                
                # Write to CSV
                writer.writerow([symbol, pe_ratio, trust_score, status, error_msg])
                
            except Exception as e:
                print(f"\033[91m❌ ERROR: {symbol} ({e})\033[0m")
                writer.writerow([symbol, "N/A", 0.0, "ERROR", str(e)])

    print(f"\nValidation complete. Report saved to {results_file}")

if __name__ == "__main__":
    validate_realtime()
