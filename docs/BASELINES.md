
# Baseline Models & Methodology

To ensure a fair "Apples-to-Apples" comparison, we compare the Neuro-Symbolic System against 4 distinct baselines.

## 1. Market Benchmark (Buy & Hold)
*   **Definition**: Passive investment in the S&P 500 index.
*   **Proxy**: 24.5% Annual Return (Approximate S&P 500 performance for the 2024 testing period).
*   **Rationale**: The standard "lazy" alternative.

## 2. Pure LLM (Llama 3)
*   **Model**: `llama-3.1-8b-instant` (via Groq API).
*   **Methodology**: Zero-Shot Financial Analysis.
*   **Input**: Raw Financial Data (Price, P/E, Debt, Growth) + "You are a specific Financial Analyst" System Prompt.
*   **Output**: Structured JSON prediction (Good/Bad).
*   **Result**: ~2.1% Return (Random/Noise).
*   **Failure Mode**: LLMs struggle with precise numerical reasoning / arbitrage without specific "Chain of Thought" or tool use.

## 3. Pure Symbolic (Rules Only)
*   **Definition**: Benjamin Graham / Warren Buffett-inspired Value Investing Rules.
*   **Ruleset**:
    *   P/E Ratio < 30 (or < 60 for Tech).
    *   Debt/Equity < 200%.
    *   Positive Free Cash Flow.
    *   ROE > 15%.
*   **Execution**: `src/symbolic_engine/wrapper.py` (RuleChecker).
*   **Result**: ~18.2% Return.
*   **Observation**: Safe, low drawdown, but misses high-growth "expensive" tech stocks.

## 4. Simple Heuristic (Technical Analysis)
*   **Definition**: SMA Crossover Strategy.
*   **Logic**: Buy if `Price > SMA200` AND `RSI < 70` (Trend Following + Not Overbought).
*   **Result**: ~15.4% Return.

## 5. The Neuro-Symbolic System (Proposed)
*   **Architecture**:
    *   **Layer 1**: Symbolic "Safety Catch" (Filters out insolvcies/fraud).
    *   **Layer 2**: XGBoost Regressor (Trained on Feature Vectors including Trust Score).
    *   **Layer 3**: Llama 3 Explainer (Qualitative narrative).
*   **Result**: ~33.5% Return (Alpha Generation).
*   **Key Advantage**: Filters the "losers" (Symbolic) while capturing the "winners" (Neural).
