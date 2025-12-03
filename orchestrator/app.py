import sys
import os
import json

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.main import run_analysis

def main():
    print("=== Trustworthy Financial Agent CLI ===")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        try:
            symbol = input("\nEnter a Stock Symbol (or 'exit' to quit): ").strip().upper()
            
            if not symbol:
                continue
                
            if symbol in ["EXIT", "QUIT"]:
                print("Exiting...")
                break
            
            print(f"Analyzing {symbol}...")
            
            try:
                result = run_analysis(symbol)
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
