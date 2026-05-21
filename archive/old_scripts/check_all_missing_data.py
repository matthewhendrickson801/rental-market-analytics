import pandas as pd
import numpy as np

def comprehensive_missing_data_analysis():
    """Check for all missing data in the complete dataset"""
    
    # Load the complete dataset
    df = pd.read_csv('cleaned_rent_dataset_COMPLETE.csv')
    
    print("="*80)
    print("COMPREHENSIVE MISSING DATA ANALYSIS - COMPLETE DATASET")
    print("="*80)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Total data points: {df.shape[0] * df.shape[1]:,}")
    
    # Calculate missing values for all columns
    missing_counts = df.isnull().sum()
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    
    # Create summary table
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_counts,
        'Missing_Percentage': missing_percentages,
        'Data_Type': df.dtypes
    })
    
    # Sort by missing percentage (highest first)
    missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)
    
    # Filter to show only columns with missing values
    columns_with_missing = missing_summary[missing_summary['Missing_Count'] > 0]
    
    print(f"\nColumns with missing values: {len(columns_with_missing)} out of {len(df.columns)}")
    print(f"Total missing values: {missing_counts.sum():,}")
    print(f"Overall missing percentage: {(missing_counts.sum() / (df.shape[0] * df.shape[1])) * 100:.2f}%")
    
    print(f"\n" + "="*80)
    print("MISSING VALUES BY COLUMN")
    print("="*80)
    
    if len(columns_with_missing) > 0:
        print(f"{'Column':<50} | {'Missing':<8} | {'Percentage':<10} | {'Type'}")
        print("-" * 80)
        for _, row in columns_with_missing.iterrows():
            print(f"{row['Column']:<50} | {row['Missing_Count']:>8} | {row['Missing_Percentage']:>9.2f}% | {row['Data_Type']}")
    else:
        print("🎉 NO MISSING VALUES FOUND IN ANY COLUMN!")
    
    # Check median rent specifically
    rent_missing = df['Median Home Rent (2020-2024)'].isnull().sum()
    print(f"\n" + "="*80)
    print("MEDIAN RENT DATA VERIFICATION")
    print("="*80)
    print(f"Missing median rent values: {rent_missing}")
    if rent_missing == 0:
        print("✅ CONFIRMED: 100% median rent data coverage")
    else:
        print("❌ ERROR: Still missing median rent data!")
    
    # Analyze patterns in remaining missing data
    if len(columns_with_missing) > 0:
        print(f"\n" + "="*80)
        print("ANALYSIS OF REMAINING MISSING DATA PATTERNS")
        print("="*80)
        
        # Check if missing data is concentrated in certain cities
        for _, row in columns_with_missing.iterrows():
            col_name = row['Column']
            if col_name == 'rent_imputed':  # Skip our tracking column
                continue
                
            print(f"\n{col_name}:")
            missing_by_city = df[df[col_name].isnull()].groupby('city').size().sort_values(ascending=False)
            
            if len(missing_by_city) > 0:
                print("  Missing by city:")
                for city, count in missing_by_city.items():
                    total_city = len(df[df['city'] == city])
                    pct = count/total_city*100
                    print(f"    {city}: {count} out of {total_city} ({pct:.1f}%)")
            
            # Show some examples of missing values
            missing_examples = df[df[col_name].isnull()][['city', 'geoid', col_name]].head(5)
            if len(missing_examples) > 0:
                print("  Examples of missing values:")
                for _, example in missing_examples.iterrows():
                    print(f"    {example['geoid']} ({example['city']})")
    
    # Summary statistics for key variables
    print(f"\n" + "="*80)
    print("KEY VARIABLES SUMMARY STATISTICS")
    print("="*80)
    
    key_vars = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)', 
        'Total Population (2020-2024)',
        'Total Housing Units (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Unemployment Rate (2020-2024)'
    ]
    
    for var in key_vars:
        if var in df.columns:
            missing = df[var].isnull().sum()
            total = len(df)
            pct_complete = ((total - missing) / total) * 100
            print(f"{var:<50}: {pct_complete:>6.1f}% complete ({total-missing:,}/{total:,})")
    
    return missing_summary

if __name__ == "__main__":
    missing_analysis = comprehensive_missing_data_analysis()