"""
Train Hybrid Model (Option C from MODEL_COMPARISON.md)

Approach:
- Predict absolute rent (like Original Model)
- Remove regional features (like City-Normalized Model)
- Goal: R² around 0.80-0.85 with meaningful residuals
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("TRAINING HYBRID MODEL")
print("=" * 80)

# ============================================================================
# STEP 1: Load clean dataset
# ============================================================================
print("\n[1/6] Loading clean dataset...")
df = pd.read_csv('d4_modeling/data/master_dataset_with_housing_mix.csv')
print(f"   Loaded: {len(df)} ZIPs")

# ============================================================================
# STEP 2: Define features (NO REGIONAL SHORTCUTS)
# ============================================================================
print("\n[2/6] Selecting features...")

# Target variable
target = 'Median Home Rent (2020-2024)'

# Features to EXCLUDE (regional shortcuts and non-predictive)
exclude_features = [
    # Target
    target,
    
    # ID columns
    'geoid', 'feature id', 'feature label', 'shid',
    
    # Regional shortcuts (THE KEY CHANGE)
    'city', 'data_source', 'rent_imputed',
    
    # Keep these NEW geographic features (not shortcuts, real patterns)
    # 'is_coastal', 'beach_proximity', 'is_urban', 'is_suburban', 'is_rural'
    
    # But exclude the categorical version and tech hub
    'urban_rural', 'population', 'tech_hub_score',
    
    # Any region/city-based features
    'region_HighCost', 'region_Midwest', 'region_South',
    'City_Boom_Score', 'Boom_Category',
    
    # Derived features that might contain city info
    'Transit_Accessibility_Index', 'Transit_Accessibility_Index_Std',
    'Walkability_Premium_Index', 'Walkability_Premium_Index_Std',
    
    # Redundant with rent
    'Expected_Rent_From_Income',
    'Income_Rent_Mismatch_Ratio', 'Income_Rent_Mismatch_Ratio_Std',
    'Comprehensive_Mismatch_Score',
    'Basic_Rent_Waste', 'Rent_Per_Commute_Minute',
    'Commute_Rent_Mismatch', 'Comprehensive_Rent_Waste_Score',
    'Total_Monthly_Location_Cost', 'Time_Value_Rent_Waste',
    'income_rent_gap',  # Too directly related to rent (income/rent)
]

# Get all columns
all_cols = df.columns.tolist()

# Features to INCLUDE
feature_cols = [col for col in all_cols if col not in exclude_features]

print(f"   Total columns: {len(all_cols)}")
print(f"   Excluded: {len(exclude_features)}")
print(f"   Features for model: {len(feature_cols)}")

print(f"\n   Feature categories:")
print(f"      Housing age: {len([c for c in feature_cols if 'Housing Built' in c])}")
print(f"      Education: {len([c for c in feature_cols if 'education_' in c])}")
print(f"      Income: {len([c for c in feature_cols if 'Income' in c or 'income' in c])}")
print(f"      Jobs: {len([c for c in feature_cols if 'jobs' in c.lower()])}")
print(f"      Commute: {len([c for c in feature_cols if 'Commute' in c])}")
print(f"      Vacancy: {len([c for c in feature_cols if 'Vacancy' in c])}")

# ============================================================================
# STEP 3: Prepare data
# ============================================================================
print("\n[3/6] Preparing data...")

# Remove rows with missing target
df_clean = df[df[target].notna()].copy()
print(f"   After removing missing target: {len(df_clean)} ZIPs")

# Prepare X and y
X = df_clean[feature_cols].copy()
y = df_clean[target].copy()

# Replace inf values with NaN (XGBoost can handle NaN but not inf)
X = X.replace([np.inf, -np.inf], np.nan)

print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")

# Check missing values in features
missing_counts = X.isnull().sum()
missing_features = missing_counts[missing_counts > 0]
if len(missing_features) > 0:
    print(f"\n   Features with missing values:")
    for feat, count in missing_features.items():
        pct = (count / len(X)) * 100
        print(f"      {feat}: {count} ({pct:.1f}%)")
    print(f"   XGBoost will handle missing values internally")

# ============================================================================
# STEP 4: Train/test split (stratified by city)
# ============================================================================
print("\n[4/6] Creating train/test split...")

# Stratified split by city to ensure all cities represented
city_col = df_clean['city']

X_train, X_test, y_train, y_test, city_train, city_test = train_test_split(
    X, y, city_col,
    test_size=0.2,
    random_state=42,
    stratify=city_col
)

print(f"   Train set: {len(X_train)} ZIPs")
print(f"   Test set: {len(X_test)} ZIPs")

# Show city distribution
print(f"\n   Train cities:")
train_city_counts = city_train.value_counts().sort_index()
for city, count in train_city_counts.items():
    print(f"      {city}: {count}")

print(f"\n   Test cities:")
test_city_counts = city_test.value_counts().sort_index()
for city, count in test_city_counts.items():
    print(f"      {city}: {count}")

# ============================================================================
# STEP 5: Train XGBoost model
# ============================================================================
print("\n[5/6] Training XGBoost model...")

# XGBoost parameters (with stronger regularization to prevent overfitting)
params = {
    'objective': 'reg:squarederror',
    'max_depth': 4,  # Reduced from 6
    'learning_rate': 0.05,  # Reduced from 0.1
    'n_estimators': 300,  # Increased from 200
    'subsample': 0.7,  # Reduced from 0.8
    'colsample_bytree': 0.7,  # Reduced from 0.8
    'min_child_weight': 3,  # Added regularization
    'gamma': 0.1,  # Added regularization
    'reg_alpha': 0.1,  # L1 regularization
    'reg_lambda': 1.0,  # L2 regularization
    'random_state': 42,
    'tree_method': 'hist',
    'enable_categorical': False
}

model = xgb.XGBRegressor(**params)
model.fit(X_train, y_train, verbose=False)

print(f"   Model trained with {len(feature_cols)} features")

# ============================================================================
# STEP 6: Evaluate model
# ============================================================================
print("\n[6/6] Evaluating model...")

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Metrics
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

print(f"\n   TRAIN METRICS:")
print(f"      R²: {train_r2:.4f}")
print(f"      RMSE: ${train_rmse:.2f}")
print(f"      MAE: ${train_mae:.2f}")

print(f"\n   TEST METRICS:")
print(f"      R²: {test_r2:.4f}")
print(f"      RMSE: ${test_rmse:.2f}")
print(f"      MAE: ${test_mae:.2f}")

# Calculate residuals
train_residuals = y_train - y_train_pred
test_residuals = y_test - y_test_pred

print(f"\n   RESIDUALS (Test Set):")
print(f"      Mean: ${test_residuals.mean():.2f}")
print(f"      Std: ${test_residuals.std():.2f}")
print(f"      Min: ${test_residuals.min():.2f}")
print(f"      Max: ${test_residuals.max():.2f}")

# ============================================================================
# Save model and results
# ============================================================================
print("\n" + "=" * 80)
print("SAVING MODEL AND RESULTS")
print("=" * 80)

# Save model
model_path = 'd4_modeling/models/regression/xgboost_hybrid.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"\n✅ Model saved: {model_path}")

# Save feature list
features_path = 'd4_modeling/models/regression/hybrid_features.txt'
with open(features_path, 'w') as f:
    for feat in feature_cols:
        f.write(f"{feat}\n")
print(f"✅ Features saved: {features_path}")

# Save predictions for analysis
results_df = pd.DataFrame({
    'geoid': df_clean.loc[X_test.index, 'geoid'],
    'city': city_test,
    'actual_rent': y_test,
    'predicted_rent': y_test_pred,
    'residual': test_residuals,
    'abs_residual': np.abs(test_residuals),
    'pct_error': (test_residuals / y_test * 100)
})

results_path = 'd4_modeling/results/hybrid_model_predictions.csv'
results_df.to_csv(results_path, index=False)
print(f"✅ Predictions saved: {results_path}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

importance_path = 'd4_modeling/results/hybrid_feature_importance.csv'
feature_importance.to_csv(importance_path, index=False)
print(f"✅ Feature importance saved: {importance_path}")

print(f"\n   Top 10 Most Important Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"      {row['feature']}: {row['importance']:.4f}")

# ============================================================================
# Create visualizations
# ============================================================================
print("\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

# 1. Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Rent ($)')
plt.ylabel('Predicted Rent ($)')
plt.title(f'Hybrid Model: Actual vs Predicted Rent\nTest R² = {test_r2:.4f}')
plt.tight_layout()
plt.savefig('d4_modeling/results/hybrid_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: hybrid_actual_vs_predicted.png")

# 2. Residuals distribution
plt.figure(figsize=(10, 6))
plt.hist(test_residuals, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(x=0, color='r', linestyle='--', linewidth=2)
plt.xlabel('Residual ($)')
plt.ylabel('Frequency')
plt.title(f'Hybrid Model: Residuals Distribution\nMean = ${test_residuals.mean():.2f}, Std = ${test_residuals.std():.2f}')
plt.tight_layout()
plt.savefig('d4_modeling/results/hybrid_residuals_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: hybrid_residuals_distribution.png")

# 3. Feature importance
plt.figure(figsize=(10, 8))
top_features = feature_importance.head(15)
plt.barh(range(len(top_features)), top_features['importance'])
plt.yticks(range(len(top_features)), top_features['feature'])
plt.xlabel('Importance')
plt.title('Hybrid Model: Top 15 Feature Importance')
plt.tight_layout()
plt.savefig('d4_modeling/results/hybrid_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: hybrid_feature_importance.png")

print("\n" + "=" * 80)
print("HYBRID MODEL TRAINING COMPLETE")
print("=" * 80)
print(f"\n🎯 Test R²: {test_r2:.4f}")
print(f"📊 Test RMSE: ${test_rmse:.2f}")
print(f"📈 Test MAE: ${test_mae:.2f}")
print("\n✅ Model ready for StateofJax analysis!")
print("=" * 80)
