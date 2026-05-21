"""
Residual Analysis: Identify ZIP codes with biggest rent discrepancies
Find where actual rent differs most from predicted rent
"""

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("RESIDUAL ANALYSIS: IDENTIFYING RENT DISCREPANCIES")
print("=" * 80)

# Load best model (XGBoost)
print("\n📂 Loading XGBoost model (best performer)...")
with open('models/regression/xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

# Load test data
test_data = pd.read_csv('results/prepared_data/test_data.csv')
X_test = test_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_test = test_data['rent']
cities = test_data['city']
geoids = test_data['geoid']

print(f"✅ Test set: {len(y_test)} ZIP codes")

# Make predictions
print("\n🔮 Generating predictions...")
y_pred = model.predict(X_test)

# Calculate residuals
residuals = y_test - y_pred
abs_residuals = np.abs(residuals)
pct_error = (residuals / y_test) * 100

# Create results dataframe
results = pd.DataFrame({
    'geoid': geoids,
    'city': cities,
    'actual_rent': y_test,
    'predicted_rent': y_pred,
    'residual': residuals,
    'abs_residual': abs_residuals,
    'pct_error': pct_error
})

# Sort by absolute residual
results = results.sort_values('abs_residual', ascending=False)

# Save full results
results.to_csv('results/metrics/test_set_predictions.csv', index=False)
print("\n💾 Full predictions saved: results/metrics/test_set_predictions.csv")

# ============================================================================
# TOP DISCREPANCIES
# ============================================================================
print("\n" + "=" * 80)
print("TOP 20 BIGGEST RENT DISCREPANCIES")
print("=" * 80)

print("\n🔴 UNDERPRICED MARKETS (Actual < Predicted - Good deals!):")
print("   ZIP codes where rent is LOWER than expected\n")
underpriced = results[results['residual'] < 0].head(10)
for i, row in underpriced.iterrows():
    print(f"   {row['city']:15s} | ZIP {row['geoid']} | "
          f"Actual: ${row['actual_rent']:,.0f} | "
          f"Predicted: ${row['predicted_rent']:,.0f} | "
          f"Savings: ${-row['residual']:,.0f} ({-row['pct_error']:.1f}%)")

print("\n🔵 OVERPRICED MARKETS (Actual > Predicted - Expensive!):")
print("   ZIP codes where rent is HIGHER than expected\n")
overpriced = results[results['residual'] > 0].head(10)
for i, row in overpriced.iterrows():
    print(f"   {row['city']:15s} | ZIP {row['geoid']} | "
          f"Actual: ${row['actual_rent']:,.0f} | "
          f"Predicted: ${row['predicted_rent']:,.0f} | "
          f"Premium: ${row['residual']:,.0f} (+{row['pct_error']:.1f}%)")

# ============================================================================
# CITY-LEVEL ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("CITY-LEVEL RENT DISCREPANCY SUMMARY")
print("=" * 80)

city_summary = results.groupby('city').agg({
    'residual': ['mean', 'std'],
    'abs_residual': 'mean',
    'pct_error': 'mean',
    'geoid': 'count'
}).round(2)

city_summary.columns = ['Avg_Residual', 'Std_Residual', 'Avg_Abs_Residual', 
                        'Avg_Pct_Error', 'Num_ZIPs']
city_summary = city_summary.sort_values('Avg_Abs_Residual', ascending=False)

print("\n📊 Cities ranked by average prediction error:\n")
print(city_summary.to_string())

city_summary.to_csv('results/metrics/city_level_residuals.csv')
print("\n💾 City summary saved: results/metrics/city_level_residuals.csv")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Create 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Actual vs Predicted
ax1 = axes[0, 0]
ax1.scatter(y_test, y_pred, alpha=0.5, s=30)
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
ax1.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
ax1.set_xlabel('Actual Rent ($)', fontsize=12)
ax1.set_ylabel('Predicted Rent ($)', fontsize=12)
ax1.set_title('Actual vs Predicted Rent (XGBoost)', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Residual Distribution
ax2 = axes[0, 1]
ax2.hist(residuals, bins=50, edgecolor='black', alpha=0.7)
ax2.axvline(x=0, color='r', linestyle='--', lw=2, label='Zero Error')
ax2.set_xlabel('Residual (Actual - Predicted) ($)', fontsize=12)
ax2.set_ylabel('Frequency', fontsize=12)
ax2.set_title('Distribution of Prediction Errors', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Residuals vs Predicted
ax3 = axes[1, 0]
ax3.scatter(y_pred, residuals, alpha=0.5, s=30)
ax3.axhline(y=0, color='r', linestyle='--', lw=2)
ax3.set_xlabel('Predicted Rent ($)', fontsize=12)
ax3.set_ylabel('Residual ($)', fontsize=12)
ax3.set_title('Residual Plot (Check for Patterns)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# 4. City-level average residuals
ax4 = axes[1, 1]
city_avg = results.groupby('city')['residual'].mean().sort_values()
colors = ['green' if x < 0 else 'red' for x in city_avg.values]
ax4.barh(range(len(city_avg)), city_avg.values, color=colors, alpha=0.7)
ax4.set_yticks(range(len(city_avg)))
ax4.set_yticklabels(city_avg.index, fontsize=10)
ax4.axvline(x=0, color='black', linestyle='-', lw=1)
ax4.set_xlabel('Average Residual ($)', fontsize=12)
ax4.set_title('Average Rent Discrepancy by City', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('results/plots/residual_analysis.png', dpi=300, bbox_inches='tight')
print("\n💾 Visualization saved: results/plots/residual_analysis.png")

# ============================================================================
# FEATURE IMPORTANCE VISUALIZATION
# ============================================================================
print("\n📊 Creating feature importance plot...")

# Load feature importance
rf_importance = pd.read_csv('results/metrics/random_forest_feature_importance.csv')
xgb_importance = pd.read_csv('results/metrics/xgboost_feature_importance.csv')

# Plot top 15 features for both models
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Random Forest
ax1 = axes[0]
top_rf = rf_importance.head(15).sort_values('Importance')
ax1.barh(range(len(top_rf)), top_rf['Importance'], color='forestgreen', alpha=0.7)
ax1.set_yticks(range(len(top_rf)))
ax1.set_yticklabels([f.replace(' (2020-2024)', '') for f in top_rf['Feature']], fontsize=9)
ax1.set_xlabel('Importance', fontsize=12)
ax1.set_title('Random Forest - Top 15 Features', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# XGBoost
ax2 = axes[1]
top_xgb = xgb_importance.head(15).sort_values('Importance')
ax2.barh(range(len(top_xgb)), top_xgb['Importance'], color='steelblue', alpha=0.7)
ax2.set_yticks(range(len(top_xgb)))
ax2.set_yticklabels([f.replace(' (2020-2024)', '') for f in top_xgb['Feature']], fontsize=9)
ax2.set_xlabel('Importance', fontsize=12)
ax2.set_title('XGBoost - Top 15 Features', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('results/plots/feature_importance_comparison.png', dpi=300, bbox_inches='tight')
print("💾 Feature importance plot saved: results/plots/feature_importance_comparison.png")

# ============================================================================
# MODEL COMPARISON VISUALIZATION
# ============================================================================
print("\n📊 Creating model comparison plot...")

comparison = pd.read_csv('results/metrics/all_models_comparison.csv')

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# RMSE Comparison
ax1 = axes[0]
models = comparison['Model']
train_rmse = comparison['Train_RMSE']
val_rmse = comparison['Val_RMSE']
x = np.arange(len(models))
width = 0.35
ax1.bar(x - width/2, train_rmse, width, label='Training', alpha=0.8)
ax1.bar(x + width/2, val_rmse, width, label='Validation', alpha=0.8)
ax1.set_ylabel('RMSE ($)', fontsize=12)
ax1.set_title('Model Comparison: RMSE', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(models, rotation=15, ha='right')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# R² Comparison
ax2 = axes[1]
train_r2 = comparison['Train_R2']
val_r2 = comparison['Val_R2']
ax2.bar(x - width/2, train_r2, width, label='Training', alpha=0.8)
ax2.bar(x + width/2, val_r2, width, label='Validation', alpha=0.8)
ax2.set_ylabel('R² Score', fontsize=12)
ax2.set_title('Model Comparison: R²', fontsize=14, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(models, rotation=15, ha='right')
ax2.axhline(y=0, color='red', linestyle='--', lw=1, alpha=0.5)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/plots/model_comparison.png', dpi=300, bbox_inches='tight')
print("💾 Model comparison plot saved: results/plots/model_comparison.png")

print("\n" + "=" * 80)
print("✅ RESIDUAL ANALYSIS COMPLETE!")
print("=" * 80)
print("\n📁 Files created:")
print("   - results/metrics/test_set_predictions.csv")
print("   - results/metrics/city_level_residuals.csv")
print("   - results/plots/residual_analysis.png")
print("   - results/plots/feature_importance_comparison.png")
print("   - results/plots/model_comparison.png")
