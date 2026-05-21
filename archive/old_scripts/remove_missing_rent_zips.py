import pandas as pd

def remove_missing_rent_zip_codes():
    """Remove zip codes that originally had missing median rent data instead of imputing"""
    
    # Load the original combined dataset (before any imputation)
    df_original = pd.read_csv('combined_city_data.csv')
    
    print("="*80)
    print("REMOVING ZIP CODES WITH ORIGINALLY MISSING RENT DATA")
    print("="*80)
    
    # Identify zip codes that originally had missing rent data
    originally_missing_rent = df_original[df_original['Median Home Rent (2020-2024)'].isnull()]
    
    print(f"Original dataset: {len(df_original)} zip codes")
    print(f"Zip codes with missing rent data: {len(originally_missing_rent)}")
    print(f"Zip codes with rent data: {len(df_original) - len(originally_missing_rent)}")
    
    # Remove non-residential areas (same criteria as before)
    remove_criteria = (
        ((df_original['Total Housing Units (2020-2024)'] <= 10) & (df_original['Total Population (2020-2024)'] <= 50)) |
        (df_original['Total Housing Units (2020-2024)'] == 0)
    )
    
    non_residential = df_original[remove_criteria]
    
    # Create final dataset: remove non-residential AND missing rent zip codes
    final_dataset = df_original[
        ~remove_criteria &  # Remove non-residential
        df_original['Median Home Rent (2020-2024)'].notna()  # Keep only zip codes with rent data
    ].copy()
    
    print(f"\nREMOVAL SUMMARY:")
    print(f"Non-residential zip codes removed: {len(non_residential)}")
    print(f"Missing rent zip codes removed: {len(originally_missing_rent)}")
    
    # Check for overlap
    overlap = set(non_residential['geoid']).intersection(set(originally_missing_rent['geoid']))
    print(f"Overlap (zip codes in both categories): {len(overlap)}")
    
    total_removed = len(non_residential) + len(originally_missing_rent) - len(overlap)
    print(f"Total unique zip codes removed: {total_removed}")
    print(f"Final dataset size: {len(final_dataset)}")
    
    # Verify no missing rent data
    final_missing_rent = final_dataset['Median Home Rent (2020-2024)'].isnull().sum()
    print(f"Missing rent data in final dataset: {final_missing_rent}")
    
    # Add tracking column for transparency
    final_dataset['data_source'] = 'original_complete_data'
    
    # Show breakdown by city
    print(f"\n" + "="*80)
    print("FINAL DATASET BY CITY")
    print("="*80)
    
    city_summary = final_dataset.groupby('city').size().sort_values(ascending=False)
    for city, count in city_summary.items():
        original_city_count = len(df_original[df_original['city'] == city])
        removed_count = original_city_count - count
        pct_kept = count/original_city_count*100
        print(f"{city:<15}: {count:>3} zip codes (kept {pct_kept:>5.1f}%, removed {removed_count})")
    
    # Create comprehensive removal log
    all_removed = pd.concat([
        non_residential.assign(removal_reason='non_residential'),
        originally_missing_rent.assign(removal_reason='missing_rent_data')
    ]).drop_duplicates(subset=['geoid'])
    
    # For overlapping zip codes, prioritize non_residential reason
    all_removed = all_removed.sort_values('removal_reason').drop_duplicates(subset=['geoid'], keep='first')
    
    print(f"\n" + "="*80)
    print("REMOVAL BREAKDOWN BY REASON")
    print("="*80)
    
    removal_summary = all_removed['removal_reason'].value_counts()
    for reason, count in removal_summary.items():
        pct = count/len(df_original)*100
        print(f"{reason}: {count} zip codes ({pct:.1f}%)")
    
    # Save files
    final_dataset.to_csv('final_rent_dataset_complete_cases_only.csv', index=False)
    all_removed.to_csv('all_removed_zip_codes_final.csv', index=False)
    
    print(f"\nFiles saved:")
    print(f"- final_rent_dataset_complete_cases_only.csv ({len(final_dataset)} zip codes)")
    print(f"- all_removed_zip_codes_final.csv ({len(all_removed)} zip codes)")
    
    # Final statistics
    print(f"\n" + "="*80)
    print("FINAL DATASET STATISTICS")
    print("="*80)
    
    rent_stats = final_dataset['Median Home Rent (2020-2024)'].describe()
    print(f"Rent statistics:")
    for stat, value in rent_stats.items():
        print(f"  {stat}: ${value:,.0f}")
    
    print(f"\nData completeness for key variables:")
    key_vars = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)', 
        'Total Population (2020-2024)',
        'Total Housing Units (2020-2024)'
    ]
    
    for var in key_vars:
        missing = final_dataset[var].isnull().sum()
        complete = len(final_dataset) - missing
        pct = complete/len(final_dataset)*100
        print(f"  {var}: {pct:.1f}% complete ({complete:,}/{len(final_dataset):,})")
    
    return final_dataset, all_removed

if __name__ == "__main__":
    final_df, removed_df = remove_missing_rent_zip_codes()