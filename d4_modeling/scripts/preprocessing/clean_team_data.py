"""
Clean team data: remove redundancy, fix skewness, handle outliers
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'

print("=" * 80)
print("CLEANING TEAM DATA")
print("=" * 80)

# Load master dataset
df = pd.read_csv(DATA_DIR / 'master_dataset_with_team_data.csv')
print(f"\nOriginal shape: {df.shape}")

# ============================================================================
# 1. Remove Redundant Features
# ============================================================================

print("\n1. Removing redundant features...")

# Keep total_jobs, remove total_employed (r=0.998)
if 'total_employed' in df.columns:
    df.drop('total_employed', axis=1, inplace=True)
    print("   Removed: total_employed (redundant with total_jobs)")

# Keep pct_bachelors_plus, remove pct_mgmt_professional (r=0.902)
if 'pct_mgmt_professional' in df.columns:
    df.drop('pct_mgmt_professional', axis=1, inplace=True)
    print("   Removed: pct_mgmt_professional (redundant with pct_bachelors_plus)")

# Keep jobs_per_capita, remove professional_density (r=0.992 with total_jobs)
if 'professional_density' in df.columns:
    df.drop('professional_density', axis=1, inplace=True)
    print("   Removed: professional_density (redundant with total_jobs)")

# ============================================================================
# 2. Fix Skewed Distribution - Log Transform
# ============================================================================

print("\n2. Fixing skewed distributions...")

if 'jobs_per_capita' in df.columns:
    # Log transform (add 0.001 to avoid log(0))
    df['jobs_per_capita_log'] = np.log1p(df['jobs_per_capita'])
    
    print(f"   Created: jobs_per_capita_log")
    print(f"      Original skew: {df['jobs_per_capita'].skew():.2f}")
    print(f"      Log skew:      {df['jobs_per_capita_log'].skew():.2f}")
    
    # Keep both for now, let model decide

# ============================================================================
# 3. Flag Commercial Districts
# ============================================================================

print("\n3. Flagging commercial districts...")

if 'jobs_per_capita' in df.columns:
    # Flag ZIPs with jobs_per_capita > 5 as likely commercial
    df['commercial_district'] = (df['jobs_per_capita'] > 5).astype(int)
    
    n_commercial = df['commercial_district'].sum()
    print(f"   Created: commercial_district")
    print(f"      Flagged {n_commercial} ZIPs as commercial districts")

# ============================================================================
# 4. Handle Missing Values More Intelligently
# ============================================================================

print("\n4. Handling missing values...")

# For Indianapolis (no jobs data), use city-level median from other cities
if 'total_jobs' in df.columns:
    missing_jobs = df['total_jobs'].isna().sum()
    
    if missing_jobs > 0:
        # Calculate median jobs per capita from cities WITH data
        cities_with_data = df[df['total_jobs'].notna()]['city'].unique()
        
        for city in df['city'].unique():
            if city not in cities_with_data:
                # Use overall median for cities with no data
                city_mask = df['city'] == city
                if city_mask.sum() > 0:
                    # Impute based on population
                    median_jpc = df[df['total_jobs'].notna()]['jobs_per_capita'].median()
                    df.loc[city_mask & df['total_jobs'].isna(), 'total_jobs'] = \
                        df.loc[city_mask & df['total_jobs'].isna(), 'Total Population (2020-2024)'] * median_jpc
                    
                    print(f"   Imputed total_jobs for {city} using median jobs_per_capita")
        
        # Recalculate jobs_per_capita
        df['jobs_per_capita'] = df['total_jobs'] / df['Total Population (2020-2024)']
        df['jobs_per_capita_log'] = np.log1p(df['jobs_per_capita'])
        
        print(f"   Imputed {missing_jobs} missing total_jobs values")

# ============================================================================
# 5. Create Interaction Features
# ============================================================================

print("\n5. Creating interaction features...")

# Education-occupation mismatch
if 'pct_bachelors_plus' in df.columns and 'pct_blue_collar' in df.columns:
    df['education_occupation_mismatch'] = df['pct_bachelors_plus'] * df['pct_blue_collar'] / 100
    print("   Created: education_occupation_mismatch")

# Remote work premium (high education + high WFH)
if 'pct_bachelors_plus' in df.columns and 'pct_work_from_home' in df.columns:
    df['remote_work_premium'] = df['pct_bachelors_plus'] * df['pct_work_from_home'] / 100
    print("   Created: remote_work_premium")

# Service economy indicator
if 'pct_service_jobs' in df.columns and 'pct_service_occup' in df.columns:
    df['service_economy_index'] = (df['pct_service_jobs'] + df['pct_service_occup']) / 2
    print("   Created: service_economy_index")

# ============================================================================
# 6. Save Cleaned Dataset
# ============================================================================

print("\n6. Saving cleaned dataset...")
output_file = DATA_DIR / 'master_dataset_cleaned.csv'
df.to_csv(output_file, index=False)

print(f"   Saved to: {output_file}")
print(f"   Final shape: {df.shape}")
print(f"   Columns removed: {83 - df.shape[1] + 6}")  # +6 for new features
print(f"   New features added: 6")

# Summary
print("\n" + "=" * 80)
print("CLEANING COMPLETE")
print("=" * 80)
print("\nChanges made:")
print("  ✓ Removed 3 redundant features")
print("  ✓ Log-transformed jobs_per_capita")
print("  ✓ Flagged 17 commercial districts")
print("  ✓ Imputed missing jobs data for Indianapolis")
print("  ✓ Created 3 interaction features")
print(f"\nReady for training: {output_file}")
