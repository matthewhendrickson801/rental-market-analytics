"""
Fix Data Leakage - Remove Features Derived from Target Variable

Some engineered features from D3 EDA were calculated using rent (our target).
We must remove these to prevent data leakage.
"""

import pandas as pd

def identify_leakage_features():
    """Identify features that contain information about the target"""
    
    # Features that were calculated FROM rent (data leakage!)
    leakage_features = [
        # Rent Waste features - all calculated using rent
        'Basic_Rent_Waste',
        'Rent_Per_Commute_Minute',
        'Commute_Rent_Mismatch',
        'Comprehensive_Rent_Waste_Score',
        'Total_Monthly_Location_Cost',
        'Time_Value_Rent_Waste',
        
        # Mismatch features that use rent
        'Expected_Rent_From_Income',  # This is OK - predicts rent from income
        'Income_Rent_Mismatch_Ratio',  # Uses actual rent / expected rent - LEAKAGE!
        'Income_Rent_Mismatch_Ratio_Std',  # Standardized version - LEAKAGE!
        'Walkability_Premium_Index',  # Uses rent premium - LEAKAGE!
        'Walkability_Premium_Index_Std',  # Standardized version - LEAKAGE!
        'Comprehensive_Mismatch_Score',  # Uses rent mismatch - LEAKAGE!
        
        # Economic Vitality uses rent/income ratio - LEAKAGE!
        'Economic_Vitality_Score'
    ]
    
    return leakage_features

def remove_leakage_features(df, leakage_features):
    """Remove leakage features from dataframe"""
    
    # Find which leakage features actually exist in the dataframe
    existing_leakage = [f for f in leakage_features if f in df.columns]
    
    if len(existing_leakage) == 0:
        print("✓ No leakage features found")
        return df
    
    print(f"Removing {len(existing_leakage)} leakage features:")
    for feat in existing_leakage:
        print(f"  - {feat}")
    
    # Remove leakage features
    df_clean = df.drop(columns=existing_leakage)
    
    return df_clean

def main():
    """Fix data leakage in prepared datasets"""
    
    print("="*80)
    print("FIXING DATA LEAKAGE")
    print("="*80)
    
    # Identify leakage features
    leakage_features = identify_leakage_features()
    
    print(f"\nIdentified {len(leakage_features)} potential leakage features")
    
    # Load and fix each dataset
    for dataset_name in ['train_data', 'val_data', 'test_data']:
        print(f"\n{dataset_name}.csv:")
        print("-" * 40)
        
        df = pd.read_csv(f'results/prepared_data/{dataset_name}.csv')
        print(f"Original shape: {df.shape}")
        
        # Separate metadata
        meta_cols = ['rent', 'city', 'geoid', 'sample_weight']
        metadata = df[meta_cols]
        features = df.drop(columns=meta_cols)
        
        # Remove leakage features
        features_clean = remove_leakage_features(features, leakage_features)
        
        # Recombine
        df_clean = pd.concat([features_clean, metadata], axis=1)
        
        print(f"Cleaned shape: {df_clean.shape}")
        print(f"Features removed: {features.shape[1] - features_clean.shape[1]}")
        
        # Save cleaned version
        df_clean.to_csv(f'results/prepared_data/{dataset_name}_clean.csv', index=False)
        print(f"✓ Saved {dataset_name}_clean.csv")
    
    # Update feature list
    train_df = pd.read_csv('results/prepared_data/train_data_clean.csv')
    meta_cols = ['rent', 'city', 'geoid', 'sample_weight']
    feature_cols = [col for col in train_df.columns if col not in meta_cols]
    
    with open('results/prepared_data/feature_list_clean.txt', 'w') as f:
        f.write("Features used in modeling (after removing leakage):\n")
        f.write("="*50 + "\n")
        for i, feat in enumerate(feature_cols, 1):
            f.write(f"{i:2d}. {feat}\n")
    
    print(f"\n✓ Saved feature_list_clean.txt ({len(feature_cols)} features)")
    
    print("\n" + "="*80)
    print("DATA LEAKAGE FIXED")
    print("="*80)
    print(f"Original features: 56")
    print(f"Cleaned features: {len(feature_cols)}")
    print(f"Removed: {56 - len(feature_cols)} leakage features")
    print("\nUse *_clean.csv files for training from now on!")
    print("="*80)

if __name__ == "__main__":
    main()
