"""
Train Advanced Models (Tier 3 & 4): Random Forest and XGBoost
Captures non-linear relationships and interactions between features
"""

import pandas as pd
import numpy as np
import pickle
import time
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("TIER 3 & 4: ADVANCED MODELS - RANDOM FOREST & XGBOOST")
print("=" * 80)

# Load prepared data
print("\n📂 Loading prepared data...")
train_data = pd.read_csv('results/prepared_data/train_data.csv')
val_data = pd.read_csv('results/prepared_data/val_data.csv')
test_data = pd.read_csv('results/prepared_data/test_data.csv')

# Separate features and target
# Drop target, sample_weight, and metadata columns (city, geoid)
X_train = train_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_train = train_data['rent']
weights_train = train_data['sample_weight']

X_val = val_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_val = val_data['rent']

X_test = test_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_test = test_data['rent']

print(f"✅ Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
print(f"✅ Validation set: {X_val.shape[0]} samples")
print(f"✅ Test set: {X_test.shape[0]} samples")

# ============================================================================
# TIER 3: RANDOM FOREST REGRESSOR
# ============================================================================
print("\n" + "=" * 80)
print("TIER 3: RANDOM FOREST REGRESSOR")
print("=" * 80)
print("🌲 Captures non-linear relationships and feature interactions")
print("🌲 Robust to outliers and multicollinearity")
print("🌲 Provides feature importance rankings")

# Train Random Forest
print("\n🔧 Training Random Forest...")
start_time = time.time()

rf_model = RandomForestRegressor(
    n_estimators=200,           # More trees for stability
    max_depth=15,               # Prevent overfitting
    min_samples_split=10,       # Require minimum samples to split
    min_samples_leaf=5,         # Require minimum samples in leaf
    max_features='sqrt',        # Use sqrt(n_features) per split
    random_state=42,
    n_jobs=-1                   # Use all CPU cores
)

rf_model.fit(X_train, y_train, sample_weight=weights_train)
training_time = time.time() - start_time

print(f"✅ Training completed in {training_time:.2f} seconds")

# Predictions
y_train_pred_rf = rf_model.predict(X_train)
y_val_pred_rf = rf_model.predict(X_val)

# Metrics
train_rmse_rf = np.sqrt(mean_squared_error(y_train, y_train_pred_rf))
val_rmse_rf = np.sqrt(mean_squared_error(y_val, y_val_pred_rf))
train_r2_rf = r2_score(y_train, y_train_pred_rf)
val_r2_rf = r2_score(y_val, y_val_pred_rf)
train_mae_rf = mean_absolute_error(y_train, y_train_pred_rf)
val_mae_rf = mean_absolute_error(y_val, y_val_pred_rf)

print("\n📊 Random Forest Performance:")
print(f"   Training RMSE: ${train_rmse_rf:,.2f}")
print(f"   Validation RMSE: ${val_rmse_rf:,.2f}")
print(f"   Training R²: {train_r2_rf:.4f}")
print(f"   Validation R²: {val_r2_rf:.4f}")
print(f"   Training MAE: ${train_mae_rf:,.2f}")
print(f"   Validation MAE: ${val_mae_rf:,.2f}")

# Save model
with open('models/regression/random_forest.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("\n💾 Model saved: models/regression/random_forest.pkl")

# ============================================================================
# TIER 4: XGBOOST REGRESSOR
# ============================================================================
print("\n" + "=" * 80)
print("TIER 4: XGBOOST REGRESSOR")
print("=" * 80)
print("🚀 State-of-the-art gradient boosting")
print("🚀 Handles complex patterns and interactions")
print("🚀 Optimized for accuracy")

# Train XGBoost
print("\n🔧 Training XGBoost...")
start_time = time.time()

xgb_model = XGBRegressor(
    n_estimators=200,           # Number of boosting rounds
    max_depth=5,                # Reduced from 6 to prevent overfitting
    learning_rate=0.05,         # Reduced from 0.1 for smoother learning
    subsample=0.7,              # Reduced from 0.8 for more regularization
    colsample_bytree=0.7,       # Reduced from 0.8 for more regularization
    min_child_weight=5,         # Increased from 3 to prevent overfitting
    gamma=0.2,                  # Increased from 0.1 for more regularization
    reg_alpha=0.5,              # Increased L1 regularization
    reg_lambda=2.0,             # Increased L2 regularization
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(X_train, y_train, sample_weight=weights_train)
training_time_xgb = time.time() - start_time

print(f"✅ Training completed in {training_time_xgb:.2f} seconds")

# Predictions
y_train_pred_xgb = xgb_model.predict(X_train)
y_val_pred_xgb = xgb_model.predict(X_val)

# Metrics
train_rmse_xgb = np.sqrt(mean_squared_error(y_train, y_train_pred_xgb))
val_rmse_xgb = np.sqrt(mean_squared_error(y_val, y_val_pred_xgb))
train_r2_xgb = r2_score(y_train, y_train_pred_xgb)
val_r2_xgb = r2_score(y_val, y_val_pred_xgb)
train_mae_xgb = mean_absolute_error(y_train, y_train_pred_xgb)
val_mae_xgb = mean_absolute_error(y_val, y_val_pred_xgb)

print("\n📊 XGBoost Performance:")
print(f"   Training RMSE: ${train_rmse_xgb:,.2f}")
print(f"   Validation RMSE: ${val_rmse_xgb:,.2f}")
print(f"   Training R²: {train_r2_xgb:.4f}")
print(f"   Validation R²: {val_r2_xgb:.4f}")
print(f"   Training MAE: ${train_mae_xgb:,.2f}")
print(f"   Validation MAE: ${val_mae_xgb:,.2f}")

# Save model
with open('models/regression/xgboost.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)
print("\n💾 Model saved: models/regression/xgboost.pkl")

# ============================================================================
# MODEL COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("MODEL COMPARISON: ALL 4 TIERS")
print("=" * 80)

# Load baseline results
baseline_results = pd.read_csv('results/metrics/baseline_models_comparison.csv')

# Create comparison dataframe
comparison = pd.DataFrame({
    'Model': ['Linear Regression', 'Ridge Regression', 'Random Forest', 'XGBoost'],
    'Train_RMSE': [
        baseline_results.loc[0, 'Train_RMSE'],
        baseline_results.loc[1, 'Train_RMSE'],
        train_rmse_rf,
        train_rmse_xgb
    ],
    'Val_RMSE': [
        baseline_results.loc[0, 'Val_RMSE'],
        baseline_results.loc[1, 'Val_RMSE'],
        val_rmse_rf,
        val_rmse_xgb
    ],
    'Train_R2': [
        baseline_results.loc[0, 'Train_R2'],
        baseline_results.loc[1, 'Train_R2'],
        train_r2_rf,
        train_r2_xgb
    ],
    'Val_R2': [
        baseline_results.loc[0, 'Val_R2'],
        baseline_results.loc[1, 'Val_R2'],
        val_r2_rf,
        val_r2_xgb
    ],
    'Train_MAE': [
        baseline_results.loc[0, 'Train_MAE'],
        baseline_results.loc[1, 'Train_MAE'],
        train_mae_rf,
        train_mae_xgb
    ],
    'Val_MAE': [
        baseline_results.loc[0, 'Val_MAE'],
        baseline_results.loc[1, 'Val_MAE'],
        val_mae_rf,
        val_mae_xgb
    ],
    'Training_Time': [
        baseline_results.loc[0, 'Training_Time'],
        baseline_results.loc[1, 'Training_Time'],
        training_time,
        training_time_xgb
    ]
})

# Save comparison
comparison.to_csv('results/metrics/all_models_comparison.csv', index=False)
print("\n💾 Comparison saved: results/metrics/all_models_comparison.csv")

# Display comparison
print("\n📊 VALIDATION SET PERFORMANCE:")
print(comparison[['Model', 'Val_RMSE', 'Val_R2', 'Val_MAE']].to_string(index=False))

# Calculate improvements
best_baseline_rmse = comparison.loc[1, 'Val_RMSE']  # Ridge
rf_improvement = ((best_baseline_rmse - val_rmse_rf) / best_baseline_rmse) * 100
xgb_improvement = ((best_baseline_rmse - val_rmse_xgb) / best_baseline_rmse) * 100

print(f"\n🎯 IMPROVEMENTS OVER RIDGE REGRESSION:")
print(f"   Random Forest: {rf_improvement:.1f}% reduction in RMSE")
print(f"   XGBoost: {xgb_improvement:.1f}% reduction in RMSE")

# ============================================================================
# FEATURE IMPORTANCE ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)

# Random Forest Feature Importance
rf_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n🌲 TOP 10 FEATURES (Random Forest):")
for i, row in rf_importance.head(10).iterrows():
    print(f"   {row['Feature']}: {row['Importance']:.4f}")

# XGBoost Feature Importance
xgb_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': xgb_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n🚀 TOP 10 FEATURES (XGBoost):")
for i, row in xgb_importance.head(10).iterrows():
    print(f"   {row['Feature']}: {row['Importance']:.4f}")

# Save feature importance
rf_importance.to_csv('results/metrics/random_forest_feature_importance.csv', index=False)
xgb_importance.to_csv('results/metrics/xgboost_feature_importance.csv', index=False)

print("\n" + "=" * 80)
print("✅ ADVANCED MODELS TRAINING COMPLETE!")
print("=" * 80)
print("\n📁 Files created:")
print("   - models/regression/random_forest.pkl")
print("   - models/regression/xgboost.pkl")
print("   - results/metrics/all_models_comparison.csv")
print("   - results/metrics/random_forest_feature_importance.csv")
print("   - results/metrics/xgboost_feature_importance.csv")
