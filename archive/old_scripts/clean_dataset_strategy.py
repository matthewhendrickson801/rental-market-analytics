import pandas as pd
import numpy as np

def create_cleaned_dataset():
    """
    Create a cleaned dataset with strategic handling of missing rent data:
    - REMOVE: Commercial/industrial zones with no housing
    - KEEP: Luxury markets and rural areas (impute or flag for separate analysis)
    """
    
    # Load the data
    df = pd.read_csv("combined_city_data.csv")
    
    print("="*80)
    print("STRATEGIC DATA CLEANING FOR RENT ANALYSIS")
    print("="*80)
    print(f"Original dataset: {len(df)} zip codes")
    
    # Identify zip codes to REMOVE (truly non-residential)
    remove_criteria = (
        # Zero or very minimal housing units AND zero or very low population
        ((df['Total Housing Units (2020-2024)'] <= 10) & (df['Total Population (2020-2024)'] <= 50)) |
        # Zero housing units regardless of population (commercial/industrial)
        (df['Total Housing Units (2020-2024)'] == 0)
    )
    
    zip_codes_to_remove = df[remove_criteria]
    
    print(f"\nZIP CODES TO REMOVE (Non-residential areas):")
    print(f"Count: {len(zip_codes_to_remove)} zip codes")
    print("Criteria: ≤10 housing units AND ≤50 population, OR 0 housing units")
    
    # Show examples of what we're removing
    print(f"\nExamples of zip codes being removed:")
    for _, row in zip_codes_to_remove.head(10).iterrows():
        print(f"  {row['geoid']} ({row['city']}): {row['Total Population (2020-2024)']} people, {row['Total Housing Units (2020-2024)']} housing units")
    
    # Create cleaned dataset
    df_cleaned = df[~remove_criteria].copy()
    
    print(f"\nCleaned dataset: {len(df_cleaned)} zip codes")
    print(f"Removed: {len(zip_codes_to_remove)} zip codes ({len(zip_codes_to_remove)/len(df)*100:.1f}%)")
    
    # Analyze remaining missing rent data
    missing_rent_remaining = df_cleaned[df_cleaned['Median Home Rent (2020-2024)'].isnull()]
    
    print(f"\n" + "="*80)
    print("REMAINING MISSING RENT DATA ANALYSIS")
    print("="*80)
    print(f"Zip codes with missing rent after cleaning: {len(missing_rent_remaining)}")
    print(f"Percentage of cleaned dataset: {len(missing_rent_remaining)/len(df_cleaned)*100:.1f}%")
    
    # Categorize remaining missing rent areas
    luxury_markets = missing_rent_remaining[
        missing_rent_remaining['Median Household Income (2020-2024)'] > 100000
    ]
    
    rural_areas = missing_rent_remaining[
        (missing_rent_remaining['Total Population (2020-2024)'] < 2000) &
        (missing_rent_remaining['Median Household Income (2020-2024)'] <= 100000)
    ]
    
    owner_dominated = missing_rent_remaining[
        (missing_rent_remaining['Total Population (2020-2024)'] >= 2000) &
        (missing_rent_remaining['Median Household Income (2020-2024)'] <= 100000)
    ]
    
    print(f"\nBreakdown of remaining missing rent areas:")
    print(f"  Luxury markets (>$100K income): {len(luxury_markets)} zip codes")
    print(f"  Rural areas (<2K population, ≤$100K income): {len(rural_areas)} zip codes")
    print(f"  Owner-dominated markets (≥2K population, ≤$100K income): {len(owner_dominated)} zip codes")
    
    # Strategy for handling each category
    print(f"\n" + "="*80)
    print("IMPUTATION STRATEGY FOR REMAINING MISSING RENT")
    print("="*80)
    
    df_final = df_cleaned.copy()
    
    # Strategy 1: Luxury Markets - Use city-based luxury market median
    print(f"\n1. LUXURY MARKETS ({len(luxury_markets)} zip codes):")
    print("   Strategy: Impute with city's high-income area median rent")
    
    for city in luxury_markets['city'].unique():
        city_data = df_final[df_final['city'] == city]
        city_luxury_missing = luxury_markets[luxury_markets['city'] == city]
        
        # Find high-income areas in the same city with rent data
        city_high_income = city_data[
            (city_data['Median Household Income (2020-2024)'] > 80000) &
            (city_data['Median Home Rent (2020-2024)'].notna())
        ]
        
        if len(city_high_income) > 0:
            luxury_rent_estimate = city_high_income['Median Home Rent (2020-2024)'].median()
            print(f"   {city}: Imputing {len(city_luxury_missing)} zip codes with ${luxury_rent_estimate:,.0f}")
            
            # Apply imputation
            mask = (df_final['city'] == city) & (df_final['geoid'].isin(city_luxury_missing['geoid']))
            df_final.loc[mask, 'Median Home Rent (2020-2024)'] = luxury_rent_estimate
            df_final.loc[mask, 'rent_imputed'] = 'luxury_market'
        else:
            print(f"   {city}: No high-income reference data available")
    
    # Strategy 2: Rural Areas - Use city-based rural/suburban median
    print(f"\n2. RURAL AREAS ({len(rural_areas)} zip codes):")
    print("   Strategy: Impute with city's lower-income area median rent")
    
    for city in rural_areas['city'].unique():
        city_data = df_final[df_final['city'] == city]
        city_rural_missing = rural_areas[rural_areas['city'] == city]
        
        # Find lower-income areas in the same city with rent data
        city_moderate_income = city_data[
            (city_data['Median Household Income (2020-2024)'] <= 80000) &
            (city_data['Median Home Rent (2020-2024)'].notna())
        ]
        
        if len(city_moderate_income) > 0:
            rural_rent_estimate = city_moderate_income['Median Home Rent (2020-2024)'].median()
            print(f"   {city}: Imputing {len(city_rural_missing)} zip codes with ${rural_rent_estimate:,.0f}")
            
            # Apply imputation
            mask = (df_final['city'] == city) & (df_final['geoid'].isin(city_rural_missing['geoid']))
            df_final.loc[mask, 'Median Home Rent (2020-2024)'] = rural_rent_estimate
            df_final.loc[mask, 'rent_imputed'] = 'rural_area'
        else:
            print(f"   {city}: No moderate-income reference data available")
    
    # Strategy 3: Owner-Dominated Markets - Use city median
    print(f"\n3. OWNER-DOMINATED MARKETS ({len(owner_dominated)} zip codes):")
    print("   Strategy: Impute with city's overall median rent")
    
    for city in owner_dominated['city'].unique():
        city_data = df_final[df_final['city'] == city]
        city_owner_missing = owner_dominated[owner_dominated['city'] == city]
        
        # Use city's overall median rent
        city_median_rent = city_data['Median Home Rent (2020-2024)'].median()
        
        if pd.notna(city_median_rent):
            print(f"   {city}: Imputing {len(city_owner_missing)} zip codes with ${city_median_rent:,.0f}")
            
            # Apply imputation
            mask = (df_final['city'] == city) & (df_final['geoid'].isin(city_owner_missing['geoid']))
            df_final.loc[mask, 'Median Home Rent (2020-2024)'] = city_median_rent
            df_final.loc[mask, 'rent_imputed'] = 'owner_dominated'
        else:
            print(f"   {city}: No city median rent available")
    
    # Add imputation flag for originally complete data
    df_final['rent_imputed'] = df_final['rent_imputed'].fillna('original_data')
    
    # Final summary
    print(f"\n" + "="*80)
    print("FINAL DATASET SUMMARY")
    print("="*80)
    
    final_missing = df_final['Median Home Rent (2020-2024)'].isnull().sum()
    print(f"Final dataset size: {len(df_final)} zip codes")
    print(f"Remaining missing rent values: {final_missing}")
    print(f"Successfully imputed: {len(missing_rent_remaining) - final_missing} zip codes")
    
    # Imputation summary
    imputation_summary = df_final['rent_imputed'].value_counts()
    print(f"\nImputation breakdown:")
    for category, count in imputation_summary.items():
        pct = count/len(df_final)*100
        print(f"  {category}: {count} zip codes ({pct:.1f}%)")
    
    # Save the cleaned dataset
    df_final.to_csv('cleaned_rent_dataset.csv', index=False)
    
    # Save removal log
    zip_codes_to_remove.to_csv('removed_zip_codes.csv', index=False)
    
    print(f"\nFiles saved:")
    print(f"  - cleaned_rent_dataset.csv (main analysis dataset)")
    print(f"  - removed_zip_codes.csv (log of removed non-residential areas)")
    
    return df_final, zip_codes_to_remove

