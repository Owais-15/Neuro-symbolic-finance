# Research Paper Outline: Neuro-Symbolic AI for Financial Prediction
**Target Audience**: Academic Reviewers / Quantitative Researchers

---

## 1. Abstract (The Hook)
*   **The Problem**: Black-box ML models (LLMs) fail in finance due to lack of explainability and trust. Pure rule-based systems lack predictive power.
*   **The Solution**: A Neuro-Symbolic architecture combining XGBoost (Neuro) with Financial Rules (Symbolic).
*   **The Result**: Achieved **r=0.25** (p < 1e-7) out-of-sample correlation and **0.88 Sharpe Ratio** on N=461 stocks.
*   **Key Contribution**: Demonstrating that "Hybrid Explainability" outperforms both pure ML (r=0.03) and pure rules (r=0.12).

---

## 2. Introduction
*   **Context**: The EU AI Act and financial regulations demand explainability.
*   **Gap**: Existing solutions are either "accurate but opaque" (Deep Learning) or "transparent but weak" (Rules).
*   **Your Approach**: A "Safety First" pipeline. Rules filter risk (Symbolic), ML ranks growth (Neuro).
*   **Thesis Statement**: "We propose a dual-system architecture that uses symbolic reasoning as a 'conscience' and machine learning as a 'brain', achieving superior risk-adjusted returns."

---

## 3. Methodology (The Core)
*   **Data Pipeline**:
    *   **Strict Temporal Split**: Defined Cutoff Date (Jan 1, 2024). No "time travel" (Reference the Hindsight Bias fix).
*   **Symbolic Engine (The "Safety Catch")**:
    *   List the 7 Rules (Citation: Graham, Altman, Buffett).
    *   Explain the "Trust Score" metric.
*   **Neural Engine (The "Predictor")**:
    *   XGBoost Regressor.
    *   Inputs: Technicals + Fundamentals + **Trust Score** (This is the neuro-symbolic fusion).
    *   Training: TimeSeriesSplit (5-fold) to prevent overfitting.
*   **The Graveyard Test**:
    *   Explicitly describe how you tested on bankrupt firms (SVB, WeWork).

---

## 4. Experiments & Results
*   **Setup**: Training on 2020-2023, Testing on Jan 2024–Dec 2024.
*   **Main Result**:
    *   Show `01_predictive_power.png`: The r=0.25 scatter plot.
    *   "The slope implies a 1% predicted rise correlates to a 0.25% actual rise."
*   **Model Comparison**:
    *   Show `03_model_comparison.png` or `model_return_comparison.png`.
    *   Neuro-Symbolic (~33.5%) vs Market (~24.5%).
*   **Risk Analysis**:
    *   Show `02_survivorship_defense.png`.
    *   "The model successfully rejected 4/4 known bankrupt stocks."

---

## 5. Discussion
*   **Why r=0.25 Matters**:
    *   Acknowledge that 0.25 is "low" compared to physics, but "elite" in finance.
*   **Survivorship Bias**:
    *   Admit the limitation (using 2024 S&P list).
    *   Estimate impact (likely 1-3% inflation).
*   **Explainability**:
    *   Show an example verdict (e.g., "Rejected LULU because PE > 60").

---

## 6. Conclusion
*   **Summary**: Successfully unified rules and ML.
*   **Impact**: Practical tool for regulated asset management.
*   **Future Work**: Expanding dataset, adding Transaction Costs.

---
**References**:
*   Graham & Dodd (Valuation)
*   Altman (Z-Score)
*   Kahneman (System 1 vs System 2 thinking - heavily applicable to Neuro-Symbolic)
