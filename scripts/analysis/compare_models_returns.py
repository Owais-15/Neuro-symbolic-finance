"""
MODEL COMPARISON: AVERAGE RETURNS
Visualizes the profitability of different architectures.

Baselines:
1. Buy & Hold (Market Benchmark)
2. Pure LLM (Llama 3 only)
3. Simple Heuristic (SMA Crossover)
4. Pure Rules (Symbolic Only)
5. Neuro-Symbolic (Our Hybrid System)
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 12

OUTPUT_DIR = "results/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_return_comparison():
    print("📊 Generating Model Return Comparison...")
    
    # Rigorous Metrics (Bootstrap N=1000)
    # Market: 21.22% (CI: [16.9, 25.9])
    # Heuristic: 18.04% (CI: [12.3, 23.9])
    # Random: 19.71% (CI: [14.8, 25.4])
    # Neural: 35.43% (CI: [21.0, 51.8])
    # Neuro-Symbolic: 44.61% (CI: [30.4, 60.1])
    
    models = ['Market', 'Random', 'Heuristic', 'Neural (XGB)', 'Neuro-Symbolic']
    means = [21.2, 19.7, 18.0, 35.4, 44.6]
    errors = [4.5, 5.3, 5.8, 15.4, 14.8] # Approx symmetric error from CI width/2
    
    colors = ['#95a5a6', '#7f8c8d', '#e74c3c', '#3498db', '#2ecc71'] # Gray, DarkGray, Red, Blue, Green
    
    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models, means, yerr=errors, capsize=10, color=colors, edgecolor='black', width=0.6, alpha=0.9)
    
    # Add Threshold Lines
    plt.axhline(y=21.2, color='#e67e22', linestyle='--', linewidth=1.5, label='Market Benchmark (21.2%)')
    
    # Labels and Title
    plt.ylabel('Annual Return (%)', fontsize=12, fontweight='bold')
    plt.title('Performance with Uncertainty (95% CI)', fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='upper left')
    
    # Add Value Labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.ylim(0, 70)
    plt.tight_layout()
    
    output_path = f"{OUTPUT_DIR}/model_return_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Chart Saved: {output_path}")

if __name__ == "__main__":
    generate_return_comparison()
