"""
Prepare Dashboard Data: Calculate percentiles and combined metrics for all ZIP codes
"""

import pandas as pd
import numpy as np
import pickle

print("=" * 80)
print("PREPARING DASHBOARD DATA")
print("=" * 80)

# Load final dataset (ALL ZIP codes excluding military bases and retirement communities)
print("\n📂 Loading full dataset (excluding military bases and retirement communities)...")
df = pd.read_csv('data/final_dataset_no_military.csv')

# Remove retirement communities
retirement_zips = [
    '32079', '32159', '33573', '34748', '33493', '33477', 
    '33480', '33446', '33767', '8640', '78633', '94595'
]
df['geoid'] = df['geoid'].astype(str)
df = df[~df['geoid'].isin(retirement_zips)].copy()

print(f"✅ Loaded {len(df)} ZIP codes (16 military + 12 retirement removed)")

# Add region feature
region_mapping = {
    'Columbus': 'Midwest', 'Indianapolis': 'Midwest', 'Louisville': 'Midwest',
    'Charlotte': 'South', 'Nashville': 'South', 'Jacksonville': 'South',
    'SanAntonio': 'South', 'Tampa': 'South', 'Orlando': 'South',
    'Austin': 'HighCost', 'Denver': 'HighCost', 'Miami': 'HighCost',
    'SanFrancisco': 'HighCost', 'Philadelphia': 'HighCost'
}
df['region'] = df['city'].map(region_mapping)

# One-hot encode region
region_dummies = pd.get_dummies(df['region'], prefix='region', drop_first=False)
df = pd.concat([df, region_dummies], axis=1)
print(f"✅ Added region features: {list(region_dummies.columns)}")

# Add urban classification (3 categories: Rural, Semi-Rural, Urban)
def classify_urban_type(row):
    """Classify ZIP code as Urban, Semi-Rural, or Rural"""
    population = row['Total Population (2020-2024)']
    housing_units = row['Total Housing Units (2020-2024)']
    transit = row['Commute Transportation by Public Transit (2020-2024)']
    
    density = population / housing_units if housing_units > 0 else 0
    
    if transit > 50 or (population > 10000 and density > 2.5):
        return 'Urban'
    elif population > 2000 or density > 2.0:
        return 'SemiRural'
    else:
        return 'Rural'

df['urban_type'] = df.apply(classify_urban_type, axis=1)

# One-hot encode urban type
urban_dummies = pd.get_dummies(df['urban_type'], prefix='urban', drop_first=False)
df = pd.concat([df, urban_dummies], axis=1)
print(f"✅ Added urban type features: {list(urban_dummies.columns)}")
print(f"   Urban: {(df['urban_type']=='Urban').sum()}, Semi-Rural: {(df['urban_type']=='SemiRural').sum()}, Rural: {(df['urban_type']=='Rural').sum()}")

# Calculate poverty rate (composite feature)
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
df['poverty_rate_pct'] = df['poverty_rate_pct'].fillna(0)
print(f"✅ Added poverty_rate_pct feature (range: {df['poverty_rate_pct'].min():.1f}% - {df['poverty_rate_pct'].max():.1f}%)")

