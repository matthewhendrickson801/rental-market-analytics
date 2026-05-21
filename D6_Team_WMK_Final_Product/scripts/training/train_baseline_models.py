"""
Baseline Regression Models Training
Tier 1: Linear Regression
Tier 2: Ridge Regression

These establish baseline performance before moving to complex models
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.impute import SimpleImputer
import joblib
import os
import time

def load_prepared_data():
    """Load the prepared train/val/test data"""
    print("="*80)
    print("LOADING PREPARED DATA")
    print("="*80)
    
    train_df = pd.read_csv('results/prepared_data/train_data.csv')
    val_df = pd.read_csv('results/prepared_data/val_data.csv')
    test_df = pd.read_csv('results/prepared_data/test_data.csv')
    
    # Separate features, target, metadata, and weights
    meta_cols = ['rent', 'city', 'geoid', 'sample_weight']
    
    X_train = train_df.drop(columns=meta_cols)
    y_train = train_df['rent']
    weights_train = train_df['sample_weight']
    
    X_val = val_df.drop(columns=meta_cols)
    y_val = val_df['rent']
    weights_val = val_df['sample_weight']
    
    X_test = test_df.drop(columns=meta_cols)
    y_test = test_df['rent']
    weights_test = test_df['sample_weight']
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Check for missing values
    missing_train = X_train.isnull().sum().sum()
    if missing_train > 0:
        print(f"\n⚠️  {missing_train} missing values detected in training data")
        print("Missing values by feature:")
        print(X_train.isnull().sum()[X_train.isnull().sum() > 0])
    
    return X_train, X_val, X_test, y_train, y_val, y_test, weights_train, weights_val, weights_test

def handle_missing_values(X_train, X_val, X_test):
    """
    Handle missing values using median imputation
    Fit imputer on training data only to prevent data leakage
    """
    print("\n" + "="*80)
    print("HANDLING MISSING VALUES")
    print("="*80)
    
    # Check which columns have missing values
    missing_cols = X_train.columns[X_train.isnull().any()].tolist()
    
    if len(missing_cols) == 0:
        print("✓ No missing values to handle")
        return X_train, X_val, X_test, None
    
    print(f"Columns with missing values: {len(missing_cols)}")
    for col in missing_cols:
        missing_count = X_train[col].isnull().sum()
        print(f"  {col}: {missing_count} missing ({missing_count/len(X_train)*100:.1f}%)")
    
    # Use median imputation (robust to outliers)
    imputer = SimpleImputer(strategy='median')
    
    # Fit on training data only
    X_train_imputed = pd.DataFrame(
        imputer.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    
    X_val_imputed = pd.DataFrame(
        imputer.transform(X_val),
        columns=X_val.columns,
        index=X_val.index
    )
    
    X_test_imputed = pd.DataFrame(
        imputer.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    
    print(f"\n✓ Missing values imputed using median strategy")
    print(f"✓ Imputer fitted on training data only")
    
    return X_train_imputed, X_val_imputed, X_test_imputed, imputer

def evaluate_model(model, X, y, weights, set_name=""):
    """
    Evaluate model performance
    
    Returns:
    --------
    metrics : dict
        Dictionary containing RMSE, R2, MAE
    """
    predictions = model.predict(X)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y, predictions, sample_weight=weights))
    r2 = r2_score(y, predictions, sample_weight=weights)
    mae = mean_absolute_error(y, predictions, sample_weight=weights)
    
    # Calculate residuals
    residuals = y - predictions
    
    metrics = {
        'rmse': rmse,
        'r2': r2,
        'mae': mae,
        'predictions': predictions,
        'residuals': residuals
    }
    
    if set_name:
        print(f"\n{set_name} Performance:")
        print(f"  RMSE: ${rmse:,.2f}")
        print(f"  R²:   {r2:.4f} ({r2*100:.2f}% variance explained)")
        print(f"  MAE:  ${mae:,.2f}")
    
    return metrics

def train_linear_regression(X_train, y_train, X_val, y_val, weights_train, weights_val):
    """
    Tier 1: Linear Regression (Baseline)
    
    Simplest model - assumes linear relationships
    Fast training, highly interpretable
    Expected to underperform due to non-linear patterns from D3 EDA
    """
    print("\n" + "="*80)
    print("TIER 1: LINEAR REGRESSION (BASELINE)")
    print("="*80)
    
    print("\nModel Characteristics:")
    print("  ✓ Simplest regression model")
    print("  ✓ Assumes linear relationships between features and target")
    print("  ✓ Highly interpretable (can see feature coefficients)")
    print("  ✓ Fast training and prediction")
    print("  ✗ Cannot capture non-linear patterns")
    print("  ✗ Sensitive to multicollinearity")
    
    # Train model
    print("\nTraining Linear Regression...")
    start_time = time.time()
    
    model = LinearRegression()
    model.fit(X_train, y_train, sample_weight=weights_train)
    
    training_time = time.time() - start_time
    print(f"✓ Training completed in {training_time:.2f} seconds")
    
    # Evaluate on training set
    train_metrics = evaluate_model(model, X_train, y_train, weights_train, "Training Set")
    
    # Evaluate on validation set
    val_metrics = evaluate_model(model, X_val, y_val, weights_val, "Validation Set")
    
    # Check for overfitting
    overfit_gap = train_metrics['rmse'] - val_metrics['rmse']
    print(f"\nOverfitting Check:")
    print(f"  Training RMSE:   ${train_metrics['rmse']:,.2f}")
    print(f"  Validation RMSE: ${val_metrics['rmse']:,.2f}")
    print(f"  Gap: ${abs(overfit_gap):,.2f}")
    
    if abs(overfit_gap) < 50:
        print(f"  ✓ Minimal overfitting (gap < $50)")
    elif abs(overfit_gap) < 100:
        print(f"  ⚠️  Moderate overfitting (gap < $100)")
    else:
        print(f"  ⚠️  Significant overfitting (gap > $100)")
    
    # Feature importance (top 10 coefficients by absolute value)
    print(f"\nTop 10 Most Important Features (by coefficient magnitude):")
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': model.coef_
    })
    feature_importance['abs_coef'] = abs(feature_importance['coefficient'])
    feature_importance = feature_importance.sort_values('abs_coef', ascending=False)
    
    for i, row in feature_importance.head(10).iterrows():
        direction = "↑" if row['coefficient'] > 0 else "↓"
        print(f"  {direction} {row['feature'][:50]:<50} | Coef: {row['coefficient']:>10.2f}")
    
    return model, train_metrics, val_metrics, training_time

def train_ridge_regression(X_train, y_train, X_val, y_val, weights_train, weights_val, alpha=1.0):
    """
    Tier 2: Ridge Regression (L2 Regularization)
    
    Adds penalty for large coefficients
    Handles multicollinearity better than Linear Regression
    Still interpretable, slightly more complex
    """
    print("\n" + "="*80)
    print("TIER 2: RIDGE REGRESSION (L2 REGULARIZATION)")
    print("="*80)
    
    print("\nModel Characteristics:")
    print("  ✓ Adds L2 regularization penalty")
    print("  ✓ Handles multicollinearity (correlated features)")
    print("  ✓ Prevents overfitting through coefficient shrinkage")
    print("  ✓ Still interpretable")
    print(f"  ✓ Alpha (regularization strength): {alpha}")
    print("  ✗ Still assumes linear relationships")
    
    # Train model
    print("\nTraining Ridge Regression...")
    start_time = time.time()
    
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train, sample_weight=weights_train)
    
    training_time = time.time() - start_time
    print(f"✓ Training completed in {training_time:.2f} seconds")
    
    # Evaluate on training set
    train_metrics = evaluate_model(model, X_train, y_train, weights_train, "Training Set")
    
    # Evaluate on validation set
    val_metrics = evaluate_model(model, X_val, y_val, weights_val, "Validation Set")
    
    # Check for overfitting
    overfit_gap = train_metrics['rmse'] - val_metrics['rmse']
    print(f"\nOverfitting Check:")
    print(f"  Training RMSE:   ${train_metrics['rmse']:,.2f}")
    print(f"  Validation RMSE: ${val_metrics['rmse']:,.2f}")
    print(f"  Gap: ${abs(overfit_gap):,.2f}")
    
    if abs(overfit_gap) < 50:
        print(f"  ✓ Minimal overfitting (gap < $50)")
    elif abs(overfit_gap) < 100:
        print(f"  ⚠️  Moderate overfitting (gap < $100)")
    else:
        print(f"  ⚠️  Significant overfitting (gap > $100)")
    
    # Feature importance
    print(f"\nTop 10 Most Important Features (by coefficient magnitude):")
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': model.coef_
    })
    feature_importance['abs_coef'] = abs(feature_importance['coefficient'])
    feature_importance = feature_importance.sort_values('abs_coef', ascending=False)
    
    for i, row in feature_importance.head(10).iterrows():
        direction = "↑" if row['coefficient'] > 0 else "↓"
        print(f"  {direction} {row['feature'][:50]:<50} | Coef: {row['coefficient']:>10.2f}")
    
    return model, train_metrics, val_metrics, training_time

def save_models_and_results(models_dict, imputer):
    """Save trained models and results"""
    print("\n" + "="*80)
    print("SAVING MODELS AND RESULTS")
    print("="*80)
    
    # Create directories
    os.makedirs('models/regression', exist_ok=True)
    os.makedirs('results/metrics', exist_ok=True)
    
    # Save models
    for model_name, model_data in models_dict.items():
        model_path = f'models/regression/{model_name}.pkl'
        joblib.dump(model_data['model'], model_path)
        print(f"✓ Saved {model_name}.pkl")
    
    # Save imputer
    if imputer is not None:
        joblib.dump(imputer, 'models/regression/imputer.pkl')
        print(f"✓ Saved imputer.pkl")
    
    # Save metrics comparison
    metrics_df = pd.DataFrame({
        'Model': list(models_dict.keys()),
        'Train_RMSE': [models_dict[m]['train_metrics']['rmse'] for m in models_dict],
        'Val_RMSE': [models_dict[m]['val_metrics']['rmse'] for m in models_dict],
        'Train_R2': [models_dict[m]['train_metrics']['r2'] for m in models_dict],
        'Val_R2': [models_dict[m]['val_metrics']['r2'] for m in models_dict],
        'Train_MAE': [models_dict[m]['train_metrics']['mae'] for m in models_dict],
        'Val_MAE': [models_dict[m]['val_metrics']['mae'] for m in models_dict],
        'Training_Time': [models_dict[m]['training_time'] for m in models_dict]
    })
    
    metrics_df.to_csv('results/metrics/baseline_models_comparison.csv', index=False)
    print(f"✓ Saved baseline_models_comparison.csv")
    
    print("\nAll models and results saved successfully!")

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("BASELINE REGRESSION MODELS TRAINING")
    print("Team WMK - Deliverable 4")
    print("="*80 + "\n")
    
    # Load data
    X_train, X_val, X_test, y_train, y_val, y_test, weights_train, weights_val, weights_test = load_prepared_data()
    
    # Handle missing values
    X_train, X_val, X_test, imputer = handle_missing_values(X_train, X_val, X_test)
    
    # Dictionary to store all models and results
    models_dict = {}
    
    # Train Tier 1: Linear Regression
    lr_model, lr_train_metrics, lr_val_metrics, lr_time = train_linear_regression(
        X_train, y_train, X_val, y_val, weights_train, weights_val
    )
    models_dict['linear_regression'] = {
        'model': lr_model,
        'train_metrics': lr_train_metrics,
        'val_metrics': lr_val_metrics,
        'training_time': lr_time
    }
    
    # Train Tier 2: Ridge Regression
    ridge_model, ridge_train_metrics, ridge_val_metrics, ridge_time = train_ridge_regression(
        X_train, y_train, X_val, y_val, weights_train, weights_val, alpha=1.0
    )
    models_dict['ridge_regression'] = {
        'model': ridge_model,
        'train_metrics': ridge_train_metrics,
        'val_metrics': ridge_val_metrics,
        'training_time': ridge_time
    }
    
    # Save everything
    save_models_and_results(models_dict, imputer)
    
    # Final comparison
    print("\n" + "="*80)
    print("BASELINE MODELS COMPARISON")
    print("="*80)
    
    print(f"\n{'Model':<20} | {'Val RMSE':<12} | {'Val R²':<10} | {'Val MAE':<12} | {'Time':<8}")
    print("-" * 80)
    
    for model_name, data in models_dict.items():
        val_rmse = data['val_metrics']['rmse']
        val_r2 = data['val_metrics']['r2']
        val_mae = data['val_metrics']['mae']
        train_time = data['training_time']
        
        print(f"{model_name:<20} | ${val_rmse:>10,.2f} | {val_r2:>9.4f} | ${val_mae:>10,.2f} | {train_time:>6.2f}s")
    
    # Determine best baseline model
    best_model = min(models_dict.items(), key=lambda x: x[1]['val_metrics']['rmse'])
    print(f"\n✓ Best Baseline Model: {best_model[0]}")
    print(f"  Validation RMSE: ${best_model[1]['val_metrics']['rmse']:,.2f}")
    print(f"  Validation R²: {best_model[1]['val_metrics']['r2']:.4f}")
    
    print("\n" + "="*80)
    print("BASELINE TRAINING COMPLETE")
    print("="*80)
    print("Next: Train advanced models (Random Forest, XGBoost)")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
