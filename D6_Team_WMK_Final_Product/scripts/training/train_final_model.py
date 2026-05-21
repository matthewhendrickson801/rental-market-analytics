"""
Train final model with 70/15/15 split
Then analyze residuals to find affordable housing opportunities
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
print("TRAINING FINAL MODEL - 70/15/15 SPLIT")
print("=" * 80)

# Load cleaned dataset
df = pd.read_csv(DATA_DIR / 'master_dataset_cleaned.csv')
print(f"\nDataset: {df.shape[0]} ZIPs, {df.shape[1]} columns")

# Prepare features
target_col = 'Median Home Rent (2020-2024)'
exclude_cols = [
    'city', 'geoid', 'feature label', 'feature id', 'shid',
    target_col, 'data_source',
    'Expected_Rent_From_Income', 'Income_Rent_Mismatch_Ratio',
    'Basic_Rent_Waste', 'Rent_Per_Commute_Minute', 'Commute_Rent_Mismatch',
    'Comprehensive_Rent_Waste_Score', 'Total_Monthly_Location_Cost',
    'Time_Value_Rent_Waste', 'Comprehensive_Mismatch_Score',
    'Walkability_Premium_Index', 'Luxury_Vacancy_Flag',
    'Income_Rent_Mismatch_Ratio_Std', 'Walkability_Premium_Index_Std',
    'Boom_Category', 'jobs_per_capita'
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

# Add dummies
if 'Transit_Accessibility_Index' in X.columns:
    X['urban_Urban'] = ((X['Commute Transportation by Public Transit (2020-2024)'] > 50) | 
                        ((X['Total Population (2020-2024)'] > 10000) & 
                         (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.5))).astype(int)
    X['urban_SemiRural'] = ((X['Total Population (2020-2024)'] > 2000) | 
                            (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.0)).astype(int)
    X['urban_Rural'] = ((X['urban_Urban'] == 0) & (X['urban_SemiRural'] == 0)).astype(int)
    
    high_cost_cities = ['Austin', 'Denver', 'Miami', 'SanFrancisco', 'Philadelphia']
    midwest_cities = ['Columbus', 'Indianapolis', 'Louisville']
    
    X['region_HighCost'] = df['city'].isin(high_cost_cities).astype(int)
    X['region_Midwest'] = df['city'].isin(midwest_cities).astype(int)
    X['region_South'] = ((~df['city'].isin(high_cost_cities)) & (~df['city'].isin(midwest_cities))).astype(int)

print(f"Features: {X.shape[1]}")

# 70/15/15 split
print("\nCreating 70/15/15 split...")
test_size = 0.15
val_size = 0.15 / 0.85  # 15% of remaining after test

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

# Train
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
print("\nMaking predictions on all data...")
X_all_scaled = scaler.transform(X)
y_pred_all = model.predict(X_all_scaled)

# Add predictions and residuals to dataframe
df['predicted_rent'] = y_pred_all
df['residual'] = y - y_pred_all  # Actual - Predicted
df['residual_pct'] = (df['residual'] / y) * 100
df['abs_residual'] = np.abs(df['residual'])

# Evaluate
print("\nModel Performance:")
print("=" * 80)

y_train_pred = model.predict(X_train_scaled)
y_val_pred = model.predict(X_val_scaled)
y_test_pred = model.predict(X_test_scaled)

train_r2 = r2_score(y_train, y_train_pred)
val_r2 = r2_score(y_val, y_val_pred)
test_r2 = r2_score(y_test, y_test_pred)

print(f"Train R²: {train_r2:.4f}")
print(f"Val R²:   {val_r2:.4f}")
print(f"Test R²:  {test_r2:.4f}")
print(f"Gap:      {train_r2 - val_r2:.4f}")

# Save model
print("\nSaving model...")
model_path = MODELS_DIR / 'xgboost_final.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

scaler_path = MODELS_DIR / 'scaler_final.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

# Save predictions with residuals
predictions_path = DATA_DIR / 'predictions_with_residuals.csv'
df.to_csv(predictions_path, index=False)
print(f"Saved predictions: {predictions_path}")

print("\n" + "=" * 80)
print("TRAINING COMPLETE - Ready for mismatch analysis")
print("=" * 80)
