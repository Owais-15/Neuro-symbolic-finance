import json
import os
import sys
from dotenv import load_dotenv

# Ensure we can import from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.llm_interface import LLMRunner
from symbolic_engine.rule_checker import FinancialRuleEngine, StockData
from orchestrator.data_loader import get_real_stock_data

# Try to use multi-key manager, fallback to single key
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils'))
    from groq_key_manager import get_groq_api_key
    api_key = get_groq_api_key()
    print("✅ Using multi-key manager")
except:
    api_key = os.environ.get("GROQ_API_KEY")
    print("⚠️  Using single key (multi-key manager not available)")

# Initialize Engines
llm_runner = LLMRunner(api_key=api_key)
rule_engine = FinancialRuleEngine()

def run_analysis(symbol: str):
    print(f"Starting V2 analysis for {symbol}...")

    # 1. Fetch Real Data
    print(f"Fetching real data for {symbol}...")
    raw_data = get_real_stock_data(symbol)

    # Validation Check
    if raw_data["current_price"] == 0.0:
        return {
            "symbol": symbol,
            "trust_score": 0.0,
            "verdict": "DATA ERROR",
            "error": "Could not fetch financial data."
        }

    # 2. Run Symbolic Engine (The "Police" First)
    # We convert raw dict to Pydantic model for validation
    stock_model = StockData(**raw_data)
    rule_result = rule_engine.evaluate(stock_model)

    # 3. Run Neural Engine (The "Brain")
    # We pass the data to LLM for qualitative reasoning
    print("Querying Llama 3 (Groq)...")
    llm_response = llm_runner.analyze_stock(symbol, raw_data)

    # Handle response (Dict or String)
    if isinstance(llm_response, str):
        try:
            llm_json = json.loads(llm_response)
            reasoning = llm_json.get("reasoning", "No reasoning provided.")
        except:
            reasoning = str(llm_response)
    else:
        # It's already a dict from the Universal Fuzzy Parser
        reasoning = llm_response.get("reasoning", "No reasoning provided.")

    # 4. Final Payload
    return {
        "symbol": symbol,
        "trust_score": rule_result["score"],
        "verdict": rule_result["verdict"],
        "price": raw_data["current_price"],
        "pe_ratio": raw_data["pe_ratio"],
        "metrics": {
            "current_price": raw_data["current_price"],
            "pe_ratio": raw_data["pe_ratio"],
            "debt_to_equity": raw_data["debt_to_equity"],
            "revenue_growth": raw_data["revenue_growth"],
            "cash_reserves": raw_data["cash_reserves"],
            "operating_costs": raw_data["operating_costs"],
            "net_income": raw_data["net_income"],
            "profit_margins": raw_data["profit_margins"],
            "roe": raw_data["roe"],
            "free_cash_flow": raw_data["free_cash_flow"],
            "dividend_yield": raw_data["dividend_yield"],
            "analyst_target": raw_data["analyst_target"],
            "sector": raw_data["sector"]
        },
        "breakdown": rule_result["breakdown"],
        "rule_violations": [v for v in rule_result["breakdown"] if v["status"] == "FAIL"],
        "llm_reasoning": reasoning
    }

if __name__ == "__main__":
    # Test Run
    result = run_analysis("NVDA")
    print(json.dumps(result, indent=2))
