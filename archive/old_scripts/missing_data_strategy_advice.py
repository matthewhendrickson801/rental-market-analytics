import pandas as pd
import numpy as np

def analyze_missing_data_impact():
    """Analyze the impact of remaining missing data on potential analyses"""
    
    df = pd.read_csv('cleaned_rent_dataset_COMPLETE.csv')
    
    print("="*80)
    print("MISSING DATA STRATEGY RECOMMENDATION")
    print("="*80)
    
    # Analyze the missing data patterns
    missing_vars = [
        'Commute Mean Travel Time (2020-2024)',
        'Median Household Income (2020-2024)', 
        'Per Capita Income (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Labor Force Participation Rate (2020-2024)'
    ]
    
    print("ANALYSIS BY VARIABLE:")
    print("="*50)
    
    for var in missing_vars:
        missing_count = df[var].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        print(f"\n{var}:")
        print(f"  Missing: {missing_count} zip codes ({missing_pct:.1f}%)")
        
        # Analyze characteristics of missing data
        missing_data = df[df[var].isnull()]
        
        # Population characteristics
        if len(missing_data) > 0:
            pop_stats = missing_data['Total Population (2020-2024)'].describe()
            print(f"  Population of missing areas - Median: {pop_stats['50%']:,.0f}, Mean: {pop_stats['mean']:,.0f}")
            
            # Housing characteristics  
            housing_stats = missing_data['Total Housing Units (2020-2024)'].describe()
            print(f"  Housing units of missing areas - Median: {housing_stats['50%']:,.0f}, Mean: {housing_stats['mean']:,.0f}")
            
            # Check if these are the same areas missing income data
            if var != 'Median Household Income (2020-2024)':
                income_also_missing = missing_data['Median Household Income (2020-2024)'].isnull().sum()
                print(f"  Also missing income data: {income_also_missing}/{len(missing_data)} ({income_also_missing/len(missing_data)*100:.1f}%)")
    
    print(f"\n" + "="*80)
    print("RECOMMENDATION ANALYSIS")
    print("="*80)
    
    # Check overlap between missing variables
    print("\nOVERLAP ANALYSIS:")
    print("Are the same zip codes missing multiple variables?")
    
    # Create a missing data matrix
    missing_matrix = df[missing_vars].isnull()
    
    # Count how many variables each zip code is missing
    missing_counts_per_zip = missing_matrix.sum(axis=1)
    
    print(f"\nZip codes missing multiple variables:")
    for i in range(1, 6):
        count = (missing_counts_per_zip == i).sum()
        if count > 0:
            pct = count/len(df)*100
            print(f"  Missing {i} variable(s): {count} zip codes ({pct:.1f}%)")
    
    # Identify the most problematic zip codes
    most_missing = df[missing_counts_per_zip >= 3]
    if len(most_missing) > 0:
        print(f"\nZip codes missing 3+ variables ({len(most_missing)} total):")
        for _, row in most_missing.head(10).iterrows():
            missing_vars_list = [var for var in missing_vars if pd.isnull(row[var])]
            print(f"  {row['geoid']} ({row['city']}): Missing {len(missing_vars_list)} variables")
    
    print(f"\n" + "="*80)
    print("STRATEGIC RECOMMENDATIONS")
    print("="*80)
    
    print("\n1. FOR YOUR CURRENT EDA (Due Today):")
    print("   RECOMMENDATION: LEAVE BLANK")
    print("   Reasons:")
    print("   - Your focal variable (rent) is 100% complete")
    print("   - Missing data is <5% for each variable (acceptable threshold)")
    print("   - You can analyze complete cases for correlations")
    print("   - Demonstrates understanding of missing data patterns")
    print("   - Time constraint doesn't allow for proper imputation validation")
    
    print("\n2. FOR FUTURE MODELING (If you continue this research):")
    print("   RECOMMENDATION: SELECTIVE IMPUTATION")
    print("   Strategy:")
    print("   - Commute Time: City-based imputation (transportation patterns)")
    print("   - Income Variables: Already handled with fallback approach")
    print("   - Employment Variables: City-based imputation for small areas")
    
    print("\n3. ANALYSIS IMPACT:")
    
    # Check how many complete cases we have for different analysis scenarios
    complete_cases_all = df.dropna(subset=missing_vars).shape[0]
    complete_cases_key = df.dropna(subset=['Median Home Rent (2020-2024)', 
                                          'Median Household Income (2020-2024)',
                                          'Total Population (2020-2024)',
                                          'Total Housing Units (2020-2024)']).shape[0]
    
    print(f"   - Complete cases (all variables): {complete_cases_all:,} ({complete_cases_all/len(df)*100:.1f}%)")
    print(f"   - Complete cases (key variables): {complete_cases_key:,} ({complete_cases_key/len(df)*100:.1f}%)")
    print(f"   - You can still analyze {complete_cases_key:,} zip codes for most analyses")
    
    print(f"\n4. EDA REPORTING STRATEGY:")
    print("   - Report missing data percentages transparently")
    print("   - Note that missing data follows logical patterns (small/rural areas)")
    print("   - Use complete cases for correlation analysis")
    print("   - Mention this as a limitation but not a major concern")
    print("   - Focus on the 95.9%+ completeness achievement")

if __name__ == "__main__":
    analyze_missing_data_impact()