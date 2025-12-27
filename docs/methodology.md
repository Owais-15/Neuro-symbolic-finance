# Methodology: Theoretical Basis for Symbolic Rules

This document outlines the academic and financial theory underpinning the 7 symbolic rules used in the Neuro-Symbolic Agent V2.0. Each rule is derived from established financial literature to ensure the "Safety Catch" mechanism is grounded in rigorous theory rather than arbitrary heuristics.

## 1. Valuation Check (Context Aware P/E)
**Rule**: Buy if P/E is within sector limits (e.g., < 30 for General, < 60 for Tech).

*   **Theoretical Basis**: Meaningful P/E thresholds prevent overpayment for future earnings.
*   **Citation**: Graham, B., & Dodd, D. (1934). *Security Analysis*. McGraw-Hill.
    *   *Note*: Graham advises against purchasing stocks with P/E ratios significantly above the market average, arguing that high multiples imply speculative rather than investment value.

## 2. Solvency (The Leverage Limit)
**Rule**: Buy if Debt/Equity < 2.0.

*   **Theoretical Basis**: High leverage increases the probability of default/bankruptcy during economic downturns.
*   **Citation**: Altman, E. I. (1968). "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy". *The Journal of Finance*.
    *   *Note*: The Altman Z-Score heavily weights the "Retained Earnings / Total Assets" and "Market Value of Equity / Book Value of Total Liabilities" ratios. Our simplified D/E check acts as a first-order proxy for this risk.

## 3. Growth (The Momentum Check)
**Rule**: Buy if Revenue Growth > 5%.

*   **Theoretical Basis**: Sustainable stock price appreciation requires underlying business expansion (GARP - Growth At a Reasonable Price).
*   **Citation**: Lynch, P. (1989). *One Up On Wall Street*. Simon & Schuster.
    *   *Note*: Lynch emphasizes the "PEG Ratio" (Price/Earnings to Growth). By demanding minimum positive growth, we filter out "Value Traps" (cheap but dying companies).

## 4. Profitability (The Margin Check)
**Rule**: Buy if Net Profit Margin > 10%.

*   **Theoretical Basis**: Margins indicate competitive advantage (moat) and operational efficiency.
*   **Citation**: Soliman, M. T. (2008). "The Use of DuPont Analysis by Market Participants". *The Accounting Review*.
    *   *Note*: The DuPont Identity decomposes ROE into Profit Margin, Asset Turnover, and Financial Leverage. High margins are the most sustainable driver of long-term ROE.

## 5. Efficiency (Return on Equity)
**Rule**: Buy if ROE > 15%.

*   **Theoretical Basis**: ROE measures management's ability to allocate capital effectively.
*   **Citation**: Buffett, W. E. (Selected Letters). *Berkshire Hathaway Shareholder Letters*.
    *   *Note*: Buffett consistently cites "Return on Invested Capital" (ROIC) or ROE as the primary metric for evaluating management quality, often looking for strictly >15%.

## 6. Cash Health (Free Cash Flow)
**Rule**: Buy if Free Cash Flow (FCF) > 0.

*   **Theoretical Basis**: Earnings can be manipulated (accrual accounting); Cash Flow is truth.
*   **Citation**: Jensen, M. C. (1986). "Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers". *American Economic Review*.
    *   *Note*: Positive FCF reduces the need for external financing (dilution or debt) and allows for shareholder returns (dividends/buybacks).

## 7. Liquidity Runway (The Insolvency Safety Catch)
**Rule**: **CRITICAL FAIL** if (Net Income < 0) AND (Cash < Operating Costs).

*   **Theoretical Basis**: Calculating the "Runway" prevents investment in companies facing imminent liquidity crises.
*   **Citation**: Ries, E. (2011). *The Lean Startup*. Crown Business.
    *   *References*: While Ries focuses on startups, the logic applies to distressed public equities. "Burn Rate" exceeding cash reserves without a path to profitability is a precursor to insolvency.

---
**Summary of Approach**:
By combining these constraints, we implement a **"Safety First"** investment strategy (Safety First Ratio, Roy, 1952) that prioritizes the avoidance of catastrophic loss (bankruptcy) over the maximization of speculative gain.
