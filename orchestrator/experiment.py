import csv
import sys
import os
from groq import Groq

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.main import run_analysis

# Configuration
API_KEY = os.environ.get("GROQ_API_KEY")
DATASET = ['TSLA', 'AAPL', 'NVDA', 'AMZN', 'GOOGL', 'GME', 'AMC', 'INTC', 'PFE', 'F']

def run_baseline(client, symbol):
    """
    Baseline Agent: Pure LLM approach.
    """
    prompt = f"Is {symbol} a risky investment? Answer YES or NO and give 1 sentence of reasoning."
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        return f"Error: {e}"

def run_neurosymbolic(symbol):
    """
    Neuro-Symbolic Agent: LLM + Rule Engine.
    """
    try:
        result = run_analysis(symbol)
        return result["trust_score"], result["final_verdict"]
    except Exception as e:
        return 0.0, f"Error: {e}"

def main():
    print("Starting Comparative Experiment...")
    client = Groq(api_key=API_KEY)
    
    results_file = "experiment_results.csv"
    
    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Baseline_Verdict", "Neuro_Score", "Conflict_Detected", "Baseline_Reasoning"])
        
        for symbol in DATASET:
            print(f"\nAnalyzing {symbol}...")
            
            # 1. Run Baseline
            baseline_raw = run_baseline(client, symbol)
            # Simple parsing for YES/NO
            if "YES" in baseline_raw.upper() and "NO" not in baseline_raw.upper():
                baseline_verdict = "Risky"
            elif "NO" in baseline_raw.upper():
                baseline_verdict = "Safe"
            else:
                baseline_verdict = "Ambiguous"
            
            print(f"Baseline: {baseline_verdict} ({baseline_raw[:50]}...)")
            
            # 2. Run Neuro-Symbolic
            neuro_score, neuro_verdict = run_neurosymbolic(symbol)
            print(f"Neuro-Symbolic: Score {neuro_score}")
            
            # 3. Detect Conflict
            # Conflict: Baseline says Safe, but Neuro says Risky (Score < 0.5)
            conflict = False
            if baseline_verdict == "Safe" and neuro_score < 0.5:
                conflict = True
                print(">>> CONFLICT DETECTED: Safety Catch! <<<")
            
            writer.writerow([symbol, baseline_verdict, neuro_score, conflict, baseline_raw])
            
    print(f"\nExperiment complete. Results saved to {results_file}")

if __name__ == "__main__":
    main()
