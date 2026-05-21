import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_missing_values(csv_file="combined_city_data.csv"):
    """Analyze missing values in the dataset"""
    
    # Load the data
    df = pd.read_csv(csv_file)
    
    print("="*60)
    print("MISSING VALUES ANALYSIS")
    print("="*60)
    
    # Basic dataset info
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Total data points: {df.shape[0] * df.shape[1]:,}")
    
    # Calculate missing values
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
    
    print("\n" + "="*60)
    print("MISSING VALUES BY COLUMN")
    print("="*60)
    
    if len(columns_with_missing) > 0:
        for _, row in columns_with_missing.iterrows():
            print(f"{row['Column']:<50} | {row['Missing_Count']:>6} ({row['Missing_Percentage']:>6.2f}%)")
    else:
        print("No missing values found in the dataset!")
    
    # Missing values by city
    print("\n" + "="*60)
    print("MISSING VALUES BY CITY")
    print("="*60)
    
    city_missing = df.groupby('city').apply(lambda x: x.isnull().sum().sum())
    city_total = df.groupby('city').size() * (df.shape[1] - 1)  # Exclude city column itself
    city_missing_pct = (city_missing / city_total) * 100
    
    city_summary = pd.DataFrame({
        'City': city_missing.index,
        'Missing_Values': city_missing.values,
        'Total_Possible': city_total.values,
        'Missing_Percentage': city_missing_pct.values
    }).sort_values('Missing_Percentage', ascending=False)
    
    for _, row in city_summary.iterrows():
        print(f"{row['City']:<15} | {row['Missing_Values']:>6} / {row['Total_Possible']:>6} ({row['Missing_Percentage']:>6.2f}%)")
    
    # Create visualizations
    create_missing_value_plots(df, missing_summary)
    
    return missing_summary, city_summary

def create_missing_value_plots(df, missing_summary):
    """Create visualizations for missing values"""
    
    # Filter to columns with missing values for plotting
    columns_with_missing = missing_summary[missing_summary['Missing_Count'] > 0]
    
    if len(columns_with_missing) == 0:
        print("\nNo missing values to visualize!")
        return
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Missing values by column (bar chart)
    if len(columns_with_missing) > 0:
        columns_with_missing_top = columns_with_missing.head(15)  # Top 15 for readability
        
        axes[0].barh(range(len(columns_with_missing_top)), columns_with_missing_top['Missing_Percentage'])
        axes[0].set_yticks(range(len(columns_with_missing_top)))
        axes[0].set_yticklabels([col[:30] + '...' if len(col) > 30 else col 
                                for col in columns_with_missing_top['Column']], fontsize=8)
        axes[0].set_xlabel('Missing Percentage (%)')
        axes[0].set_title('Missing Values by Column (Top 15)')
        axes[0].grid(axis='x', alpha=0.3)
        
        # Add percentage labels on bars
        for i, v in enumerate(columns_with_missing_top['Missing_Percentage']):
            axes[0].text(v + 0.1, i, f'{v:.1f}%', va='center', fontsize=8)
    
    # Plot 2: Missing values heatmap by city and column (top missing columns only)
    if len(columns_with_missing) > 0:
        top_missing_cols = columns_with_missing.head(10)['Column'].tolist()
        missing_by_city = df.groupby('city')[top_missing_cols].apply(lambda x: x.isnull().sum())
        
        sns.heatmap(missing_by_city.T, annot=True, fmt='d', cmap='Reds', 
                   ax=axes[1], cbar_kws={'label': 'Missing Count'})
        axes[1].set_title('Missing Values Heatmap by City (Top 10 Missing Columns)')
        axes[1].set_xlabel('City')
        axes[1].set_ylabel('Column')
        plt.setp(axes[1].get_yticklabels(), rotation=0, fontsize=8)
        plt.setp(axes[1].get_xticklabels(), rotation=45, fontsize=8)
    
    plt.tight_layout()
    plt.savefig('missing_values_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nVisualization saved as 'missing_values_analysis.png'")

if __name__ == "__main__":
    missing_summary, city_summary = analyze_missing_values()
    
    # Save detailed results to CSV
    missing_summary.to_csv('missing_values_summary.csv', index=False)
    city_summary.to_csv('missing_values_by_city.csv', index=False)
    
    print(f"\nDetailed results saved to:")
    print("- missing_values_summary.csv")
    print("- missing_values_by_city.csv")