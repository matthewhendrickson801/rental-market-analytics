"""
Hyperparameter Tuning for XGBoost
Uses GridSearchCV to find optimal parameters
"""

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import time

print("=" * 80)
print("XGBOOST HYPERPARAMETER TUNING")
print("=" * 80)

# Load prepared data
print("\n📂 Loading prepared data...")
train_data = pd.read_csv('results/prepared_data/train_data.csv')
val_data = pd.read_csv('results/prepared_data/val_data.csv')

X_train = train_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_train = train_data['rent']
weights_train = train_data['sample_weight']

X_val = val_data.drop(['rent', 'sample_weight', 'city', 'geoid'], axis=1)
y_val = val_data['rent']

print(f"✅ Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
print(f"✅ Validation set: {X_val.shape[0]} samples")

# Define parameter grid
param_grid = {
    'n_estimators': [300, 500],
    'max_depth': [4, 5, 6],
    'learning_rate': [0.03, 0.05, 0.1],
    'subsample': [0.7, 0.8],
    'colsample_bytree': [0.7, 0.8],
    'min_child_weight': [3, 5],
    'gamma': [0.1, 0.2]
}

print(f"\n🔍 Parameter grid:")
for param, values in param_grid.items():
    print(f"   {param}: {values}")

total_combinations = np.prod([len(v) for v in param_grid.values()])
print(f"\n⏱️  Total combinations to test: {total_combinations}")
print(f"   Estimated time: {total_combinations * 2 / 60:.1f} minutes")

# Create base model
base_model = XGBRegressor(
    random_state=42,
    n_jobs=-1,
    reg_alpha=0.1,
    reg_lambda=1.0
)

# Grid search with 3-fold CV
print("\n🚀 Starting grid search...")
start_time = time.time()

grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    cv=3,
    scoring='r2',
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train, sample_weight=weights_train)

elapsed_time = time.time() - start_time
print(f"\n✅ Grid search completed in {elapsed_time/60:.1f} minutes")

# Best parameters
print("\n" + "=" * 80)
print("BEST PARAMETERS")
print("=" * 80)
for param, value in grid_search.best_params_.items():
    print(f"   {param}: {value}")

# Evaluate best model
best_model = grid_search.best_estimator_

y_train_pred = best_model.predict(X_train)
y_val_pred = best_model.predict(X_val)

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
train_r2 = r2_score(y_train, y_train_pred)
val_r2 = r2_score(y_val, y_val_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
val_mae = mean_absolute_error(y_val, y_val_pred)

print("\n" + "=" * 80)
print("BEST MODEL PERFORMANCE")
print("=" * 80)
print(f"\n📊 Training:")
print(f"   RMSE: ${train_rmse:,.2f}")
print(f"   R²: {train_r2:.4f}")
print(f"   MAE: ${train_mae:,.2f}")

print(f"\n📊 Validation:")
print(f"   RMSE: ${val_rmse:,.2f}")
print(f"   R²: {val_r2:.4f}")
print(f"   MAE: ${val_mae:,.2f}")

# Compare to default model
print("\n" + "=" * 80)
print("COMPARISON TO DEFAULT MODEL")
print("=" * 80)
print(f"Default R²: 0.733")
print(f"Tuned R²: {val_r2:.4f}")
print(f"Improvement: {(val_r2 - 0.733):.4f} ({(val_r2 - 0.733)/0.733*100:.1f}%)")

# Save best model
import pickle
with open('models/regression/xgboost_tuned.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print(f"\n💾 Best model saved: models/regression/xgboost_tuned.pkl")

# Save results
results_df = pd.DataFrame({
    'Parameter': list(grid_search.best_params_.keys()),
    'Value': list(grid_search.best_params_.values())
})
results_df.to_csv('results/metrics/xgboost_best_params.csv', index=False)
print(f"💾 Best parameters saved: results/metrics/xgboost_best_params.csv")
