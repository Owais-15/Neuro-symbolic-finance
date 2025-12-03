import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Ensure we can import from sibling directories if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_DIR = "results"
DATA_FILE = os.path.join(RESULTS_DIR, "thesis_comparison_data.csv")

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return None
    
    df = pd.read_csv(DATA_FILE)
    
    # Clean data: Convert scores to numeric, handle errors
    df['Baseline_Score'] = pd.to_numeric(df['Baseline_Score'], errors='coerce')
    df['Trust_Score'] = pd.to_numeric(df['Trust_Score'], errors='coerce')
    df['PE_Ratio'] = pd.to_numeric(df['PE_Ratio'], errors='coerce')
    
    # Drop rows with NaN scores for visualization
    df = df.dropna(subset=['Baseline_Score', 'Trust_Score'])
    return df

def plot_safety_gap(df):
    """
    Chart 1: The 'Safety Gap' (Bar Chart) for Distressed/Volatile stocks.
    """
    subset = df[df['Sector'] == 'Distressed/Volatile'].copy()
    
    if subset.empty:
        print("No Distressed/Volatile data found for Safety Gap chart.")
        return

    # Melt for seaborn
    melted = subset.melt(id_vars=['Symbol'], value_vars=['Baseline_Score', 'Trust_Score'], 
                         var_name='Agent', value_name='Score')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=melted, x='Symbol', y='Score', hue='Agent', palette={'Baseline_Score': '#ff9999', 'Trust_Score': '#99ff99'})
    
    plt.title("The Safety Gap: Baseline vs. Neuro-Symbolic (Distressed/Volatile)", fontsize=14)
    plt.ylabel("Safety Score (0-1)", fontsize=12)
    plt.xlabel("Stock Symbol", fontsize=12)
    plt.ylim(0, 1.1)
    plt.legend(title='Agent')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_path = os.path.join(RESULTS_DIR, "chart_safety_gap.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved {output_path}")
    plt.close()

def plot_valuation_discipline(df):
    """
    Chart 2: The 'Valuation Discipline' (Scatter Plot).
    """
    # Filter out extreme P/E outliers or N/A for better visualization
    subset = df[df['PE_Ratio'] > 0].copy()
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=subset, x='PE_Ratio', y='Trust_Score', hue='Sector', style='Sector', s=100)
    
    plt.title("Valuation Discipline: P/E Ratio vs. Trust Score", fontsize=14)
    plt.xlabel("P/E Ratio", fontsize=12)
    plt.ylabel("Trust Score", fontsize=12)
    plt.ylim(-0.1, 1.1)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    output_path = os.path.join(RESULTS_DIR, "chart_valuation_discipline.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved {output_path}")
    plt.close()

def plot_confusion_matrix(df):
    """
    Chart 3: The 'Confusion Matrix' (Heatmap) comparing classifications.
    """
    def categorize(score):
        if score >= 0.7: return "Safe"
        elif score >= 0.4: return "Caution"
        else: return "Risky"

    df['Baseline_Class'] = df['Baseline_Score'].apply(categorize)
    df['Neuro_Class'] = df['Trust_Score'].apply(categorize)
    
    # Create confusion matrix
    categories = ["Safe", "Caution", "Risky"]
    cm = pd.crosstab(df['Baseline_Class'], df['Neuro_Class'], rownames=['Baseline (LLM)'], colnames=['Neuro-Symbolic'])
    
    # Reindex to ensure all categories exist
    cm = cm.reindex(index=categories, columns=categories, fill_value=0)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, square=True, annot_kws={"size": 16})
    
    plt.title("Classification Comparison", fontsize=14)
    
    output_path = os.path.join(RESULTS_DIR, "chart_confusion_matrix.png")
    plt.savefig(output_path, dpi=300)
    print(f"Saved {output_path}")
    plt.close()

def main():
    print("Generating visualizations...")
    df = load_data()
    if df is not None:
        plot_safety_gap(df)
        plot_valuation_discipline(df)
        plot_confusion_matrix(df)
        print("Visualization complete.")

if __name__ == "__main__":
    main()
