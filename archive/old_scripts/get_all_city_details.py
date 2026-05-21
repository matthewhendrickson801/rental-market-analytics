import pandas as pd

# Load the removed zip codes data
removed_df = pd.read_csv('removed_zip_codes.csv')

print('ALL REMOVED ZIP CODES BY CITY:')
print('='*50)

for city in sorted(removed_df['city'].unique()):
    city_removed = removed_df[removed_df['city'] == city]
    print(f'\n{city.upper()} ({len(city_removed)} zip codes removed):')
    
    for _, row in city_removed.iterrows():
        zip_code = row['geoid']
        pop = row['Total Population (2020-2024)']
        housing = row['Total Housing Units (2020-2024)']
        
        # Determine reason
        if housing == 0 and pop == 0:
            reason = "Commercial/industrial zone with no residential presence"
        elif housing == 0 and pop > 0:
            reason = "Institutional area with population but no housing stock"
        elif housing <= 10 and pop <= 50:
            reason = "Below threshold (≤50 population AND ≤10 housing units)"
        else:
            reason = "Other criteria met"
            
        print(f'- {zip_code}: {pop} population, {housing} housing units')
        print(f'  Reason: {reason}')

print(f'\nTOTAL REMOVED: {len(removed_df)} zip codes')

# Also get imputation details for all cities
df_final = pd.read_csv('cleaned_rent_dataset.csv')

print('\n\nALL IMPUTED ZIP CODES BY CITY AND CATEGORY:')
print('='*60)

for city in sorted(df_final['city'].unique()):
    city_data = df_final[df_final['city'] == city]
    
    luxury = city_data[city_data['rent_imputed'] == 'luxury_market']
    rural = city_data[city_data['rent_imputed'] == 'rural_area'] 
    owner = city_data[city_data['rent_imputed'] == 'owner_dominated']
    
    if len(luxury) > 0 or len(rural) > 0 or len(owner) > 0:
        print(f'\n{city.upper()}:')
        
        if len(luxury) > 0:
            rent_val = luxury.iloc[0]['Median Home Rent (2020-2024)']
            zip_list = ', '.join([str(z) for z in sorted(luxury['geoid'].tolist())])
            print(f'  Luxury Market ({len(luxury)} zip codes): {zip_list}')
            print(f'    Each imputed ${rent_val:.0f}')
            
        if len(rural) > 0:
            rent_val = rural.iloc[0]['Median Home Rent (2020-2024)']
            zip_list = ', '.join([str(z) for z in sorted(rural['geoid'].tolist())])
            print(f'  Rural Areas ({len(rural)} zip codes): {zip_list}')
            print(f'    Each imputed ${rent_val:.0f}')
            
        if len(owner) > 0:
            rent_val = owner.iloc[0]['Median Home Rent (2020-2024)']
            zip_list = ', '.join([str(z) for z in sorted(owner['geoid'].tolist())])
            print(f'  Owner-Dominated ({len(owner)} zip codes): {zip_list}')
            print(f'    Each imputed ${rent_val:.0f}')