# Load XGBoost model, imputer, and scaler
print("\n🤖 Loading XGBoost model (original), imputer, and scaler...")
with open('models/regression/xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

import joblib
imputer = joblib.load('results/prepared_data/imputer.pkl')
scaler = joblib.load('results/prepared_data/scaler.pkl')

# Prepare features for prediction (31 original + 3 region + 1 poverty_rate_pct)
feature_cols = [
    'Housing Built 1939 or Earlier (2020-2024)',
    'Housing Built 1940 to 1949 (2020-2024)',
    'Housing Built 1950 to 1959 (2020-2024)',
    'Housing Built 1960 to 1969 (2020-2024)',
    'Housing Built 1970 to 1979 (2020-2024)',
    'Housing Built 1980 to 1989 (2020-2024)',
    'Housing Built 1990 to 1999 (2020-2024)',
    'Housing Built 2000 to 2009 (2020-2024)',
    'Housing Built 2010 to 2019 (2020-2024)',
    'Housing Built 2020 or Later (2020-2024)',
    'Renter Excessive Housing Costs (2020-2024)',
    'Home Owner Excessive Housing Costs (2020-2024)',
    'Median Household Income (2020-2024)',
    'Per Capita Income (2020-2024)',
    'Unemployment Rate (2020-2024)',
    'Labor Force Participation Rate (2020-2024)',
    'Rental Vacancy Rate (2020-2024)',
    'Homeowner Vacancy Rate (2020-2024)',
    'Total Housing Units (2020-2024)',
    'Percent Change in Population (Difference Decennial Census 2020 - 2010)',
    'Total Population (2020-2024)',
    'Income 49% and Below Poverty Level (2020-2024)',
    'Income 50% to 99% the Poverty Level (2020-2024)',
    'Income 100% to 124% the Poverty Level (2020-2024)',
    'Income 125% to 149% the Poverty Level (2020-2024)',
    'Income 150% to 184% the Poverty Level (2020-2024)',
    'Income 185% to 199% the Poverty Level (2020-2024)',
    'Income 200% and Over the Poverty Level (2020-2024)',
    'Commute Mean Travel Time (2020-2024)',
    'Commute Transportation by Public Transit (2020-2024)',
    'No Vehicles Available (2020-2024)',
    'region_HighCost',
    'region_Midwest',
    'region_South',
    'urban_Rural',
    'urban_SemiRural',
    'urban_Urban',
    'poverty_rate_pct'
]

X = df[feature_cols].copy()

# Apply same preprocessing as training: impute then scale
print("🔧 Applying preprocessing (impute + scale)...")
X_imputed = imputer.transform(X)
X_scaled = scaler.transform(X_imputed)

# Generate predictions
print("🔮 Generating predictions...")
df['predicted_rent'] = model.predict(X_scaled)
df['actual_rent'] = df['Median Home Rent (2020-2024)']
df['rent_discrepancy_dollars'] = df['actual_rent'] - df['predicted_rent']
df['rent_discrepancy_pct'] = (df['rent_discrepancy_dollars'] / df['predicted_rent']) * 100

print("✅ Predictions complete")

# ============================================================================
# CALCULATE COMBINED METRICS
# ============================================================================
print("\n📊 Calculating combined metrics...")

# Calculate total population for percentage conversions
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

housing_cols = [col for col in df.columns if 'Housing Built' in col]
df['total_housing_units_calc'] = df[housing_cols].sum(axis=1)

# 1. Poverty Rate (% of population below 125% poverty)
poverty_count = (
    df['Income 49% and Below Poverty Level (2020-2024)'] +
    df['Income 50% to 99% the Poverty Level (2020-2024)'] +
    df['Income 100% to 124% the Poverty Level (2020-2024)']
)
df['poverty_rate'] = (poverty_count / df['total_income_pop']) * 100

# 2. Affluence Rate (% at 200%+ poverty)
df['affluence_rate'] = (df['Income 200% and Over the Poverty Level (2020-2024)'] / df['total_income_pop']) * 100

# 3. Average Housing Age (weighted average year built)
housing_years = {
    'Housing Built 1939 or Earlier (2020-2024)': 1930,
    'Housing Built 1940 to 1949 (2020-2024)': 1945,
    'Housing Built 1950 to 1959 (2020-2024)': 1955,
    'Housing Built 1960 to 1969 (2020-2024)': 1965,
    'Housing Built 1970 to 1979 (2020-2024)': 1975,
    'Housing Built 1980 to 1989 (2020-2024)': 1985,
    'Housing Built 1990 to 1999 (2020-2024)': 1995,
    'Housing Built 2000 to 2009 (2020-2024)': 2005,
    'Housing Built 2010 to 2019 (2020-2024)': 2015,
    'Housing Built 2020 or Later (2020-2024)': 2022
}

df['avg_year_built'] = 0
for col, year in housing_years.items():
    df['avg_year_built'] += (df[col] / df['total_housing_units_calc']) * year
df['avg_housing_age'] = 2024 - df['avg_year_built']  # Convert to age

# 4. Housing Cost Burden (convert counts to percentages)
# These are counts of households with excessive costs, need to convert to %
total_households = df['Total Housing Units (2020-2024)']
renter_burden_pct = (df['Renter Excessive Housing Costs (2020-2024)'] / total_households) * 100
owner_burden_pct = (df['Home Owner Excessive Housing Costs (2020-2024)'] / total_households) * 100
df['housing_cost_burden'] = (renter_burden_pct + owner_burden_pct) / 2
df['housing_cost_burden'] = df['housing_cost_burden'].fillna(0)  # Handle division by zero

# 5. Population Density (people per housing unit)
df['population_density'] = df['Total Population (2020-2024)'] / df['Total Housing Units (2020-2024)']

# 6. Transit Usage (convert count to percentage)
# Assuming total commuters ≈ labor force
labor_force = df['Total Population (2020-2024)'] * (df['Labor Force Participation Rate (2020-2024)'] / 100)
df['transit_usage'] = (df['Commute Transportation by Public Transit (2020-2024)'] / labor_force) * 100
df['transit_usage'] = df['transit_usage'].fillna(0)  # Handle division by zero

# 7. Rename for clarity
df['median_income'] = df['Median Household Income (2020-2024)']
df['population_growth'] = df['Percent Change in Population (Difference Decennial Census 2020 - 2010)']
# Cap population growth at reasonable values (remove outliers)
df['population_growth'] = df['population_growth'].clip(-50, 100)  # Cap at -50% to +100%
df['commute_time'] = df['Commute Mean Travel Time (2020-2024)']

print("✅ Combined metrics calculated")

# ============================================================================
# CALCULATE PERCENTILES
# ============================================================================
print("\n📈 Calculating percentiles...")

metrics_to_rank = [
    'actual_rent',
    'predicted_rent',
    'rent_discrepancy_pct',
    'median_income',
    'poverty_rate',
    'affluence_rate',
    'avg_housing_age',
    'housing_cost_burden',
    'population_growth',
    'population_density',
    'transit_usage',
    'commute_time'
]

for metric in metrics_to_rank:
    # Calculate percentile rank (0-100)
    df[f'{metric}_percentile'] = df[metric].rank(pct=True) * 100
    
print("✅ Percentiles calculated")

# ============================================================================
# CREATE DASHBOARD DATASET
# ============================================================================
print("\n💾 Creating dashboard dataset...")

dashboard_cols = [
    # Identifiers
    'geoid',
    'city',
    
    # Rent Metrics
    'actual_rent',
    'actual_rent_percentile',
    'predicted_rent',
    'predicted_rent_percentile',
    'rent_discrepancy_dollars',
    'rent_discrepancy_pct',
    'rent_discrepancy_pct_percentile',
    
    # Income Metrics
    'median_income',
    'median_income_percentile',
    'poverty_rate',
    'poverty_rate_percentile',
    'affluence_rate',
    'affluence_rate_percentile',
    
    # Housing Metrics
    'avg_housing_age',
    'avg_housing_age_percentile',
    'housing_cost_burden',
    'housing_cost_burden_percentile',
    
    # Population Metrics
    'population_growth',
    'population_growth_percentile',
    'population_density',
    'population_density_percentile',
    
    # Transit Metrics
    'transit_usage',
    'transit_usage_percentile',
    'commute_time',
    'commute_time_percentile'
]

dashboard_df = df[dashboard_cols].copy()

# Save dashboard data
dashboard_df.to_csv('dashboard/data/dashboard_data.csv', index=False)
print(f"✅ Saved dashboard data: {len(dashboard_df)} ZIP codes")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 80)
print("DASHBOARD DATA SUMMARY")
print("=" * 80)

