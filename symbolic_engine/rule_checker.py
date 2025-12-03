
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class StockData(BaseModel):
    symbol: str
    current_price: float
    pe_ratio: float
    debt_to_equity: float
    revenue_growth: float
    cash_reserves: float
    operating_costs: float
    net_income: float

class FinancialRuleEngine:
    """
    Symbolic Rule Engine for verifying claims against logic rules.
    """
    def evaluate(self, data: StockData) -> Dict[str, Any]:
        """
        Validate the provided stock data against hard-coded financial rules.
        
        Args:
            data (StockData): Structured financial data.
            
        Returns:
            dict: Validation results including a trust score and violations.
        """
        violations = []
        trust_score = 1.0

        # Rule 1 (Valuation)
        if data.pe_ratio > 50:
            violations.append({"rule": "Valuation", "violation": "Overvalued", "severity": "High"})
            trust_score -= 0.4

        # Rule 2 (Solvency)
        if data.debt_to_equity > 2.0:
            violations.append({"rule": "Solvency", "violation": "High Debt Risk", "severity": "High"})
            trust_score -= 0.4

        # Rule 3 (Growth)
        if data.revenue_growth < 0.0:
            violations.append({"rule": "Growth", "violation": "Declining Revenue", "severity": "Medium"})
            trust_score -= 0.2

        # Rule 4 (Runway) - UPDATED
        # Only flag if company is losing money AND has low cash
        if (data.net_income < 0) and (data.cash_reserves < data.operating_costs):
            violations.append({"rule": "Runway", "violation": "Insolvent Risk", "severity": "Critical"})
            trust_score -= 1.0

        # Clamp trust score to be non-negative
        trust_score = max(0.0, trust_score)

        return {
            "trust_score": round(trust_score, 2),
            "violations": violations
        }

# Legacy stub for backward compatibility if needed, or can be removed if we fully switch
class RuleChecker:
    def validate_claims(self, claims: list) -> dict:
        return {"trust_score": 0.0, "details": []}
