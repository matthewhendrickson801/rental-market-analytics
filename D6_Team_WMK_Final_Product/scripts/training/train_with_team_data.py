"""
Train XGBoost with integrated team data
Goal: Push R² from 0.757 to 0.86+
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
print("TRAINING XGBOOST WITH TEAM DATA")
print("Goal: R² > 0.86")
print("=" * 80)

# Load master dataset
print("\n1. Loading master dataset...")
df = pd.read_csv(DATA_DIR / 'master_dataset_with_team_data.csv')
print(f"   Shape: {df.shape}")
print(f"   Cities: {df['city'].nunique()}")

# Prepare features
print("\n2. Preparing features...")

# Target variable
target_col = 'Median Home Rent (2020-2024)'
y = df[target_col].copy()

# Remove rows with missing target
valid_idx = y.notna()
df = df[valid_idx].copy()
y = y[valid_idx].copy()
print(f"   Valid samples: {len(df)}")

# Feature columns to exclude
exclude_cols = [
    'city', 'geoid', 'feature label', 'feature id', 'shid',
    target_col, 'data_source',
    # Exclude engineered features that use rent
    'Expected_Rent_From_Income', 'Income_Rent_Mismatch_Ratio',
    'Basic_Rent_Waste', 'Rent_Per_Commute_Minute', 'Commute_Rent_Mismatch',
    'Comprehensive_Rent_Waste_Score', 'Total_Monthly_Location_Cost',
    'Time_Value_Rent_Waste', 'Comprehensive_Mismatch_Score',
    'Walkability_Premium_Index', 'Luxury_Vacancy_Flag',
    'Income_Rent_Mismatch_Ratio_Std', 'Walkability_Premium_Index_Std',
    'Boom_Category'
]

# Get feature columns
feature_cols = [col for col in df.columns if col not in exclude_cols]
print(f"   Feature columns: {len(feature_cols)}")

# Handle missing values
X = df[feature_cols].copy()
for col in X.columns:
    if X[col].isna().sum() > 0:
        X[col].fillna(X[col].median(), inplace=True)

# Create urban/region dummies
if 'Transit_Accessibility_Index' in X.columns:
    # Urban classification
    X['urban_Urban'] = ((X['Commute Transportation by Public Transit (2020-2024)'] > 50) | 
                        ((X['Total Population (2020-2024)'] > 10000) & 
                         (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.5))).astype(int)
    X['urban_SemiRural'] = ((X['Total Population (2020-2024)'] > 2000) | 
                            (X['Total Population (2020-2024)'] / X['Total Housing Units (2020-2024)'] > 2.0)).astype(int)
    X['urban_Rural'] = ((X['urban_Urban'] == 0) & (X['urban_SemiRural'] == 0)).astype(int)
    
    # Region classification
    high_cost_cities = ['Austin', 'Denver', 'Miami', 'SanFrancisco', 'Philadelphia']
    midwest_cities = ['Columbus', 'Indianapolis', 'Louisville']
    
    X['region_HighCost'] = df['city'].isin(high_cost_cities).astype(int)
    X['region_Midwest'] = df['city'].isin(midwest_cities).astype(int)
    X['region_South'] = ((~df['city'].isin(high_cost_cities)) & (~df['city'].isin(midwest_cities))).astype(int)

print(f"   Final features: {X.shape[1]}")

# Stratified split by city
print("\n3. Creating train/val/test splits...")
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=df['city']
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.1875, random_state=42, stratify=df.loc[X_temp.index, 'city']  # 0.1875 of 0.80 = 0.15 of total
)

print(f"   Train: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"   Val:   {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
print(f"   Test:  {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")

# Standardize features
print("\n4. Standardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost
print("\n5. Training XGBoost...")
print("   Hyperparameters:")
params = {
    'objective': 'reg:squarederror',
    'max_depth': 6,  # Increased from 5
    'learning_rate': 0.05,
    'n_estimators': 300,  # Increased from 200
    'min_child_weight': 3,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'gamma': 0.1,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'random_state': 42,
    'n_jobs': -1
}

for key, value in params.items():
    print(f"      {key}: {value}")

model = xgb.XGBRegressor(**params)
model.fit(
    X_train_scaled, y_train,
    eval_set=[(X_train_scaled, y_train), (X_val_scaled, y_val)],
    verbose=False
)

# Predictions
print("\n6. Making predictions...")
y_train_pred = model.predict(X_train_scaled)
y_val_pred = model.predict(X_val_scaled)
y_test_pred = model.predict(X_test_scaled)

# Evaluate
print("\n7. Model Performance:")
print("=" * 80)

def evaluate(y_true, y_pred, dataset_name):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.median(np.abs((y_true - y_pred) / y_true)) * 100
    
    print(f"\n{dataset_name}:")
    print(f"   R² Score:  {r2:.4f}")
    print(f"   RMSE:      ${rmse:.2f}")
    print(f"   MAE:       ${mae:.2f}")
    print(f"   MAPE:      {mape:.2f}%")
    
    return {'r2': r2, 'rmse': rmse, 'mae': mae, 'mape': mape}

train_metrics = evaluate(y_train, y_train_pred, "Training Set")
val_metrics = evaluate(y_val, y_val_pred, "Validation Set")
test_metrics = evaluate(y_test, y_test_pred, "Test Set")

print("\n" + "=" * 80)
print(f"VALIDATION R²: {val_metrics['r2']:.4f}")
print(f"TARGET: 0.8600")
if val_metrics['r2'] >= 0.86:
    print("🎉 TARGET ACHIEVED!")
else:
    improvement_needed = 0.86 - val_metrics['r2']
    print(f"📊 Need +{improvement_needed:.4f} to reach target")
print("=" * 80)

# Feature importance
print("\n8. Top 20 Most Important Features:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for i, row in feature_importance.head(20).iterrows():
    print(f"   {row['feature']:50s} {row['importance']:.4f}")

# Save model
print("\n9. Saving model...")
model_path = MODELS_DIR / 'xgboost_with_team_data.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"   Model saved to: {model_path}")

# Save scaler
scaler_path = MODELS_DIR / 'scaler_with_team_data.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"   Scaler saved to: {scaler_path}")

# Save metrics
metrics_path = RESULTS_DIR / 'metrics' / 'xgboost_with_team_data_metrics.json'
metrics = {
    'train': train_metrics,
    'validation': val_metrics,
    'test': test_metrics,
    'n_features': X.shape[1],
    'n_samples': len(X),
    'hyperparameters': params
}
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2)
print(f"   Metrics saved to: {metrics_path}")

# Save feature importance
fi_path = RESULTS_DIR / 'metrics' / 'xgboost_with_team_data_feature_importance.csv'
feature_importance.to_csv(fi_path, index=False)
print(f"   Feature importance saved to: {fi_path}")

print("\n" + "=" * 80)
print("TRAINING COMPLETE!")
print("=" * 80)
