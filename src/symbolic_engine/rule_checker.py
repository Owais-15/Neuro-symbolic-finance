from pydantic import BaseModel
from typing import List, Dict, Any

class StockData(BaseModel):
    symbol: str = "UNKNOWN"
    sector: str = "Unknown"
    current_price: float = 0.0
    pe_ratio: float = 0.0
    debt_to_equity: float = 0.0
    revenue_growth: float = 0.0
    cash_reserves: float = 0.0
    operating_costs: float = 0.0
    net_income: float = 0.0
    profit_margins: float = 0.0
    roe: float = 0.0
    free_cash_flow: float = 0.0
    dividend_yield: float = 0.0
    analyst_target: float = 0.0

class FinancialRuleEngine:
    def evaluate(self, data: StockData) -> Dict[str, Any]:
        rules_passed = 0
        total_rules = 0
        breakdown = []

        def check_rule(name, condition, reason_pass, reason_fail):
            nonlocal rules_passed, total_rules
            total_rules += 1
            if condition:
                rules_passed += 1
                breakdown.append({"rule": name, "status": "PASS", "detail": reason_pass})
            else:
                breakdown.append({"rule": name, "status": "FAIL", "detail": reason_fail})

        # --- RULE 1: VALUATION (Context Aware) ---
        pe_limit = 60.0 if data.sector in ["Technology", "Communication Services"] else 30.0
        check_rule(
            "Valuation",
            data.pe_ratio < pe_limit and data.pe_ratio > 0,
            f"P/E {data.pe_ratio:.1f} is within limit {pe_limit}",
            f"P/E {data.pe_ratio:.1f} exceeds limit {pe_limit}"
        )

        # --- RULE 2: SOLVENCY ---
        check_rule(
            "Solvency",
            data.debt_to_equity < 200.0, # Yahoo returns D/E as %, so 200 = 2.0 ratio
            f"Debt/Equity {data.debt_to_equity/100:.2f} is healthy (< 2.0)",
            f"Debt/Equity {data.debt_to_equity/100:.2f} is risky (> 2.0)"
        )

        # --- RULE 3: GROWTH ---
        check_rule(
            "Growth",
            data.revenue_growth > 0.05,
            f"Revenue Growth {data.revenue_growth:.1%} > 5%",
            f"Revenue Growth {data.revenue_growth:.1%} is sluggish"
        )

        # --- RULE 4: PROFITABILITY ---
        check_rule(
            "Profitability",
            data.profit_margins > 0.10,
            f"Net Margin {data.profit_margins:.1%} is healthy",
            f"Net Margin {data.profit_margins:.1%} is thin"
        )

        # --- RULE 5: EFFICIENCY (ROE) ---
        check_rule(
            "Efficiency",
            data.roe > 0.15,
            f"ROE {data.roe:.1%} indicates strong management",
            f"ROE {data.roe:.1%} is below target 15%"
        )

        # --- RULE 6: CASH HEALTH ---
        check_rule(
            "Free Cash Flow",
            data.free_cash_flow > 0,
            "Generating positive Free Cash Flow",
            "Burning cash (Negative FCF)"
        )

        # --- RULE 7: LIQUIDITY (The Apple Fix) ---
        # Only penalize cash if they are LOSING money
        if data.net_income < 0:
            check_rule(
                "Liquidity Runway",
                data.cash_reserves > data.operating_costs,
                f"Cash reserves (${data.cash_reserves/1e6:.1f}M) cover burn rate (${data.operating_costs/1e6:.1f}M)",
                f"CRITICAL: Cash (${data.cash_reserves/1e6:.1f}M) insufficient for burn (${data.operating_costs/1e6:.1f}M)"
            )
        else:
            # Use check_rule for consistency (profitable companies pass automatically)
            check_rule(
                "Liquidity Runway",
                True,
                "Company is profitable (liquidity not at risk)",
                "N/A"
            )

        # Calculate Score
        final_score = (rules_passed / total_rules) * 100 if total_rules > 0 else 0.0
        
        return {
            "score": round(final_score, 1),
            "verdict": "TRUSTED" if final_score >= 70 else "CAUTION" if final_score >= 40 else "RISKY",
            "breakdown": breakdown
        }
