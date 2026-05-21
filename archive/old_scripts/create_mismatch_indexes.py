import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def create_mismatch_indexes():
    """Create specialized indexes to identify rental market mismatches"""
    
    # Load the data
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    print("="*80)
    print("CREATING RENTAL MISMATCH DETECTION INDEXES")
    print("="*80)
    
    # 1. TRANSIT ACCESSIBILITY INDEX (based on 93% correlation discovery)
    print("\n1. TRANSIT ACCESSIBILITY INDEX")
    print("-" * 40)
    
    # Combine historic housing with transit usage
    historic_housing = (
        df['Housing Built 1939 or Earlier (2020-2024)'] + 
        df['Housing Built 1940 to 1949 (2020-2024)'] + 
        df['Housing Built 1950 to 1959 (2020-2024)']
    )
    
    total_housing = df['Total Housing Units (2020-2024)']
    historic_ratio = historic_housing / total_housing
    
    # Normalize transit usage
    transit_usage = df['Commute Transportation by Public Transit (2020-2024)'] / df['Total Population (2020-2024)']
    
    # Create Transit Accessibility Index (0-100 scale)
    df['Transit_Accessibility_Index'] = (
        (historic_ratio * 0.6 + transit_usage * 0.4) * 100
    ).fillna(0)
    
    print(f"Transit Accessibility Index created:")
    print(f"  Range: {df['Transit_Accessibility_Index'].min():.1f} - {df['Transit_Accessibility_Index'].max():.1f}")
    print(f"  Mean: {df['Transit_Accessibility_Index'].mean():.1f}")
    
    # 2. INCOME-RENT MISMATCH RATIO
    print("\n2. INCOME-RENT MISMATCH RATIO")
    print("-" * 40)
    
    # Calculate expected rent based on income (using our 0.653 correlation)
    income_data = df[df['Median Household Income (2020-2024)'].notna()]
    
    # Simple linear relationship: Expected Rent = Income * factor
    income_rent_slope = 0.0087  # Approximate from our analysis
    income_rent_intercept = 783  # Approximate intercept
    
    df['Expected_Rent_From_Income'] = (
        df['Median Household Income (2020-2024)'] * income_rent_slope + income_rent_intercept
    )
    
    # Mismatch ratio: Actual / Expected (1.0 = perfect match)
    df['Income_Rent_Mismatch_Ratio'] = (
        df['Median Home Rent (2020-2024)'] / df['Expected_Rent_From_Income']
    )
    
    print(f"Income-Rent Mismatch Ratio created:")
    print(f"  Range: {df['Income_Rent_Mismatch_Ratio'].min():.2f} - {df['Income_Rent_Mismatch_Ratio'].max():.2f}")
    print(f"  Mean: {df['Income_Rent_Mismatch_Ratio'].mean():.2f}")
    print(f"  >1.2 (High-rent mismatch): {(df['Income_Rent_Mismatch_Ratio'] > 1.2).sum()} zip codes")
    print(f"  <0.8 (Low-rent mismatch): {(df['Income_Rent_Mismatch_Ratio'] < 0.8).sum()} zip codes")
    
    # 3. WALKABILITY PREMIUM INDEX
    print("\n3. WALKABILITY PREMIUM INDEX")
    print("-" * 40)
    
    # Combine car-free living with short commutes
    car_free_ratio = df['No Vehicles Available (2020-2024)'] / df['Total Housing Units (2020-2024)']
    
    # Invert commute time (shorter = better walkability)
    max_commute = df['Commute Mean Travel Time (2020-2024)'].max()
    walkable_commute = (max_commute - df['Commute Mean Travel Time (2020-2024)']) / max_commute
    walkable_commute = walkable_commute.fillna(0.5)  # Average for missing
    
    # Create Walkability Index (0-100 scale)
    df['Walkability_Premium_Index'] = (
        (car_free_ratio * 0.7 + walkable_commute * 0.3) * 100
    ).fillna(0)
    
    print(f"Walkability Premium Index created:")
    print(f"  Range: {df['Walkability_Premium_Index'].min():.1f} - {df['Walkability_Premium_Index'].max():.1f}")
    print(f"  Mean: {df['Walkability_Premium_Index'].mean():.1f}")
    
    # 4. VACANCY QUALITY INDICATOR
    print("\n4. VACANCY QUALITY INDICATOR")
    print("-" * 40)
    
    # High vacancy + High rent = Luxury market (not oversupply)
    high_rent_threshold = df['Median Home Rent (2020-2024)'].quantile(0.75)  # Top 25%
    high_vacancy_threshold = df['Rental Vacancy Rate (2020-2024)'].quantile(0.75)  # Top 25%
    
    df['Luxury_Vacancy_Flag'] = (
        (df['Median Home Rent (2020-2024)'] > high_rent_threshold) & 
        (df['Rental Vacancy Rate (2020-2024)'] > high_vacancy_threshold)
    ).astype(int)
    
    # Create continuous Vacancy Quality Score
    rent_percentile = df['Median Home Rent (2020-2024)'].rank(pct=True)
    vacancy_percentile = df['Rental Vacancy Rate (2020-2024)'].rank(pct=True)
    
    df['Vacancy_Quality_Score'] = (rent_percentile * vacancy_percentile * 100).fillna(0)
    
    print(f"Vacancy Quality Indicator created:")
    print(f"  Luxury Vacancy Flag: {df['Luxury_Vacancy_Flag'].sum()} zip codes")
    print(f"  Vacancy Quality Score range: {df['Vacancy_Quality_Score'].min():.1f} - {df['Vacancy_Quality_Score'].max():.1f}")
    
    # 5. HOUSING AGE DIVERSITY INDEX
    print("\n5. HOUSING AGE DIVERSITY INDEX")
    print("-" * 40)
    
    # Calculate Shannon diversity for housing age distribution
    housing_age_cols = [col for col in df.columns if 'Housing Built' in col and '2020-2024' in col]
    
    diversity_scores = []
    for idx, row in df.iterrows():
        age_counts = [row[col] for col in housing_age_cols]
        total = sum(age_counts)
        
        if total > 0:
            proportions = [count/total for count in age_counts if count > 0]
            # Shannon diversity index
            diversity = -sum(p * np.log(p) for p in proportions if p > 0)
            diversity_scores.append(diversity)
        else:
            diversity_scores.append(0)
    
    df['Housing_Age_Diversity_Index'] = diversity_scores
    
    print(f"Housing Age Diversity Index created:")
    print(f"  Range: {df['Housing_Age_Diversity_Index'].min():.2f} - {df['Housing_Age_Diversity_Index'].max():.2f}")
    print(f"  Mean: {df['Housing_Age_Diversity_Index'].mean():.2f}")
    
    # 6. ECONOMIC STRESS INDEX
    print("\n6. ECONOMIC STRESS INDEX")
    print("-" * 40)
    
    # Combine unemployment, low income, and housing costs
    unemployment_norm = df['Unemployment Rate (2020-2024)'] / df['Unemployment Rate (2020-2024)'].max()
    
    # Poverty rate (below 100% poverty level)
    poverty_households = (
        df['Income 49% and Below Poverty Level (2020-2024)'] + 
        df['Income 50% to 99% the Poverty Level (2020-2024)']
    )
    total_households = df[[col for col in df.columns if 'Income' in col and 'Poverty Level' in col]].sum(axis=1)
    poverty_rate = poverty_households / total_households
    
    # Housing cost burden
    cost_burden = (
        df['Renter Excessive Housing Costs (2020-2024)'] + 
        df['Home Owner Excessive Housing Costs (2020-2024)']
    ) / df['Total Housing Units (2020-2024)']
    
    # Create Economic Stress Index (0-100, higher = more stress)
    df['Economic_Stress_Index'] = (
        (unemployment_norm * 0.4 + poverty_rate * 0.4 + cost_burden * 0.2) * 100
    ).fillna(0)
    
    print(f"Economic Stress Index created:")
    print(f"  Range: {df['Economic_Stress_Index'].min():.1f} - {df['Economic_Stress_Index'].max():.1f}")
    print(f"  Mean: {df['Economic_Stress_Index'].mean():.1f}")
    
    # 7. COMPREHENSIVE MISMATCH SCORE
    print("\n7. COMPREHENSIVE MISMATCH SCORE")
    print("-" * 40)
    
    # Standardize all indexes for combination
    scaler = StandardScaler()
    
    index_cols = [
        'Transit_Accessibility_Index',
        'Income_Rent_Mismatch_Ratio', 
        'Walkability_Premium_Index',
        'Vacancy_Quality_Score',
        'Economic_Stress_Index'
    ]
    
    # Create standardized versions
    for col in index_cols:
        df[f'{col}_Std'] = scaler.fit_transform(df[[col]])
    
    # Comprehensive Mismatch Score (higher = more likely to be a mismatch)
    df['Comprehensive_Mismatch_Score'] = (
        abs(df['Income_Rent_Mismatch_Ratio_Std']) * 0.3 +  # Income mismatch weight
        df['Vacancy_Quality_Score_Std'] * 0.2 +            # Luxury vacancy weight
        abs(df['Transit_Accessibility_Index_Std']) * 0.2 +  # Transit access weight
        df['Walkability_Premium_Index_Std'] * 0.15 +       # Walkability weight
        df['Economic_Stress_Index_Std'] * 0.15             # Economic stress weight
    )
    
    print(f"Comprehensive Mismatch Score created:")
    print(f"  Range: {df['Comprehensive_Mismatch_Score'].min():.2f} - {df['Comprehensive_Mismatch_Score'].max():.2f}")
    print(f"  Mean: {df['Comprehensive_Mismatch_Score'].mean():.2f}")
    
    # Identify top mismatches
    top_mismatches = df.nlargest(10, 'Comprehensive_Mismatch_Score')
    
    print(f"\nTOP 10 RENTAL MARKET MISMATCHES:")
    print("-" * 50)
    for i, (_, row) in enumerate(top_mismatches.iterrows(), 1):
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']})")
        print(f"    Rent: ${row['Median Home Rent (2020-2024)']:,.0f}")
        print(f"    Mismatch Score: {row['Comprehensive_Mismatch_Score']:.2f}")
        print(f"    Income Ratio: {row['Income_Rent_Mismatch_Ratio']:.2f}")
        print(f"    Transit Index: {row['Transit_Accessibility_Index']:.1f}")
        print()
    
    # Save enhanced dataset
    df.to_csv('final_dataset_with_mismatch_indexes.csv', index=False)
    
    print(f"Enhanced dataset saved with {len([col for col in df.columns if 'Index' in col or 'Score' in col or 'Ratio' in col])} new mismatch indicators")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_mismatch_indexes()