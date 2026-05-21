import pandas as pd
import numpy as np

def investigate_remaining_missing():
    """Investigate what rent data is still missing after cleaning and imputation"""
    
    # Load the cleaned dataset
    df_cleaned = pd.read_csv('cleaned_rent_dataset.csv')
    
    print("="*80)
    print("INVESTIGATION OF REMAINING MISSING RENT DATA")
    print("="*80)
    
    # Check current status
    total_zips = len(df_cleaned)
    missing_rent = df_cleaned['Median Home Rent (2020-2024)'].isnull().sum()
    complete_rent = df_cleaned['Median Home Rent (2020-2024)'].notna().sum()
    
    print(f"Total zip codes in cleaned dataset: {total_zips}")
    print(f"Zip codes with rent data: {complete_rent} ({complete_rent/total_zips*100:.1f}%)")
    print(f"Zip codes still missing rent data: {missing_rent} ({missing_rent/total_zips*100:.1f}%)")
    
    if missing_rent == 0:
        print("\n🎉 SUCCESS: All zip codes now have rent data!")
        return
    
    # Analyze what's still missing
    still_missing = df_cleaned[df_cleaned['Median Home Rent (2020-2024)'].isnull()].copy()
    
    print(f"\n" + "="*80)
    print("ANALYSIS OF REMAINING MISSING ZIP CODES")
    print("="*80)
    
    print(f"\nBreakdown by city:")
    city_missing = still_missing.groupby('city').size().sort_values(ascending=False)
    for city, count in city_missing.items():
        total_city = len(df_cleaned[df_cleaned['city'] == city])
        pct = count/total_city*100
        print(f"  {city:<15}: {count:>2} out of {total_city:>3} ({pct:>5.1f}%)")
    
    print(f"\n" + "="*80)
    print("DETAILED ANALYSIS OF EACH REMAINING MISSING ZIP CODE")
    print("="*80)
    
    for _, row in still_missing.iterrows():
        zip_code = row['geoid']
        city = row['city']
        population = row['Total Population (2020-2024)']
        housing_units = row['Total Housing Units (2020-2024)']
        median_income = row['Median Household Income (2020-2024)']
        rental_vacancy = row['Rental Vacancy Rate (2020-2024)']
        
        print(f"\nZIP {zip_code} ({city}):")
        print(f"  Population: {population:,}")
        print(f"  Housing Units: {housing_units:,}")
        print(f"  Median Income: ${median_income:,.0f}" if pd.notna(median_income) else "  Median Income: Not Available")
        print(f"  Rental Vacancy: {rental_vacancy:.1f}%" if pd.notna(rental_vacancy) else "  Rental Vacancy: Not Available")
        
        # Analyze why this wasn't imputed
        reasons = []
        
        if pd.isna(median_income):
            reasons.append("Missing income data - couldn't categorize for imputation")
        
        # Check if it should have been categorized
        if pd.notna(median_income):
            if median_income > 100000:
                reasons.append("Should be luxury market but wasn't imputed - possible error")
            elif population < 2000 and median_income <= 100000:
                reasons.append("Should be rural area but wasn't imputed - possible error")
            elif population >= 2000 and median_income <= 100000:
                reasons.append("Should be owner-dominated but wasn't imputed - possible error")
        
        if not reasons:
            reasons.append("Unknown - needs investigation")
        
        print(f"  Likely issue: {'; '.join(reasons)}")
    
    # Check if there are cities with no reference data for imputation
    print(f"\n" + "="*80)
    print("CHECKING CITY-LEVEL REFERENCE DATA AVAILABILITY")
    print("="*80)
    
    for city in still_missing['city'].unique():
        city_data = df_cleaned[df_cleaned['city'] == city]
        city_with_rent = city_data[city_data['Median Home Rent (2020-2024)'].notna()]
        city_with_income = city_data[city_data['Median Household Income (2020-2024)'].notna()]
        
        print(f"\n{city}:")
        print(f"  Total zip codes: {len(city_data)}")
        print(f"  Zip codes with rent data: {len(city_with_rent)}")
        print(f"  Zip codes with income data: {len(city_with_income)}")
        
        if len(city_with_rent) == 0:
            print(f"  ⚠️  NO RENT DATA AVAILABLE for imputation reference!")
        
        if len(city_with_income) == 0:
            print(f"  ⚠️  NO INCOME DATA AVAILABLE for categorization!")
    
    return still_missing

