
import sys
import os
import json
import random

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.llm_interface import LLMRunner
from symbolic_engine.rule_checker import FinancialRuleEngine, StockData
from orchestrator.data_loader import get_real_stock_data

def fetch_data(symbol: str) -> dict:
    """
    Fetch real financial data for a given symbol.
    """
    return get_real_stock_data(symbol)

def run_analysis(symbol: str) -> dict:
    """
    Run the full Neuro-Symbolic analysis pipeline.
    """
    print(f"Starting analysis for {symbol}...")
    
    # Initialize Engines
    # Note: In a real app, we'd load the model once globally or pass it in
    neural_engine = LLMRunner()
    try:
        neural_engine.load_model()
    except Exception as e:
        print(f"Warning: Model loading failed (expected if no GPU/local model). Proceeding with mock logic if needed or failing.")
        # For this implementation, we assume load_model works or we handle it. 
        # If it fails, we can't proceed with neural analysis.
        pass

    symbolic_engine = FinancialRuleEngine()

    # 1. Fetch Data
    raw_data = fetch_data(symbol)
    print(f"Fetched data: {raw_data}")

    # 2. Neural Analysis (LLM)
    try:
        # Use the robust analyze_stock method which returns a dict
        llm_response = neural_engine.analyze_stock(symbol, raw_data)
        print(f"LLM Response: {json.dumps(llm_response, indent=2)}")
        
        # 3. Validate
        try:
            extracted_metrics = llm_response.get("extracted_metrics", {})
            reasoning = llm_response.get("reasoning", "No reasoning provided.")
            
            # Ensure symbol is present in metrics
            if "symbol" not in extracted_metrics:
                extracted_metrics["symbol"] = symbol

            # Validate with Pydantic
            stock_data = StockData(**extracted_metrics)
            
        except (ValueError, TypeError) as e:
            print(f"Validation Error: {e}")
            return {
                "symbol": symbol,
                "llm_analysis": str(llm_response),
                "metrics": {},
                "rule_violations": [],
                "trust_score": 0.0,
                "final_verdict": f"Validation Error: {str(e)}"
            }

        # 4. Symbolic Verification (Rule Engine)
        verification_result = symbolic_engine.evaluate(stock_data)
        
        return {
            "symbol": symbol,
            "llm_analysis": reasoning,
            "metrics": extracted_metrics,
            "rule_violations": verification_result["violations"],
            "trust_score": verification_result["trust_score"],
            "final_verdict": "Analysis Complete"
        }

    except Exception as e:
        print(f"Pipeline Error: {e}")
        return {
            "symbol": symbol,
            "llm_analysis": "Error",
            "rule_violations": [],
            "trust_score": 0.0,
            "final_verdict": f"Pipeline Error: {str(e)}"
        }

def main():
    """
    Main entry point for the Trustworthy Financial Agent.
    """
    # Example run
    result = run_analysis("TSLA")
    print("\n=== Final Result ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
