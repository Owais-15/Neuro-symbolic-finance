
"""
ONE-CLICK REPRODUCTION SCRIPT
=============================
Usage: python scripts/run_repro.py [--smoke]

Orchestrates the full experiment pipeline:
1. Data Generation (Temporal Split)
2. Validation (Graveyard Test)
3. Analysis (Rigorous Metrics)
4. Artifacts (Thesis Charts)

Options:
  --smoke   Run on a small sample for CI/Quick Check.
"""

import os
import sys
import argparse
import subprocess
import time

def run_step(desc, cmd):
    print(f"\n🚀 [STEP] {desc}")
    print(f"   Command: {cmd}")
    start = time.time()
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ PASS ({time.time() - start:.2f}s)")
    except subprocess.CalledProcessError:
        print(f"❌ FAIL: {desc}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="Run quick smoke test")
    args = parser.parse_args()

    print("==================================================")
    print("    NEURO-SYMBOLIC THESIS: REPRODUCTION SUITE     ")
    print("==================================================")
    
    # 1. Data
    data_cmd = "python scripts/generation/generate_temporal_dataset.py"
    if args.smoke:
        data_cmd += " --limit 10"
        
    run_step("Data Validation", data_cmd)

    # 2. Validation
    # Graveyard test is fast.
    run_step("Safety Validation (Graveyard)", "python scripts/validation/validate_tier2.py")

    # 3. Metrics & Charts
    metrics_cmd = "python scripts/analysis/generate_rigorous_metrics.py"
    if args.smoke:
        metrics_cmd += " --smoke"
        
    run_step("Statistical Metrics (Bootstrap)", metrics_cmd)
    
    # Charts usually fine, but might look empty with 10 points. run anyway.
    run_step("Thesis Charts (Visuals)", "python scripts/generation/generate_thesis_charts.py")
    run_step("Model Comparison (Return Chart)", "python scripts/analysis/compare_models_returns.py")

    print("\n🏆 REPRODUCTION COMPLETE. Results in results/figures/ and results/metrics/")

if __name__ == "__main__":
    main()
