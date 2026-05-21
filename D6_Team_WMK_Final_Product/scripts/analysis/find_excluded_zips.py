"""
Find excluded ZIPs in the master dataset with full features
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'

print("Finding excluded ZIPs in master dataset...")
print("=" * 80)

# Load the simplified excluded files to get ZIP codes
military_simple = pd.read_csv(DATA_DIR / 'removed_military_zips.csv')
retirement_simple = pd.read_csv(DATA_DIR / 'removed_retirement_zips.csv')

military_zips = set(military_simple['geoid'].astype(str))
retirement_zips = set(retirement_simple['geoid'].astype(str))

print(f"\nLooking for:")
print(f"  Military ZIPs: {len(military_zips)}")
print(f"  Retirement ZIPs: {len(retirement_zips)}")
print(f"  Total: {len(military_zips) + len(retirement_zips)}")

# Load master dataset
master_df = pd.read_csv(DATA_DIR / 'master_dataset_with_team_data.csv')
master_df['geoid'] = master_df['geoid'].astype(str)

print(f"\nMaster dataset shape: {master_df.shape}")

# Find matches
military_found = master_df[master_df['geoid'].isin(military_zips)].copy()
retirement_found = master_df[master_df['geoid'].isin(retirement_zips)].copy()

print(f"\nFound in master dataset:")
print(f"  Military ZIPs: {len(military_found)}")
print(f"  Retirement ZIPs: {len(retirement_found)}")
print(f"  Total: {len(military_found) + len(retirement_found)}")

# Add exclusion type
military_found['exclusion_type'] = 'Military'
retirement_found['exclusion_type'] = 'Retirement'

# Combine
excluded_full = pd.concat([military_found, retirement_found], ignore_index=True)

# Save
output_path = DATA_DIR / 'excluded_zips_full_features.csv'
excluded_full.to_csv(output_path, index=False)

print(f"\n✓ Saved to: {output_path}")
print(f"  Columns: {excluded_full.shape[1]}")
print(f"  Rows: {excluded_full.shape[0]}")

# Show sample
print("\nSample excluded ZIPs found:")
print(excluded_full[['geoid', 'city', 'exclusion_type', 'Median Home Rent (2020-2024)']].head(10))

# Check which ones have rent data
with_rent = excluded_full['Median Home Rent (2020-2024)'].notna().sum()
print(f"\nZIPs with rent data: {with_rent}/{len(excluded_full)}")
