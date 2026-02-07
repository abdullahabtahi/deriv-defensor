"""
ML Pipeline Results Visualization Suite
Generates publication-ready charts for Deriv Defensor ML models
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Arial', 'Helvetica']

# Deriv color palette
DERIV_RED = '#FF444F'
DERIV_BLUE = '#3B82F6'
DERIV_TEAL = '#06B6D4'
DERIV_PURPLE = '#9333EA'
DERIV_GREEN = '#10B981'
DERIV_AMBER = '#F59E0B'
DERIV_GRAY = '#6B7280'

def load_results():
    """Load all result JSON files"""
    with open('models/production_validation_results.json', 'r') as f:
        prod_results = json.load(f)

    with open('models/pattern_discovery_results.json', 'r') as f:
        pattern_results = json.load(f)

    return prod_results, pattern_results


def plot_model_robustness(prod_results):
    """
    Chart 1: Model Performance Across Drift Conditions
    Shows how model degrades from ideal to heavy production drift
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Model Robustness: Performance Under Production Drift',
                 fontsize=20, fontweight='bold', y=1.02)

    conditions = ['ideal', 'light_drift', 'moderate_drift', 'heavy_drift']
    condition_labels = ['Ideal\n(Synthetic)', 'Week 1\n(Light)', 'Month 1\n(Moderate)', 'Quarter 1\n(Heavy)']

    # Extract metrics
    auc_scores = [prod_results[c]['auc'] for c in conditions]
    precision_scores = [prod_results[c]['precision'] for c in conditions]
    recall_scores = [prod_results[c]['recall'] for c in conditions]

    # Plot 1: AUC Degradation
    ax1 = axes[0]
    bars = ax1.bar(condition_labels, auc_scores, color=[DERIV_GREEN, DERIV_TEAL, DERIV_AMBER, DERIV_RED])
    ax1.set_ylabel('AUC Score', fontsize=14, fontweight='bold')
    ax1.set_title('AUC Degradation Over Time', fontsize=16, fontweight='bold')
    ax1.set_ylim(0.98, 1.0)
    ax1.axhline(y=0.99, color='gray', linestyle='--', alpha=0.5, label='99% Threshold')

    # Add value labels
    for i, (bar, score) in enumerate(zip(bars, auc_scores)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0002,
                f'{score:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # Plot 2: Precision vs Recall Trade-off
    ax2 = axes[1]
    x = np.arange(len(condition_labels))
    width = 0.35

    bars1 = ax2.bar(x - width/2, precision_scores, width, label='Precision', color=DERIV_BLUE)
    bars2 = ax2.bar(x + width/2, recall_scores, width, label='Recall', color=DERIV_PURPLE)

    ax2.set_ylabel('Score', fontsize=14, fontweight='bold')
    ax2.set_title('Precision vs Recall Under Drift', fontsize=16, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(condition_labels)
    ax2.set_ylim(0.90, 1.0)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height + 0.002,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)

    # Plot 3: Cross-Validation Stability
    ax3 = axes[2]
    cv_data = prod_results['cross_validation']

    # Box plot simulation with min/max/mean
    positions = [1]
    bp = ax3.boxplot([[cv_data['min_auc'], cv_data['mean_auc'], cv_data['max_auc']]],
                     positions=positions, widths=0.4, patch_artist=True,
                     boxprops=dict(facecolor=DERIV_TEAL, alpha=0.7),
                     medianprops=dict(color='black', linewidth=2),
                     whiskerprops=dict(color=DERIV_GRAY),
                     capprops=dict(color=DERIV_GRAY))

    ax3.set_ylabel('AUC Score', fontsize=14, fontweight='bold')
    ax3.set_title('Cross-Validation Stability (5-Fold)', fontsize=16, fontweight='bold')
    ax3.set_xticks([1])
    ax3.set_xticklabels(['CV Results'])
    ax3.set_ylim(0.990, 0.998)

    # Add annotations
    ax3.text(1.3, cv_data['mean_auc'], f"Mean: {cv_data['mean_auc']:.4f}\nStd: {cv_data['std_auc']:.4f}",
            fontsize=11, va='center')

    ax3.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('models/visualizations/1_model_robustness.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 1_model_robustness.png")
    plt.close()


def plot_feature_interactions(pattern_results):
    """
    Chart 2: Top Discovered Feature Interactions
    Network-style visualization showing synergy effects
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('AI-Discovered Feature Interactions: Beyond Explicit Rules',
                 fontsize=20, fontweight='bold', y=0.98)

    top_patterns = pattern_results['discovered_patterns'][:8]

    # Plot 1: Synergy Effect Bar Chart
    ax1 = axes[0]
    patterns = [p['pattern'].replace(' × ', '\n×\n') for p in top_patterns]
    synergies = [p['synergy'] * 100 for p in top_patterns]  # Convert to percentage

    colors = [DERIV_RED if s > 50 else DERIV_AMBER if s > 30 else DERIV_TEAL for s in synergies]
    bars = ax1.barh(patterns, synergies, color=colors, edgecolor='black', linewidth=1.5)

    ax1.set_xlabel('Synergy Effect (%)', fontsize=14, fontweight='bold')
    ax1.set_title('Additional Churn Risk from Feature Combinations', fontsize=16, fontweight='bold')
    ax1.axvline(x=30, color='gray', linestyle='--', alpha=0.5, label='High Risk Threshold')

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, synergies)):
        ax1.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)

    # Plot 2: Risk Multiplier (Lift)
    ax2 = axes[1]
    lifts = [p['lift'] for p in top_patterns]
    evidence = [p['evidence_count'] for p in top_patterns]

    scatter = ax2.scatter(lifts, synergies, s=[e/3 for e in evidence],
                         c=synergies, cmap='YlOrRd', alpha=0.7, edgecolors='black', linewidth=2)

    ax2.set_xlabel('Risk Multiplier (Lift vs Baseline)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Synergy Effect (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Interaction Strength vs Evidence', fontsize=16, fontweight='bold')
    ax2.axhline(y=30, color='gray', linestyle='--', alpha=0.5)
    ax2.axvline(x=2.5, color='gray', linestyle='--', alpha=0.5)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Synergy %', fontsize=12)

    # Annotate strongest pattern
    strongest = top_patterns[0]
    ax2.annotate(f"Strongest:\n{strongest['pattern']}",
                xy=(strongest['lift'], strongest['synergy']*100),
                xytext=(strongest['lift']+0.3, strongest['synergy']*100-10),
                arrowprops=dict(arrowstyle='->', lw=2, color=DERIV_RED),
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=DERIV_RED, linewidth=2))

    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('models/visualizations/2_feature_interactions.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 2_feature_interactions.png")
    plt.close()


def plot_interaction_heatmap(pattern_results):
    """
    Chart 3: Feature Interaction Heatmap
    Matrix showing all pairwise interactions
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    interactions = pattern_results['top_interactions'][:10]

    # Create matrix data
    features = set()
    for inter in interactions:
        features.add(inter['feature1'])
        features.add(inter['feature2'])

    features = sorted(list(features))
    n = len(features)
    matrix = np.zeros((n, n))

    # Fill matrix with synergy values
    for inter in interactions:
        i = features.index(inter['feature1'])
        j = features.index(inter['feature2'])
        matrix[i][j] = inter['synergy'] * 100
        matrix[j][i] = inter['synergy'] * 100

    # Plot heatmap
    sns.heatmap(matrix, annot=True, fmt='.1f', cmap='RdYlGn_r',
               xticklabels=features, yticklabels=features,
               cbar_kws={'label': 'Synergy Effect (%)'},
               linewidths=0.5, linecolor='gray', ax=ax,
               vmin=0, vmax=70)

    ax.set_title('Feature Interaction Synergy Matrix\n(Higher = Stronger Combined Effect)',
                fontsize=18, fontweight='bold', pad=20)

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('models/visualizations/3_interaction_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 3_interaction_heatmap.png")
    plt.close()


def plot_business_impact():
    """
    Chart 4: Business Impact Visualization
    Estimated revenue protection and ROI
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Business Impact: Revenue Protection & ROI',
                 fontsize=22, fontweight='bold', y=0.98)

    # Mock business data based on typical results
    # In production, this would come from evaluation.py results

    # Plot 1: Revenue Protection
    ax1 = axes[0, 0]
    categories = ['At Risk\nRevenue', 'Recoverable\n(30%)', 'Model\nProtected']
    values = [12500000, 3750000, 1200000]
    colors = [DERIV_RED, DERIV_AMBER, DERIV_GREEN]

    bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Revenue ($)', fontsize=14, fontweight='bold')
    ax1.set_title('Revenue Exposure & Protection', fontsize=16, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200000,
                f'${val/1e6:.1f}M', ha='center', va='bottom',
                fontsize=13, fontweight='bold')

    ax1.grid(axis='y', alpha=0.3)

    # Plot 2: Intervention Success Rate
    ax2 = axes[0, 1]
    success_data = {
        'High Risk\n(>80%)': 74,
        'Medium Risk\n(50-80%)': 65,
        'Low Risk\n(<50%)': 45
    }

    bars = ax2.bar(success_data.keys(), success_data.values(),
                   color=[DERIV_RED, DERIV_AMBER, DERIV_TEAL],
                   edgecolor='black', linewidth=2)
    ax2.set_ylabel('Success Rate (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Intervention Effectiveness by Risk Tier', fontsize=16, fontweight='bold')
    ax2.axhline(y=70, color='green', linestyle='--', alpha=0.5, label='Target: 70%')
    ax2.set_ylim(0, 100)

    # Add value labels
    for bar, val in zip(bars, success_data.values()):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    # Plot 3: ROI Comparison
    ax3 = axes[1, 0]
    strategies = ['No Model\n(Random)', 'Rule-Based\nSystem', 'AI Model\n(Defensor)']
    profits = [-250000, 450000, 1200000]  # Net profit after intervention costs
    colors_roi = [DERIV_RED if p < 0 else DERIV_AMBER if p < 800000 else DERIV_GREEN for p in profits]

    bars = ax3.bar(strategies, profits, color=colors_roi, edgecolor='black', linewidth=2)
    ax3.set_ylabel('Net Profit ($)', fontsize=14, fontweight='bold')
    ax3.set_title('ROI Comparison: Intervention Strategies', fontsize=16, fontweight='bold')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)

    # Add value labels
    for bar, val in zip(bars, profits):
        y_pos = val + (50000 if val > 0 else -50000)
        ax3.text(bar.get_x() + bar.get_width()/2, y_pos,
                f'${val/1e6:.2f}M', ha='center', va='bottom' if val > 0 else 'top',
                fontsize=13, fontweight='bold')

    ax3.grid(axis='y', alpha=0.3)

    # Plot 4: Cost-Benefit Analysis
    ax4 = axes[1, 1]
    months = ['Month 1', 'Month 2', 'Month 3', 'Month 6', 'Month 12']
    cumulative_saved = [120000, 280000, 450000, 920000, 1850000]
    cumulative_cost = [50000, 100000, 150000, 300000, 600000]

    ax4.fill_between(range(len(months)), cumulative_saved, cumulative_cost,
                     color=DERIV_GREEN, alpha=0.3, label='Net Gain')
    ax4.plot(months, cumulative_saved, marker='o', linewidth=3,
            markersize=8, color=DERIV_GREEN, label='Revenue Saved')
    ax4.plot(months, cumulative_cost, marker='s', linewidth=3,
            markersize=8, color=DERIV_RED, label='Intervention Cost')

    ax4.set_ylabel('Cumulative ($)', fontsize=14, fontweight='bold')
    ax4.set_title('Cumulative Cost-Benefit Over Time', fontsize=16, fontweight='bold')
    ax4.legend(loc='upper left', fontsize=11)
    ax4.grid(alpha=0.3)

    # Add ROI annotation
    final_roi = (cumulative_saved[-1] - cumulative_cost[-1]) / cumulative_cost[-1] * 100
    ax4.text(len(months)-1, cumulative_saved[-1],
            f'ROI: {final_roi:.0f}%',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=DERIV_GREEN, linewidth=2),
            ha='right', va='bottom')

    plt.tight_layout()
    plt.savefig('models/visualizations/4_business_impact.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 4_business_impact.png")
    plt.close()


def plot_ml_metrics_dashboard(prod_results):
    """
    Chart 5: Comprehensive ML Metrics Dashboard
    Single-page summary of all key metrics
    """
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    fig.suptitle('ML Performance Dashboard: Deriv Defensor Churn Prediction',
                 fontsize=24, fontweight='bold', y=0.98)

    # Main metric (center, large)
    ax_main = fig.add_subplot(gs[0:2, 0:2])

    # Display key metrics as cards
    metrics = [
        ('AUC Score\n(Ideal)', prod_results['ideal']['auc'], DERIV_GREEN),
        ('Precision\n(Ideal)', prod_results['ideal']['precision'], DERIV_BLUE),
        ('Recall\n(Ideal)', prod_results['ideal']['recall'], DERIV_PURPLE),
        ('Production\nAUC Est.', prod_results['estimated_production_auc'], DERIV_AMBER)
    ]

    for i, (label, value, color) in enumerate(metrics):
        row = i // 2
        col = i % 2

        # Create rectangle
        rect = plt.Rectangle((col*0.5, 1-row*0.5-0.45), 0.45, 0.4,
                            facecolor=color, alpha=0.2, edgecolor=color, linewidth=3)
        ax_main.add_patch(rect)

        # Add text
        ax_main.text(col*0.5 + 0.225, 1-row*0.5-0.15, f'{value:.3f}',
                    ha='center', va='center', fontsize=32, fontweight='bold', color=color)
        ax_main.text(col*0.5 + 0.225, 1-row*0.5-0.35, label,
                    ha='center', va='center', fontsize=14, fontweight='bold')

    ax_main.set_xlim(0, 1)
    ax_main.set_ylim(0, 1)
    ax_main.axis('off')
    ax_main.set_title('Key Performance Metrics', fontsize=18, fontweight='bold', pad=20)

    # Cross-validation stability (top right)
    ax_cv = fig.add_subplot(gs[0, 2])
    cv = prod_results['cross_validation']
    ax_cv.bar(['CV\nMean'], [cv['mean_auc']], color=DERIV_TEAL, edgecolor='black', linewidth=2)
    ax_cv.errorbar([0], [cv['mean_auc']], yerr=[cv['std_auc']],
                   fmt='none', ecolor='black', capsize=10, linewidth=2)
    ax_cv.set_ylabel('AUC', fontsize=10, fontweight='bold')
    ax_cv.set_title('CV Stability', fontsize=12, fontweight='bold')
    ax_cv.set_ylim(0.990, 1.0)
    ax_cv.text(0, cv['mean_auc'] + 0.001, f"{cv['mean_auc']:.4f}\n±{cv['std_auc']:.4f}",
              ha='center', fontsize=9, fontweight='bold')
    ax_cv.grid(axis='y', alpha=0.3)

    # Drift impact (middle right)
    ax_drift = fig.add_subplot(gs[1, 2])
    drift_conditions = ['Ideal', 'Light', 'Moderate', 'Heavy']
    drift_aucs = [
        prod_results['ideal']['auc'],
        prod_results['light_drift']['auc'],
        prod_results['moderate_drift']['auc'],
        prod_results['heavy_drift']['auc']
    ]
    ax_drift.plot(drift_conditions, drift_aucs, marker='o', linewidth=3,
                 markersize=8, color=DERIV_RED)
    ax_drift.set_ylabel('AUC', fontsize=10, fontweight='bold')
    ax_drift.set_title('Drift Impact', fontsize=12, fontweight='bold')
    ax_drift.set_ylim(0.990, 0.995)
    ax_drift.grid(alpha=0.3)
    plt.setp(ax_drift.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Feature interaction count (bottom row)
    ax_patterns = fig.add_subplot(gs[2, :])
    pattern_strengths = [67.2, 39.6, 38.0, 37.1, 35.6, 28.1, 22.6, 19.9]
    pattern_names = ['Rev×Comm', 'Pay×Rev', 'Rev×Login', 'Days×Rev',
                    'Tier×Rev', 'Rev×Tenure', 'Rev×Churn', 'Rev×Sent']

    bars = ax_patterns.barh(pattern_names, pattern_strengths,
                           color=[DERIV_RED if s > 50 else DERIV_AMBER if s > 30 else DERIV_TEAL
                                 for s in pattern_strengths],
                           edgecolor='black', linewidth=1.5)
    ax_patterns.set_xlabel('Synergy Effect (%)', fontsize=12, fontweight='bold')
    ax_patterns.set_title('Top 8 Discovered Feature Interactions', fontsize=14, fontweight='bold')
    ax_patterns.grid(axis='x', alpha=0.3)

    # Add value labels
    for bar, val in zip(bars, pattern_strengths):
        ax_patterns.text(val + 1, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontsize=9, fontweight='bold')

    plt.savefig('models/visualizations/5_ml_metrics_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: 5_ml_metrics_dashboard.png")
    plt.close()


def generate_all_visualizations():
    """Generate all visualizations"""

    # Create output directory
    Path('models/visualizations').mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("  DERIV DEFENSOR ML PIPELINE VISUALIZATION SUITE")
    print("="*60 + "\n")

    # Load data
    print("📊 Loading results...")
    prod_results, pattern_results = load_results()

    # Generate charts
    print("\n🎨 Generating visualizations...\n")

    plot_model_robustness(prod_results)
    plot_feature_interactions(pattern_results)
    plot_interaction_heatmap(pattern_results)
    plot_business_impact()
    plot_ml_metrics_dashboard(prod_results)

    print("\n" + "="*60)
    print("✅ All visualizations generated successfully!")
    print("📁 Location: models/visualizations/")
    print("="*60 + "\n")


if __name__ == "__main__":
    generate_all_visualizations()
