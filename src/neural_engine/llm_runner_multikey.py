"""
Enhanced LLM Runner with Multi-Key Support

Automatically rotates between multiple Groq API keys on rate limits.
"""

import os
from groq import Groq
import json
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / 'utils'))

try:
    from groq_key_manager import get_groq_api_key, handle_groq_error
    USE_KEY_MANAGER = True
except ImportError:
    USE_KEY_MANAGER = False
    from dotenv import load_dotenv
    load_dotenv()

def analyze_stock(symbol: str, data: dict, max_retries=3):
    """
    Analyze stock using Groq LLM with automatic key rotation on rate limits.
    
    Args:
        symbol: Stock ticker
        data: Stock data dictionary
        max_retries: Maximum number of retries on rate limit
    
    Returns:
        dict: Analysis results
    """
    for attempt in range(max_retries):
        try:
            # Get current API key
            if USE_KEY_MANAGER:
                api_key = get_groq_api_key()
            else:
                api_key = os.getenv("GROQ_API_KEY")
            
            # Create Groq client
            client = Groq(api_key=api_key)
            
            # Prepare prompt
            prompt = f"""
            Analyze this stock and provide a brief assessment:
            
            Symbol: {symbol}
            Sector: {data.get('sector', 'Unknown')}
            P/E Ratio: {data.get('pe_ratio', 0):.2f}
            Debt/Equity: {data.get('debt_to_equity', 0):.2f}
            Revenue Growth: {data.get('revenue_growth', 0):.2%}
            Profit Margins: {data.get('profit_margins', 0):.2%}
            ROE: {data.get('roe', 0):.2%}
            
            Provide a JSON response with:
            - sentiment: "positive", "neutral", or "negative"
            - confidence: 0-100
            - brief_reason: one sentence explanation
            """
            
            # Query LLM
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Try to extract JSON
            try:
                # Find JSON in response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "sentiment": "neutral",
                        "confidence": 50,
                        "brief_reason": "Analysis completed"
                    }
            except json.JSONDecodeError:
                result = {
                    "sentiment": "neutral",
                    "confidence": 50,
                    "brief_reason": "Analysis completed"
                }
            
            return result
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a rate limit error
            if "rate_limit" in error_str.lower() or "429" in error_str:
                if USE_KEY_MANAGER:
                    # Try to rotate key
                    if handle_groq_error(e):
                        print(f"   Retrying with different key (attempt {attempt + 1}/{max_retries})...")
                        continue
                    else:
                        # All keys exhausted
                        if attempt < max_retries - 1:
                            print(f"   All keys rate-limited, waiting before retry...")
                            import time
                            time.sleep(5)
                            continue
                else:
                    # Single key mode - wait and retry
                    if attempt < max_retries - 1:
                        print(f"   Rate limit hit, waiting 5 seconds...")
                        import time
                        time.sleep(5)
                        continue
            
            # Other errors or max retries reached
            print(f"   LLM Error: {error_str}")
            return {
                "sentiment": "neutral",
                "confidence": 0,
                "brief_reason": f"Error: {error_str[:50]}"
            }
    
    # Max retries exhausted
    return {
        "sentiment": "neutral",
        "confidence": 0,
        "brief_reason": "Max retries exhausted"
    }


if __name__ == "__main__":
    # Test the enhanced LLM runner
    print("Testing Enhanced LLM Runner with Multi-Key Support...")
    print("="*60)
    
    test_data = {
        'sector': 'Technology',
        'pe_ratio': 25.5,
        'debt_to_equity': 0.5,
        'revenue_growth': 0.15,
        'profit_margins': 0.20,
        'roe': 0.18
    }
    
    result = analyze_stock("AAPL", test_data)
    print(f"\nResult: {result}")
