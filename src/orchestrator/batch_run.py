import csv
import sys
import os

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.main import run_analysis

def batch_run():
    symbols = ["TSLA", "AAPL", "NVDA", "AMZN", "MSFT", "GOOGL"]
    results_file = "final_results.csv"
    
    print(f"Starting batch analysis for: {symbols}")
    
    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write Header
        writer.writerow(["Symbol", "Current Price", "P/E Ratio", "Trust Score", "Verdict", "Rule Violations"])
        
        for symbol in symbols:
            print(f"\nProcessing {symbol}...")
            try:
                result = run_analysis(symbol)
                
                # Extract data
                metrics = result.get("metrics", {})
                current_price = metrics.get("current_price", "N/A")
                pe_ratio = metrics.get("pe_ratio", "N/A")
                trust_score = result.get("trust_score", 0.0)
                
                # Determine Verdict based on score
                if trust_score >= 0.8:
                    verdict = "Safe"
                elif trust_score >= 0.5:
                    verdict = "Caution"
                else:
                    verdict = "Risky"
                
                # Format violations
                violations = result.get("rule_violations", [])
                violation_str = ", ".join([v["violation"] for v in violations]) if violations else "None"
                
                # Write to CSV
                writer.writerow([symbol, current_price, pe_ratio, trust_score, verdict, violation_str])
                
                print(f"Finished {symbol}: Score {trust_score} ({verdict})")
                
            except Exception as e:
                print(f"Failed to process {symbol}: {e}")
                writer.writerow([symbol, "Error", "Error", 0.0, "Error", str(e)])

    print(f"\nBatch analysis complete. Results saved to {results_file}")

if __name__ == "__main__":
    batch_run()
