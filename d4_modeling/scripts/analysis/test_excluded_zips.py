"""
Test if improved model can predict excluded ZIPs (military bases & retirement communities)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models' / 'regression'

print("=" * 80)
print("TESTING EXCLUDED ZIPS WITH IMPROVED MODEL")
print("=" * 80)

# Load model and scaler
print("\n1. Loading model...")
with open(MODELS_DIR / 'xgboost_with_team_data.pkl', 'rb') as f:
    model = pickle.load(f)
with open(MODELS_DIR / 'scaler_with_team_data.pkl', 'rb') as f:
    scaler = pickle.load(f)
print("   ✓ Model loaded (R² = 0.9724)")

# Load excluded ZIPs with full features
print("\n2. Loading excluded ZIPs...")
excluded_df = pd.read_csv(DATA_DIR / 'excluded_zips_full_features.csv')
print(f"   Total excluded ZIPs found: {len(excluded_df)}")
print(f"   Exclusion types: {excluded_df['exclusion_type'].value_counts().to_dict()}")

# Prepare features (same as training)
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
    'Boom_Category', 'exclusion_type'
]

# Get valid samples with rent data
valid_idx = excluded_df[target_col].notna()
test_df = excluded_df[valid_idx].copy()
y_true = test_df[target_col].values

print(f"\n3. Valid samples with rent data: {len(test_df)}")

if len(test_df) == 0:
    print("\n❌ No excluded ZIPs have rent data to test predictions")
    print("   This is expected - these ZIPs were excluded because they're outliers")
    exit(0)

# Prepare features
feature_cols = [col for col in test_df.columns if col not in exclude_cols]
X_test = test_df[feature_cols].copy()

# Handle missing values
for col in X_test.columns:
    if X_test[col].isna().sum() > 0:
        X_test[col].fillna(X_test[col].median(), inplace=True)

# Create urban/region dummies
if 'Transit_Accessibility_Index' in X_test.columns:
    X_test['urban_Urban'] = ((X_test['Commute Transportation by Public Transit (2020-2024)'] > 50) | 
                             ((X_test['Total Population (2020-2024)'] > 10000) & 
                              (X_test['Total Population (2020-2024)'] / X_test['Total Housing Units (2020-2024)'] > 2.5))).astype(int)
    X_test['urban_SemiRural'] = ((X_test['Total Population (2020-2024)'] > 2000) | 
                                 (X_test['Total Population (2020-2024)'] / X_test['Total Housing Units (2020-2024)'] > 2.0)).astype(int)
    X_test['urban_Rural'] = ((X_test['urban_Urban'] == 0) & (X_test['urban_SemiRural'] == 0)).astype(int)
    
    high_cost_cities = ['Austin', 'Denver', 'Miami', 'SanFrancisco', 'Philadelphia']
    midwest_cities = ['Columbus', 'Indianapolis', 'Louisville']
    
    X_test['region_HighCost'] = test_df['city'].isin(high_cost_cities).astype(int)
    X_test['region_Midwest'] = test_df['city'].isin(midwest_cities).astype(int)
    X_test['region_South'] = ((~test_df['city'].isin(high_cost_cities)) & (~test_df['city'].isin(midwest_cities))).astype(int)

# Standardize
X_test_scaled = scaler.transform(X_test)

# Predict
print("\n4. Making predictions...")
y_pred = model.predict(X_test_scaled)

# Evaluate
print("\n5. Results:")
print("=" * 80)

r2 = r2_score(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
mape = np.median(np.abs((y_true - y_pred) / y_true)) * 100

print(f"\nOverall Performance on Excluded ZIPs:")
print(f"   R² Score:  {r2:.4f}")
print(f"   RMSE:      ${rmse:.2f}")
print(f"   MAE:       ${mae:.2f}")
print(f"   MAPE:      {mape:.2f}%")

# By exclusion type
print("\n" + "-" * 80)
print("By Exclusion Type:")
for exc_type in test_df['exclusion_type'].unique():
    mask = test_df['exclusion_type'] == exc_type
    if mask.sum() > 0:
        y_t = y_true[mask]
        y_p = y_pred[mask]
        r2_type = r2_score(y_t, y_p)
        rmse_type = np.sqrt(mean_squared_error(y_t, y_p))
        mae_type = mean_absolute_error(y_t, y_p)
        
        print(f"\n{exc_type} ({mask.sum()} ZIPs):")
        print(f"   R² Score:  {r2_type:.4f}")
        print(f"   RMSE:      ${rmse_type:.2f}")
        print(f"   MAE:       ${mae_type:.2f}")

# Sample predictions
print("\n" + "-" * 80)
print("Sample Predictions:")
print(f"{'City':<15} {'ZIP':<8} {'Type':<12} {'Actual':<10} {'Predicted':<10} {'Error':<10}")
print("-" * 80)

test_df['predicted_rent'] = y_pred
test_df['error'] = y_pred - y_true
test_df['abs_error'] = np.abs(test_df['error'])

for _, row in test_df.nsmallest(10, 'abs_error').iterrows():
    print(f"{row['city']:<15} {row['geoid']:<8} {row['exclusion_type']:<12} "
          f"${row[target_col]:<9.0f} ${row['predicted_rent']:<9.0f} ${row['error']:<9.0f}")

print("\n" + "=" * 80)
print("INTERPRETATION:")
print("=" * 80)

if r2 > 0.70:
    print("✅ Model predicts excluded ZIPs well (R² > 0.70)")
    print("   → Consider including them back in training data")
    print("   → They may not be as anomalous as initially thought")
elif r2 > 0.50:
    print("⚠️  Model has moderate predictive power (R² 0.50-0.70)")
    print("   → Some excluded ZIPs follow normal patterns")
    print("   → Review individual cases for inclusion")
else:
    print("❌ Model struggles with excluded ZIPs (R² < 0.50)")
    print("   → Correct decision to exclude them")
    print("   → They are true outliers with unique characteristics")

print("\n" + "=" * 80)
