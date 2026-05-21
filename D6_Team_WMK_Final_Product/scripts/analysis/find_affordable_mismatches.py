"""
Find affordable housing mismatches
Negative residuals = actual rent < predicted rent = AFFORDABLE
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RESULTS_DIR = BASE_DIR / 'results'

print("=" * 80)
print("FINDING AFFORDABLE HOUSING MISMATCHES")
print("=" * 80)

# Load predictions with residuals (city-normalized model)
df = pd.read_csv(DATA_DIR / 'predictions_city_normalized.csv')
# Use the normalized predictions
df['predicted_rent'] = df['predicted_rent_normalized']
df['residual'] = df['residual_normalized']
df['residual_pct'] = (df['residual'] / df['predicted_rent']) * 100
df['abs_residual'] = np.abs(df['residual'])
print(f"\nTotal ZIPs: {len(df)}")

# Filter for valid predictions
df = df[df['predicted_rent'].notna()].copy()
print(f"ZIPs with predictions: {len(df)}")

# Analyze residuals
print("\n" + "=" * 80)
print("RESIDUAL ANALYSIS")
print("=" * 80)

print(f"\nResidual Statistics:")
print(f"  Mean:   ${df['residual'].mean():.2f}")
print(f"  Median: ${df['residual'].median():.2f}")
print(f"  Std:    ${df['residual'].std():.2f}")
print(f"  Min:    ${df['residual'].min():.2f} (most underpriced)")
print(f"  Max:    ${df['residual'].max():.2f} (most overpriced)")

# Categorize ZIPs
df['affordability_category'] = 'Market Rate'
df.loc[df['residual'] < -100, 'affordability_category'] = 'Highly Affordable'
df.loc[(df['residual'] >= -100) & (df['residual'] < -50), 'affordability_category'] = 'Affordable'
df.loc[df['residual'] > 100, 'affordability_category'] = 'Overpriced'
df.loc[df['residual'] > 200, 'affordability_category'] = 'Highly Overpriced'

print(f"\nAffordability Categories:")
for cat in ['Highly Affordable', 'Affordable', 'Market Rate', 'Overpriced', 'Highly Overpriced']:
    count = (df['affordability_category'] == cat).sum()
    pct = count / len(df) * 100
    print(f"  {cat:<20} {count:4d} ({pct:5.1f}%)")

# Top affordable ZIPs (negative residuals)
print("\n" + "=" * 80)
print("TOP 30 AFFORDABLE ZIPS (Actual < Predicted)")
print("=" * 80)

affordable = df[df['residual'] < 0].copy()
affordable = affordable.sort_values('residual')

print(f"\n{'City':<15} {'ZIP':<8} {'Actual':<9} {'Predicted':<9} {'Savings':<9} {'% Below':<8}")
print("-" * 80)

for i, (_, row) in enumerate(affordable.head(30).iterrows(), 1):
    print(f"{row['city']:<15} {row['geoid']:<8} "
          f"${row['Median Home Rent (2020-2024)']:<8.0f} "
          f"${row['predicted_rent']:<8.0f} "
          f"${-row['residual']:<8.0f} "
          f"{-row['residual_pct']:<7.1f}%")

# Jacksonville specific
print("\n" + "=" * 80)
print("JACKSONVILLE AFFORDABLE OPPORTUNITIES")
print("=" * 80)

jax = df[df['city'] == 'Jacksonville'].copy()
jax_affordable = jax[jax['residual'] < 0].sort_values('residual')

print(f"\nJacksonville ZIPs: {len(jax)}")
print(f"Affordable (actual < predicted): {len(jax_affordable)} ({len(jax_affordable)/len(jax)*100:.1f}%)")

if len(jax_affordable) > 0:
    print(f"\n{'ZIP':<8} {'Actual':<9} {'Predicted':<9} {'Savings':<9} {'% Below':<8} {'Category'}")
    print("-" * 80)
    
    for _, row in jax_affordable.iterrows():
        print(f"{row['geoid']:<8} "
              f"${row['Median Home Rent (2020-2024)']:<8.0f} "
              f"${row['predicted_rent']:<8.0f} "
              f"${-row['residual']:<8.0f} "
              f"{-row['residual_pct']:<7.1f}% "
              f"{row['affordability_category']}")
else:
    print("\n⚠️  No Jacksonville ZIPs with negative residuals found")
    print("   Jacksonville market may be efficiently priced")

# By city summary
print("\n" + "=" * 80)
print("AFFORDABLE OPPORTUNITIES BY CITY")
print("=" * 80)

city_summary = df.groupby('city').agg({
    'geoid': 'count',
    'residual': ['mean', 'min', 'max']
}).round(2)

city_summary.columns = ['Total_ZIPs', 'Avg_Residual', 'Min_Residual', 'Max_Residual']
city_summary['Affordable_Count'] = df[df['residual'] < 0].groupby('city').size()
city_summary['Affordable_Pct'] = (city_summary['Affordable_Count'] / city_summary['Total_ZIPs'] * 100).round(1)
city_summary = city_summary.sort_values('Affordable_Pct', ascending=False)

print(f"\n{'City':<15} {'Total':<7} {'Affordable':<12} {'%':<6} {'Avg Residual':<14} {'Best Deal'}")
print("-" * 80)

for city, row in city_summary.iterrows():
    print(f"{city:<15} {row['Total_ZIPs']:<7.0f} "
          f"{row['Affordable_Count']:<12.0f} "
          f"{row['Affordable_Pct']:<5.1f}% "
          f"${row['Avg_Residual']:<13.2f} "
          f"${-row['Min_Residual']:.0f} below")

# Save affordable ZIPs
affordable_path = RESULTS_DIR / 'affordable_zips.csv'
affordable_df = df[df['residual'] < -50][['city', 'geoid', 'Median Home Rent (2020-2024)', 
                                           'predicted_rent', 'residual', 'residual_pct', 
                                           'affordability_category']].copy()
affordable_df = affordable_df.sort_values('residual')
affordable_df.to_csv(affordable_path, index=False)
print(f"\n✓ Saved {len(affordable_df)} affordable ZIPs to: {affordable_path}")

# Save Jacksonville report
jax_path = RESULTS_DIR / 'jacksonville_affordability.csv'
jax.to_csv(jax_path, index=False)
print(f"✓ Saved Jacksonville analysis to: {jax_path}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
