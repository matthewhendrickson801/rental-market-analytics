"""
Generate detailed Jacksonville report for sanity checking
"""

import pandas as pd
import pickle

print("=" * 80)
print("JACKSONVILLE DETAILED REPORT")
print("=" * 80)

# Load data
df = pd.read_csv('d4_modeling/data/master_dataset_final.csv')
jax = df[df['city'] == 'Jacksonville'].copy()

print(f"\nTotal Jacksonville ZIPs: {len(jax)}")

# Load model and make predictions
with open('d4_modeling/models/regression/xgboost_hybrid.pkl', 'rb') as f:
    model = pickle.load(f)

# Load feature list
with open('d4_modeling/models/regression/hybrid_features.txt', 'r') as f:
    feature_cols = [line.strip() for line in f.readlines()]

# Prepare features
X_jax = jax[feature_cols].copy()
X_jax = X_jax.replace([float('inf'), float('-inf')], float('nan'))

# Make predictions
jax['predicted_rent'] = model.predict(X_jax)
jax['residual'] = jax['Median Home Rent (2020-2024)'] - jax['predicted_rent']
jax['abs_residual'] = abs(jax['residual'])
jax['pct_error'] = (jax['residual'] / jax['Median Home Rent (2020-2024)'] * 100)

# Sort by residual (most underpriced first)
jax_sorted = jax.sort_values('residual', ascending=False)

# Create report
report = []
report.append("=" * 80)
report.append("JACKSONVILLE ZIP CODE ANALYSIS")
report.append("=" * 80)
report.append("")
report.append(f"Total ZIPs analyzed: {len(jax)}")
report.append(f"Average actual rent: ${jax['Median Home Rent (2020-2024)'].mean():.0f}")
report.append(f"Average predicted rent: ${jax['predicted_rent'].mean():.0f}")
report.append(f"Average error: ${jax['abs_residual'].mean():.0f}")
report.append("")

# Summary stats
report.append("=" * 80)
report.append("SUMMARY STATISTICS")
report.append("=" * 80)
report.append("")
report.append(f"Rent range: ${jax['Median Home Rent (2020-2024)'].min():.0f} - ${jax['Median Home Rent (2020-2024)'].max():.0f}")
report.append(f"Median rent: ${jax['Median Home Rent (2020-2024)'].median():.0f}")
report.append(f"Population range: {jax['Total Population (2020-2024)'].min():.0f} - {jax['Total Population (2020-2024)'].max():.0f}")
report.append(f"Median population: {jax['Total Population (2020-2024)'].median():.0f}")
report.append("")

# Education stats
if 'education_bachelors_plus' in jax.columns:
    report.append(f"Bachelor's+ education: {jax['education_bachelors_plus'].mean():.1f}% (avg)")
    report.append(f"High school education: {jax['education_high_school'].mean():.1f}% (avg)")
    report.append("")

# Income stats
report.append(f"Median household income: ${jax['Median Household Income (2020-2024)'].mean():.0f} (avg)")
report.append(f"Per capita income: ${jax['Per Capita Income (2020-2024)'].mean():.0f} (avg)")
report.append("")

# Urban/Rural breakdown
if 'urban_rural' in jax.columns:
    report.append("Urban/Rural breakdown:")
    for category, count in jax['urban_rural'].value_counts().items():
        report.append(f"  {category}: {count} ZIPs ({count/len(jax)*100:.1f}%)")
    report.append("")

# Top 10 underpriced opportunities
report.append("=" * 80)
report.append("TOP 10 UNDERPRICED OPPORTUNITIES (Positive Residual)")
report.append("=" * 80)
report.append("Model predicts HIGHER rent than actual = Affordable opportunity")
report.append("")

underpriced = jax_sorted[jax_sorted['residual'] > 0].head(10)
for idx, row in underpriced.iterrows():
    report.append(f"\nZIP {int(row['geoid'])}:")
    report.append(f"  Actual rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    report.append(f"  Predicted rent: ${row['predicted_rent']:.0f}")
    report.append(f"  Opportunity: ${row['residual']:.0f} ({row['pct_error']:.1f}% underpriced)")
    report.append(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    if 'education_bachelors_plus' in row:
        report.append(f"  Bachelor's+: {row['education_bachelors_plus']:.1f}%")
    report.append(f"  Median income: ${row['Median Household Income (2020-2024)']:.0f}")
    report.append(f"  Urban/Rural: {row['urban_rural']}")

# Top 10 overpriced
report.append("")
report.append("=" * 80)
report.append("TOP 10 OVERPRICED ZIPS (Negative Residual)")
report.append("=" * 80)
report.append("Model predicts LOWER rent than actual = Premium location")
report.append("")

overpriced = jax_sorted[jax_sorted['residual'] < 0].tail(10)
for idx, row in overpriced.iterrows():
    report.append(f"\nZIP {int(row['geoid'])}:")
    report.append(f"  Actual rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    report.append(f"  Predicted rent: ${row['predicted_rent']:.0f}")
    report.append(f"  Premium: ${abs(row['residual']):.0f} ({abs(row['pct_error']):.1f}% overpriced)")
    report.append(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    if 'education_bachelors_plus' in row:
        report.append(f"  Bachelor's+: {row['education_bachelors_plus']:.1f}%")
    report.append(f"  Median income: ${row['Median Household Income (2020-2024)']:.0f}")
    report.append(f"  Urban/Rural: {row['urban_rural']}")

# All ZIPs table
report.append("")
report.append("=" * 80)
report.append("ALL JACKSONVILLE ZIPS (Sorted by Opportunity)")
report.append("=" * 80)
report.append("")

# Create summary table
summary_cols = [
    'geoid',
    'Median Home Rent (2020-2024)',
    'predicted_rent',
    'residual',
    'Total Population (2020-2024)',
    'education_bachelors_plus',
    'Median Household Income (2020-2024)',
    'urban_rural',
    'beach_proximity'
]

available_cols = [col for col in summary_cols if col in jax_sorted.columns]
summary_table = jax_sorted[available_cols].copy()

# Rename for readability
summary_table.columns = [
    'ZIP',
    'Actual_Rent',
    'Predicted_Rent',
    'Opportunity',
    'Population',
    'Bachelors_%',
    'Median_Income',
    'Type',
    'Beach_Score'
]

# Format
summary_table['ZIP'] = summary_table['ZIP'].astype(int)
summary_table['Actual_Rent'] = summary_table['Actual_Rent'].fillna(0).round(0).astype(int)
summary_table['Predicted_Rent'] = summary_table['Predicted_Rent'].fillna(0).round(0).astype(int)
summary_table['Opportunity'] = summary_table['Opportunity'].fillna(0).round(0).astype(int)
summary_table['Population'] = summary_table['Population'].fillna(0).round(0).astype(int)
summary_table['Bachelors_%'] = summary_table['Bachelors_%'].fillna(0).round(1)
summary_table['Median_Income'] = summary_table['Median_Income'].fillna(0).round(0).astype(int)
summary_table['Beach_Score'] = summary_table['Beach_Score'].fillna(0).round(1)

report.append(summary_table.to_string(index=False))

# Save report
report_text = '\n'.join(report)
output_path = 'd4_modeling/results/Jacksonville_Detailed_Report.txt'
with open(output_path, 'w') as f:
    f.write(report_text)

print(f"\n✅ Report saved: {output_path}")

# Also print to console
print("\n" + report_text)

# Save CSV for easy viewing
csv_path = 'd4_modeling/results/Jacksonville_All_ZIPs.csv'
summary_table.to_csv(csv_path, index=False)
print(f"\n✅ CSV saved: {csv_path}")