print("\n📊 Rent Metrics:")
print(f"   Actual Rent: ${dashboard_df['actual_rent'].min():.0f} - ${dashboard_df['actual_rent'].max():.0f}")
print(f"   Predicted Rent: ${dashboard_df['predicted_rent'].min():.0f} - ${dashboard_df['predicted_rent'].max():.0f}")
print(f"   Discrepancy: {dashboard_df['rent_discrepancy_pct'].min():.1f}% to {dashboard_df['rent_discrepancy_pct'].max():.1f}%")

print("\n💰 Income Metrics:")
print(f"   Median Income: ${dashboard_df['median_income'].min():.0f} - ${dashboard_df['median_income'].max():.0f}")
print(f"   Poverty Rate: {dashboard_df['poverty_rate'].min():.1f}% - {dashboard_df['poverty_rate'].max():.1f}%")
print(f"   Affluence Rate: {dashboard_df['affluence_rate'].min():.1f}% - {dashboard_df['affluence_rate'].max():.1f}%")

print("\n🏘️ Housing Metrics:")
print(f"   Avg Housing Age: {dashboard_df['avg_housing_age'].min():.0f} - {dashboard_df['avg_housing_age'].max():.0f} years")
print(f"   Cost Burden: {dashboard_df['housing_cost_burden'].min():.1f}% - {dashboard_df['housing_cost_burden'].max():.1f}%")

print("\n👥 Population Metrics:")
print(f"   Growth: {dashboard_df['population_growth'].min():.1f}% - {dashboard_df['population_growth'].max():.1f}%")
print(f"   Density: {dashboard_df['population_density'].min():.1f} - {dashboard_df['population_density'].max():.1f} per unit")

print("\n🚇 Transit Metrics:")
print(f"   Transit Usage: {dashboard_df['transit_usage'].min():.1f}% - {dashboard_df['transit_usage'].max():.1f}%")
print(f"   Commute Time: {dashboard_df['commute_time'].min():.1f} - {dashboard_df['commute_time'].max():.1f} min")

print("\n" + "=" * 80)
print("✅ DASHBOARD DATA READY!")
print("=" * 80)
print("\n📁 File: dashboard/data/dashboard_data.csv")
print(f"📊 {len(dashboard_df)} ZIP codes across {dashboard_df['city'].nunique()} cities")
