"""
Generate predictions for ALL ZIPs in the dataset (not just test set)
for comprehensive reporting
"""

import pandas as pd
import pickle
import numpy as np

print("=" * 80)
print("GENERATING PREDICTIONS FOR ALL ZIPS")
print("=" * 80)

# Load full dataset
df = pd.read_csv('d4_modeling/data/master_dataset_with_housing_mix.csv')
print(f"\nTotal ZIPs in dataset: {len(df)}")

# Load model
with open('d4_modeling/models/regression/xgboost_hybrid.pkl', 'rb') as f:
    model = pickle.load(f)

# Load feature list
with open('d4_modeling/models/regression/hybrid_features.txt', 'r') as f:
    feature_cols = [line.strip() for line in f.readlines()]

print(f"Model features: {len(feature_cols)}")

# Prepare features
X = df[feature_cols].copy()
X = X.replace([np.inf, -np.inf], np.nan)

# Make predictions
predictions = model.predict(X)

# Create results dataframe
results = pd.DataFrame({
    'geoid': df['geoid'],
    'city': df['city'],
    'actual_rent': df['Median Home Rent (2020-2024)'],
    'predicted_rent': predictions,
    'residual': df['Median Home Rent (2020-2024)'] - predictions,
    'abs_residual': np.abs(df['Median Home Rent (2020-2024)'] - predictions),
    'pct_error': ((df['Median Home Rent (2020-2024)'] - predictions) / df['Median Home Rent (2020-2024)'] * 100),
    'population': df['Total Population (2020-2024)'],
    'bachelors_plus': df['education_bachelors_plus'],
    'median_income': df['Median Household Income (2020-2024)'],
    'urban_rural': df['urban_rural'],
    'beach_proximity': df['beach_proximity'],
    'is_coastal': df['is_coastal']
})

# Save
output_path = 'd4_modeling/results/all_predictions.csv'
results.to_csv(output_path, index=False)
print(f"\n✅ Saved: {output_path}")

# Summary by city
print("\n" + "=" * 80)
print("PREDICTIONS BY CITY")
print("=" * 80)

city_summary = results.groupby('city').agg({
    'geoid': 'count',
    'actual_rent': 'mean',
    'predicted_rent': 'mean',
    'abs_residual': 'mean'
}).round(2)

city_summary.columns = ['ZIPs', 'Avg_Actual', 'Avg_Predicted', 'MAE']
print(city_summary.to_string())

print("\n" + "=" * 80)