def validate_cleaning_strategy():
    """Validate the cleaning approach with summary statistics"""
    
    df_original = pd.read_csv("combined_city_data.csv")
    df_cleaned = pd.read_csv("cleaned_rent_dataset.csv")
    
    print(f"\n" + "="*80)
    print("VALIDATION OF CLEANING STRATEGY")
    print("="*80)
    
    print(f"Original rent data availability:")
    original_with_rent = df_original['Median Home Rent (2020-2024)'].notna().sum()
    print(f"  Zip codes with rent data: {original_with_rent} ({original_with_rent/len(df_original)*100:.1f}%)")
    
    print(f"\nCleaned dataset rent data availability:")
    cleaned_with_rent = df_cleaned['Median Home Rent (2020-2024)'].notna().sum()
    print(f"  Zip codes with rent data: {cleaned_with_rent} ({cleaned_with_rent/len(df_cleaned)*100:.1f}%)")
    
    print(f"\nImprovement:")
    improvement = (cleaned_with_rent/len(df_cleaned)) - (original_with_rent/len(df_original))
    print(f"  Data completeness improved by: {improvement*100:.1f} percentage points")
    
    # Show rent distribution
    print(f"\nRent distribution in cleaned dataset:")
    rent_stats = df_cleaned['Median Home Rent (2020-2024)'].describe()
    for stat, value in rent_stats.items():
        print(f"  {stat}: ${value:,.0f}")

if __name__ == "__main__":
    df_final, removed_zips = create_cleaned_dataset()
    validate_cleaning_strategy()