
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

class LLMRunner:
    """
    Interface for the Groq API to handle text analysis.
    """
    def __init__(self, api_key: str = None, model_id: str = "llama-3.1-8b-instant"):
        """
        Initialize the LLM Interface with Groq client.
        
        Args:
            api_key (str): Groq API key.
            model_id (str): Groq model identifier.
        """
        self.model_id = model_id
        # Use provided key or fallback to env var
        key = api_key or os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=key)
        
    def load_model(self):
        """
        Placeholder for compatibility. API client is initialized in __init__.
        """
        print("Groq API client initialized.")

    def analyze_stock(self, symbol: str, price_data: dict) -> dict:
        """
        Analyze the stock data and return a structured dictionary.
        
        Args:
            symbol (str): Stock symbol.
            price_data (dict): Dictionary containing price and financial metrics.
            
        Returns:
            dict: Parsed and sanitized JSON response.
        """
        json_str = self.analyze_json(symbol, price_data)
        
        try:
            # 1. Parse string to dict
            try:
                raw_data = json.loads(json_str)
            except:
                # Fallback: try to find the first { and last }
                start = json_str.find('{')
                end = json_str.rfind('}') + 1
                raw_data = json.loads(json_str[start:end])
            
            # Preserve reasoning if available before flattening
            reasoning = raw_data.get("reasoning", "Parsed via Universal Translator")
            
            # 2. Handle Nesting (The "TSLA" wrapper)
            # Flatten the dict if the first value is also a dict
            if len(raw_data) == 1 and isinstance(list(raw_data.values())[0], dict):
                raw_data = list(raw_data.values())[0]
            elif "extracted_metrics" in raw_data:
                raw_data = raw_data["extracted_metrics"]
                # Double check if extracted_metrics is ALSO nested
                if len(raw_data) == 1 and isinstance(list(raw_data.values())[0], dict):
                    raw_data = list(raw_data.values())[0]
            
            # 3. Fuzzy Key Mapping (The Nuclear Fix)
            clean_data = {}
            key_map = {
                "symbol": ["symbol", "ticker"],
                "current_price": ["price", "current"],
                "pe_ratio": ["pe_", "p/e", "price_to_earnings"],
                "debt_to_equity": ["debt", "d/e"],
                "revenue_growth": ["revenue", "growth"],
                "cash_reserves": ["cash", "reserves"],
                "operating_costs": ["operating", "costs", "expenses"],
                "net_income": ["income", "profit", "net"]
            }
            
            # Iterate over every messy key from the AI
            for dirty_key, value in raw_data.items():
                dirty_key_lower = dirty_key.lower()
                # Check which standard key it matches
                for standard_key, aliases in key_map.items():
                    if any(alias in dirty_key_lower for alias in aliases):
                        clean_data[standard_key] = value
                        break
                else:
                    # Keep original if no match found (fallback)
                    clean_data[dirty_key] = value
            
            # Ensure symbol is present if missing
            if "symbol" not in clean_data:
                clean_data["symbol"] = symbol
                
            return {"reasoning": reasoning, "extracted_metrics": clean_data}
            
        except Exception as e:
            print(f"Error in analyze_stock: {e}")
            return {"reasoning": f"Error: {str(e)}", "extracted_metrics": {}}

    def analyze_json(self, symbol: str, data: dict, mock: bool = False) -> str:
        """
        Analyze the stock data and return a JSON string.
        
        Args:
            symbol (str): Stock symbol.
            data (dict): Dictionary containing price and financial metrics.
            mock (bool): If True, return a mock response to bypass inference.
            
        Returns:
            str: JSON string containing reasoning and extracted_metrics.
        """
        if mock:
            return json.dumps({
                "reasoning": "Mock analysis: High volatility detected but strong cash flow.",
                "extracted_metrics": {
                    "symbol": "TSLA",
                    "current_price": 200.0,
                    "pe_ratio": 62.0,
                    "debt_to_equity": 0.5,
                    "revenue_growth": 0.09,
                    "cash_reserves": 1000.0,
                    "operating_costs": 500.0
                }
            })

        system_prompt = (
            "You are a Financial Analyst. Output JSON with keys: reasoning, extracted_metrics. "
            "extracted_metrics MUST contain: symbol, current_price, pe_ratio, debt_to_equity, "
            "revenue_growth, cash_reserves, operating_costs, net_income. "
            "CRITICAL FORMATTING RULE: Return the metrics as a FLAT JSON object. "
            "Do NOT nest them under the ticker symbol. Do NOT create a key like 'TSLA': {...}. "
            "The keys 'current_price', 'pe_ratio', etc., must be at the root of the 'extracted_metrics' object."
        )
        user_content = f"Symbol: {symbol}\nData: {data}"
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {e}")
            return json.dumps({"reasoning": f"API Error: {str(e)}", "extracted_metrics": {}})

# Legacy stub for backward compatibility
class LLMInterface(LLMRunner):
    def analyze_query(self, query: str) -> list:
        return []
