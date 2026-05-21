"""
Add Geographic Features (Fast Version): 
Uses population density and transit as proxies for urban/rural classification
Filters out rural ZIPs without needing geocoding
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("ADDING GEOGRAPHIC FEATURES (FAST METHOD)")
print("=" * 80)

# Load dataset
print("\n📂 Loading dataset...")
df = pd.read_csv('data/final_dataset_with_boom_index.csv')
print(f"✅ Loaded {len(df)} ZIP codes")

# ============================================================================
# CLASSIFY URBAN/SUBURBAN/RURAL (WITHOUT GEOCODING)
# ============================================================================
print("\n🏙️ Classifying ZIP codes using population density + transit...")

def classify_urban_rural_fast(row):
    """
    Classify ZIP code as Urban, Suburban, or Rural using available data
    
    Criteria:
    - Urban: High transit usage OR high population + high density
    - Suburban: Medium population, low transit
    - Rural: Low population OR very low density
    """
    population = row['Total Population (2020-2024)']
    housing_units = row['Total Housing Units (2020-2024)']
    transit = row['Commute Transportation by Public Transit (2020-2024)']
    
    # Calculate density
    density = population / housing_units if housing_units > 0 else 0
    
    # Urban: Has transit OR (high pop + high density)
    if transit > 50 or (population > 10000 and density > 2.5):
        return 'Urban'
    
    # Suburban: Medium population, reasonable density
    elif population > 2000 and density > 2.0:
        return 'Suburban'
    
    # Rural: Low population OR low density
    else:
        return 'Rural'

df['urban_classification'] = df.apply(classify_urban_rural_fast, axis=1)

print(f"  Urban: {(df['urban_classification'] == 'Urban').sum()} ZIPs")
print(f"  Suburban: {(df['urban_classification'] == 'Suburban').sum()} ZIPs")
print(f"  Rural: {(df['urban_classification'] == 'Rural').sum()} ZIPs")

# ============================================================================
# FILTER OUT RURAL/EXURBAN ZIPS
# ============================================================================
print("\n🔍 Applying filters to remove rural ZIPs...")

# Criteria for EXCLUSION (remove if ANY of these are true):
# 1. Population < 2,000 (tiny rural areas)
# 2. Classified as Rural
# 3. Zero transit AND population < 5,000 (exurban)

initial_count = len(df)

# Mark ZIPs for removal
df['remove_rural'] = (
    (df['Total Population (2020-2024)'] < 2000) |
    (df['urban_classification'] == 'Rural') |
    ((df['Commute Transportation by Public Transit (2020-2024)'] == 0) & 
     (df['Total Population (2020-2024)'] < 5000))
)

# Create filtered dataset
df_filtered = df[~df['remove_rural']].copy()

removed_count = initial_count - len(df_filtered)

print(f"  Initial ZIP codes: {initial_count}")
print(f"  Removed: {removed_count} rural/exurban ZIPs ({removed_count/initial_count*100:.1f}%)")
print(f"  Remaining: {len(df_filtered)} urban/suburban ZIPs ({len(df_filtered)/initial_count*100:.1f}%)")

# ============================================================================
# ANALYZE REMOVED ZIPS
# ============================================================================
print("\n📊 Analyzing removed ZIP codes...")

removed_df = df[df['remove_rural']]

print(f"\nRemoved ZIPs by City:")
for city in sorted(df['city'].unique()):
    city_total = len(df[df['city'] == city])
    city_removed = len(removed_df[removed_df['city'] == city])
    city_kept = city_total - city_removed
    print(f"  {city:15s}: Removed {city_removed:3d} / {city_total:3d} ({city_removed/city_total*100:5.1f}%) | Kept {city_kept:3d}")

# ============================================================================
# CHECK IF PROBLEM ZIPS ARE REMOVED
# ============================================================================
print("\n🎯 Checking if problematic ZIPs are removed...")

problem_zips = [46186, 43126, 46111, 43766, 37095]  # The ones with $2000+ overprediction

for zip_code in problem_zips:
    if zip_code in removed_df['geoid'].values:
        row = removed_df[removed_df['geoid'] == zip_code].iloc[0]
        print(f"  ✅ ZIP {zip_code} ({row['city']}): REMOVED - "
              f"Pop={row['Total Population (2020-2024)']:.0f}, "
              f"Transit={row['Commute Transportation by Public Transit (2020-2024)']:.0f}, "
              f"Class={row['urban_classification']}")
    else:
        print(f"  ❌ ZIP {zip_code}: KEPT (still in dataset)")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n💾 Saving results...")

# Save full dataset with classification
df.to_csv('data/final_dataset_with_geography.csv', index=False)
print(f"✅ Saved full dataset: data/final_dataset_with_geography.csv")

# Save filtered dataset (urban/suburban only)
df_filtered.drop('remove_rural', axis=1, inplace=True)
df_filtered.to_csv('data/final_dataset_urban_suburban.csv', index=False)
print(f"✅ Saved filtered dataset: data/final_dataset_urban_suburban.csv")

# Save list of removed ZIPs for reference
removed_df[['geoid', 'city', 'Total Population (2020-2024)', 
            'Commute Transportation by Public Transit (2020-2024)',
            'urban_classification', 'Median Home Rent (2020-2024)']].to_csv(
    'data/removed_rural_zips.csv', index=False
)
print(f"✅ Saved removed ZIPs list: data/removed_rural_zips.csv")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 80)
print("FILTERED DATASET SUMMARY")
print("=" * 80)

print("\n📊 Population Statistics (Filtered):")
print(f"   Min: {df_filtered['Total Population (2020-2024)'].min():.0f}")
print(f"   Max: {df_filtered['Total Population (2020-2024)'].max():.0f}")
print(f"   Mean: {df_filtered['Total Population (2020-2024)'].mean():.0f}")
print(f"   Median: {df_filtered['Total Population (2020-2024)'].median():.0f}")

print("\n💰 Rent Statistics (Filtered):")
print(f"   Min: ${df_filtered['Median Home Rent (2020-2024)'].min():.0f}")
print(f"   Max: ${df_filtered['Median Home Rent (2020-2024)'].max():.0f}")
print(f"   Mean: ${df_filtered['Median Home Rent (2020-2024)'].mean():.0f}")
print(f"   Median: ${df_filtered['Median Home Rent (2020-2024)'].median():.0f}")

print("\n🏙️ Urban Classification (Filtered):")
for classification in ['Urban', 'Suburban']:
    count = (df_filtered['urban_classification'] == classification).sum()
    pct = (count / len(df_filtered)) * 100
    print(f"   {classification}: {count} ({pct:.1f}%)")

print("\n" + "=" * 80)
print("✅ GEOGRAPHIC FILTERING COMPLETE!")
print("=" * 80)
print("\n📁 Next steps:")
print("   1. Use 'data/final_dataset_urban_suburban.csv' for re-training models")
print("   2. Re-run prepare_data_original_features.py with new dataset")
print("   3. Re-train all models")
print("   4. Update dashboard")
