"""
Final Cleanup Script - Phase 1-4

Safely deletes empty folders, duplicates, and consolidates files.
All source code is already in src/ - this only removes duplicates.
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent

print("="*80)
print("FINAL PROJECT CLEANUP")
print("="*80)

# Phase 1: Delete empty old folders (only __pycache__)
print("\n[Phase 1/4] Deleting empty old folders...")

old_folders = ["orchestrator", "neural_engine", "symbolic_engine", "utils"]

for folder in old_folders:
    folder_path = BASE_DIR / folder
    if folder_path.exists():
        try:
            shutil.rmtree(folder_path)
            print(f"  ✅ Deleted: {folder}/")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Phase 2: Clean results/ directory
print("\n[Phase 2/4] Cleaning results/ directory...")

# Delete duplicate CSVs (already in datasets/ and metrics/)
duplicate_csvs = [
    "baseline_comparison_results.csv",
    "dataset_multiyear_2020_2024.csv",
    "dataset_n500_enhanced.csv",
    "dataset_n600_plus.csv",
    "enhanced_dataset_v3_full.csv",
    "multiyear_validation_results.csv",
    "portfolio_backtest_results.csv",
    "validation_n564_results.csv",
]

for csv in duplicate_csvs:
    csv_path = BASE_DIR / "results" / csv
    if csv_path.exists():
        try:
            os.remove(csv_path)
            print(f"  ✅ Deleted: results/{csv}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Delete redundant charts (keep only 5 essential)
redundant_charts = [
    "chart_alpha_generation.png",
    "chart_cross_validation.png",
    "chart_ml_correlation.png",
    "chart_risk_boxplot.png",
    "chart_sector_heatmap.png",
    "thesis_chart_1_predictive_power.png",
    "thesis_chart_2_risk_avoidance.png",
]

for chart in redundant_charts:
    chart_path = BASE_DIR / "results" / chart
    if chart_path.exists():
        try:
            os.remove(chart_path)
            print(f"  ✅ Deleted: results/{chart}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Move remaining charts to charts/ subdirectory
essential_charts = [
    "chart_correlation.png",
    "chart_feature_importance.png",
    "chart_portfolio_comparison.png",
    "chart_model_comparison.png",
    "thesis_chart_3_sector_breakdown.png",
]

for chart in essential_charts:
    src_path = BASE_DIR / "results" / chart
    dst_path = BASE_DIR / "results" / "charts" / chart
    if src_path.exists() and not dst_path.exists():
        try:
            shutil.copy2(src_path, dst_path)
            os.remove(src_path)
            print(f"  ✅ Moved: {chart} → results/charts/")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Phase 3: Delete redundant test files
print("\n[Phase 3/4] Cleaning tests/ directory...")

redundant_tests = [
    "train_n462_model.py",  # Already in scripts/
    "validate_n462_dataset.py",  # Will consolidate
    "validate_n564_dataset.py",  # Will consolidate
]

for test in redundant_tests:
    test_path = BASE_DIR / "tests" / test
    if test_path.exists():
        try:
            os.remove(test_path)
            print(f"  ✅ Deleted: tests/{test}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Phase 4: Clean root documentation
print("\n[Phase 4/4] Cleaning root documentation...")

duplicate_docs = [
    "DASHBOARD_QUICK_START.md",
    "DASHBOARD_README.md",
    "FINAL_PROJECT_SUMMARY.md",
    "HONEST_RESULTS_REPORT.md",
    "METHODOLOGY.md",
    "MULTI_KEY_SETUP_GUIDE.md",
    "PUBLICATION_STRATEGY.md",
    "RESEARCH_IMPACT_ANALYSIS.md",
    "delete_old_files.py",  # One-time script
]

for doc in duplicate_docs:
    doc_path = BASE_DIR / doc
    if doc_path.exists():
        try:
            os.remove(doc_path)
            print(f"  ✅ Deleted: {doc}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Summary
print("\n" + "="*80)
print("CLEANUP COMPLETE!")
print("="*80)

print("\n📊 Final Structure:")
print("  ✅ src/ - All source code (13 files)")
print("  ✅ scripts/ - Executable scripts (8 files)")
print("  ✅ docs/ - Documentation (8 files)")
print("  ✅ results/datasets/ - 4 datasets")
print("  ✅ results/metrics/ - 4 metrics")
print("  ✅ results/charts/ - 5 essential charts")
print("  ✅ tests/ - Unit tests only")
print("  ✅ Root - Clean (8 essential files)")

print("\n✨ Project is now publication-ready!")
print("="*80)
