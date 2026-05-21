"""
Create Visualizations for Deliverable 4
Generate publication-quality charts for the report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import pickle

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

print("Creating D4 Visualizations...")
print("="*80)

# Create output directory
import os
os.makedirs('visualizations/d4', exist_ok=True)

# ============================================================================
# 1. MODEL COMPARISON CHART
# ============================================================================
print("\n1. Creating Model Comparison Chart...")

models_data = {
    'Model': ['Linear\nRegression', 'Ridge\nRegression', 'Random\nForest', 'XGBoost\n(Selected)'],
    'Validation_R2': [-75.56, -67.62, 0.709, 0.757],
    'Validation_RMSE': [5795, 5486, 264, 241]
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# R² comparison
colors = ['#d62728', '#d62728', '#2ca02c', '#1f77b4']
bars1 = ax1.bar(models_data['Model'], models_data['Validation_R2'], color=colors, alpha=0.8, edgecolor='black')
ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_ylabel('Validation R² Score', fontsize=12, fontweight='bold')
ax1.set_title('Model Performance: R² Comparison', fontsize=14, fontweight='bold')
ax1.set_ylim(-80, 1)
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    if height < 0:
        label_y = height - 5
        va = 'top'
    else:
        label_y = height + 0.02
        va = 'bottom'
    ax1.text(bar.get_x() + bar.get_width()/2., label_y,
             f'{height:.3f}' if height > 0 else f'{height:.1f}',
             ha='center', va=va, fontweight='bold', fontsize=10)

# RMSE comparison (only for successful models)
successful_models = ['Random\nForest', 'XGBoost\n(Selected)']
successful_rmse = [264, 241]
colors2 = ['#2ca02c', '#1f77b4']

bars2 = ax2.bar(successful_models, successful_rmse, color=colors2, alpha=0.8, edgecolor='black')
ax2.set_ylabel('Validation RMSE ($)', fontsize=12, fontweight='bold')
ax2.set_title('Model Performance: RMSE Comparison\n(Successful Models Only)', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'${height:.0f}',
             ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('visualizations/d4/01_model_comparison.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/01_model_comparison.png")
plt.close()

# ============================================================================
# 2. FEATURE IMPORTANCE
# ============================================================================
print("\n2. Creating Feature Importance Chart...")

feat_imp = pd.read_csv('results/metrics/xgboost_feature_importance.csv')
top_features = feat_imp.head(15)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top_features)), top_features['Importance'], color='#1f77b4', alpha=0.8, edgecolor='black')
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'], fontsize=10)
ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Most Important Features (XGBoost)', fontsize=14, fontweight='bold')
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_features['Importance'])):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}',
            ha='left', va='center', fontsize=9, fontweight='bold')

# Highlight top 3
for i in range(3):
    bars[i].set_color('#ff7f0e')
    bars[i].set_alpha(0.9)

plt.tight_layout()
plt.savefig('visualizations/d4/02_feature_importance.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/02_feature_importance.png")
plt.close()

# ============================================================================
# 3. TRAINING VS VALIDATION PERFORMANCE
# ============================================================================
print("\n3. Creating Training vs Validation Performance Chart...")

metrics_data = {
    'Metric': ['R²', 'RMSE ($)', 'MAE ($)'],
    'Training': [0.9652, 100, 75],
    'Validation': [0.7571, 241, 182],
    'Test': [0.7459, 273, 205]
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, metric in enumerate(metrics_data['Metric']):
    ax = axes[idx]
    values = [metrics_data['Training'][idx], metrics_data['Validation'][idx], metrics_data['Test'][idx]]
    colors_split = ['#2ca02c', '#1f77b4', '#ff7f0e']
    
    bars = ax.bar(['Training', 'Validation', 'Test'], values, color=colors_split, alpha=0.8, edgecolor='black')
    ax.set_title(f'{metric}', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        if 'RMSE' in metric or 'MAE' in metric:
            label = f'${val:.0f}'
        else:
            label = f'{val:.4f}'
        ax.text(bar.get_x() + bar.get_width()/2., height + (height * 0.02),
                label, ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.suptitle('Model Performance Across Data Splits', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('visualizations/d4/03_train_val_test_performance.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/03_train_val_test_performance.png")
plt.close()



# ============================================================================
# 4. JACKSONVILLE AFFORDABILITY MAP
# ============================================================================
print("\n4. Creating Jacksonville Affordability Analysis...")

# Load Jacksonville data
df = pd.read_csv('dashboard/data/dashboard_data.csv')
df['geoid'] = df['geoid'].astype(str)
jax_df = df[df['city'] == 'Jacksonville'].copy()

# Create affordability categories
def categorize_affordability(row):
    pct = row['rent_discrepancy_pct']
    if pct < -15:
        return 'Highly Affordable\n(<-15%)'
    elif pct < -5:
        return 'Affordable\n(-15% to -5%)'
    elif pct < 5:
        return 'Fair Value\n(-5% to +5%)'
    elif pct < 15:
        return 'Slightly Overpriced\n(+5% to +15%)'
    else:
        return 'Overpriced\n(>+15%)'

jax_df['affordability_category'] = jax_df.apply(categorize_affordability, axis=1)

# Count by category
category_counts = jax_df['affordability_category'].value_counts()
category_order = [
    'Highly Affordable\n(<-15%)',
    'Affordable\n(-15% to -5%)',
    'Fair Value\n(-5% to +5%)',
    'Slightly Overpriced\n(+5% to +15%)',
    'Overpriced\n(>+15%)'
]
category_counts = category_counts.reindex(category_order, fill_value=0)

fig, ax = plt.subplots(figsize=(12, 7))
colors_afford = ['#2ca02c', '#90ee90', '#ffd700', '#ff8c00', '#d62728']
bars = ax.bar(range(len(category_counts)), category_counts.values, color=colors_afford, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(category_counts)))
ax.set_xticklabels(category_counts.index, fontsize=10, fontweight='bold')
ax.set_ylabel('Number of ZIP Codes', fontsize=12, fontweight='bold')
ax.set_title('Jacksonville Rental Market Affordability Distribution\n(55 ZIP Codes Analyzed)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels and percentages
for bar, val in zip(bars, category_counts.values):
    height = bar.get_height()
    pct = (val / len(jax_df)) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{int(val)} ZIPs\n({pct:.1f}%)',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add summary text
summary_text = f"Total: {len(jax_df)} Jacksonville ZIPs\nMean Rent: ${jax_df['actual_rent'].mean():.0f}\nMarket Efficiency: 97.5%"
ax.text(0.98, 0.97, summary_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('visualizations/d4/04_jacksonville_affordability_distribution.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/04_jacksonville_affordability_distribution.png")
plt.close()

# ============================================================================
# 5. JACKSONVILLE TOP OPPORTUNITIES
# ============================================================================
print("\n5. Creating Jacksonville Top Opportunities Chart...")

# Get top affordable and overpriced
jax_sorted = jax_df.sort_values('rent_discrepancy_pct')
top_affordable = jax_sorted.head(5)
top_overpriced = jax_sorted.tail(5).iloc[::-1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Top Affordable
y_pos1 = range(len(top_affordable))
bars1 = ax1.barh(y_pos1, top_affordable['rent_discrepancy_pct'], color='#2ca02c', alpha=0.8, edgecolor='black')
ax1.set_yticks(y_pos1)
ax1.set_yticklabels([f"{row['geoid']}\n${row['actual_rent']:.0f}" for _, row in top_affordable.iterrows()], fontsize=10)
ax1.set_xlabel('Affordability (% Below Predicted)', fontsize=11, fontweight='bold')
ax1.set_title('Top 5 Most Affordable Jacksonville ZIPs', fontsize=13, fontweight='bold')
ax1.invert_yaxis()
ax1.grid(axis='x', alpha=0.3)
ax1.axvline(x=0, color='black', linestyle='-', linewidth=1)

for i, (bar, val) in enumerate(zip(bars1, top_affordable['rent_discrepancy_pct'])):
    ax1.text(val - 1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%',
            ha='right', va='center', fontsize=10, fontweight='bold', color='white')

# Top Overpriced
y_pos2 = range(len(top_overpriced))
bars2 = ax2.barh(y_pos2, top_overpriced['rent_discrepancy_pct'], color='#d62728', alpha=0.8, edgecolor='black')
ax2.set_yticks(y_pos2)
ax2.set_yticklabels([f"{row['geoid']}\n${row['actual_rent']:.0f}" for _, row in top_overpriced.iterrows()], fontsize=10)
ax2.set_xlabel('Overpricing (% Above Predicted)', fontsize=11, fontweight='bold')
ax2.set_title('Top 5 Most Overpriced Jacksonville ZIPs', fontsize=13, fontweight='bold')
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)
ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)

for i, (bar, val) in enumerate(zip(bars2, top_overpriced['rent_discrepancy_pct'])):
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
            f'+{val:.1f}%',
            ha='left', va='center', fontsize=10, fontweight='bold', color='white')

plt.suptitle('Jacksonville Rental Market Opportunities & Concerns', fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('visualizations/d4/05_jacksonville_top_opportunities.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/05_jacksonville_top_opportunities.png")
plt.close()

# ============================================================================
# 6. DATA EXCLUSION SUMMARY
# ============================================================================
print("\n6. Creating Data Exclusion Summary...")

exclusion_data = {
    'Category': ['Military Bases', 'Retirement\nCommunities', 'Included\nZIP Codes'],
    'Count': [16, 12, 1738],
    'Colors': ['#d62728', '#ff7f0e', '#2ca02c']
}

fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.bar(exclusion_data['Category'], exclusion_data['Count'], 
              color=exclusion_data['Colors'], alpha=0.8, edgecolor='black', linewidth=2)
ax.set_ylabel('Number of ZIP Codes', fontsize=12, fontweight='bold')
ax.set_title('Dataset Composition: Exclusions & Included ZIP Codes', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar, val in zip(bars, exclusion_data['Count']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 20,
            f'{val} ZIPs',
            ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add explanation text
explanation = ("Excluded: 28 ZIPs with non-market rental dynamics\n"
               "• Military bases: BAH rates, transient populations\n"
               "• Retirement communities: Age-restricted, <40% labor force\n\n"
               "Final Dataset: 1,738 ZIPs across 14 cities\n"
               "Jacksonville: 55 ZIPs (no exclusions)")
ax.text(0.98, 0.97, explanation, transform=ax.transAxes,
        fontsize=10, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.savefig('visualizations/d4/06_data_exclusions.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/d4/06_data_exclusions.png")
plt.close()

print("\n" + "="*80)
print("✅ All visualizations created successfully!")
print("="*80)
print("\nFiles saved in: visualizations/d4/")
print("  1. 01_model_comparison.png")
print("  2. 02_feature_importance.png")
print("  3. 03_train_val_test_performance.png")
print("  4. 04_jacksonville_affordability_distribution.png")
print("  5. 05_jacksonville_top_opportunities.png")
print("  6. 06_data_exclusions.png")
