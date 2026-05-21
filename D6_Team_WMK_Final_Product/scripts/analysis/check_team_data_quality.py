"""
Data Quality Checks for Team Data Integration
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'

print("=" * 80)
print("TEAM DATA QUALITY CHECKS")
print("=" * 80)

# Load master dataset
df = pd.read_csv(DATA_DIR / 'master_dataset_with_team_data.csv')
print(f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================================
# CHECK 1: Percentage Sums
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 1: Do Education Percentages Sum to ~100%?")
print("=" * 80)

edu_cols = ['pct_less_than_hs', 'pct_hs_only', 'pct_some_college', 'pct_bachelors_plus']
if all(col in df.columns for col in edu_cols):
    df['edu_total_pct'] = df[edu_cols].sum(axis=1)
    
    print(f"\nEducation percentage totals:")
    print(f"  Mean:   {df['edu_total_pct'].mean():.2f}%")
    print(f"  Median: {df['edu_total_pct'].median():.2f}%")
    print(f"  Min:    {df['edu_total_pct'].min():.2f}%")
    print(f"  Max:    {df['edu_total_pct'].max():.2f}%")
    print(f"  Std:    {df['edu_total_pct'].std():.2f}%")
    
    # Check how many are close to 100%
    within_5pct = ((df['edu_total_pct'] >= 95) & (df['edu_total_pct'] <= 105)).sum()
    print(f"\n  ZIPs within 95-105%: {within_5pct}/{len(df)} ({within_5pct/len(df)*100:.1f}%)")
    
    if df['edu_total_pct'].mean() < 90 or df['edu_total_pct'].mean() > 110:
        print("  ⚠️  WARNING: Education percentages don't sum to ~100%")
        print("     This suggests missing categories or data quality issues")
    else:
        print("  ✅ Education percentages look reasonable")
else:
    print("  ⚠️  Education columns not found")

# Check occupation percentages
occup_cols = ['pct_mgmt_professional', 'pct_service_occup', 'pct_sales_office', 'pct_blue_collar']
if all(col in df.columns for col in occup_cols):
    df['occup_total_pct'] = df[occup_cols].sum(axis=1)
    
    print(f"\nOccupation percentage totals:")
    print(f"  Mean:   {df['occup_total_pct'].mean():.2f}%")
    print(f"  Median: {df['occup_total_pct'].median():.2f}%")
    
    within_5pct = ((df['occup_total_pct'] >= 95) & (df['occup_total_pct'] <= 105)).sum()
    print(f"  ZIPs within 95-105%: {within_5pct}/{len(df)} ({within_5pct/len(df)*100:.1f}%)")
    
    if df['occup_total_pct'].mean() < 90:
        print("  ⚠️  WARNING: Occupation percentages sum to less than 90%")
        print("     Missing occupation categories (e.g., military, unemployed)")
    else:
        print("  ✅ Occupation percentages look reasonable")

# ============================================================================
# CHECK 2: Missing Values
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 2: Missing Values in Team Data")
print("=" * 80)

team_cols = [
    'total_jobs', 'pct_less_than_hs', 'pct_hs_only', 'pct_some_college', 'pct_bachelors_plus',
    'pct_tech_jobs', 'pct_service_jobs', 'pct_manufacturing_jobs',
    'pct_mgmt_professional', 'pct_service_occup', 'pct_sales_office', 'pct_blue_collar',
    'pct_work_from_home', 'total_employed', 'jobs_per_capita', 'education_income_ratio',
    'high_tech_area', 'professional_density', 'high_remote_work'
]

print(f"\n{'Feature':<35} {'Missing':<10} {'%':<8} {'Status'}")
print("-" * 80)

for col in team_cols:
    if col in df.columns:
        missing = df[col].isna().sum()
        pct_missing = missing / len(df) * 100
        
        if pct_missing == 0:
            status = "✅"
        elif pct_missing < 5:
            status = "⚠️"
        else:
            status = "❌"
        
        print(f"{col:<35} {missing:<10} {pct_missing:<7.1f}% {status}")
    else:
        print(f"{col:<35} {'NOT FOUND':<10} {'':<8} ❌")

# ============================================================================
# CHECK 3: Outliers
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 3: Outlier Detection")
print("=" * 80)

# Jobs per capita
if 'jobs_per_capita' in df.columns:
    print(f"\nJobs per capita:")
    print(f"  Mean:   {df['jobs_per_capita'].mean():.3f}")
    print(f"  Median: {df['jobs_per_capita'].median():.3f}")
    print(f"  Min:    {df['jobs_per_capita'].min():.3f}")
    print(f"  Max:    {df['jobs_per_capita'].max():.3f}")
    
    extreme = (df['jobs_per_capita'] > 5).sum()
    if extreme > 0:
        print(f"  ⚠️  {extreme} ZIPs have jobs_per_capita > 5 (suspicious)")
        print(f"     These may be commercial districts, not residential")
    else:
        print(f"  ✅ No extreme outliers")

# Education percentages
for col in ['pct_less_than_hs', 'pct_hs_only', 'pct_some_college', 'pct_bachelors_plus']:
    if col in df.columns:
        negative = (df[col] < 0).sum()
        over_100 = (df[col] > 100).sum()
        
        if negative > 0 or over_100 > 0:
            print(f"\n{col}:")
            if negative > 0:
                print(f"  ❌ {negative} ZIPs have negative values")
            if over_100 > 0:
                print(f"  ❌ {over_100} ZIPs have values > 100%")

# ============================================================================
# CHECK 4: Feature Distributions
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 4: Feature Distributions")
print("=" * 80)

key_features = ['pct_hs_only', 'pct_bachelors_plus', 'pct_work_from_home', 'jobs_per_capita']

for col in key_features:
    if col in df.columns and df[col].notna().sum() > 0:
        print(f"\n{col}:")
        print(f"  Mean:   {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Std:    {df[col].std():.2f}")
        print(f"  Skew:   {df[col].skew():.2f}")
        
        if abs(df[col].skew()) > 1:
            print(f"  ⚠️  Highly skewed distribution (may need transformation)")

# ============================================================================
# CHECK 5: Feature Correlations
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 5: High Correlations (Potential Redundancy)")
print("=" * 80)

# Select numeric team features
numeric_team_cols = [col for col in team_cols if col in df.columns and df[col].dtype in ['float64', 'int64']]
corr_matrix = df[numeric_team_cols].corr()

# Find high correlations (> 0.9)
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.9:
            high_corr_pairs.append((
                corr_matrix.columns[i],
                corr_matrix.columns[j],
                corr_matrix.iloc[i, j]
            ))

if high_corr_pairs:
    print(f"\nFound {len(high_corr_pairs)} highly correlated pairs (|r| > 0.9):")
    for feat1, feat2, corr in high_corr_pairs:
        print(f"  {feat1:<30} <-> {feat2:<30} r={corr:.3f}")
    print("\n  ⚠️  Consider removing redundant features")
else:
    print("\n  ✅ No highly correlated features (|r| > 0.9)")

# ============================================================================
# CHECK 6: City Coverage
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 6: Team Data Coverage by City")
print("=" * 80)

if 'city' in df.columns and 'total_jobs' in df.columns:
    print(f"\n{'City':<20} {'Total ZIPs':<12} {'With Jobs Data':<18} {'Coverage %'}")
    print("-" * 80)
    
    for city in sorted(df['city'].unique()):
        city_df = df[df['city'] == city]
        total = len(city_df)
        with_data = city_df['total_jobs'].notna().sum()
        pct = with_data / total * 100
        
        status = "✅" if pct == 100 else "⚠️" if pct > 90 else "❌"
        print(f"{city:<20} {total:<12} {with_data:<18} {pct:>6.1f}% {status}")

print("\n" + "=" * 80)
print("QUALITY CHECK COMPLETE")
print("=" * 80)
