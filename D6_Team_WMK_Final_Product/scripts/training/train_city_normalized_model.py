"""
Train model with city-normalized rent
Target: Deviation from city median rent
This removes regional bias and forces model to learn within-city patterns
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
import pickle
import json

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models' / 'regression'
RESULTS_DIR = BASE_DIR / 'results'

print("=" * 80)
print("TRAINING CITY-NORMALIZED MODEL")
print("Target: Rent deviation from city median")
print("=" * 80)

# Load cleaned dataset
df = pd.read_csv(DATA_DIR / 'master_dataset_cleaned.csv')
print(f"\nDataset: {df.shape[0]} ZIPs, {df.shape[1]} columns")

# Calculate city median rents
print("\nCalculating city median rents...")
city_medians = df.groupby('city')['Median Home Rent (2020-2024)'].median()
print("\nCity Median Rents:")
for city, median in city_medians.sort_values().items():
    print(f"  {city:<20} ${median:,.0f}")

# Create normalized target: deviation from city median
df['city_median_rent'] = df['city'].map(city_medians)
df['rent_deviation'] = df['Median Home Rent (2020-2024)'] - df['city_median_rent']
df['rent_deviation_pct'] = (df['rent_deviation'] / df['city_median_rent']) * 100

print(f"\nRent Deviation Statistics:")
print(f"  Mean:   ${df['rent_deviation'].mean():.2f}")
print(f"  Median: ${df['rent_deviation'].median():.2f}")
print(f"  Std:    ${df['rent_deviation'].std():.2f}")
print(f"  Min:    ${df['rent_deviation'].min():.2f}")
print(f"  Max:    ${df['rent_deviation'].max():.2f}")

# Prepare features - REMOVE REGION FEATURES
target_col = 'rent_deviation'
exclude_cols = [
    'city', 'geoid', 'feature label', 'feature id', 'shid',
    'Median Home Rent (2020-2024)', 'data_source',
    'Expected_Rent_From_Income', 'Income_Rent_Mismatch_Ratio',
    'Basic_Rent_Waste', 'Rent_Per_Commute_Minute', 'Commute_Rent_Mismatch',
    'Comprehensive_Rent_Waste_Score', 'Total_Monthly_Location_Cost',
    'Time_Value_Rent_Waste', 'Comprehensive_Mismatch_Score',
    'Walkability_Premium_Index', 'Luxury_Vacancy_Flag',
    'Income_Rent_Mismatch_Ratio_Std', 'Walkability_Premium_Index_Std',
    'Boom_Category', 'jobs_per_capita',
    # NEW: Remove city/region identifiers
    'city_median_rent', 'rent_deviation', 'rent_deviation_pct'
]

y = df[target_col].copy()
valid_idx = y.notna()
df = df[valid_idx].copy()
y = y[valid_idx].copy()

feature_cols = [col for col in df.columns if col not in exclude_cols]
X = df[feature_cols].copy()

# Fill missing
for col in X.columns:
    if X[col].isna().sum() > 0:
        X[col] = X[col].fillna(X[col].median())

# Add urban dummies but NOT region dummies
if 'Transit_Accessibility_Index' in X.columns:
    X['urban_Urban'] = ((X['Commute Transportation by Public Transit (2020-2024)'] > 50) | 
                        ((X['Total Population (2020-2024)'] > 10000) & 
                         (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.5))).astype(int)
    X['urban_SemiRural'] = ((X['Total Population (2020-2024)'] > 2000) | 
                            (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.0)).astype(int)
    X['urban_Rural'] = ((X['urban_Urban'] == 0) & (X['urban_SemiRural'] == 0)).astype(int)
    
    # DO NOT ADD REGION FEATURES
    print(f"\n✓ Added urban classification (no region features)")

print(f"\nFeatures: {X.shape[1]}")

# Check if region features were removed
region_features = [col for col in X.columns if 'region' in col.lower()]
if region_features:
    print(f"⚠️  WARNING: Region features still present: {region_features}")
else:
    print(f"✓ Region features successfully removed")

# 70/15/15 split
print("\nCreating 70/15/15 split...")
test_size = 0.15
val_size = 0.15 / 0.85

X_temp, X_test, y_temp, y_test, idx_temp, idx_test = train_test_split(
    X, y, X.index, test_size=test_size, random_state=42, stratify=df['city']
)
X_train, X_val, y_train, y_val, idx_train, idx_val = train_test_split(
    X_temp, y_temp, X_temp.index, test_size=val_size, random_state=42, 
    stratify=df.loc[X_temp.index, 'city']
)

print(f"  Train: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"  Val:   {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
print(f"  Test:  {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")

# Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Train with same hyperparameters
print("\nTraining XGBoost...")
params = {
    'objective': 'reg:squarederror',
    'max_depth': 5,
    'learning_rate': 0.03,
    'n_estimators': 400,
    'min_child_weight': 5,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'gamma': 0.2,
    'reg_alpha': 0.5,
    'reg_lambda': 2.0,
    'random_state': 42,
    'n_jobs': -1
}

model = xgb.XGBRegressor(**params)
model.fit(X_train_scaled, y_train, verbose=False)

# Predict on ALL data
print("\nMaking predictions...")
X_all_scaled = scaler.transform(X)
y_pred_deviation = model.predict(X_all_scaled)

# Convert back to actual rent
df['predicted_deviation'] = y_pred_deviation
df['predicted_rent_normalized'] = df['city_median_rent'] + df['predicted_deviation']
df['residual_normalized'] = df['Median Home Rent (2020-2024)'] - df['predicted_rent_normalized']

# Evaluate
print("\nModel Performance (predicting deviation from city median):")
print("=" * 80)

y_train_pred = model.predict(X_train_scaled)
y_val_pred = model.predict(X_val_scaled)
y_test_pred = model.predict(X_test_scaled)

train_r2 = r2_score(y_train, y_train_pred)
val_r2 = r2_score(y_val, y_val_pred)
test_r2 = r2_score(y_test, y_test_pred)

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

print(f"\nDeviation Prediction:")
print(f"  Train R²: {train_r2:.4f}  (RMSE: ${train_rmse:.2f})")
print(f"  Val R²:   {val_r2:.4f}  (RMSE: ${val_rmse:.2f})")
print(f"  Test R²:  {test_r2:.4f}  (RMSE: ${test_rmse:.2f})")
print(f"  Gap:      {train_r2 - val_r2:.4f}")

# Evaluate actual rent prediction
y_train_actual = df.loc[idx_train, 'Median Home Rent (2020-2024)']
y_val_actual = df.loc[idx_val, 'Median Home Rent (2020-2024)']
y_test_actual = df.loc[idx_test, 'Median Home Rent (2020-2024)']

y_train_pred_actual = df.loc[idx_train, 'predicted_rent_normalized']
y_val_pred_actual = df.loc[idx_val, 'predicted_rent_normalized']
y_test_pred_actual = df.loc[idx_test, 'predicted_rent_normalized']

train_r2_actual = r2_score(y_train_actual, y_train_pred_actual)
val_r2_actual = r2_score(y_val_actual, y_val_pred_actual)
test_r2_actual = r2_score(y_test_actual, y_test_pred_actual)

print(f"\nActual Rent Prediction (after adding city median back):")
print(f"  Train R²: {train_r2_actual:.4f}")
print(f"  Val R²:   {val_r2_actual:.4f}")
print(f"  Test R²:  {test_r2_actual:.4f}")

# Feature importance
print("\nTop 20 Most Important Features:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for i, row in feature_importance.head(20).iterrows():
    print(f"   {row['feature']:50s} {row['importance']:.4f}")

# Save model
print("\nSaving model...")
model_path = MODELS_DIR / 'xgboost_city_normalized.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

scaler_path = MODELS_DIR / 'scaler_city_normalized.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

# Save city medians for deployment
city_medians_path = MODELS_DIR / 'city_medians.json'
with open(city_medians_path, 'w') as f:
    json.dump(city_medians.to_dict(), f, indent=2)

# Save predictions
predictions_path = DATA_DIR / 'predictions_city_normalized.csv'
df.to_csv(predictions_path, index=False)

print(f"✓ Model saved to: {model_path}")
print(f"✓ City medians saved to: {city_medians_path}")
print(f"✓ Predictions saved to: {predictions_path}")

print("\n" + "=" * 80)
print("COMPARISON TO ORIGINAL MODEL")
print("=" * 80)
print(f"\nOriginal model (with region features):")
print(f"  Val R²: 0.9815")
print(f"\nCity-normalized model (no region features):")
print(f"  Val R²: {val_r2_actual:.4f}")
print(f"\nDifference: {0.9815 - val_r2_actual:.4f}")

if val_r2_actual < 0.90:
    print("\n✓ SUCCESS: Model R² reduced, residuals should be more meaningful")
else:
    print("\n⚠️  Model still very accurate - may need more aggressive changes")

print("\n" + "=" * 80)
