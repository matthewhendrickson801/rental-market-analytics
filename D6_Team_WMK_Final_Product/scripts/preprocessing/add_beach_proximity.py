"""
1. Remove ZIPs with population < 1,000 (likely non-residential)
2. Add beach proximity feature (more granular than just coastal city)
"""

import pandas as pd

print("=" * 80)
print("CLEANING DATA & ADDING BEACH PROXIMITY")
print("=" * 80)

# Load dataset
df = pd.read_csv('d4_modeling/data/master_dataset_with_geography.csv')
print(f"\nStarting with: {len(df)} ZIPs")

# ============================================================================
# STEP 1: Remove low population ZIPs
# ============================================================================
print("\n[1/2] Removing low population ZIPs...")

low_pop = df[df['Total Population (2020-2024)'] < 1000]
print(f"   ZIPs with population < 1,000: {len(low_pop)}")

# Show some examples
print(f"\n   Examples of removed ZIPs:")
examples = low_pop.sort_values('Total Population (2020-2024)').head(10)
for _, row in examples.iterrows():
    print(f"      {int(row['geoid'])} ({row['city']}): {row['Total Population (2020-2024)']:.0f} people")

# Remove them
df_clean = df[df['Total Population (2020-2024)'] >= 1000].copy()
print(f"\n   After removal: {len(df_clean)} ZIPs")
print(f"   Removed: {len(df) - len(df_clean)} ZIPs")

# ============================================================================
# STEP 2: Add beach proximity feature
# ============================================================================
print("\n[2/2] Adding beach proximity feature...")

# Define beach/waterfront ZIPs for each coastal city
# 0 = inland, 1 = near water, 2 = beachfront/waterfront
beach_zips = {
    # Jacksonville - Atlantic beaches
    'Jacksonville': {
        2: [32250, 32266],  # Jacksonville Beach, Neptune Beach, Atlantic Beach
        1: [32233, 32224, 32225],  # Near beaches
    },
    
    # Miami - Atlantic beaches and waterfront
    'Miami': {
        2: [33109, 33139, 33140, 33141, 33154, 33160, 33180, 33181,  # Miami Beach
            33149, 33156, 33133, 33129, 33131],  # Waterfront areas
        1: [33125, 33126, 33127, 33128, 33130, 33132, 33134, 33135,  # Near water
            33136, 33137, 33138, 33142, 33145, 33146, 33150, 33155],
    },
    
    # San Francisco - Bay and ocean
    'SanFrancisco': {
        2: [94121, 94122, 94116, 94129, 94130,  # Ocean Beach, Presidio
            94133, 94111, 94105, 94107, 94158],  # Waterfront
        1: [94102, 94103, 94110, 94112, 94114, 94115, 94117,  # Near water
            94118, 94123, 94124, 94131, 94132],
    },
    
    # Tampa - Gulf coast
    'Tampa': {
        2: [33706, 33707, 33708, 33785, 33786,  # Beaches
            33767, 33770, 33771],  # Waterfront
        1: [33701, 33702, 33703, 33704, 33705, 33709,  # Near water
            33710, 33711, 33712, 33713, 33714],
    },
}

# Initialize beach_proximity column
df_clean['beach_proximity'] = 0  # Default: inland

# Assign beach proximity scores
for city, proximity_dict in beach_zips.items():
    for proximity_score, zip_list in proximity_dict.items():
        mask = (df_clean['city'] == city) & (df_clean['geoid'].isin(zip_list))
        df_clean.loc[mask, 'beach_proximity'] = proximity_score

# For non-coastal cities, beach_proximity stays 0
# For coastal cities not in the beach_zips dict, use is_coastal as proxy
coastal_cities = ['Jacksonville', 'Miami', 'SanFrancisco', 'Tampa']
for city in coastal_cities:
    # ZIPs in coastal city but not specifically marked as beach/waterfront get score of 0.5
    mask = (df_clean['city'] == city) & (df_clean['beach_proximity'] == 0)
    df_clean.loc[mask, 'beach_proximity'] = 0.5

print(f"\n   Beach proximity distribution:")
proximity_counts = df_clean['beach_proximity'].value_counts().sort_index()
for score, count in proximity_counts.items():
    if score == 0:
        label = "Inland"
    elif score == 0.5:
        label = "Coastal city (not beachfront)"
    elif score == 1:
        label = "Near beach/water"
    elif score == 2:
        label = "Beachfront/Waterfront"
    else:
        label = f"Score {score}"
    print(f"      {label}: {count} ZIPs ({count/len(df_clean)*100:.1f}%)")

# Show by city
print(f"\n   Beach proximity by coastal city:")
for city in coastal_cities:
    city_data = df_clean[df_clean['city'] == city]
    if len(city_data) > 0:
        print(f"\n      {city}:")
        city_proximity = city_data['beach_proximity'].value_counts().sort_index()
        for score, count in city_proximity.items():
            if score == 0.5:
                label = "Coastal (not beachfront)"
            elif score == 1:
                label = "Near beach"
            elif score == 2:
                label = "Beachfront"
            else:
                label = f"Score {score}"
            print(f"         {label}: {count} ZIPs")

# Check correlation with rent
rent_col = 'Median Home Rent (2020-2024)'
if rent_col in df_clean.columns:
    corr = df_clean['beach_proximity'].corr(df_clean[rent_col])
    print(f"\n   Correlation with rent: {corr:.3f}")
    
    # Compare to is_coastal
    coastal_corr = df_clean['is_coastal'].corr(df_clean[rent_col])
    print(f"   is_coastal correlation: {coastal_corr:.3f}")
    print(f"   Improvement: {corr - coastal_corr:.3f}")

# ============================================================================
# Save cleaned dataset
# ============================================================================
print("\n" + "=" * 80)
print("SAVING CLEANED DATASET")
print("=" * 80)

output_path = 'd4_modeling/data/master_dataset_final.csv'
df_clean.to_csv(output_path, index=False)

print(f"\n✅ Saved: {output_path}")
print(f"   Total ZIPs: {len(df_clean)}")
print(f"   Total columns: {len(df_clean.columns)}")
print(f"   Removed {len(df) - len(df_clean)} low-population ZIPs")
print(f"   Added beach_proximity feature (0, 0.5, 1, 2)")

print("\n" + "=" * 80)
