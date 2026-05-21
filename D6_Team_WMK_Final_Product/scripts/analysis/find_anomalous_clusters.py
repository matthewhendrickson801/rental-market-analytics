"""
Find Anomalous ZIP Code Clusters
Identify ZIP codes with unusual characteristics that may distort the model
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("SEARCHING FOR ANOMALOUS ZIP CODE CLUSTERS")
print("=" * 80)

# Load data
df = pd.read_csv('data/final_dataset_no_military.csv')
df['geoid'] = df['geoid'].astype(str)

# Remove already-excluded retirement communities
retirement_zips = ['32079', '32159', '33573', '34748', '33493', '33477', 
                   '33480', '33446', '33767', '8640', '78633', '94595']
df = df[~df['geoid'].isin(retirement_zips)]

print(f"\nAnalyzing {len(df)} ZIP codes")

# Load predictions to find high-error ZIPs
dashboard_df = pd.read_csv('dashboard/data/dashboard_data.csv')
dashboard_df['geoid'] = dashboard_df['geoid'].astype(str)

# Merge predictions
df = df.merge(dashboard_df[['geoid', 'predicted_rent', 'rent_discrepancy_pct']], 
              on='geoid', how='left')

print("\n" + "=" * 80)
print("CLUSTER 1: COLLEGE TOWNS / UNIVERSITY AREAS")
print("=" * 80)
print("Characteristics: High population, low income, high rental vacancy")

# College towns: High rental vacancy (>10%), low median income (<$50k), high population (>5k)
college_candidates = df[
    (df['Rental Vacancy Rate (2020-2024)'] > 10) &
    (df['Median Household Income (2020-2024)'] < 50000) &
    (df['Total Population (2020-2024)'] > 5000)
].copy()

print(f"\nFound {len(college_candidates)} potential college town ZIPs:")
for idx, row in college_candidates.head(15).iterrows():
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    print(f"  Median Income: ${row['Median Household Income (2020-2024)']:.0f}")
    print(f"  Rental Vacancy: {row['Rental Vacancy Rate (2020-2024)']:.1f}%")
    print(f"  Actual Rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    if not pd.isna(row['rent_discrepancy_pct']):
        print(f"  Prediction Error: {row['rent_discrepancy_pct']:.1f}%")

print("\n" + "=" * 80)
print("CLUSTER 2: EXTREME POVERTY AREAS")
print("=" * 80)
print("Characteristics: Very high poverty (>50%), low income")

# Calculate poverty rate
income_cols = [
    'Income 49% and Below Poverty Level (2020-2024)',
    'Income 50% to 99% the Poverty Level (2020-2024)',
    'Income 100% to 124% the Poverty Level (2020-2024)',
    'Income 125% to 149% the Poverty Level (2020-2024)',
    'Income 150% to 184% the Poverty Level (2020-2024)',
    'Income 185% to 199% the Poverty Level (2020-2024)',
    'Income 200% and Over the Poverty Level (2020-2024)'
]
df['total_income_pop'] = df[income_cols].sum(axis=1)
poverty_count = (df['Income 49% and Below Poverty Level (2020-2024)'] +
                 df['Income 50% to 99% the Poverty Level (2020-2024)'] +
                 df['Income 100% to 124% the Poverty Level (2020-2024)'])
df['poverty_rate_pct'] = (poverty_count / df['total_income_pop']) * 100

extreme_poverty = df[df['poverty_rate_pct'] > 50].copy()

print(f"\nFound {len(extreme_poverty)} extreme poverty ZIPs (>50% poverty rate):")
for idx, row in extreme_poverty.head(15).iterrows():
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Poverty Rate: {row['poverty_rate_pct']:.1f}%")
    print(f"  Median Income: ${row['Median Household Income (2020-2024)']:.0f}")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    print(f"  Actual Rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    if not pd.isna(row['rent_discrepancy_pct']):
        print(f"  Prediction Error: {row['rent_discrepancy_pct']:.1f}%")

print("\n" + "=" * 80)
print("CLUSTER 3: VERY SMALL POPULATIONS")
print("=" * 80)
print("Characteristics: Population <500 (too small for reliable rent data)")

tiny_pop = df[df['Total Population (2020-2024)'] < 500].copy()

print(f"\nFound {len(tiny_pop)} very small population ZIPs (<500 people):")
for idx, row in tiny_pop.head(15).iterrows():
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    print(f"  Housing Units: {row['Total Housing Units (2020-2024)']:.0f}")
    print(f"  Actual Rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    print(f"  Labor Force: {row['Labor Force Participation Rate (2020-2024)']:.1f}%")
    if not pd.isna(row['rent_discrepancy_pct']):
        print(f"  Prediction Error: {row['rent_discrepancy_pct']:.1f}%")

print("\n" + "=" * 80)
print("CLUSTER 4: EXTREME RENT OUTLIERS")
print("=" * 80)
print("Characteristics: Rent >3 std deviations from mean")

mean_rent = df['Median Home Rent (2020-2024)'].mean()
std_rent = df['Median Home Rent (2020-2024)'].std()
threshold = 3 * std_rent

extreme_outliers = df[
    (df['Median Home Rent (2020-2024)'] < mean_rent - threshold) |
    (df['Median Home Rent (2020-2024)'] > mean_rent + threshold)
].copy()

print(f"\nFound {len(extreme_outliers)} extreme rent outliers (>3 std from mean):")
print(f"Mean rent: ${mean_rent:.0f}, Std: ${std_rent:.0f}")
print(f"Threshold: <${mean_rent - threshold:.0f} or >${mean_rent + threshold:.0f}")

for idx, row in extreme_outliers.head(15).iterrows():
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Actual Rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    print(f"  Median Income: ${row['Median Household Income (2020-2024)']:.0f}")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    if not pd.isna(row['rent_discrepancy_pct']):
        print(f"  Prediction Error: {row['rent_discrepancy_pct']:.1f}%")

print("\n" + "=" * 80)
print("CLUSTER 5: COMMERCIAL/INDUSTRIAL AREAS")
print("=" * 80)
print("Characteristics: Very low housing units relative to population")

# Commercial areas: Very high density (>5 people per housing unit) - likely apartments/commercial
commercial_candidates = df[
    (df['Total Population (2020-2024)'] / df['Total Housing Units (2020-2024)'] > 5) &
    (df['Total Population (2020-2024)'] > 1000)
].copy()

print(f"\nFound {len(commercial_candidates)} potential commercial/industrial ZIPs:")
print("(Density >5 people per housing unit)")

for idx, row in commercial_candidates.head(15).iterrows():
    density = row['Total Population (2020-2024)'] / row['Total Housing Units (2020-2024)']
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    print(f"  Housing Units: {row['Total Housing Units (2020-2024)']:.0f}")
    print(f"  Density: {density:.1f} people/unit")
    print(f"  Actual Rent: ${row['Median Home Rent (2020-2024)']:.0f}")
    if not pd.isna(row['rent_discrepancy_pct']):
        print(f"  Prediction Error: {row['rent_discrepancy_pct']:.1f}%")

print("\n" + "=" * 80)
print("CLUSTER 6: HIGH PREDICTION ERROR ZIPS")
print("=" * 80)
print("Characteristics: Absolute prediction error >40%")

high_error = df[abs(df['rent_discrepancy_pct']) > 40].copy()
high_error = high_error.sort_values('rent_discrepancy_pct', key=abs, ascending=False)

print(f"\nFound {len(high_error)} high-error ZIPs (>40% prediction error):")

for idx, row in high_error.head(20).iterrows():
    print(f"\n{row['geoid']} ({row['city']})")
    print(f"  Actual: ${row['Median Home Rent (2020-2024)']:.0f}, Predicted: ${row['predicted_rent']:.0f}")
    print(f"  Error: {row['rent_discrepancy_pct']:.1f}%")
    print(f"  Income: ${row['Median Household Income (2020-2024)']:.0f}")
    print(f"  Population: {row['Total Population (2020-2024)']:.0f}")
    print(f"  Labor Force: {row['Labor Force Participation Rate (2020-2024)']:.1f}%")
    print(f"  Poverty: {row['poverty_rate_pct']:.1f}%")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nPotential clusters to investigate:")
print(f"  College towns: {len(college_candidates)} ZIPs")
print(f"  Extreme poverty: {len(extreme_poverty)} ZIPs")
print(f"  Very small population: {len(tiny_pop)} ZIPs")
print(f"  Extreme rent outliers: {len(extreme_outliers)} ZIPs")
print(f"  Commercial/industrial: {len(commercial_candidates)} ZIPs")
print(f"  High prediction error: {len(high_error)} ZIPs")
