import pandas as pd
import numpy as np

def generate_statistical_summary():
    """Generate comprehensive statistical summary for EDA"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    print("STATISTICAL SUMMARY FOR EDA")
    print("="*60)
    
    # Key continuous variables for analysis
    continuous_vars = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Total Population (2020-2024)',
        'Total Housing Units (2020-2024)',
        'Rental Vacancy Rate (2020-2024)',
        'Homeowner Vacancy Rate (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Labor Force Participation Rate (2020-2024)',
        'Commute Mean Travel Time (2020-2024)'
    ]
    
    print("CONTINUOUS VARIABLES STATISTICS:")
    print("-" * 60)
    
    for var in continuous_vars:
        if var in df.columns:
            data = df[var].dropna()
            
            mean_val = data.mean()
            median_val = data.median()
            std_val = data.std()
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            
            # Calculate skewness indicator
            skewness = (mean_val - median_val) / std_val if std_val > 0 else 0
            
            print(f"\n{var}:")
            print(f"  Mean: {mean_val:,.2f}")
            print(f"  Median: {median_val:,.2f}")
            print(f"  Std Dev: {std_val:,.2f}")
            print(f"  IQR: {iqr:,.2f} (Q1: {q1:,.2f}, Q3: {q3:,.2f})")
            print(f"  Range: {data.min():,.2f} - {data.max():,.2f}")
            
            # Skewness interpretation
            if abs(skewness) > 0.5:
                skew_direction = "right" if skewness > 0 else "left"
                print(f"  Skewness: {skewness:.3f} (significantly {skew_direction}-skewed)")
            else:
                print(f"  Skewness: {skewness:.3f} (approximately normal)")
            
            # High variance indicator
            cv = std_val / mean_val if mean_val > 0 else 0
            if cv > 0.5:
                print(f"  Coefficient of Variation: {cv:.3f} (HIGH VARIANCE)")
            else:
                print(f"  Coefficient of Variation: {cv:.3f}")
    
    print(f"\n" + "="*60)
    print("CATEGORICAL VARIABLES CARDINALITY:")
    print("-" * 60)
    
    categorical_vars = ['city', 'geoid']
    
    for var in categorical_vars:
        unique_count = df[var].nunique()
        total_count = len(df)
        cardinality_ratio = unique_count / total_count
        
        print(f"\n{var}:")
        print(f"  Unique Values: {unique_count:,}")
        print(f"  Total Records: {total_count:,}")
        print(f"  Cardinality Ratio: {cardinality_ratio:.3f}")
        
        if cardinality_ratio > 0.9:
            print(f"  Status: HIGH CARDINALITY - consider for encoding/dropping")
        elif cardinality_ratio < 0.1:
            print(f"  Status: LOW CARDINALITY - good for grouping")
        else:
            print(f"  Status: MODERATE CARDINALITY")
    
    print(f"\n" + "="*60)
    print("SPARSE FEATURES ANALYSIS:")
    print("-" * 60)
    
    # Check for sparse features (mostly zeros)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    sparse_threshold = 0.8  # 80% zeros considered sparse
    
    for col in numeric_cols:
        if col not in ['geoid']:  # Skip ID columns
            zero_count = (df[col] == 0).sum()
            zero_percentage = zero_count / len(df)
            
            if zero_percentage > sparse_threshold:
                print(f"\n{col}:")
                print(f"  Zero values: {zero_count:,} ({zero_percentage:.1%})")
                print(f"  Status: SPARSE FEATURE - may impact model performance")
    
    print(f"\n" + "="*60)
    print("VARIABLES REQUIRING NORMALIZATION:")
    print("-" * 60)
    
    # Identify variables that may need normalization
    for var in continuous_vars:
        if var in df.columns:
            data = df[var].dropna()
            
            # Check for different scales
            range_val = data.max() - data.min()
            mean_val = data.mean()
            
            if range_val > 1000 or mean_val > 1000:
                print(f"- {var}: Large scale (range: {range_val:,.0f}, mean: {mean_val:,.0f})")
    
    return df

if __name__ == "__main__":
    df = generate_statistical_summary()