
import pytest
from neural_engine.llm_interface import LLMInterface
from symbolic_engine.rule_checker import RuleChecker

def test_neural_engine_instantiation():
    """Test that the Neural Engine can be instantiated."""
    engine = LLMInterface()
    assert engine is not None

def test_symbolic_engine_instantiation():
    """Test that the Symbolic Engine can be instantiated."""
    engine = RuleChecker()
    assert engine is not None

def test_workflow_stub():
    """Test the basic data flow between stubs."""
    neural = LLMInterface()
    symbolic = RuleChecker()
    
    claims = neural.analyze_query("test")
    assert isinstance(claims, list)
    
    result = symbolic.validate_claims(claims)
    assert "trust_score" in result

def test_financial_rule_engine_tesla():
    """Test case for Tesla (failing P/E)."""
    from symbolic_engine.rule_checker import FinancialRuleEngine, StockData
    
    engine = FinancialRuleEngine()
    # Dummy data for Tesla: High P/E (>50)
    data = StockData(
        symbol="TSLA",
        current_price=200.0,
        pe_ratio=60.0,  # Violation: Overvalued (High) -> -0.4
        debt_to_equity=0.5,
        revenue_growth=0.1,
        cash_reserves=1000.0,
        operating_costs=500.0,
        net_income=100.0
    )
    
    result = engine.evaluate(data)
    # Expected score: 1.0 - 0.4 = 0.6
    assert result["trust_score"] == 0.6
    assert len(result["violations"]) == 1
    assert result["violations"][0]["violation"] == "Overvalued"

def test_financial_rule_engine_apple():
    """Test case for Apple (passing)."""
    from symbolic_engine.rule_checker import FinancialRuleEngine, StockData
    
    engine = FinancialRuleEngine()
    # Dummy data for Apple: All good
    data = StockData(
        symbol="AAPL",
        current_price=150.0,
        pe_ratio=25.0,
        debt_to_equity=1.5,
        revenue_growth=0.05,
        cash_reserves=2000.0,
        operating_costs=1000.0,
        net_income=500.0
    )
    
    result = engine.evaluate(data)
    # Expected score: 1.0
    assert result["trust_score"] == 1.0
    assert len(result["violations"]) == 0

def test_financial_rule_engine_insolvent():
    """Test case for critical failure (Insolvent)."""
    from symbolic_engine.rule_checker import FinancialRuleEngine, StockData
    
    engine = FinancialRuleEngine()
    data = StockData(
        symbol="BAD",
        current_price=10.0,
        pe_ratio=10.0,
        debt_to_equity=0.0,
        revenue_growth=0.0,
        cash_reserves=100.0,
        operating_costs=200.0,
        net_income=-50.0 # Violation: Insolvent (Critical) -> -1.0
    )
    
    result = engine.evaluate(data)
    assert result["trust_score"] == 0.0
    assert any(v["violation"] == "Insolvent Risk" for v in result["violations"])

def test_orchestrator_integration():
    """Test the full orchestrator pipeline with mocked LLM."""
    from unittest.mock import MagicMock, patch
    import json
    from orchestrator.main import run_analysis
    
    # Mock LLMRunner to avoid loading model
    with patch("orchestrator.main.LLMRunner") as MockLLMRunner:
        mock_instance = MockLLMRunner.return_value
        
        # Mock analyze_json return value
        mock_response = {
            "reasoning": "Company looks good.",
            "extracted_metrics": {
                "symbol": "AAPL",
                "current_price": 150.0,
                "pe_ratio": 25.0,
                "debt_to_equity": 1.5,
                "revenue_growth": 0.05,
                "cash_reserves": 2000.0,
                "operating_costs": 1000.0,
                "net_income": 500.0
            }
        }
        mock_instance.analyze_json.return_value = json.dumps(mock_response)
        
        result = run_analysis("AAPL")
        
        assert result["symbol"] == "AAPL"
        assert result["trust_score"] == 1.0
        assert len(result["rule_violations"]) == 0
        assert result["final_verdict"] == "Analysis Complete"

def test_orchestrator_json_error():
    """Test orchestrator handling of bad JSON from LLM."""
    from unittest.mock import MagicMock, patch
    from orchestrator.main import run_analysis
    
    with patch("orchestrator.main.LLMRunner") as MockLLMRunner:
        mock_instance = MockLLMRunner.return_value
        mock_instance.analyze_json.return_value = "This is not JSON."
        
        result = run_analysis("AAPL")
        
        assert result["trust_score"] == 0.0
        assert "Parsing Error" in result["final_verdict"]
