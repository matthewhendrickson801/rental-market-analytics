import pandas as pd

# Load the removed zip codes data
removed_df = pd.read_csv('removed_zip_codes.csv')
philly_removed = removed_df[removed_df['city'] == 'Philadelphia']

print('PHILADELPHIA ZIP CODES REMOVED:')
print(f'Total: {len(philly_removed)} zip codes')
print()

for _, row in philly_removed.iterrows():
    zip_code = row['geoid']
    pop = row['Total Population (2020-2024)']
    housing = row['Total Housing Units (2020-2024)']
    print(f'{zip_code}: {pop} population, {housing} housing units')

# Also get the imputed Philadelphia zip codes
df_final = pd.read_csv('cleaned_rent_dataset.csv')
philly_luxury = df_final[(df_final['city'] == 'Philadelphia') & (df_final['rent_imputed'] == 'luxury_market')]
philly_rural = df_final[(df_final['city'] == 'Philadelphia') & (df_final['rent_imputed'] == 'rural_area')]
philly_owner = df_final[(df_final['city'] == 'Philadelphia') & (df_final['rent_imputed'] == 'owner_dominated')]

print(f'\nPHILADELPHIA LUXURY MARKET IMPUTATIONS ({len(philly_luxury)} zip codes):')
for _, row in philly_luxury.iterrows():
    print(f'{row["geoid"]}: Imputed ${row["Median Home Rent (2020-2024)"]:.0f}')

print(f'\nPHILADELPHIA RURAL AREA IMPUTATIONS ({len(philly_rural)} zip codes):')
for _, row in philly_rural.iterrows():
    print(f'{row["geoid"]}: Imputed ${row["Median Home Rent (2020-2024)"]:.0f}')

print(f'\nPHILADELPHIA OWNER-DOMINATED IMPUTATIONS ({len(philly_owner)} zip codes):')
for _, row in philly_owner.iterrows():
    print(f'{row["geoid"]}: Imputed ${row["Median Home Rent (2020-2024)"]:.0f}')