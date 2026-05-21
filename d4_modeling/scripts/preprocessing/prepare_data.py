"""
Data Preparation for Regression Modeling
Prepares dataset for predicting Median Home Rent with focus on outlier detection
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_data():
    """Load the final dataset from D3 EDA"""
    print("="*80)
    print("LOADING DATA")
    print("="*80)
    
    df = pd.read_csv('data/final_dataset_with_boom_index.csv')
    
    print(f"Dataset loaded: {df.shape[0]} ZIP codes × {df.shape[1]} features")
    print(f"Cities: {df['city'].nunique()}")
    print(f"City distribution:\n{df['city'].value_counts()}")
    
    return df

def prepare_features_target(df):
    """Separate features and target variable"""
    print("\n" + "="*80)
    print("PREPARING FEATURES AND TARGET")
    print("="*80)
    
    # Target variable: Median Home Rent
    target_col = 'Median Home Rent (2020-2024)'
    y = df[target_col].copy()
    
    print(f"Target Variable: {target_col}")
    print(f"  Range: ${y.min():,.0f} - ${y.max():,.0f}")
    print(f"  Mean: ${y.mean():,.0f}")
    print(f"  Median: ${y.median():,.0f}")
    print(f"  Std Dev: ${y.std():,.0f}")
    
    # Identify outliers (for weighting later)
    q10 = y.quantile(0.10)
    q90 = y.quantile(0.90)
    
    low_outliers = (y < q10).sum()
    high_outliers = (y > q90).sum()
    
    print(f"\nOutlier Analysis:")
    print(f"  Low rent outliers (<${q10:,.0f}): {low_outliers} ZIP codes")
    print(f"  High rent outliers (>${q90:,.0f}): {high_outliers} ZIP codes")
    print(f"  Normal range: {len(y) - low_outliers - high_outliers} ZIP codes")
    
    # Features: Exclude identifiers and target
    exclude_cols = [
        'geoid',           # ZIP code identifier
        'feature label',   # Geographic label
        'feature id',      # Feature ID
        'shid',           # Shape ID
        'city',           # City name (we'll handle separately)
        target_col,       # Target variable
        'data_source',    # Data source indicator
        'Boom_Category'   # Categorical (we have numeric boom score)
    ]
    
    # Get feature columns
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    print(f"\nFeatures selected: {len(feature_cols)}")
    print(f"Feature categories:")
    
    # Categorize features for documentation
    demographic_features = [col for col in feature_cols if 'Population' in col or 'Income' in col or 'Poverty' in col]
    housing_features = [col for col in feature_cols if 'Housing' in col or 'Vacancy' in col]
    economic_features = [col for col in feature_cols if 'Unemployment' in col or 'Labor' in col or 'Excessive' in col]
    transport_features = [col for col in feature_cols if 'Commute' in col or 'Transit' in col or 'Vehicles' in col]
    engineered_features = [col for col in feature_cols if 'Index' in col or 'Score' in col or 'Ratio' in col or 'Waste' in col or 'Mismatch' in col or 'Boom' in col]
    
    print(f"  Demographic: {len(demographic_features)}")
    print(f"  Housing: {len(housing_features)}")
    print(f"  Economic: {len(economic_features)}")
    print(f"  Transportation: {len(transport_features)}")
    print(f"  Engineered: {len(engineered_features)}")
    
    X = df[feature_cols].copy()
    
    # Store city information for later analysis
    cities = df['city'].copy()
    zip_codes = df['geoid'].copy()
    
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Target vector shape: {y.shape}")
    
    # Check for any missing values
    missing = X.isnull().sum().sum()
    if missing > 0:
        print(f"\n⚠️  WARNING: {missing} missing values found!")
        print(X.isnull().sum()[X.isnull().sum() > 0])
    else:
        print(f"\n✓ No missing values - data is clean!")
    
    return X, y, cities, zip_codes, feature_cols

def create_sample_weights(y, weight_multiplier=3.0):
    """
    Create sample weights to emphasize outliers
    
    Parameters:
    -----------
    y : array-like
        Target variable (rent values)
    weight_multiplier : float
        How much more weight to give outliers (default: 3x)
    
    Returns:
    --------
    weights : array
        Sample weights for each observation
    """
    print("\n" + "="*80)
    print("CREATING SAMPLE WEIGHTS FOR OUTLIER EMPHASIS")
    print("="*80)
    
    # Initialize all weights to 1
    weights = np.ones(len(y))
    
    # Define outliers as bottom 10% and top 10%
    q10 = y.quantile(0.10)
    q90 = y.quantile(0.90)
    
    # Give higher weight to outliers
    low_outlier_mask = y < q10
    high_outlier_mask = y > q90
    
    weights[low_outlier_mask] = weight_multiplier
    weights[high_outlier_mask] = weight_multiplier
    
    print(f"Weight multiplier: {weight_multiplier}x for outliers")
    print(f"Low rent outliers (<${q10:,.0f}): {low_outlier_mask.sum()} ZIP codes → weight = {weight_multiplier}")
    print(f"High rent outliers (>${q90:,.0f}): {high_outlier_mask.sum()} ZIP codes → weight = {weight_multiplier}")
    print(f"Normal range: {(~low_outlier_mask & ~high_outlier_mask).sum()} ZIP codes → weight = 1.0")
    
    return weights

def split_data(X, y, cities, zip_codes, weights, test_size=0.2, val_size=0.15, random_state=42):
    """
    Split data into train, validation, and test sets
    Uses stratified split by city to ensure geographic representation
    
    Parameters:
    -----------
    test_size : float
        Proportion for test set (default: 0.2 = 20%)
    val_size : float
        Proportion of remaining data for validation (default: 0.15)
    """
    print("\n" + "="*80)
    print("SPLITTING DATA: TRAIN / VALIDATION / TEST")
    print("="*80)
    
    # First split: separate test set (20%)
    X_temp, X_test, y_temp, y_test, cities_temp, cities_test, zip_temp, zip_test, weights_temp, weights_test = train_test_split(
        X, y, cities, zip_codes, weights,
        test_size=test_size,
        random_state=random_state,
        stratify=cities  # Stratify by city for geographic balance
    )
    
    # Second split: separate validation from training
    # val_size=0.15 means 15% of remaining 80% = 12% of total
    val_proportion = val_size / (1 - test_size)
    
    X_train, X_val, y_train, y_val, cities_train, cities_val, zip_train, zip_val, weights_train, weights_val = train_test_split(
        X_temp, y_temp, cities_temp, zip_temp, weights_temp,
        test_size=val_proportion,
        random_state=random_state,
        stratify=cities_temp
    )
    
    print(f"Split ratios:")
    print(f"  Training:   {len(X_train):>4} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  Validation: {len(X_val):>4} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  Test:       {len(X_test):>4} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    print(f"\nCity distribution in splits:")
    print(f"Training set:")
    print(cities_train.value_counts().sort_index())
    print(f"\nValidation set:")
    print(cities_val.value_counts().sort_index())
    print(f"\nTest set:")
    print(cities_test.value_counts().sort_index())
    
    # Verify rent distribution is similar across splits
    print(f"\nRent distribution across splits:")
    print(f"  Training:   Mean=${y_train.mean():>7,.0f}, Std=${y_train.std():>6,.0f}")
    print(f"  Validation: Mean=${y_val.mean():>7,.0f}, Std=${y_val.std():>6,.0f}")
    print(f"  Test:       Mean=${y_test.mean():>7,.0f}, Std=${y_test.std():>6,.0f}")
    
    return (X_train, X_val, X_test, 
            y_train, y_val, y_test,
            cities_train, cities_val, cities_test,
            zip_train, zip_val, zip_test,
            weights_train, weights_val, weights_test)

def scale_features(X_train, X_val, X_test):
    """
    Scale features using StandardScaler
    Fit on training data only to prevent data leakage
    """
    print("\n" + "="*80)
    print("SCALING FEATURES")
    print("="*80)
    
    scaler = StandardScaler()
    
    # Fit on training data only
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"StandardScaler fitted on training data")
    print(f"  Mean: {scaler.mean_[:5]} ... (showing first 5)")
    print(f"  Std:  {scaler.scale_[:5]} ... (showing first 5)")
    
    # Convert back to DataFrames to preserve column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val.columns, index=X_val.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    print(f"✓ Features scaled successfully")
    
    return X_train_scaled, X_val_scaled, X_test_scaled, scaler

def save_prepared_data(X_train, X_val, X_test, y_train, y_val, y_test,
                       cities_train, cities_val, cities_test,
                       zip_train, zip_val, zip_test,
                       weights_train, weights_val, weights_test,
                       scaler, feature_cols):
    """Save all prepared data for modeling"""
    print("\n" + "="*80)
    print("SAVING PREPARED DATA")
    print("="*80)
    
    # Create output directory
    os.makedirs('results/prepared_data', exist_ok=True)
    
    # Save splits as CSV for easy inspection
    train_df = X_train.copy()
    train_df['rent'] = y_train
    train_df['city'] = cities_train
    train_df['geoid'] = zip_train
    train_df['sample_weight'] = weights_train
    train_df.to_csv('results/prepared_data/train_data.csv', index=False)
    
    val_df = X_val.copy()
    val_df['rent'] = y_val
    val_df['city'] = cities_val
    val_df['geoid'] = zip_val
    val_df['sample_weight'] = weights_val
    val_df.to_csv('results/prepared_data/val_data.csv', index=False)
    
    test_df = X_test.copy()
    test_df['rent'] = y_test
    test_df['city'] = cities_test
    test_df['geoid'] = zip_test
    test_df['sample_weight'] = weights_test
    test_df.to_csv('results/prepared_data/test_data.csv', index=False)
    
    # Save scaler
    joblib.dump(scaler, 'results/prepared_data/scaler.pkl')
    
    # Save feature list
    with open('results/prepared_data/feature_list.txt', 'w') as f:
        f.write("Features used in modeling:\n")
        f.write("="*50 + "\n")
        for i, feat in enumerate(feature_cols, 1):
            f.write(f"{i:2d}. {feat}\n")
    
    print(f"✓ Saved train_data.csv ({len(train_df)} rows)")
    print(f"✓ Saved val_data.csv ({len(val_df)} rows)")
    print(f"✓ Saved test_data.csv ({len(test_df)} rows)")
    print(f"✓ Saved scaler.pkl")
    print(f"✓ Saved feature_list.txt ({len(feature_cols)} features)")
    
    print(f"\nData preparation complete!")
    print(f"Ready for model training.")

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("DATA PREPARATION FOR REGRESSION MODELING")
    print("Team WMK - Deliverable 4")
    print("="*80 + "\n")
    
    # Load data
    df = load_data()
    
    # Prepare features and target
    X, y, cities, zip_codes, feature_cols = prepare_features_target(df)
    
    # Create sample weights (emphasize outliers)
    weights = create_sample_weights(y, weight_multiplier=3.0)
    
    # Split data
    (X_train, X_val, X_test, 
     y_train, y_val, y_test,
     cities_train, cities_val, cities_test,
     zip_train, zip_val, zip_test,
     weights_train, weights_val, weights_test) = split_data(X, y, cities, zip_codes, weights)
    
    # Scale features
    X_train_scaled, X_val_scaled, X_test_scaled, scaler = scale_features(X_train, X_val, X_test)
    
    # Save everything
    save_prepared_data(X_train_scaled, X_val_scaled, X_test_scaled,
                      y_train, y_val, y_test,
                      cities_train, cities_val, cities_test,
                      zip_train, zip_val, zip_test,
                      weights_train, weights_val, weights_test,
                      scaler, feature_cols)
    
    print("\n" + "="*80)
    print("PREPARATION SUMMARY")
    print("="*80)
    print(f"✓ Dataset: 1,766 ZIP codes across 14 cities")
    print(f"✓ Features: {len(feature_cols)} variables")
    print(f"✓ Target: Median Home Rent")
    print(f"✓ Outlier weighting: 3x for top/bottom 10%")
    print(f"✓ Splits: 68% train, 12% validation, 20% test")
    print(f"✓ Stratified by city for geographic balance")
    print(f"✓ Features scaled with StandardScaler")
    print(f"✓ All data saved to results/prepared_data/")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
