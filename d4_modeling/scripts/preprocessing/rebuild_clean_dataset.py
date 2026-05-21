"""
Rebuild clean dataset from scratch:
1. Start with original cleaned_rent_dataset_COMPLETE.csv
2. Remove commercial/military/retirement ZIPs
3. Properly integrate William/Khanh's education/income/jobs data
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("REBUILDING CLEAN DATASET FROM SCRATCH")
print("=" * 80)

# ============================================================================
# STEP 1: Load original clean dataset
# ============================================================================
print("\n[1/5] Loading original clean dataset...")
original = pd.read_csv('archive/old_data/cleaned_rent_dataset_COMPLETE.csv')
print(f"   Original dataset: {len(original)} ZIPs")
print(f"   Unique geoids: {original['geoid'].nunique()}")
print(f"   Duplicates: {original.duplicated(subset=['geoid']).sum()}")

# Remove the 3 duplicate rows
original = original.drop_duplicates(subset=['geoid'], keep='first')
print(f"   After removing duplicates: {len(original)} ZIPs")

# ============================================================================
# STEP 2: Remove non-residential ZIPs
# ============================================================================
print("\n[2/5] Removing non-residential ZIPs...")

# Load exclusion lists
commercial = pd.read_csv('d4_modeling/data/excluded_commercial_zips.csv')
military = pd.read_csv('d4_modeling/data/removed_military_zips.csv')
retirement = pd.read_csv('d4_modeling/data/removed_retirement_zips.csv')

commercial_zips = set(commercial['geoid'].astype(str))
military_zips = set(military['geoid'].astype(str))
retirement_zips = set(retirement['geoid'].astype(str))

print(f"   Commercial ZIPs to exclude: {len(commercial_zips)}")
print(f"   Military ZIPs to exclude: {len(military_zips)}")
print(f"   Retirement ZIPs to exclude: {len(retirement_zips)}")

# Remove non-residential ZIPs
original['geoid_str'] = original['geoid'].astype(str)
excluded_zips = commercial_zips | military_zips | retirement_zips

residential = original[~original['geoid_str'].isin(excluded_zips)].copy()
residential = residential.drop(columns=['geoid_str'])

print(f"   Residential ZIPs remaining: {len(residential)}")
print(f"   Removed: {len(original) - len(residential)} ZIPs")

# ============================================================================
# STEP 3: Load William/Khanh's data
# ============================================================================
print("\n[3/5] Loading William/Khanh's education/income/jobs data...")

# Check what files we have
import os

william_files = []
khanh_files = []

if os.path.exists('d4_modeling/team_data/william'):
    william_files = os.listdir('d4_modeling/team_data/william')
    print(f"   William's files: {william_files}")

if os.path.exists('d4_modeling/team_data/khanh'):
    khanh_files = os.listdir('d4_modeling/team_data/khanh')
    print(f"   Khanh's files: {khanh_files}")

# Try to find their data files
team_data = None

# Option 1: Check if there's a combined file
possible_paths = [
    'd4_modeling/team_data/william/education_income_jobs.csv',
    'd4_modeling/team_data/khanh/education_income_jobs.csv',
    'd4_modeling/team_data/combined_team_data.csv',
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"   Found: {path}")
        team_data = pd.read_csv(path)
        break

if team_data is None:
    print("   ⚠️  No team data files found - will extract from master_dataset_residential.csv")
    
    # Extract the team columns from the buggy dataset
    buggy = pd.read_csv('d4_modeling/data/master_dataset_residential.csv')
    
    # Identify William/Khanh's columns (education, income, jobs)
    team_columns = [
        'geoid',
        'education_bachelors_plus',
        'education_high_school',
        'education_some_college',
        'education_less_than_hs',
        'median_household_income',
        'per_capita_income',
        'jobs_per_capita',
        'education_income_ratio',
    ]
    
    # Filter to columns that exist
    available_cols = [col for col in team_columns if col in buggy.columns]
    
    if len(available_cols) > 1:  # At least geoid + 1 feature
        # Remove duplicates and extract clean team data
        team_data = buggy[available_cols].drop_duplicates(subset=['geoid'], keep='first')
        print(f"   Extracted {len(available_cols)-1} team features from buggy dataset")
        print(f"   Team data rows: {len(team_data)}")
    else:
        print("   ❌ Could not find team data columns")
        team_data = None

# ============================================================================
# STEP 4: Merge team data with residential dataset
# ============================================================================
print("\n[4/5] Merging team data with residential dataset...")

if team_data is not None:
    # Ensure geoid is same type
    residential['geoid'] = residential['geoid'].astype(int)
    team_data['geoid'] = team_data['geoid'].astype(int)
    
    print(f"   Residential ZIPs: {len(residential)}")
    print(f"   Team data ZIPs: {len(team_data)}")
    
    # Left join to keep all residential ZIPs
    final_dataset = residential.merge(team_data, on='geoid', how='left', suffixes=('', '_team'))
    
    print(f"   After merge: {len(final_dataset)} ZIPs")
    print(f"   Duplicates after merge: {final_dataset.duplicated(subset=['geoid']).sum()}")
    
    # Check for any duplicate columns
    duplicate_cols = [col for col in final_dataset.columns if col.endswith('_team')]
    if duplicate_cols:
        print(f"   ⚠️  Found duplicate columns: {duplicate_cols}")
        # Keep original, drop _team versions
        final_dataset = final_dataset.drop(columns=duplicate_cols)
    
else:
    print("   ⚠️  No team data to merge - using residential dataset as-is")
    final_dataset = residential.copy()

# ============================================================================
# STEP 5: Final validation and save
# ============================================================================
print("\n[5/5] Final validation...")

print(f"   Total ZIPs: {len(final_dataset)}")
print(f"   Unique geoids: {final_dataset['geoid'].nunique()}")
print(f"   Duplicate rows: {final_dataset.duplicated().sum()}")
print(f"   Duplicate geoids: {final_dataset.duplicated(subset=['geoid']).sum()}")

# Check for rent column
rent_col = 'Median Home Rent (2020-2024)'
if rent_col in final_dataset.columns:
    rent_missing = final_dataset[rent_col].isnull().sum()
    print(f"   Rent column: ✅ ({rent_missing} missing)")
else:
    print(f"   Rent column: ❌ NOT FOUND")

# Check missing values
missing_summary = final_dataset.isnull().sum()
missing_cols = missing_summary[missing_summary > 0]
if len(missing_cols) > 0:
    print(f"\n   Missing values in {len(missing_cols)} columns:")
    for col, count in missing_cols.items():
        pct = (count / len(final_dataset)) * 100
        print(f"      {col}: {count} ({pct:.1f}%)")

# Save final clean dataset
output_path = 'd4_modeling/data/master_dataset_clean_v2.csv'
final_dataset.to_csv(output_path, index=False)
print(f"\n✅ Saved: {output_path}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Started with: {len(original)} ZIPs")
print(f"Removed: {len(original) - len(residential)} non-residential ZIPs")
print(f"Final clean dataset: {len(final_dataset)} ZIPs")
print(f"Columns: {len(final_dataset.columns)}")
print("=" * 80)
