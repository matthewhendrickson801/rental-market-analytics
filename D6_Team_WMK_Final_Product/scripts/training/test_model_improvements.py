"""
Test Quick Model Improvements
Try different approaches to boost R² without adding features
"""

import pandas as pd
import numpy as np
import pickle
import joblib
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

print("=" * 80)
print("TESTING MODEL IMPROVEMENTS")
print("=" * 80)

# Load prepared data
train_df = pd.read_csv('results/prepared_data/train_data.csv')
val_df = pd.read_csv('results/prepared_data/val_data.csv')

# Separate features and target
feature_cols = [col for col in train_df.columns if col not in ['rent', 'city', 'geoid', 'sample_weight']]
X_train = train_df[feature_cols]
y_train = train_df['rent']
weights_train = train_df['sample_weight']

X_val = val_df[feature_cols]
y_val = val_df['rent']

print(f"\n📊 Dataset: {len(X_train)} training, {len(X_val)} validation")
print(f"   Features: {len(feature_cols)}")

# Current baseline
print("\n" + "=" * 80)
print("BASELINE: Current XGBoost")
print("=" * 80)

with open('models/regression/xgboost.pkl', 'rb') as f:
    baseline_model = pickle.load(f)

val_pred = baseline_model.predict(X_val)
baseline_r2 = r2_score(y_val, val_pred)
baseline_rmse = np.sqrt(mean_squared_error(y_val, val_pred))

print(f"Validation R²: {baseline_r2:.4f}")
print(f"Validation RMSE: ${baseline_rmse:.2f}")

# Test 1: More trees
print("\n" + "=" * 80)
print("TEST 1: Increase n_estimators (200 → 500)")
print("=" * 80)

model1 = XGBRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    random_state=42,
    n_jobs=-1
)
model1.fit(X_train, y_train, sample_weight=weights_train)
val_pred1 = model1.predict(X_val)
r2_1 = r2_score(y_val, val_pred1)
rmse_1 = np.sqrt(mean_squared_error(y_val, val_pred1))

print(f"Validation R²: {r2_1:.4f} (Δ {r2_1 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_1:.2f}")

# Test 2: Lower learning rate, more trees
print("\n" + "=" * 80)
print("TEST 2: Lower learning rate (0.05 → 0.03) + more trees (500)")
print("=" * 80)

model2 = XGBRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.03,
    random_state=42,
    n_jobs=-1
)
model2.fit(X_train, y_train, sample_weight=weights_train)
val_pred2 = model2.predict(X_val)
r2_2 = r2_score(y_val, val_pred2)
rmse_2 = np.sqrt(mean_squared_error(y_val, val_pred2))

print(f"Validation R²: {r2_2:.4f} (Δ {r2_2 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_2:.2f}")

# Test 3: Deeper trees
print("\n" + "=" * 80)
print("TEST 3: Deeper trees (max_depth 5 → 7)")
print("=" * 80)

model3 = XGBRegressor(
    n_estimators=300,
    max_depth=7,
    learning_rate=0.05,
    random_state=42,
    n_jobs=-1
)
model3.fit(X_train, y_train, sample_weight=weights_train)
val_pred3 = model3.predict(X_val)
r2_3 = r2_score(y_val, val_pred3)
rmse_3 = np.sqrt(mean_squared_error(y_val, val_pred3))

print(f"Validation R²: {r2_3:.4f} (Δ {r2_3 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_3:.2f}")

# Test 4: Ensemble (average XGBoost + Random Forest)
print("\n" + "=" * 80)
print("TEST 4: Ensemble (XGBoost + Random Forest average)")
print("=" * 80)

with open('models/regression/random_forest.pkl', 'rb') as f:
    rf_model = pickle.load(f)

rf_pred = rf_model.predict(X_val)
xgb_pred = baseline_model.predict(X_val)
ensemble_pred = (rf_pred + xgb_pred) / 2

r2_4 = r2_score(y_val, ensemble_pred)
rmse_4 = np.sqrt(mean_squared_error(y_val, ensemble_pred))

print(f"Validation R²: {r2_4:.4f} (Δ {r2_4 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_4:.2f}")

# Test 5: Weighted ensemble (70% XGBoost, 30% Random Forest)
print("\n" + "=" * 80)
print("TEST 5: Weighted Ensemble (70% XGBoost + 30% Random Forest)")
print("=" * 80)

ensemble_pred5 = (0.7 * xgb_pred) + (0.3 * rf_pred)
r2_5 = r2_score(y_val, ensemble_pred5)
rmse_5 = np.sqrt(mean_squared_error(y_val, ensemble_pred5))

print(f"Validation R²: {r2_5:.4f} (Δ {r2_5 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_5:.2f}")

# Test 6: Gradient Boosting (sklearn)
print("\n" + "=" * 80)
print("TEST 6: Sklearn GradientBoostingRegressor")
print("=" * 80)

model6 = GradientBoostingRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    random_state=42
)
model6.fit(X_train, y_train, sample_weight=weights_train)
val_pred6 = model6.predict(X_val)
r2_6 = r2_score(y_val, val_pred6)
rmse_6 = np.sqrt(mean_squared_error(y_val, val_pred6))

print(f"Validation R²: {r2_6:.4f} (Δ {r2_6 - baseline_r2:+.4f})")
print(f"Validation RMSE: ${rmse_6:.2f}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

results = [
    ("Baseline (current)", baseline_r2, baseline_rmse),
    ("More trees (500)", r2_1, rmse_1),
    ("Lower LR + 500 trees", r2_2, rmse_2),
    ("Deeper trees (depth=7)", r2_3, rmse_3),
    ("Ensemble 50/50", r2_4, rmse_4),
    ("Ensemble 70/30", r2_5, rmse_5),
    ("Sklearn GradientBoost", r2_6, rmse_6)
]

results_df = pd.DataFrame(results, columns=['Model', 'R²', 'RMSE'])
results_df = results_df.sort_values('R²', ascending=False)

print("\n📊 Results (sorted by R²):")
print(results_df.to_string(index=False))

best = results_df.iloc[0]
print(f"\n🏆 Best approach: {best['Model']}")
print(f"   R²: {best['R²']:.4f}")
print(f"   RMSE: ${best['RMSE']:.2f}")
print(f"   Improvement: {(best['R²'] - baseline_r2):.4f} ({(best['R²'] - baseline_r2)/baseline_r2*100:+.1f}%)")

if best['R²'] - baseline_r2 < 0.01:
    print("\n💡 Recommendation: Current model is already optimal")
    print("   Improvements <1% are not worth the complexity")
    print("   Move forward with R²=0.757 model")
else:
    print("\n💡 Recommendation: Use best approach above")