def fix_remaining_missing():
    """Attempt to fix remaining missing values"""
    
    df_cleaned = pd.read_csv('cleaned_rent_dataset.csv')
    still_missing = df_cleaned[df_cleaned['Median Home Rent (2020-2024)'].isnull()].copy()
    
    if len(still_missing) == 0:
        print("No missing values to fix!")
        return df_cleaned
    
    print(f"\n" + "="*80)
    print("ATTEMPTING TO FIX REMAINING MISSING VALUES")
    print("="*80)
    
    df_fixed = df_cleaned.copy()
    
    for _, row in still_missing.iterrows():
        zip_code = row['geoid']
        city = row['city']
        median_income = row['Median Household Income (2020-2024)']
        
        # Get city data for reference
        city_data = df_fixed[df_fixed['city'] == city]
        city_with_rent = city_data[city_data['Median Home Rent (2020-2024)'].notna()]
        
        if len(city_with_rent) == 0:
            print(f"  {zip_code} ({city}): No city reference data - cannot impute")
            continue
        
        # If missing income, use city median rent
        if pd.isna(median_income):
            city_median_rent = city_with_rent['Median Home Rent (2020-2024)'].median()
            mask = (df_fixed['geoid'] == zip_code)
            df_fixed.loc[mask, 'Median Home Rent (2020-2024)'] = city_median_rent
            df_fixed.loc[mask, 'rent_imputed'] = 'missing_income_fallback'
            print(f"  {zip_code} ({city}): Imputed ${city_median_rent:.0f} (city median - missing income)")
        else:
            # This should have been caught by our original logic - investigate
            print(f"  {zip_code} ({city}): Has income data but wasn't imputed - investigating...")
            
            # Apply the same logic as before
            population = row['Total Population (2020-2024)']
            
            if median_income > 100000:
                # Luxury market
                city_luxury = city_data[
                    (city_data['Median Household Income (2020-2024)'] > 80000) &
                    (city_data['Median Home Rent (2020-2024)'].notna())
                ]
                if len(city_luxury) > 0:
                    luxury_rent = city_luxury['Median Home Rent (2020-2024)'].median()
                    mask = (df_fixed['geoid'] == zip_code)
                    df_fixed.loc[mask, 'Median Home Rent (2020-2024)'] = luxury_rent
                    df_fixed.loc[mask, 'rent_imputed'] = 'luxury_market_fixed'
                    print(f"  {zip_code} ({city}): Fixed luxury market - ${luxury_rent:.0f}")
            elif population < 2000:
                # Rural area
                city_rural = city_data[
                    (city_data['Median Household Income (2020-2024)'] <= 80000) &
                    (city_data['Median Home Rent (2020-2024)'].notna())
                ]
                if len(city_rural) > 0:
                    rural_rent = city_rural['Median Home Rent (2020-2024)'].median()
                    mask = (df_fixed['geoid'] == zip_code)
                    df_fixed.loc[mask, 'Median Home Rent (2020-2024)'] = rural_rent
                    df_fixed.loc[mask, 'rent_imputed'] = 'rural_area_fixed'
                    print(f"  {zip_code} ({city}): Fixed rural area - ${rural_rent:.0f}")
            else:
                # Owner-dominated
                city_median_rent = city_with_rent['Median Home Rent (2020-2024)'].median()
                mask = (df_fixed['geoid'] == zip_code)
                df_fixed.loc[mask, 'Median Home Rent (2020-2024)'] = city_median_rent
                df_fixed.loc[mask, 'rent_imputed'] = 'owner_dominated_fixed'
                print(f"  {zip_code} ({city}): Fixed owner-dominated - ${city_median_rent:.0f}")
    
    # Check final status
    final_missing = df_fixed['Median Home Rent (2020-2024)'].isnull().sum()
    print(f"\nFinal missing count: {final_missing}")
    
    if final_missing == 0:
        print("🎉 SUCCESS: All zip codes now have rent data!")
        df_fixed.to_csv('cleaned_rent_dataset_COMPLETE.csv', index=False)
        print("Saved complete dataset as 'cleaned_rent_dataset_COMPLETE.csv'")
    
    return df_fixed

if __name__ == "__main__":
    still_missing = investigate_remaining_missing()
    if len(still_missing) > 0:
        df_final = fix_remaining_missing()
    else:
        print("Dataset is already complete!")