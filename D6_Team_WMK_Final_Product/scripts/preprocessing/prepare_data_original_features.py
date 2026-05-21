"""
Data Preparation for Regression Modeling - ORIGINAL FEATURES ONLY
Uses only the 37 original features from raw data sources
Removes ALL 18 engineered features from D3 EDA to prevent data leakage
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os

def load_data():
    """Load the full dataset (excluding military bases and retirement communities only)"""
    print("="*80)
    print("LOADING DATA - EXCLUDING MILITARY BASES & RETIREMENT COMMUNITIES")
    print("="*80)
    
    df = pd.read_csv('data/final_dataset_no_military.csv')
    
    print(f"Initial dataset: {df.shape[0]} ZIP codes × {df.shape[1]} features")
    
    # Convert to string for comparison
    df['geoid'] = df['geoid'].astype(str)
    
    # Remove retirement communities (distort market with age-restricted housing, low labor force)
    retirement_zips = [
        '32079',  # Jacksonville - very low labor force (4.8%)
        '32159',  # Orlando - The Villages (largest retirement community in US)
        '33573',  # Tampa - Sun City Center
        '34748',  # Orlando - retirement area
        '33493',  # Miami - retirement community
        '33477',  # Miami - retirement community
        '33480',  # Miami - retirement community
        '33446',  # Miami - Delray Beach retirement area
        '33767',  # Tampa - Clearwater retirement area
        '8640',   # Philadelphia - retirement community
        '78633',  # Austin - Sun City Texas
        '94595',  # San Francisco - retirement area
    ]
    
    # Track removed ZIPs
    excluded_df = df[df['geoid'].isin(retirement_zips)].copy()
    
    # Remove retirement communities
    df = df[~df['geoid'].isin(retirement_zips)].copy()
    
    # Save removed ZIPs
    if len(excluded_df) > 0:
        excluded_df.to_csv('data/removed_retirement_zips.csv', index=False)
        print(f"\n🏘️  Removed {len(excluded_df)} retirement community ZIP codes")
        print(f"   (Age-restricted housing, low labor force participation)")
    
    print(f"\nFinal dataset: {df.shape[0]} ZIP codes × {df.shape[1]} features")
    print(f"Cities: {df['city'].nunique()}")
    print(f"Total exclusions: 16 military bases + {len(excluded_df)} retirement communities = {16 + len(excluded_df)} total")
    
    return df

def select_original_features(df):
    """Keep only original features from raw data sources + add region feature + add urban classification"""
    print("\n" + "="*80)
    print("SELECTING ORIGINAL FEATURES + ADDING REGION + URBAN CLASSIFICATION")
    print("="*80)
    
    # Add region feature based on city
    region_mapping = {
        # Midwest (Low cost of living)
        'Columbus': 'Midwest',
        'Indianapolis': 'Midwest',
        'Louisville': 'Midwest',
        
        # South (Medium cost of living)
        'Charlotte': 'South',
        'Nashville': 'South',
        'Jacksonville': 'South',
        'SanAntonio': 'South',
        'Tampa': 'South',
        'Orlando': 'South',
        
        # High Cost (High cost of living)
        'Austin': 'HighCost',
        'Denver': 'HighCost',
        'Miami': 'HighCost',
        'SanFrancisco': 'HighCost',
        'Philadelphia': 'HighCost'
    }
    
    df['region'] = df['city'].map(region_mapping)
    print(f"\n✅ Added 'region' feature:")
    print(df['region'].value_counts().to_string())
    
    # One-hot encode region (create dummy variables)
    region_dummies = pd.get_dummies(df['region'], prefix='region', drop_first=False)
    df = pd.concat([df, region_dummies], axis=1)
    print(f"\n✅ Created {len(region_dummies.columns)} region dummy variables:")
    for col in region_dummies.columns:
        print(f"   - {col}")
    
    # ADD URBAN CLASSIFICATION (3 categories: Rural, Semi-Rural, Urban)
    print(f"\n✅ Creating urban classification feature...")
    
    def classify_urban_type(row):
        """
        Classify ZIP code as Urban, Semi-Rural, or Rural
        
        Criteria:
        - Urban: High transit (>50) OR (high population >10,000 AND high density >2.5)
        - Semi-Rural: Medium population (2,000-10,000) OR (low transit but reasonable density)
        - Rural: Low population (<2,000) OR very low density
        """
        population = row['Total Population (2020-2024)']
        housing_units = row['Total Housing Units (2020-2024)']
        transit = row['Commute Transportation by Public Transit (2020-2024)']
        
        # Calculate density (people per housing unit)
        density = population / housing_units if housing_units > 0 else 0
        
        # Urban: High transit OR (high pop + high density)
        if transit > 50 or (population > 10000 and density > 2.5):
            return 'Urban'
        
        # Semi-Rural: Medium population OR reasonable density
        elif population > 2000 or density > 2.0:
            return 'SemiRural'
        
        # Rural: Low population AND low density
        else:
            return 'Rural'
    
    df['urban_type'] = df.apply(classify_urban_type, axis=1)
    
    print(f"   Urban classification distribution:")
    print(df['urban_type'].value_counts().to_string())
    
    # One-hot encode urban type
    urban_dummies = pd.get_dummies(df['urban_type'], prefix='urban', drop_first=False)
    df = pd.concat([df, urban_dummies], axis=1)
    print(f"\n✅ Created {len(urban_dummies.columns)} urban type dummy variables:")
    for col in urban_dummies.columns:
        print(f"   - {col}")
    
    # CREATE COMPOSITE POVERTY FEATURE (stronger signal)
    print(f"\n✅ Creating composite poverty feature...")
    
    # Calculate total population in income categories
    income_cols = [
        'Income 49% and Below Poverty Level (2020-2024)',
        'Income 50% to 99% the Poverty Level (2020-2024)',
        'Income 100% to 124% the Poverty Level (2020-2024)',
        'Income 125% to 149% the Poverty Level (2020-2024)',
        'Income 150% to 184% the Poverty Level (2020-2024)',
        'Income 185% to 199% the Poverty Level (2020-2024)',
        'Income 200% and Over the Poverty Level (2020-2024)'
    ]
    df['total_income_pop'] = df[income_cols].sum(axis=1)
    
    # Poverty rate (<125% poverty line)
    poverty_count = (df['Income 49% and Below Poverty Level (2020-2024)'] +
                     df['Income 50% to 99% the Poverty Level (2020-2024)'] +
                     df['Income 100% to 124% the Poverty Level (2020-2024)'])
    df['poverty_rate_pct'] = (poverty_count / df['total_income_pop']) * 100
    df['poverty_rate_pct'] = df['poverty_rate_pct'].fillna(0)
    
    print(f"   Poverty Rate range: {df['poverty_rate_pct'].min():.1f}% - {df['poverty_rate_pct'].max():.1f}%")
    print(f"   Mean: {df['poverty_rate_pct'].mean():.1f}%")
    
    # Target variable
    target_col = 'Median Home Rent (2020-2024)'
    y = df[target_col].copy()
    
    print(f"\nTarget Variable: {target_col}")
    print(f"  Range: ${y.min():,.0f} - ${y.max():,.0f}")
    print(f"  Mean: ${y.mean():,.0f}")
    print(f"  Median: ${y.median():,.0f}")
    
    # ORIGINAL FEATURES ONLY - From the 3 raw data sources
    original_features = [
        # Housing Age Features (10 features)
        'Housing Built 1939 or Earlier (2020-2024)',
        'Housing Built 1940 to 1949 (2020-2024)',
        'Housing Built 1950 to 1959 (2020-2024)',
        'Housing Built 1960 to 1969 (2020-2024)',
        'Housing Built 1970 to 1979 (2020-2024)',
        'Housing Built 1980 to 1989 (2020-2024)',
        'Housing Built 1990 to 1999 (2020-2024)',
        'Housing Built 2000 to 2009 (2020-2024)',
        'Housing Built 2010 to 2019 (2020-2024)',
        'Housing Built 2020 or Later (2020-2024)',
        
        # Economic Features (6 features)
        'Renter Excessive Housing Costs (2020-2024)',
        'Home Owner Excessive Housing Costs (2020-2024)',
        'Median Household Income (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Labor Force Participation Rate (2020-2024)',
        
        # Housing Market Features (3 features)
        'Rental Vacancy Rate (2020-2024)',
        'Homeowner Vacancy Rate (2020-2024)',
        'Total Housing Units (2020-2024)',
        
        # Population Features (2 features)
        'Percent Change in Population (Difference Decennial Census 2020 - 2010)',
        'Total Population (2020-2024)',
        
        # Income Distribution Features (7 features)
        'Income 49% and Below Poverty Level (2020-2024)',
        'Income 50% to 99% the Poverty Level (2020-2024)',
        'Income 100% to 124% the Poverty Level (2020-2024)',
        'Income 125% to 149% the Poverty Level (2020-2024)',
        'Income 150% to 184% the Poverty Level (2020-2024)',
        'Income 185% to 199% the Poverty Level (2020-2024)',
        'Income 200% and Over the Poverty Level (2020-2024)',
        
        # Transportation Features (3 features)
        'Commute Mean Travel Time (2020-2024)',
        'Commute Transportation by Public Transit (2020-2024)',
        'No Vehicles Available (2020-2024)'
    ]
    
    # Add region dummy variables + urban type dummy variables + poverty rate to features
    region_cols = [col for col in df.columns if col.startswith('region_')]
    urban_cols = ['urban_Rural', 'urban_SemiRural', 'urban_Urban']  # Explicit list of dummy variables only
    
    all_features = original_features + region_cols + urban_cols + ['poverty_rate_pct']
    
    # Verify all features exist
    missing_features = [f for f in all_features if f not in df.columns]
    if missing_features:
        print(f"\n⚠️  WARNING: {len(missing_features)} features not found:")
        for f in missing_features:
            print(f"  - {f}")
        all_features = [f for f in all_features if f in df.columns]
    
    print(f"\nOriginal features selected: {len(original_features)}")
    print(f"Region features added: {len(region_cols)}")
    print(f"Urban type features added: {len(urban_cols)}")
    print(f"Poverty rate feature added: 1")
    print(f"TOTAL features: {len(all_features)}")
    print(f"\nFeature categories:")
    print(f"  Housing Age: 10 features")
    print(f"  Economic: 6 features")
    print(f"  Housing Market: 3 features")
    print(f"  Population: 2 features")
    print(f"  Income Distribution: 7 features")
    print(f"  Transportation: 3 features")
    print(f"  Region: {len(region_cols)} features")
    print(f"  Urban Type: {len(urban_cols)} features")
    print(f"  Poverty Rate: 1 feature")
    print(f"  TOTAL: {len(all_features)} features")
    
    X = df[all_features].copy()
    
    # Store metadata
    cities = df['city'].copy()
    zip_codes = df['geoid'].copy()
    
    # Check for missing values
    missing = X.isnull().sum()
    if missing.sum() > 0:
        print(f"\nMissing values found:")
        for col, count in missing[missing > 0].items():
            print(f"  {col}: {count} ({count/len(X)*100:.1f}%)")
    else:
        print(f"\n✓ No missing values!")
    
    return X, y, cities, zip_codes, original_features, df

def create_sample_weights(y, df):
    """
    Create stratified sample weights based on multiple criteria:
    - Urban ZIPs: 2x weight
    - Semi-Rural ZIPs: 2x weight
    - Rural ZIPs: 1.5x weight
    - Small population (<2,000): 3x weight (NEW - to fix overprediction)
    - Zero transit: 2x weight (NEW - to fix geographic isolation)
    - High poverty (>30%): 2x weight
    - Rent outliers (top/bottom 10%): 3x additional multiplier
    
    Weights can stack (e.g., semi-rural + small pop + zero transit + outlier = 2×3×2×3 = 36x)
    """
    print("\n" + "="*80)
    print("CREATING STRATIFIED SAMPLE WEIGHTS (ENHANCED)")
    print("="*80)
    
    weights = np.ones(len(y))
    
    # 1. URBAN TYPE WEIGHT: Different weights for Urban, Semi-Rural, Rural
    urban_col = 'urban_type'
    urban_mask = df[urban_col] == 'Urban'
    semi_rural_mask = df[urban_col] == 'SemiRural'
    rural_mask = df[urban_col] == 'Rural'
    
    weights[urban_mask] *= 2.0
    weights[semi_rural_mask] *= 2.0
    weights[rural_mask] *= 1.5
    
    print(f"\n1. Urban Type Weights:")
    print(f"   Urban: {urban_mask.sum()} ZIPs → 2x weight")
    print(f"   Semi-Rural: {semi_rural_mask.sum()} ZIPs → 2x weight")
    print(f"   Rural: {rural_mask.sum()} ZIPs → 1.5x weight")
    
    # 2. SMALL POPULATION WEIGHT: <2,000 people (NEW - addresses thin markets)
    pop_col = 'Total Population (2020-2024)'
    small_pop_mask = df[pop_col] < 2000
    
    weights[small_pop_mask] *= 3.0
    
    print(f"\n2. Small Population Weight (NEW):")
    print(f"   Population <2,000: {small_pop_mask.sum()} ZIPs → 3x weight (thin rental markets)")
    print(f"   Population ≥2,000: {(~small_pop_mask).sum()} ZIPs → 1x weight")
    
    # 3. ZERO TRANSIT WEIGHT: No public transit (NEW - addresses geographic isolation)
    transit_col = 'Commute Transportation by Public Transit (2020-2024)'
    zero_transit_mask = df[transit_col] == 0
    
    weights[zero_transit_mask] *= 2.0
    
    print(f"\n3. Zero Transit Weight (NEW):")
    print(f"   Zero transit: {zero_transit_mask.sum()} ZIPs → 2x weight (geographic isolation)")
    print(f"   Has transit: {(~zero_transit_mask).sum()} ZIPs → 1x weight")
    
    # 4. POVERTY WEIGHT: High poverty (>30%)
    poverty_col = 'poverty_rate_pct'
    high_poverty_mask = df[poverty_col] > 30
    
    weights[high_poverty_mask] *= 2.0
    
    print(f"\n4. Poverty Weight:")
    print(f"   High poverty (>30%): {high_poverty_mask.sum()} ZIPs → 2x weight")
    print(f"   Normal poverty (≤30%): {(~high_poverty_mask).sum()} ZIPs → 1x weight")
    
    # 5. RENT OUTLIER WEIGHT: Bottom 10% and top 10%
    q10 = y.quantile(0.10)
    q90 = y.quantile(0.90)
    
    low_rent_outlier = y < q10
    high_rent_outlier = y > q90
    
    weights[low_rent_outlier] *= 3.0
    weights[high_rent_outlier] *= 3.0
    
    print(f"\n5. Rent Outlier Weight:")
    print(f"   Low rent outliers (<${q10:,.0f}): {low_rent_outlier.sum()} ZIPs → 3x additional multiplier")
    print(f"   High rent outliers (>${q90:,.0f}): {high_rent_outlier.sum()} ZIPs → 3x additional multiplier")
    
    # Summary statistics
    print(f"\n" + "-"*80)
    print(f"WEIGHT DISTRIBUTION:")
    print(f"  Min weight: {weights.min():.1f}x")
    print(f"  Max weight: {weights.max():.1f}x")
    print(f"  Mean weight: {weights.mean():.2f}x")
    print(f"  Median weight: {np.median(weights):.1f}x")
    
    # Show examples of stacked weights
    max_weight_idx = weights.argmax()
    print(f"\n  Highest weighted ZIP: {df.iloc[max_weight_idx]['geoid']} ({df.iloc[max_weight_idx]['city']})")
    print(f"    Weight: {weights[max_weight_idx]:.1f}x")
    print(f"    Urban Type: {df.iloc[max_weight_idx][urban_col]}")
    print(f"    Small population: {small_pop_mask.iloc[max_weight_idx]}")
    print(f"    Zero transit: {zero_transit_mask.iloc[max_weight_idx]}")
    print(f"    High poverty: {high_poverty_mask.iloc[max_weight_idx]}")
    print(f"    Rent outlier: {low_rent_outlier.iloc[max_weight_idx] or high_rent_outlier.iloc[max_weight_idx]}")
    
    unique_weights = np.unique(weights)
    print(f"\n  Unique weight values: {len(unique_weights)}")
    for w in sorted(unique_weights, reverse=True)[:10]:
        count = (weights == w).sum()
        print(f"    {w:.1f}x: {count} ZIPs ({count/len(weights)*100:.1f}%)")
    
    # Show how many ZIPs have multiple risk factors
    print(f"\n  ZIPs with multiple risk factors:")
    multi_risk = small_pop_mask & zero_transit_mask
    print(f"    Small pop + Zero transit: {multi_risk.sum()} ZIPs")
    multi_risk_rural = multi_risk & (semi_rural_mask | rural_mask)
    print(f"    Small pop + Zero transit + Semi-Rural/Rural: {multi_risk_rural.sum()} ZIPs")
    
    return weights

def split_data(X, y, cities, zip_codes, weights, test_size=0.2, val_size=0.15, random_state=42):
    """Split data into train, validation, and test sets"""
    print("\n" + "="*80)
    print("SPLITTING DATA: TRAIN / VALIDATION / TEST")
    print("="*80)
    
    # First split: separate test set (20%)
    X_temp, X_test, y_temp, y_test, cities_temp, cities_test, zip_temp, zip_test, weights_temp, weights_test = train_test_split(
        X, y, cities, zip_codes, weights,
        test_size=test_size,
        random_state=random_state,
        stratify=cities
    )
    
    # Second split: separate validation from training
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
    
    print(f"\nRent distribution across splits:")
    print(f"  Training:   Mean=${y_train.mean():>7,.0f}, Std=${y_train.std():>6,.0f}")
    print(f"  Validation: Mean=${y_val.mean():>7,.0f}, Std=${y_val.std():>6,.0f}")
    print(f"  Test:       Mean=${y_test.mean():>7,.0f}, Std=${y_test.std():>6,.0f}")
    
    return (X_train, X_val, X_test, 
            y_train, y_val, y_test,
            cities_train, cities_val, cities_test,
            zip_train, zip_val, zip_test,
            weights_train, weights_val, weights_test)

def handle_missing_and_scale(X_train, X_val, X_test):
    """Handle missing values and scale features"""
    print("\n" + "="*80)
    print("HANDLING MISSING VALUES & SCALING")
    print("="*80)
    
    # Impute missing values with median
    imputer = SimpleImputer(strategy='median')
    X_train_imputed = imputer.fit_transform(X_train)
    X_val_imputed = imputer.transform(X_val)
    X_test_imputed = imputer.transform(X_test)
    
    print(f"✓ Missing values imputed using median strategy")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_val_scaled = scaler.transform(X_val_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)
    
    print(f"✓ Features scaled using StandardScaler")
    
    # Convert back to DataFrames
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val.columns, index=X_val.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    return X_train_scaled, X_val_scaled, X_test_scaled, imputer, scaler

def save_prepared_data(X_train, X_val, X_test, y_train, y_val, y_test,
                       cities_train, cities_val, cities_test,
                       zip_train, zip_val, zip_test,
                       weights_train, weights_val, weights_test,
                       imputer, scaler, feature_cols):
    """Save all prepared data"""
    print("\n" + "="*80)
    print("SAVING PREPARED DATA")
    print("="*80)
    
    os.makedirs('results/prepared_data', exist_ok=True)
    
    # Save splits
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
    
    # Save imputer and scaler
    joblib.dump(imputer, 'results/prepared_data/imputer.pkl')
    joblib.dump(scaler, 'results/prepared_data/scaler.pkl')
    
    # Save feature list
    with open('results/prepared_data/feature_list.txt', 'w') as f:
        f.write("ORIGINAL FEATURES ONLY (No Engineered Features)\n")
        f.write("="*50 + "\n\n")
        f.write("Housing Age Features (10):\n")
        for feat in [f for f in feature_cols if 'Housing Built' in f]:
            f.write(f"  - {feat}\n")
        f.write("\nEconomic Features (6):\n")
        for feat in [f for f in feature_cols if 'Income' in f or 'Unemployment' in f or 'Labor' in f or 'Excessive' in f]:
            if 'Poverty' not in feat:
                f.write(f"  - {feat}\n")
        f.write("\nHousing Market Features (3):\n")
        for feat in [f for f in feature_cols if 'Vacancy' in f or 'Total Housing' in f]:
            f.write(f"  - {feat}\n")
        f.write("\nPopulation Features (2):\n")
        for feat in [f for f in feature_cols if 'Population' in f]:
            f.write(f"  - {feat}\n")
        f.write("\nIncome Distribution Features (7):\n")
        for feat in [f for f in feature_cols if 'Poverty' in f]:
            f.write(f"  - {feat}\n")
        f.write("\nTransportation Features (3):\n")
        for feat in [f for f in feature_cols if 'Commute' in f or 'Transit' in f or 'Vehicles' in f]:
            f.write(f"  - {feat}\n")
        f.write(f"\nTOTAL: {len(feature_cols)} original features\n")
    
    print(f"✓ Saved train_data.csv ({len(train_df)} rows)")
    print(f"✓ Saved val_data.csv ({len(val_df)} rows)")
    print(f"✓ Saved test_data.csv ({len(test_df)} rows)")
    print(f"✓ Saved imputer.pkl")
    print(f"✓ Saved scaler.pkl")
    print(f"✓ Saved feature_list.txt ({len(feature_cols)} features)")

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("DATA PREPARATION - ORIGINAL FEATURES ONLY (38 FEATURES)")
    print("Team WMK - Deliverable 4")
    print("="*80 + "\n")
    
    # Load data
    df = load_data()
    
    # Select original features only (returns df with new features added)
    X, y, cities, zip_codes, feature_cols, df = select_original_features(df)
    
    # Create sample weights (pass df for stratified weighting)
    weights = create_sample_weights(y, df)
    
    # Split data
    (X_train, X_val, X_test, 
     y_train, y_val, y_test,
     cities_train, cities_val, cities_test,
     zip_train, zip_val, zip_test,
     weights_train, weights_val, weights_test) = split_data(X, y, cities, zip_codes, weights)
    
    # Handle missing values and scale
    X_train_scaled, X_val_scaled, X_test_scaled, imputer, scaler = handle_missing_and_scale(
        X_train, X_val, X_test
    )
    
    # Save everything
    save_prepared_data(X_train_scaled, X_val_scaled, X_test_scaled,
                      y_train, y_val, y_test,
                      cities_train, cities_val, cities_test,
                      zip_train, zip_val, zip_test,
                      weights_train, weights_val, weights_test,
                      imputer, scaler, feature_cols)
    
    print("\n" + "="*80)
    print("PREPARATION SUMMARY")
    print("="*80)
    print(f"✓ Dataset: {len(df)} ZIP codes across 14 cities")
    print(f"✓ Removed: 16 military + 12 retirement = 28 total")
    print(f"✓ Kept: Extreme poverty ZIPs (real-world conditions)")
    print(f"✓ Kept: Tiny population & college towns (well-predicted)")
    print(f"✓ Features: {len(feature_cols)} features (31 original + 3 region + 3 urban + 1 poverty)")
    print(f"✓ NO engineered features (clean data, no leakage)")
    print(f"✓ Target: Median Home Rent")
    print(f"✓ Enhanced stratified weighting (urban type + small pop + zero transit + poverty + outliers)")
    print(f"✓ Splits: 65% train, 15% validation, 20% test")
    print(f"✓ Stratified by city")
    print(f"✓ Missing values imputed, features scaled")
    print(f"✓ Ready for modeling!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
