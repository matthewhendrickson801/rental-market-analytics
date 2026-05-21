"""
Add geographic features to improve model:
1. Coastal city indicator
2. Urban/Rural classification based on population density
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("ADDING GEOGRAPHIC FEATURES")
print("=" * 80)

# Load dataset
df = pd.read_csv('d4_modeling/data/master_dataset_clean_final.csv')
print(f"\nLoaded: {len(df)} ZIPs")

# ============================================================================
# FEATURE 1: Coastal City
# ============================================================================
print("\n[1/2] Adding coastal city feature...")

# Cities with significant coastline/beaches
coastal_cities = {
    'Miami': 1,           # Atlantic coast, beaches
    'SanFrancisco': 1,    # Pacific coast, bay
    'Tampa': 1,           # Gulf coast
    'Jacksonville': 1,    # Atlantic coast
    'Orlando': 0,         # Inland (despite being in Florida)
    'Austin': 0,          # Inland
    'SanAntonio': 0,      # Inland
    'Charlotte': 0,       # Inland
    'Columbus': 0,        # Inland
    'Denver': 0,          # Inland, mountain
    'Indianapolis': 0,    # Inland
    'Louisville': 0,      # Inland (river city but not coastal)
    'Nashville': 0,       # Inland
    'Philadelphia': 0,    # River/port but not beach city
}

df['is_coastal'] = df['city'].map(coastal_cities)

coastal_count = df['is_coastal'].sum()
print(f"   Coastal ZIPs: {coastal_count} ({coastal_count/len(df)*100:.1f}%)")
print(f"   Inland ZIPs: {len(df) - coastal_count} ({(len(df)-coastal_count)/len(df)*100:.1f}%)")

print("\n   Coastal cities:")
for city, is_coastal in coastal_cities.items():
    if is_coastal:
        count = (df['city'] == city).sum()
        print(f"      {city}: {count} ZIPs")

# ============================================================================
# FEATURE 2: Urban/Rural Classification
# ============================================================================
print("\n[2/2] Adding urban/rural classification...")

# Calculate population density (people per ZIP)
# We'll use population as proxy since we don't have area
df['population'] = df['Total Population (2020-2024)']

# Define thresholds based on population distribution
# Urban: Top 33% (high population ZIPs)
# Suburban: Middle 34% (medium population ZIPs)
# Rural: Bottom 33% (low population ZIPs)

urban_threshold = df['population'].quantile(0.67)
suburban_threshold = df['population'].quantile(0.33)

print(f"\n   Population thresholds:")
print(f"      Urban (top 33%): > {urban_threshold:.0f} people")
print(f"      Suburban (middle 34%): {suburban_threshold:.0f} - {urban_threshold:.0f} people")
print(f"      Rural (bottom 33%): < {suburban_threshold:.0f} people")

# Create classification
def classify_urban_rural(pop):
    if pd.isna(pop):
        return 'Unknown'
    elif pop >= urban_threshold:
        return 'Urban'
    elif pop >= suburban_threshold:
        return 'Suburban'
    else:
        return 'Rural'

df['urban_rural'] = df['population'].apply(classify_urban_rural)

# Create binary indicators for modeling
df['is_urban'] = (df['urban_rural'] == 'Urban').astype(int)
df['is_suburban'] = (df['urban_rural'] == 'Suburban').astype(int)
df['is_rural'] = (df['urban_rural'] == 'Rural').astype(int)

print(f"\n   Distribution:")
urban_rural_counts = df['urban_rural'].value_counts()
for category, count in urban_rural_counts.items():
    pct = count / len(df) * 100
    print(f"      {category}: {count} ZIPs ({pct:.1f}%)")

# Show by city
print(f"\n   Urban/Rural by city:")
city_urban_rural = df.groupby('city')['urban_rural'].value_counts().unstack(fill_value=0)
print(city_urban_rural.to_string())

# ============================================================================
# FEATURE 3: Tech Hub Indicator (bonus)
# ============================================================================
print("\n[BONUS] Adding tech hub indicator...")

# Cities known for tech industry
tech_hubs = {
    'SanFrancisco': 1,    # Silicon Valley
    'Austin': 1,          # Silicon Hills
    'Denver': 0.5,        # Growing tech scene
    'Miami': 0,
    'Tampa': 0,
    'Jacksonville': 0,
    'Orlando': 0,
    'SanAntonio': 0,
    'Charlotte': 0,
    'Columbus': 0,
    'Indianapolis': 0,
    'Louisville': 0,
    'Nashville': 0,
    'Philadelphia': 0,
}

df['tech_hub_score'] = df['city'].map(tech_hubs)

tech_count = (df['tech_hub_score'] > 0).sum()
print(f"   Tech hub ZIPs: {tech_count} ({tech_count/len(df)*100:.1f}%)")

# ============================================================================
# Save enhanced dataset
# ============================================================================
print("\n" + "=" * 80)
print("SAVING ENHANCED DATASET")
print("=" * 80)

output_path = 'd4_modeling/data/master_dataset_with_geography.csv'
df.to_csv(output_path, index=False)

print(f"\n✅ Saved: {output_path}")
print(f"   Total ZIPs: {len(df)}")
print(f"   Total columns: {len(df.columns)}")

print(f"\n   New features added:")
print(f"      - is_coastal (binary)")
print(f"      - urban_rural (categorical)")
print(f"      - is_urban (binary)")
print(f"      - is_suburban (binary)")
print(f"      - is_rural (binary)")
print(f"      - tech_hub_score (0, 0.5, or 1)")

# Summary statistics
print(f"\n   Feature summary:")
print(f"      Coastal: {df['is_coastal'].sum()} ZIPs")
print(f"      Urban: {df['is_urban'].sum()} ZIPs")
print(f"      Suburban: {df['is_suburban'].sum()} ZIPs")
print(f"      Rural: {df['is_rural'].sum()} ZIPs")
print(f"      Tech hubs: {(df['tech_hub_score'] > 0).sum()} ZIPs")

# Check correlation with rent
print(f"\n   Correlation with rent:")
rent_col = 'Median Home Rent (2020-2024)'
if rent_col in df.columns:
    print(f"      is_coastal: {df['is_coastal'].corr(df[rent_col]):.3f}")
    print(f"      is_urban: {df['is_urban'].corr(df[rent_col]):.3f}")
    print(f"      is_suburban: {df['is_suburban'].corr(df[rent_col]):.3f}")
    print(f"      is_rural: {df['is_rural'].corr(df[rent_col]):.3f}")
    print(f"      tech_hub_score: {df['tech_hub_score'].corr(df[rent_col]):.3f}")

print("\n" + "=" * 80)
