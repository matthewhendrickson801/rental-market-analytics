"""
Compare different train/val/test split strategies
Goal: Find optimal split that balances training data vs. validation accuracy
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'

print("=" * 80)
print("COMPARING TRAIN/VAL/TEST SPLIT STRATEGIES")
print("=" * 80)

# Load cleaned dataset
df = pd.read_csv(DATA_DIR / 'master_dataset_cleaned.csv')
print(f"\nTotal dataset: {df.shape[0]} ZIPs, {df.shape[1]} columns")

# Prepare features (same as before)
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

# Model hyperparameters (consistent across all splits)
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

# Define split strategies
split_strategies = [
    {'name': 'Current (65/15/20)', 'train': 0.65, 'val': 0.15, 'test': 0.20},
    {'name': '70/15/15', 'train': 0.70, 'val': 0.15, 'test': 0.15},
    {'name': '70/10/20', 'train': 0.70, 'val': 0.10, 'test': 0.20},
    {'name': '80/10/10', 'train': 0.80, 'val': 0.10, 'test': 0.10},
    {'name': '80/15/5', 'train': 0.80, 'val': 0.15, 'test': 0.05},
]

results = []

for strategy in split_strategies:
    print(f"\n{'=' * 80}")
    print(f"STRATEGY: {strategy['name']}")
    print(f"{'=' * 80}")
    
    # Calculate split sizes
    test_size = strategy['test']
    val_size = strategy['val'] / (1 - test_size)  # Val as fraction of remaining after test
    
    # Split
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=df['city']
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=42, 
        stratify=df.loc[X_temp.index, 'city']
    )
    
    print(f"\nSplit sizes:")
    print(f"  Train: {len(X_train):4d} ({len(X_train)/len(X)*100:5.1f}%)")
    print(f"  Val:   {len(X_val):4d} ({len(X_val)/len(X)*100:5.1f}%)")
    print(f"  Test:  {len(X_test):4d} ({len(X_test)/len(X)*100:5.1f}%)")
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Train
    model = xgb.XGBRegressor(**params)
    model.fit(X_train_scaled, y_train, verbose=False)
    
    # Predict
    y_train_pred = model.predict(X_train_scaled)
    y_val_pred = model.predict(X_val_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Evaluate
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    
    val_r2 = r2_score(y_val, y_val_pred)
    val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
    
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    train_val_gap = train_r2 - val_r2
    val_test_gap = abs(val_r2 - test_r2)
    
    print(f"\nPerformance:")
    print(f"  Train R²:       {train_r2:.4f}  (RMSE: ${train_rmse:.2f})")
    print(f"  Val R²:         {val_r2:.4f}  (RMSE: ${val_rmse:.2f})")
    print(f"  Test R²:        {test_r2:.4f}  (RMSE: ${test_rmse:.2f})")
    print(f"\nOverfitting:")
    print(f"  Train-Val gap:  {train_val_gap:.4f}")
    print(f"  Val-Test gap:   {val_test_gap:.4f}")
    
    if train_val_gap < 0.05:
        overfit_status = "✅ Minimal"
    elif train_val_gap < 0.10:
        overfit_status = "⚠️  Moderate"
    else:
        overfit_status = "❌ High"
    
    print(f"  Status:         {overfit_status}")
    
    # Store results
    results.append({
        'strategy': strategy['name'],
        'train_size': len(X_train),
        'val_size': len(X_val),
        'test_size': len(X_test),
        'train_r2': train_r2,
        'val_r2': val_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'val_rmse': val_rmse,
        'test_rmse': test_rmse,
        'train_val_gap': train_val_gap,
        'val_test_gap': val_test_gap,
        'overfit_status': overfit_status
    })

# Summary comparison
print(f"\n{'=' * 80}")
print("SUMMARY COMPARISON")
print(f"{'=' * 80}")

results_df = pd.DataFrame(results)

print(f"\n{'Strategy':<20} {'Train':<7} {'Val':<7} {'Test':<7} {'Val R²':<8} {'Test R²':<8} {'Gap':<7} {'Status'}")
print("-" * 80)

for _, row in results_df.iterrows():
    print(f"{row['strategy']:<20} "
          f"{row['train_size']:<7} "
          f"{row['val_size']:<7} "
          f"{row['test_size']:<7} "
          f"{row['val_r2']:<8.4f} "
          f"{row['test_r2']:<8.4f} "
          f"{row['train_val_gap']:<7.4f} "
          f"{row['overfit_status']}")

# Recommendation
print(f"\n{'=' * 80}")
print("RECOMMENDATION")
print(f"{'=' * 80}")

# Find best by validation R²
best_val = results_df.loc[results_df['val_r2'].idxmax()]
print(f"\nHighest Validation R²: {best_val['strategy']}")
print(f"  Val R²: {best_val['val_r2']:.4f}")
print(f"  Test R²: {best_val['test_r2']:.4f}")

# Find best by consistency (lowest val-test gap)
best_consistent = results_df.loc[results_df['val_test_gap'].idxmin()]
print(f"\nMost Consistent (Val-Test): {best_consistent['strategy']}")
print(f"  Val R²: {best_consistent['val_r2']:.4f}")
print(f"  Test R²: {best_consistent['test_r2']:.4f}")
print(f"  Gap: {best_consistent['val_test_gap']:.4f}")

# Find best by least overfitting
best_overfit = results_df.loc[results_df['train_val_gap'].idxmin()]
print(f"\nLeast Overfitting (Train-Val): {best_overfit['strategy']}")
print(f"  Train R²: {best_overfit['train_r2']:.4f}")
print(f"  Val R²: {best_overfit['val_r2']:.4f}")
print(f"  Gap: {best_overfit['train_val_gap']:.4f}")

print(f"\n{'=' * 80}")
print("ANALYSIS COMPLETE")
print(f"{'=' * 80}")
