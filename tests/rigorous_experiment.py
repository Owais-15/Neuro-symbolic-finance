import csv
import time
import sys
import os
import re
from groq import Groq

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.main import run_analysis

# Configuration
API_KEY = os.environ.get("GROQ_API_KEY")
RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "thesis_comparison_data.csv")

DATASET = {
    "Tech/Growth": ['NVDA', 'AMD', 'PLTR', 'TSLA', 'SMCI'],
    "Legacy/Stable": ['KO', 'JNJ', 'PG', 'WMT', 'MCD'],
    "Distressed/Volatile": ['AMC', 'GME', 'PTON', 'CVNA', 'RIVN'],
    "Financials": ['JPM', 'BAC', 'C', 'SOFI']
}

def get_baseline_score(client, symbol):
    """
    Agent A (Baseline): Ask Groq for a safety rating.
    """
    prompt = f"Rate {symbol} safety from 0.0 (Risk) to 1.0 (Safe). Output ONLY the number."
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = completion.choices[0].message.content.strip()
        # Extract number using regex to handle potential extra text
        match = re.search(r"0\.\d+|1\.0|[01]", content)
        if match:
            return float(match.group())
        return "N/A"
    except Exception as e:
        print(f"Baseline Error for {symbol}: {e}")
        return "Error"

def run_experiment():
    # Ensure results directory exists
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        
    client = Groq(api_key=API_KEY)
    
    print("Starting Rigorous Experiment...")
    
    with open(RESULTS_FILE, mode='w', newline='') as file:
        # Columns: Symbol, Sector, Baseline_Score, Trust_Score, PE_Ratio, Verdict
        # Added Net_Income as requested for context
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Sector", "Baseline_Score", "Trust_Score", "PE_Ratio", "Net_Income", "Verdict"])
        
        for sector, symbols in DATASET.items():
            for symbol in symbols:
                print(f"\nProcessing {symbol} ({sector})...")
                
                # Agent A: Baseline
                baseline_score = get_baseline_score(client, symbol)
                print(f"  Baseline: {baseline_score}")
                
                # Agent B: Neuro-Symbolic
                try:
                    result = run_analysis(symbol)
                    trust_score = result.get("trust_score", "N/A")
                    metrics = result.get("metrics", {})
                    pe_ratio = metrics.get("pe_ratio", "N/A")
                    net_income = metrics.get("net_income", "N/A")
                    verdict = result.get("final_verdict", "N/A")
                    
                    print(f"  Neuro-Symbolic: {trust_score} (PE: {pe_ratio})")
                except Exception as e:
                    print(f"  Neuro-Symbolic Error: {e}")
                    trust_score = "Error"
                    pe_ratio = "N/A"
                    net_income = "N/A"
                    verdict = "Error"
                
                writer.writerow([symbol, sector, baseline_score, trust_score, pe_ratio, net_income, verdict])
                
                # Rate Limiting
                time.sleep(1)

    print(f"\nExperiment complete. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    run_experiment()
