import pandas as pd
import os
from pathlib import Path

def combine_city_data():
    """Combine all city data from the three datasets into one comprehensive CSV"""
    
    # Define the cities (note: Louisville has different spelling in main_data)
    cities = [
        'Miami', 'Tampa', 'Austin', 'Denver', 'Orlando', 'Columbus', 
        'Charlotte', 'Nashville', 'Louisville', 'SanAntonio', 
        'SanFrancisco', 'Indianapolis', 'Jacksonville', 'Philadelphia'
    ]
    
    all_data = []
    
    for city in cities:
        print(f"Processing {city}...")
        
        # Handle Louisville spelling difference
        main_city_name = 'Louisvillle' if city == 'Louisville' else city
        
        try:
            # Read housing data
            housing_file = f"housing_data/{city}_simple.csv"
            housing_df = pd.read_csv(housing_file)
            
            # Read main data
            main_file = f"main_data/Others/{main_city_name}_simple.csv"
            main_df = pd.read_csv(main_file)
            
            # Read population data
            pop_file = f"population_data/{city}_simple.csv"
            pop_df = pd.read_csv(pop_file)
            
            # Add city column to each dataset
            housing_df['city'] = city
            main_df['city'] = city
            pop_df['city'] = city
            
            # Merge on geoid (zip code)
            # Start with housing data as base
            merged = housing_df.copy()
            
            # Merge with main data
            merged = merged.merge(
                main_df.drop(['feature id', 'feature label', 'shid'], axis=1), 
                on=['geoid', 'city'], 
                how='outer'
            )
            
            # Merge with population data
            merged = merged.merge(
                pop_df.drop(['feature id', 'feature label', 'shid'], axis=1), 
                on=['geoid', 'city'], 
                how='outer'
            )
            
            all_data.append(merged)
            print(f"  - {city}: {len(merged)} zip codes processed")
            
        except Exception as e:
            print(f"  - Error processing {city}: {e}")
    
    # Combine all city data
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Reorder columns to put key identifiers first
    key_cols = ['city', 'geoid', 'feature label']
    other_cols = [col for col in final_df.columns if col not in key_cols]
    final_df = final_df[key_cols + other_cols]
    
    # Save to CSV
    output_file = "combined_city_data.csv"
    final_df.to_csv(output_file, index=False)
    
    print(f"\nCombined dataset saved as '{output_file}'")
    print(f"Total records: {len(final_df)}")
    print(f"Total columns: {len(final_df.columns)}")
    print(f"Cities included: {final_df['city'].nunique()}")
    print(f"Unique zip codes: {final_df['geoid'].nunique()}")
    
    return final_df

if __name__ == "__main__":
    df = combine_city_data()
    
    # Show basic info about the combined dataset
    print("\nDataset Info:")
    print(df.info())
    
    print("\nFirst few rows:")
    print(df.head())
    
    print("\nZip codes per city:")
    print(df.groupby('city')['geoid'].count().sort_values(ascending=False))