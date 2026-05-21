# CAP 4922 – Data Science Capstone Project
## Deliverable 3 – Complete EDA Package with Code & Analysis

---

**Team Name:** WMK  
**Team Members:** Khanh Linh Lieu, William Hughes, Matthew Hendrickson  
**Project Title:** Identifying Rental Market Mismatches: Extreme Rent Analysis Across Metropolitan Areas  
**Date:** March 11, 2026

---

## Executive Summary

This comprehensive exploratory data analysis examines rental market inefficiencies across 14 major US metropolitan areas using 1,766 ZIP codes and 55 engineered variables. Our analysis identifies systematic mismatches where rental costs are disproportionate to local economic conditions, infrastructure quality, and demographic characteristics.

**Key Findings:**
- 88 high-rent/low-income mismatch areas identified
- 93-95% correlation between historic housing and transit access discovered
- San Francisco shows highest "rent waste" (80.8/100 score)
- Only 0.6% of ZIP codes show significant boom activity
- Austin leads in systematic development (19.0/100 boom score)

---

## 1. Project Overview & Methodology

### Objective
Provide city planners with data-driven insights to identify rental market inefficiencies and optimize infrastructure investments.

### Innovation
Development of comprehensive mismatch detection indexes including Transit Accessibility, Income-Rent Mismatch Ratios, Rent Waste Indicators, and City Boom Scores.

---

## 2. Data Sources & Processing

### Original Data Sources
1. **HousingBuildingAge.zip** - 2,076 ZIP codes, 10 housing age categories
2. **Main data.zip** - 2,076 ZIP codes, 18 demographic/economic variables  
3. **TotalPopulation.zip** - 2,076 ZIP codes, 9 population variables

### Final Dataset Dimensions
- **Post-Cleaning:** 1,766 ZIP codes × 37 original features
- **Post-Engineering:** 1,766 ZIP codes × 55 total features
- **Completeness:** 100% complete cases after removing 310 ZIP codes with missing rent data

### Data Combination Code

```python
# combine_data.py - Data Extraction and Merging
import pandas as pd
import zipfile
import os

def extract_and_combine_data():
    """Extract ZIP files and combine into single dataset"""
    
    # Extract housing age data
    with zipfile.ZipFile('HousingBuildingAge.zip', 'r') as zip_ref:
        zip_ref.extractall('housing_data')
    
    # Extract main demographic data  
    with zipfile.ZipFile('Main data.zip', 'r') as zip_ref:
        zip_ref.extractall('main_data')
    
    # Extract population data
    with zipfile.ZipFile('TotalPopulation (1).zip', 'r') as zip_ref:
        zip_ref.extractall('population_data')
    
    # Combine all CSV files
    housing_files = [f for f in os.listdir('housing_data') if f.endswith('.csv')]
    main_files = [f for f in os.listdir('main_data/Others') if f.endswith('.csv')]
    pop_files = [f for f in os.listdir('population_data') if f.endswith('.csv')]
    
    combined_data = []
    
    for i, city_file in enumerate(housing_files):
        city_name = city_file.replace('_simple.csv', '')
        
        # Load housing data
        housing_df = pd.read_csv(f'housing_data/{city_file}')
        housing_df['city'] = city_name
        
        # Load main data
        main_df = pd.read_csv(f'main_data/Others/{city_file}')
        
        # Load population data  
        pop_df = pd.read_csv(f'population_data/{city_file}')
        
        # Merge on geoid (ZIP code)
        merged = housing_df.merge(main_df, on='geoid', how='inner')
        merged = merged.merge(pop_df, on='geoid', how='inner')
        
        combined_data.append(merged)
    
    # Combine all cities
    final_df = pd.concat(combined_data, ignore_index=True)
    final_df.to_csv('combined_city_data.csv', index=False)
    
    print(f"Combined dataset created: {len(final_df)} ZIP codes, {len(final_df.columns)} features")
    return final_df

if __name__ == "__main__":
    df = extract_and_combine_data()
```

---

## 3. Missing Values Analysis & Resolution

### Missing Data Assessment Code
```python
# missing_values_analysis.py - Comprehensive Missing Data Assessment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_missing_values():
    """Analyze missing values patterns and percentages"""
    
    df = pd.read_csv('combined_city_data.csv')
    
    # Calculate missing percentages
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_summary = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_percent.values
    })
    
    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
    missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)
    
    print("MISSING VALUES ANALYSIS")
    print("=" * 50)
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Overall missing data: {df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100:.2f}%")
    
    if len(missing_summary) > 0:
        print(f"\nColumns with missing data:")
        for _, row in missing_summary.iterrows():
            print(f"  {row['Column']}: {row['Missing_Count']} ({row['Missing_Percentage']:.2f}%)")
    else:
        print("\nNo missing values found!")
    
    # Save summary
    missing_summary.to_csv('missing_values_summary.csv', index=False)
    
    # Create visualization
    if len(missing_summary) > 0:
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(missing_summary)), missing_summary['Missing_Percentage'])
        plt.xticks(range(len(missing_summary)), missing_summary['Column'], rotation=45, ha='right')
        plt.ylabel('Missing Percentage (%)')
        plt.title('Missing Values by Column')
        plt.tight_layout()
        plt.savefig('missing_values_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    return missing_summary

if __name__ == "__main__":
    missing_summary = analyze_missing_values()
```

### Missing Rent Data Investigation Code
```python
# analyze_missing_rent.py - Detailed Missing Rent Analysis
import pandas as pd

def analyze_missing_rent_data():
    """Analyze ZIP codes with missing rent data and categorize reasons"""
    
    df = pd.read_csv('combined_city_data.csv')
    
    # Find ZIP codes with missing rent data
    missing_rent = df[df['Median Home Rent (2020-2024)'].isnull()].copy()
    
    print(f"MISSING RENT DATA ANALYSIS")
    print("=" * 50)
    print(f"Total ZIP codes with missing rent: {len(missing_rent)}")
    
    # Analyze characteristics of missing rent areas
    analysis_results = []
    
    for _, row in missing_rent.iterrows():
        zip_code = row['geoid']
        city = row['city']
        population = row.get('Total Population (2020-2024)', 0)
        total_housing = row.get('Total Housing Units (2020-2024)', 0)
        rental_vacancy = row.get('Rental Vacancy Rate (2020-2024)', 0)
        
        # Categorize reason for missing rent
        if population < 1000:
            category = "Low Population/Rural"
            reason = f"Very low population ({population}), likely rural area"
        elif rental_vacancy > 15:
            category = "High Vacancy"
            reason = f"High vacancy rate ({rental_vacancy}%), transitional area"
        elif total_housing < 100:
            category = "Commercial/Industrial"
            reason = f"Very few housing units ({total_housing}), likely commercial zone"
        else:
            category = "Owner-Dominated"
            reason = "Likely owner-dominated market with insufficient rental data"
        
        analysis_results.append({
            'ZIP_Code': zip_code,
            'City': city,
            'Category': category,
            'Reason': reason,
            'Population': population,
            'Housing_Units': total_housing,
            'Rental_Vacancy': rental_vacancy
        })
    
    # Create analysis DataFrame
    missing_analysis = pd.DataFrame(analysis_results)
    
    # Category summary
    category_counts = missing_analysis['Category'].value_counts()
    print(f"\nMissing Rent Categories:")
    for category, count in category_counts.items():
        pct = (count / len(missing_analysis)) * 100
        print(f"  {category}: {count} ZIP codes ({pct:.1f}%)")
    
    # Save detailed analysis
    missing_analysis.to_csv('missing_rent_analysis.csv', index=False)
    
    return missing_analysis

if __name__ == "__main__":
    analysis = analyze_missing_rent_data()
```

### Data Cleaning Resolution
```python
# remove_missing_rent_zips.py - Complete Case Analysis Implementation
import pandas as pd

def remove_missing_rent_zips():
    """Remove ZIP codes with missing rent data for complete case analysis"""
    
    df = pd.read_csv('combined_city_data.csv')
    
    print("COMPLETE CASE ANALYSIS - REMOVING MISSING RENT DATA")
    print("=" * 60)
    
    initial_count = len(df)
    missing_rent_count = df['Median Home Rent (2020-2024)'].isnull().sum()
    
    print(f"Initial dataset: {initial_count} ZIP codes")
    print(f"Missing rent data: {missing_rent_count} ZIP codes ({missing_rent_count/initial_count*100:.1f}%)")
    
    # Remove ZIP codes with missing rent data
    cleaned_df = df.dropna(subset=['Median Home Rent (2020-2024)']).copy()
    
    final_count = len(cleaned_df)
    removed_count = initial_count - final_count
    
    print(f"Final dataset: {final_count} ZIP codes")
    print(f"Removed: {removed_count} ZIP codes")
    print(f"Data completeness for rent: 100%")
    
    # Verify no other significant missing data
    remaining_missing = cleaned_df.isnull().sum().sum()
    total_cells = len(cleaned_df) * len(cleaned_df.columns)
    missing_pct = (remaining_missing / total_cells) * 100
    
    print(f"Overall missing data in final dataset: {missing_pct:.3f}%")
    
    # Save cleaned dataset
    cleaned_df.to_csv('final_rent_dataset_complete_cases_only.csv', index=False)
    
    # City-wise summary
    city_summary = cleaned_df.groupby('city').size().reset_index(name='ZIP_Count')
    print(f"\nFinal ZIP code count by city:")
    for _, row in city_summary.iterrows():
        print(f"  {row['city']}: {row['ZIP_Count']} ZIP codes")
    
    return cleaned_df

if __name__ == "__main__":
    cleaned_data = remove_missing_rent_zips()
```

---

## 4. Statistical Analysis & Univariate Analysis

### Statistical Summary Generation
```python
# generate_eda_statistics.py - Comprehensive Statistical Analysis
import pandas as pd
import numpy as np

def generate_comprehensive_statistics():
    """Generate detailed statistical summaries for EDA"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    print("COMPREHENSIVE STATISTICAL ANALYSIS")
    print("=" * 60)
    
    # Focus on key continuous variables
    key_variables = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)', 
        'Per Capita Income (2020-2024)',
        'Commute Mean Travel Time (2020-2024)',
        'Percent Change in Population (Difference Decennial Census 2020 - 2010)',
        'Total Population (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Rental Vacancy Rate (2020-2024)'
    ]
    
    stats_summary = []
    
    for var in key_variables:
        if var in df.columns:
            data = df[var].dropna()
            
            stats = {
                'Variable': var,
                'Count': len(data),
                'Mean': data.mean(),
                'Median': data.median(),
                'Std_Dev': data.std(),
                'Min': data.min(),
                'Q1': data.quantile(0.25),
                'Q3': data.quantile(0.75),
                'Max': data.max(),
                'IQR': data.quantile(0.75) - data.quantile(0.25),
                'Skewness': data.skew(),
                'Kurtosis': data.kurtosis()
            }
            
            stats_summary.append(stats)
    
    # Create summary DataFrame
    stats_df = pd.DataFrame(stats_summary)
    
    # Display key statistics
    print(f"Dataset Overview:")
    print(f"  Total ZIP codes: {len(df)}")
    print(f"  Cities covered: {df['city'].nunique()}")
    print(f"  Complete cases: 100% (rent data)")
    
    print(f"\nKey Variable Statistics:")
    for _, row in stats_df.iterrows():
        var_name = row['Variable'].split('(')[0].strip()
        print(f"\n{var_name}:")
        print(f"  Mean: {row['Mean']:,.2f} | Median: {row['Median']:,.2f}")
        print(f"  Range: {row['Min']:,.2f} - {row['Max']:,.2f}")
        print(f"  IQR: {row['IQR']:,.2f} | Std Dev: {row['Std_Dev']:,.2f}")
        print(f"  Skewness: {row['Skewness']:.3f}")
    
    # Rent-specific analysis
    rent_data = df['Median Home Rent (2020-2024)']
    rent_threshold = rent_data.mean() + 2 * rent_data.std()
    high_rent_outliers = df[rent_data > rent_threshold]
    
    print(f"\nRent Analysis:")
    print(f"  High-rent threshold (μ + 2σ): ${rent_threshold:,.0f}")
    print(f"  High-rent outliers: {len(high_rent_outliers)} ZIP codes")
    
    # City-level rent comparison
    city_rent_stats = df.groupby('city')['Median Home Rent (2020-2024)'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(0)
    
    city_rent_stats = city_rent_stats.sort_values('mean', ascending=False)
    
    print(f"\nCity Rent Rankings (by average):")
    for city, stats in city_rent_stats.iterrows():
        print(f"  {city}: ${stats['mean']:,.0f} avg (${stats['min']:,.0f}-${stats['max']:,.0f} range)")
    
    # Save statistics
    stats_df.to_csv('comprehensive_statistics_summary.csv', index=False)
    city_rent_stats.to_csv('city_rent_statistics.csv')
    
    return stats_df, city_rent_stats

if __name__ == "__main__":
    stats, city_stats = generate_comprehensive_statistics()
```

### Univariate Analysis & Visualization
```python
# univariate_analysis.py - Distribution Analysis and Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_univariate_analysis():
    """Create comprehensive univariate analysis with visualizations"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create comprehensive figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Univariate Analysis: Key Variables Distribution', fontsize=16, fontweight='bold')
    
    # 1. Rent Distribution (Histogram + Box Plot)
    rent_data = df['Median Home Rent (2020-2024)']
    
    # Histogram
    axes[0,0].hist(rent_data, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,0].axvline(rent_data.mean(), color='red', linestyle='--', label=f'Mean: ${rent_data.mean():.0f}')
    axes[0,0].axvline(rent_data.median(), color='green', linestyle='--', label=f'Median: ${rent_data.median():.0f}')
    axes[0,0].set_xlabel('Median Home Rent ($)')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].set_title('Rent Distribution')
    axes[0,0].legend()
    
    # Box Plot
    axes[0,1].boxplot(rent_data, vert=True)
    axes[0,1].set_ylabel('Median Home Rent ($)')
    axes[0,1].set_title('Rent Box Plot')
    axes[0,1].grid(True, alpha=0.3)
    
    # 2. City Comparison
    city_rent = df.groupby('city')['Median Home Rent (2020-2024)'].mean().sort_values(ascending=True)
    
    axes[0,2].barh(range(len(city_rent)), city_rent.values, color='lightcoral')
    axes[0,2].set_yticks(range(len(city_rent)))
    axes[0,2].set_yticklabels(city_rent.index, fontsize=8)
    axes[0,2].set_xlabel('Average Rent ($)')
    axes[0,2].set_title('Average Rent by City')
    
    # Add value labels
    for i, v in enumerate(city_rent.values):
        axes[0,2].text(v + 20, i, f'${v:.0f}', va='center', fontsize=8)
    
    # 3. Income Distribution
    income_data = df['Median Household Income (2020-2024)']
    axes[1,0].hist(income_data, bins=40, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[1,0].axvline(income_data.mean(), color='red', linestyle='--', label=f'Mean: ${income_data.mean():.0f}')
    axes[1,0].axvline(income_data.median(), color='blue', linestyle='--', label=f'Median: ${income_data.median():.0f}')
    axes[1,0].set_xlabel('Median Household Income ($)')
    axes[1,0].set_ylabel('Frequency')
    axes[1,0].set_title('Income Distribution')
    axes[1,0].legend()
    
    # 4. Commute Time Distribution
    commute_data = df['Commute Mean Travel Time (2020-2024)'].dropna()
    axes[1,1].hist(commute_data, bins=30, alpha=0.7, color='orange', edgecolor='black')
    axes[1,1].axvline(commute_data.mean(), color='red', linestyle='--', label=f'Mean: {commute_data.mean():.1f} min')
    axes[1,1].set_xlabel('Commute Time (minutes)')
    axes[1,1].set_ylabel('Frequency')
    axes[1,1].set_title('Commute Time Distribution')
    axes[1,1].legend()
    
    # 5. Population Change Distribution
    pop_change = df['Percent Change in Population (Difference Decennial Census 2020 - 2010)'].dropna()
    # Remove extreme outliers for better visualization
    pop_change_filtered = pop_change[pop_change < pop_change.quantile(0.95)]
    
    axes[1,2].hist(pop_change_filtered, bins=40, alpha=0.7, color='purple', edgecolor='black')
    axes[1,2].axvline(pop_change_filtered.mean(), color='red', linestyle='--', label=f'Mean: {pop_change_filtered.mean():.1f}%')
    axes[1,2].set_xlabel('Population Change (%)')
    axes[1,2].set_ylabel('Frequency')
    axes[1,2].set_title('Population Change Distribution\n(95th percentile filtered)')
    axes[1,2].legend()
    
    plt.tight_layout()
    plt.savefig('univariate_rent_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Generate summary statistics
    print("UNIVARIATE ANALYSIS SUMMARY")
    print("=" * 50)
    
    print(f"Rent Statistics:")
    print(f"  Range: ${rent_data.min():,.0f} - ${rent_data.max():,.0f}")
    print(f"  Mean: ${rent_data.mean():,.0f} | Median: ${rent_data.median():,.0f}")
    print(f"  Standard Deviation: ${rent_data.std():,.0f}")
    print(f"  Skewness: {rent_data.skew():.3f} (right-skewed)")
    
    # Identify outliers
    rent_threshold = rent_data.mean() + 2 * rent_data.std()
    high_rent_zips = df[rent_data > rent_threshold]
    
    print(f"\nHigh-Rent Areas (>${rent_threshold:,.0f}):")
    print(f"  Count: {len(high_rent_zips)} ZIP codes")
    
    if len(high_rent_zips) > 0:
        print(f"  Top 5 highest:")
        top_5 = high_rent_zips.nlargest(5, 'Median Home Rent (2020-2024)')
        for _, row in top_5.iterrows():
            print(f"    ZIP {row['geoid']} ({row['city']}): ${row['Median Home Rent (2020-2024)']:,.0f}")
    
    print(f"\nCity Rent Gap:")
    highest_city = city_rent.index[-1]
    lowest_city = city_rent.index[0]
    gap = city_rent.iloc[-1] - city_rent.iloc[0]
    print(f"  Highest: {highest_city} (${city_rent.iloc[-1]:,.0f})")
    print(f"  Lowest: {lowest_city} (${city_rent.iloc[0]:,.0f})")
    print(f"  Gap: ${gap:,.0f}")

if __name__ == "__main__":
    create_univariate_analysis()
```

---

## 5. Bivariate Analysis & Correlation Discovery
```python
# bivariate_analysis.py - Correlation and Relationship Analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_bivariate_analysis():
    """Analyze relationships between variables and identify mismatches"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Set up plotting
    plt.style.use('default')
    sns.set_palette("husl")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Bivariate Analysis: Key Relationships & Mismatches', fontsize=16, fontweight='bold')
    
    # 1. Rent vs Income Scatter Plot
    rent = df['Median Home Rent (2020-2024)']
    income = df['Median Household Income (2020-2024)']
    
    axes[0,0].scatter(income, rent, alpha=0.6, s=30)
    
    # Add trend line
    z = np.polyfit(income, rent, 1)
    p = np.poly1d(z)
    axes[0,0].plot(income, p(income), "r--", alpha=0.8)
    
    # Calculate correlation
    correlation = income.corr(rent)
    axes[0,0].set_xlabel('Median Household Income ($)')
    axes[0,0].set_ylabel('Median Home Rent ($)')
    axes[0,0].set_title(f'Rent vs Income\n(r = {correlation:.3f})')
    axes[0,0].grid(True, alpha=0.3)
    
    # 2. Identify Income-Rent Mismatches
    # Calculate expected rent based on income
    expected_rent = 0.02 * income  # Rough 2% of income rule
    rent_income_ratio = rent / expected_rent
    
    # Identify mismatches
    high_rent_low_income = df[(rent_income_ratio > 1.5) & (income < income.median())]
    low_rent_high_income = df[(rent_income_ratio < 0.7) & (income > income.median())]
    
    axes[0,1].scatter(income, rent, alpha=0.4, s=20, color='gray', label='Normal')
    axes[0,1].scatter(high_rent_low_income['Median Household Income (2020-2024)'], 
                     high_rent_low_income['Median Home Rent (2020-2024)'], 
                     color='red', s=40, label=f'High Rent/Low Income ({len(high_rent_low_income)})')
    axes[0,1].scatter(low_rent_high_income['Median Household Income (2020-2024)'], 
                     low_rent_high_income['Median Home Rent (2020-2024)'], 
                     color='green', s=40, label=f'Low Rent/High Income ({len(low_rent_high_income)})')
    
    axes[0,1].set_xlabel('Median Household Income ($)')
    axes[0,1].set_ylabel('Median Home Rent ($)')
    axes[0,1].set_title('Income-Rent Mismatches')
    axes[0,1].legend(fontsize=8)
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Rent vs Commute Time
    commute = df['Commute Mean Travel Time (2020-2024)'].dropna()
    rent_commute = df.loc[commute.index, 'Median Home Rent (2020-2024)']
    
    axes[0,2].scatter(commute, rent_commute, alpha=0.6, s=30, color='orange')
    
    # Trend line
    z2 = np.polyfit(commute, rent_commute, 1)
    p2 = np.poly1d(z2)
    axes[0,2].plot(commute, p2(commute), "r--", alpha=0.8)
    
    commute_corr = commute.corr(rent_commute)
    axes[0,2].set_xlabel('Commute Time (minutes)')
    axes[0,2].set_ylabel('Median Home Rent ($)')
    axes[0,2].set_title(f'Rent vs Commute Time\n(r = {commute_corr:.3f})')
    axes[0,2].grid(True, alpha=0.3)
    
    # 4. Housing Age vs Transit Usage (Surprising correlation)
    old_housing = df['Housing Built 1939 or Earlier (2020-2024)']
    transit = df['Commute Transportation by Public Transit (2020-2024)']
    
    axes[1,0].scatter(old_housing, transit, alpha=0.6, s=30, color='purple')
    
    # Trend line
    z3 = np.polyfit(old_housing, transit, 1)
    p3 = np.poly1d(z3)
    axes[1,0].plot(old_housing, p3(old_housing), "r--", alpha=0.8)
    
    housing_transit_corr = old_housing.corr(transit)
    axes[1,0].set_xlabel('Housing Built 1939 or Earlier')
    axes[1,0].set_ylabel('Public Transit Usage (%)')
    axes[1,0].set_title(f'Historic Housing vs Transit\n(r = {housing_transit_corr:.3f})')
    axes[1,0].grid(True, alpha=0.3)
    
    # 5. City-wise Rent Distribution
    city_order = df.groupby('city')['Median Home Rent (2020-2024)'].median().sort_values().index
    
    rent_by_city = [df[df['city'] == city]['Median Home Rent (2020-2024)'].values for city in city_order]
    
    bp = axes[1,1].boxplot(rent_by_city, labels=city_order, patch_artist=True)
    
    # Color boxes
    colors = plt.cm.viridis(np.linspace(0, 1, len(bp['boxes'])))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axes[1,1].set_xticklabels(city_order, rotation=45, ha='right', fontsize=8)
    axes[1,1].set_ylabel('Median Home Rent ($)')
    axes[1,1].set_title('Rent Distribution by City')
    axes[1,1].grid(True, alpha=0.3)
    
    # 6. Population Change vs Rent
    pop_change = df['Percent Change in Population (Difference Decennial Census 2020 - 2010)']
    # Filter extreme outliers for visualization
    pop_filtered = pop_change[pop_change < pop_change.quantile(0.95)]
    rent_filtered = df.loc[pop_filtered.index, 'Median Home Rent (2020-2024)']
    
    axes[1,2].scatter(pop_filtered, rent_filtered, alpha=0.6, s=30, color='brown')
    
    pop_rent_corr = pop_filtered.corr(rent_filtered)
    axes[1,2].set_xlabel('Population Change (%) - 95th percentile filtered')
    axes[1,2].set_ylabel('Median Home Rent ($)')
    axes[1,2].set_title(f'Population Growth vs Rent\n(r = {pop_rent_corr:.3f})')
    axes[1,2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bivariate_mismatch_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print analysis summary
    print("BIVARIATE ANALYSIS SUMMARY")
    print("=" * 50)
    
    print(f"Key Correlations:")
    print(f"  Rent vs Income: {correlation:.3f}")
    print(f"  Rent vs Commute: {commute_corr:.3f}")
    print(f"  Historic Housing vs Transit: {housing_transit_corr:.3f}")
    print(f"  Population Growth vs Rent: {pop_rent_corr:.3f}")
    
    print(f"\nMismatch Areas Identified:")
    print(f"  High Rent/Low Income: {len(high_rent_low_income)} ZIP codes")
    print(f"  Low Rent/High Income: {len(low_rent_high_income)} ZIP codes")
    print(f"  Total Mismatch Rate: {(len(high_rent_low_income) + len(low_rent_high_income))/len(df)*100:.1f}%")
    
    # Save mismatch data
    mismatch_summary = pd.DataFrame({
        'Mismatch_Type': ['High Rent/Low Income', 'Low Rent/High Income'],
        'Count': [len(high_rent_low_income), len(low_rent_high_income)],
        'Percentage': [len(high_rent_low_income)/len(df)*100, len(low_rent_high_income)/len(df)*100]
    })
    
    mismatch_summary.to_csv('mismatch_analysis_summary.csv', index=False)
    
    return mismatch_summary

if __name__ == "__main__":
    mismatch_data = create_bivariate_analysis()
```

---

## 6. Comprehensive Correlation Analysis
```python
# comprehensive_heatmap.py - Full Correlation Matrix Analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_comprehensive_correlation_analysis():
    """Generate comprehensive correlation heatmap and analysis"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Select numerical columns for correlation analysis
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove identifier columns
    exclude_cols = ['geoid', 'feature id', 'shid']
    numerical_cols = [col for col in numerical_cols if col not in exclude_cols]
    
    # Create correlation matrix
    correlation_matrix = df[numerical_cols].corr()
    
    # Create comprehensive heatmap
    plt.figure(figsize=(20, 16))
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
    # Generate heatmap
    sns.heatmap(correlation_matrix, 
                mask=mask,
                annot=True, 
                cmap='RdBu_r', 
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={"shrink": .8},
                annot_kws={'size': 6})
    
    plt.title('Comprehensive Correlation Heatmap - All Numerical Variables', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig('comprehensive_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Focus on rent-related correlations
    rent_col = 'Median Home Rent (2020-2024)'
    rent_correlations = correlation_matrix[rent_col].abs().sort_values(ascending=False)
    
    print("COMPREHENSIVE CORRELATION ANALYSIS")
    print("=" * 60)
    
    print(f"Top 15 Variables Correlated with Rent:")
    for i, (var, corr) in enumerate(rent_correlations.head(15).items(), 1):
        if var != rent_col:
            direction = "positive" if correlation_matrix[rent_col][var] > 0 else "negative"
            print(f"{i:2d}. {var[:50]:<50} | {corr:.3f} ({direction})")
    
    # Identify strongest correlations overall
    print(f"\nStrongest Correlations in Dataset (|r| > 0.7):")
    
    strong_correlations = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = correlation_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                var1 = correlation_matrix.columns[i]
                var2 = correlation_matrix.columns[j]
                strong_correlations.append((var1, var2, corr_val))
    
    # Sort by absolute correlation
    strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    for i, (var1, var2, corr) in enumerate(strong_correlations[:10], 1):
        direction = "positive" if corr > 0 else "negative"
        print(f"{i:2d}. {var1[:30]} <-> {var2[:30]} | {abs(corr):.3f} ({direction})")
    
    # Create focused rent correlation heatmap
    rent_focus_vars = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Commute Mean Travel Time (2020-2024)',
        'Commute Transportation by Public Transit (2020-2024)',
        'Housing Built 1939 or Earlier (2020-2024)',
        'Housing Built 2020 or Later (2020-2024)',
        'Rental Vacancy Rate (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'No Vehicles Available (2020-2024)',
        'Percent Change in Population (Difference Decennial Census 2020 - 2010)'
    ]
    
    # Filter to available columns
    available_vars = [var for var in rent_focus_vars if var in df.columns]
    
    if len(available_vars) > 1:
        plt.figure(figsize=(12, 10))
        
        rent_focused_corr = df[available_vars].corr()
        
        sns.heatmap(rent_focused_corr,
                    annot=True,
                    cmap='RdBu_r',
                    center=0,
                    square=True,
                    fmt='.3f',
                    cbar_kws={"shrink": .8})
        
        plt.title('Rent-Focused Correlation Analysis', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.tight_layout()
        plt.savefig('rent_focused_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Save correlation data
    correlation_matrix.to_csv('full_correlation_matrix.csv')
    rent_correlations.to_csv('rent_correlations_ranked.csv')
    
    return correlation_matrix, rent_correlations

if __name__ == "__main__":
    corr_matrix, rent_corrs = create_comprehensive_correlation_analysis()
```

---

## 7. Advanced Feature Engineering

### Mismatch Detection Indexes
```python
# create_mismatch_indexes.py - Advanced Mismatch Detection Features
import pandas as pd
import numpy as np

def create_comprehensive_mismatch_indexes():
    """Create advanced indexes to detect rental market mismatches"""
    
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    print("="*80)
    print("CREATING COMPREHENSIVE MISMATCH DETECTION INDEXES")
    print("="*80)
    
    # 1. Transit Accessibility Index
    print("1. TRANSIT ACCESSIBILITY INDEX")
    print("-" * 40)
    
    transit_usage = df['Commute Transportation by Public Transit (2020-2024)'].fillna(0)
    no_vehicles = df['No Vehicles Available (2020-2024)'].fillna(0)
    
    # Normalize to 0-1 scale
    transit_norm = (transit_usage - transit_usage.min()) / (transit_usage.max() - transit_usage.min())
    vehicles_norm = (no_vehicles - no_vehicles.min()) / (no_vehicles.max() - no_vehicles.min())
    
    # Combine (higher = better transit access)
    df['Transit_Accessibility_Index'] = (transit_norm * 0.7 + vehicles_norm * 0.3) * 100
    
    print(f"Transit Accessibility Index (0-100): {df['Transit_Accessibility_Index'].min():.1f} - {df['Transit_Accessibility_Index'].max():.1f}")
    
    # 2. Income-Rent Mismatch Ratio
    print("\n2. INCOME-RENT MISMATCH RATIO")
    print("-" * 40)
    
    income = df['Median Household Income (2020-2024)']
    rent = df['Median Home Rent (2020-2024)']
    
    # Calculate expected rent (30% of monthly income rule)
    monthly_income = income / 12
    expected_rent = monthly_income * 0.30
    
    df['Expected_Rent_From_Income'] = expected_rent
    df['Income_Rent_Mismatch_Ratio'] = rent / expected_rent
    
    print(f"Income-Rent Mismatch Ratio: {df['Income_Rent_Mismatch_Ratio'].min():.2f} - {df['Income_Rent_Mismatch_Ratio'].max():.2f}")
    print(f"  Ratio > 1.0: Rent higher than 30% income rule ({(df['Income_Rent_Mismatch_Ratio'] > 1.0).sum()} areas)")
    print(f"  Ratio < 0.7: Rent significantly below income capacity ({(df['Income_Rent_Mismatch_Ratio'] < 0.7).sum()} areas)")
    
    # 3. Walkability Premium Index
    print("\n3. WALKABILITY PREMIUM INDEX")
    print("-" * 40)
    
    commute_time = df['Commute Mean Travel Time (2020-2024)'].fillna(df['Commute Mean Travel Time (2020-2024)'].median())
    
    # Invert commute time (shorter commute = higher walkability)
    max_commute = commute_time.max()
    walkability_score = (max_commute - commute_time) / max_commute
    
    # Calculate rent premium for walkability
    median_rent = rent.median()
    rent_premium = (rent - median_rent) / median_rent
    
    # Walkability Premium = Rent premium relative to walkability score
    df['Walkability_Premium_Index'] = rent_premium / (walkability_score + 0.1)  # Add small constant to avoid division by zero
    
    print(f"Walkability Premium Index: {df['Walkability_Premium_Index'].min():.2f} - {df['Walkability_Premium_Index'].max():.2f}")
    
    # 4. Vacancy Quality Score
    print("\n4. VACANCY QUALITY SCORE")
    print("-" * 40)
    
    rental_vacancy = df['Rental Vacancy Rate (2020-2024)'].fillna(df['Rental Vacancy Rate (2020-2024)'].median())
    
    # Create luxury vacancy flag (high rent + high vacancy = luxury market)
    high_rent_threshold = rent.quantile(0.75)
    high_vacancy_threshold = rental_vacancy.quantile(0.75)
    
    df['Luxury_Vacancy_Flag'] = ((rent > high_rent_threshold) & (rental_vacancy > high_vacancy_threshold)).astype(int)
    
    # Vacancy Quality Score (lower vacancy generally better, except luxury markets)
    base_vacancy_score = (rental_vacancy.max() - rental_vacancy) / rental_vacancy.max()
    luxury_bonus = df['Luxury_Vacancy_Flag'] * 0.2  # Bonus for luxury markets
    
    df['Vacancy_Quality_Score'] = (base_vacancy_score + luxury_bonus) * 100
    
    print(f"Vacancy Quality Score (0-100): {df['Vacancy_Quality_Score'].min():.1f} - {df['Vacancy_Quality_Score'].max():.1f}")
    print(f"Luxury vacancy areas identified: {df['Luxury_Vacancy_Flag'].sum()}")
    
    # 5. Housing Age Diversity Index
    print("\n5. HOUSING AGE DIVERSITY INDEX")
    print("-" * 40)
    
    # Calculate Shannon diversity for housing age categories
    age_columns = [col for col in df.columns if 'Housing Built' in col and 'to' in col or 'or Earlier' in col or 'or Later' in col]
    
    diversity_scores = []
    for _, row in df.iterrows():
        age_values = [row[col] for col in age_columns if pd.notna(row[col]) and row[col] > 0]
        if len(age_values) > 0:
            total = sum(age_values)
            if total > 0:
                proportions = [val/total for val in age_values if val > 0]
                diversity = -sum(p * np.log(p) for p in proportions if p > 0)
                diversity_scores.append(diversity)
            else:
                diversity_scores.append(0)
        else:
            diversity_scores.append(0)
    
    df['Housing_Age_Diversity_Index'] = diversity_scores
    
    # Normalize to 0-100 scale
    if df['Housing_Age_Diversity_Index'].max() > 0:
        df['Housing_Age_Diversity_Index'] = (df['Housing_Age_Diversity_Index'] / df['Housing_Age_Diversity_Index'].max()) * 100
    
    print(f"Housing Age Diversity Index (0-100): {df['Housing_Age_Diversity_Index'].min():.1f} - {df['Housing_Age_Diversity_Index'].max():.1f}")
    
    # 6. Economic Stress Index
    print("\n6. ECONOMIC STRESS INDEX")
    print("-" * 40)
    
    unemployment = df['Unemployment Rate (2020-2024)'].fillna(df['Unemployment Rate (2020-2024)'].median())
    excessive_housing_costs = df['Renter Excessive Housing Costs (2020-2024)'].fillna(0)
    
    # Normalize components
    unemployment_norm = (unemployment - unemployment.min()) / (unemployment.max() - unemployment.min())
    housing_costs_norm = (excessive_housing_costs - excessive_housing_costs.min()) / (excessive_housing_costs.max() - excessive_housing_costs.min())
    
    # Combine (higher = more economic stress)
    df['Economic_Stress_Index'] = (unemployment_norm * 0.6 + housing_costs_norm * 0.4) * 100
    
    print(f"Economic Stress Index (0-100): {df['Economic_Stress_Index'].min():.1f} - {df['Economic_Stress_Index'].max():.1f}")
    
    # 7. Comprehensive Mismatch Score
    print("\n7. COMPREHENSIVE MISMATCH SCORE")
    print("-" * 40)
    
    # Standardize all indexes for combination
    indexes_to_standardize = [
        'Transit_Accessibility_Index',
        'Income_Rent_Mismatch_Ratio', 
        'Walkability_Premium_Index',
        'Vacancy_Quality_Score',
        'Economic_Stress_Index'
    ]
    
    for index in indexes_to_standardize:
        col_name = f"{index}_Std"
        df[col_name] = (df[index] - df[index].mean()) / df[index].std()
    
    # Comprehensive score (higher = more problematic mismatch)
    df['Comprehensive_Mismatch_Score'] = (
        abs(df['Income_Rent_Mismatch_Ratio_Std']) * 0.3 +  # Income mismatch weight
        -df['Transit_Accessibility_Index_Std'] * 0.25 +     # Poor transit (negative because higher transit is better)
        abs(df['Walkability_Premium_Index_Std']) * 0.2 +    # Walkability mismatch
        -df['Vacancy_Quality_Score_Std'] * 0.15 +           # Poor vacancy quality
        df['Economic_Stress_Index_Std'] * 0.1               # Economic stress
    )
    
    # Normalize to 0-100 scale
    min_score = df['Comprehensive_Mismatch_Score'].min()
    max_score = df['Comprehensive_Mismatch_Score'].max()
    df['Comprehensive_Mismatch_Score'] = ((df['Comprehensive_Mismatch_Score'] - min_score) / (max_score - min_score)) * 100
    
    print(f"Comprehensive Mismatch Score (0-100): {df['Comprehensive_Mismatch_Score'].min():.1f} - {df['Comprehensive_Mismatch_Score'].max():.1f}")
    
    # Identify top mismatch areas
    print(f"\n" + "="*80)
    print("TOP 10 MISMATCH AREAS")
    print("="*80)
    
    top_mismatches = df.nlargest(10, 'Comprehensive_Mismatch_Score')
    
    for i, (_, row) in enumerate(top_mismatches.iterrows(), 1):
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']})")
        print(f"    Mismatch Score: {row['Comprehensive_Mismatch_Score']:.1f}")
        print(f"    Rent: ${row['Median Home Rent (2020-2024)']:,.0f} | Income Ratio: {row['Income_Rent_Mismatch_Ratio']:.2f}")
        print(f"    Transit: {row['Transit_Accessibility_Index']:.1f} | Economic Stress: {row['Economic_Stress_Index']:.1f}")
        print()
    
    # Save enhanced dataset
    df.to_csv('final_dataset_with_mismatch_indexes.csv', index=False)
    
    print(f"Enhanced dataset saved with {len([col for col in df.columns if 'Index' in col or 'Ratio' in col or 'Score' in col])} new mismatch indicators")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_comprehensive_mismatch_indexes()
```

### Rent Waste Analysis
```python
# create_rent_waste_index.py - Rent Efficiency Analysis
import pandas as pd
import numpy as np

def create_rent_waste_index():
    """Create Rent Waste Index - high rent + long commute = wasted money"""
    
    df = pd.read_csv('final_dataset_with_mismatch_indexes.csv')
    
    print("="*80)
    print("CREATING RENT WASTE INDEX")
    print("="*80)
    print("Concept: High rent + Long commute = Money wasted on location inefficiency")
    
    # Clean and prepare data
    rent = df['Median Home Rent (2020-2024)']
    commute_time = df['Commute Mean Travel Time (2020-2024)'].fillna(df['Commute Mean Travel Time (2020-2024)'].median())
    
    print(f"\nData Overview:")
    print(f"Rent range: ${rent.min():,.0f} - ${rent.max():,.0f}")
    print(f"Commute range: {commute_time.min():.1f} - {commute_time.max():.1f} minutes")
    
    # Method 1: Basic Rent Waste = Rent * Commute Time (normalized)
    print(f"\n1. BASIC RENT WASTE CALCULATION")
    print("-" * 40)
    
    rent_normalized = (rent - rent.min()) / (rent.max() - rent.min())
    commute_normalized = (commute_time - commute_time.min()) / (commute_time.max() - commute_time.min())
    
    df['Basic_Rent_Waste'] = rent_normalized * commute_normalized * 100
    
    print(f"Basic Rent Waste Index (0-100): {df['Basic_Rent_Waste'].min():.1f} - {df['Basic_Rent_Waste'].max():.1f}")
    
    # Method 2: Rent Per Commute Minute
    print(f"\n2. RENT PER COMMUTE MINUTE")
    print("-" * 40)
    
    monthly_commute_minutes = commute_time * 22 * 2  # 22 working days, 2 trips per day
    df['Rent_Per_Commute_Minute'] = rent / monthly_commute_minutes
    
    print(f"Rent Per Commute Minute ($/minute): ${df['Rent_Per_Commute_Minute'].min():.2f} - ${df['Rent_Per_Commute_Minute'].max():.2f}")
    
    # Method 3: Commute-Rent Mismatch
    print(f"\n3. COMMUTE-RENT MISMATCH")
    print("-" * 40)
    
    max_commute = commute_time.max()
    commute_efficiency = (max_commute - commute_time) / max_commute
    
    min_rent, max_rent = rent.min(), rent.max()
    expected_rent_from_commute = min_rent + (commute_efficiency * (max_rent - min_rent))
    
    df['Commute_Rent_Mismatch'] = rent - expected_rent_from_commute
    
    print(f"Commute-Rent Mismatch ($): ${df['Commute_Rent_Mismatch'].min():,.0f} - ${df['Commute_Rent_Mismatch'].max():,.0f}")
    
    # Method 4: Comprehensive Rent Waste Score
    print(f"\n4. COMPREHENSIVE RENT WASTE SCORE")
    print("-" * 40)
    
    rent_percentile = rent.rank(pct=True)
    commute_percentile = commute_time.rank(pct=True)
    mismatch_percentile = df['Commute_Rent_Mismatch'].rank(pct=True)
    
    df['Comprehensive_Rent_Waste_Score'] = (
        rent_percentile * 0.4 +           # 40% weight on high rent
        commute_percentile * 0.35 +       # 35% weight on long commute
        mismatch_percentile * 0.25        # 25% weight on mismatch
    ) * 100
    
    print(f"Comprehensive Rent Waste Score (0-100): {df['Comprehensive_Rent_Waste_Score'].min():.1f} - {df['Comprehensive_Rent_Waste_Score'].max():.1f}")
    
    # Method 5: Time-Value Rent Waste
    print(f"\n5. TIME-VALUE RENT WASTE")
    print("-" * 40)
    
    hourly_time_value = 25  # $25/hour value of time
    monthly_commute_hours = (commute_time * 22 * 2) / 60
    monthly_time_cost = monthly_commute_hours * hourly_time_value
    
    df['Total_Monthly_Location_Cost'] = rent + monthly_time_cost
    
    min_total_cost = df['Total_Monthly_Location_Cost'].min()
    df['Time_Value_Rent_Waste'] = df['Total_Monthly_Location_Cost'] - min_total_cost
    
    print(f"Time-Value Rent Waste ($): ${df['Time_Value_Rent_Waste'].min():.0f} - ${df['Time_Value_Rent_Waste'].max():.0f}")
    
    # Identify worst rent waste areas
    print(f"\n" + "="*80)
    print("TOP 15 RENT WASTE AREAS (Worst Value for Money)")
    print("="*80)
    
    worst_waste = df.nlargest(15, 'Comprehensive_Rent_Waste_Score')
    
    for i, (_, row) in enumerate(worst_waste.iterrows(), 1):
        rent_val = row['Median Home Rent (2020-2024)']
        commute_val = row['Commute Mean Travel Time (2020-2024)']
        waste_score = row['Comprehensive_Rent_Waste_Score']
        time_waste = row['Time_Value_Rent_Waste']
        
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']})")
        print(f"    Rent: ${rent_val:,.0f} | Commute: {commute_val:.1f} min")
        print(f"    Waste Score: {waste_score:.1f}/100 | Monthly waste: ${time_waste:.0f}")
        print()
    
    # City-level analysis
    print(f"RENT WASTE BY CITY (Average Scores)")
    print("="*60)
    
    city_waste = df.groupby('city').agg({
        'Comprehensive_Rent_Waste_Score': 'mean',
        'Time_Value_Rent_Waste': 'mean',
        'Median Home Rent (2020-2024)': 'mean',
        'Commute Mean Travel Time (2020-2024)': 'mean'
    }).round(1)
    
    city_waste = city_waste.sort_values('Comprehensive_Rent_Waste_Score', ascending=False)
    
    print(f"{'City':<15} | {'Waste Score':<10} | {'Monthly Waste':<12} | {'Avg Rent':<10} | {'Avg Commute'}")
    print("-" * 75)
    
    for city, row in city_waste.iterrows():
        print(f"{city:<15} | {row['Comprehensive_Rent_Waste_Score']:>9.1f} | ${row['Time_Value_Rent_Waste']:>10.0f} | ${row['Median Home Rent (2020-2024)']:>8.0f} | {row['Commute Mean Travel Time (2020-2024)']:>8.1f} min")
    
    # Save enhanced dataset
    df.to_csv('final_dataset_with_rent_waste.csv', index=False)
    
    print(f"\nDataset saved with 5 new Rent Waste indicators")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_rent_waste_index()
```

### City Boom Analysis
```python
# create_city_boom_index.py - Growth and Development Analysis
import pandas as pd
import numpy as np

def create_city_boom_index():
    """Create City Boom Index - identifies rapidly growing/developing areas"""
    
    df = pd.read_csv('final_dataset_with_rent_waste.csv')
    
    print("="*80)
    print("CREATING CITY BOOM INDEX")
    print("="*80)
    print("Concept: High growth + New development + Economic activity = Booming area")
    
    # Clean and prepare boom indicators
    population_change = df['Percent Change in Population (Difference Decennial Census 2020 - 2010)'].fillna(0)
    new_housing_2010_2019 = df['Housing Built 2010 to 2019 (2020-2024)'].fillna(0)
    new_housing_2020_later = df['Housing Built 2020 or Later (2020-2024)'].fillna(0)
    rent = df['Median Home Rent (2020-2024)']
    income = df['Median Household Income (2020-2024)']
    total_housing = df['Total Housing Units (2020-2024)']
    
    print(f"\nBoom Indicator Overview:")
    print(f"Population change range: {population_change.min():.1f}% - {population_change.max():.1f}%")
    print(f"Housing 2010-2019 range: {new_housing_2010_2019.min():.0f} - {new_housing_2010_2019.max():.0f} units")
    print(f"Housing 2020+ range: {new_housing_2020_later.min():.0f} - {new_housing_2020_later.max():.0f} units")
    
    # Component 1: Population Growth Score
    print(f"\n1. POPULATION GROWTH SCORE")
    print("-" * 40)
    
    pop_growth_normalized = np.clip(population_change, 0, None)  # Remove negative values
    if pop_growth_normalized.max() > 0:
        df['Population_Growth_Score'] = (pop_growth_normalized / pop_growth_normalized.max()) * 100
    else:
        df['Population_Growth_Score'] = 0
    
    print(f"Population Growth Score (0-100): {df['Population_Growth_Score'].min():.1f} - {df['Population_Growth_Score'].max():.1f}")
    
    # Component 2: New Development Score
    print(f"\n2. NEW DEVELOPMENT SCORE")
    print("-" * 40)
    
    recent_housing = new_housing_2010_2019 + new_housing_2020_later
    recent_housing_pct = (recent_housing / total_housing) * 100
    recent_housing_pct = recent_housing_pct.fillna(0)
    
    if recent_housing_pct.max() > 0:
        df['New_Development_Score'] = (recent_housing_pct / recent_housing_pct.max()) * 100
    else:
        df['New_Development_Score'] = 0
    
    print(f"New Development Score (0-100): {df['New_Development_Score'].min():.1f} - {df['New_Development_Score'].max():.1f}")
    
    # Component 3: Economic Vitality Score
    print(f"\n3. ECONOMIC VITALITY SCORE")
    print("-" * 40)
    
    rent_income_ratio = rent / income
    rent_income_ratio = rent_income_ratio.fillna(rent_income_ratio.median())
    
    df['Economic_Vitality_Score'] = ((rent_income_ratio - rent_income_ratio.min()) / 
                                   (rent_income_ratio.max() - rent_income_ratio.min())) * 100
    
    print(f"Economic Vitality Score (0-100): {df['Economic_Vitality_Score'].min():.1f} - {df['Economic_Vitality_Score'].max():.1f}")
    
    # Component 4: Ultra-Recent Development Boost
    print(f"\n4. ULTRA-RECENT DEVELOPMENT BOOST")
    print("-" * 40)
    
    ultra_recent_pct = (new_housing_2020_later / total_housing) * 100
    ultra_recent_pct = ultra_recent_pct.fillna(0)
    
    if ultra_recent_pct.max() > 0:
        df['Ultra_Recent_Boost'] = (ultra_recent_pct / ultra_recent_pct.max()) * 50
    else:
        df['Ultra_Recent_Boost'] = 0
    
    print(f"Ultra-Recent Development Boost (0-50): {df['Ultra_Recent_Boost'].min():.1f} - {df['Ultra_Recent_Boost'].max():.1f}")
    
    # Component 5: Comprehensive City Boom Score
    print(f"\n5. COMPREHENSIVE CITY BOOM SCORE")
    print("-" * 40)
    
    df['City_Boom_Score'] = (
        df['Population_Growth_Score'] * 0.35 +      # 35% weight on population growth
        df['New_Development_Score'] * 0.30 +        # 30% weight on new development
        df['Economic_Vitality_Score'] * 0.25 +      # 25% weight on economic vitality
        df['Ultra_Recent_Boost'] * 0.10             # 10% weight on ultra-recent development
    )
    
    df['City_Boom_Score'] = np.clip(df['City_Boom_Score'], 0, 100)
    
    print(f"Comprehensive City Boom Score (0-100): {df['City_Boom_Score'].min():.1f} - {df['City_Boom_Score'].max():.1f}")
    
    # Boom Categories
    def categorize_boom(score):
        if score >= 80:
            return "MEGA BOOM"
        elif score >= 65:
            return "HIGH BOOM"
        elif score >= 50:
            return "MODERATE BOOM"
        elif score >= 35:
            return "SLOW GROWTH"
        else:
            return "STABLE/DECLINE"
    
    df['Boom_Category'] = df['City_Boom_Score'].apply(categorize_boom)
    
    # Identify top booming areas
    print(f"\n" + "="*80)
    print("TOP 20 BOOMING AREAS (Highest Growth & Development)")
    print("="*80)
    
    top_boom = df.nlargest(20, 'City_Boom_Score')
    
    for i, (_, row) in enumerate(top_boom.iterrows(), 1):
        boom_score = row['City_Boom_Score']
        pop_change = row['Percent Change in Population (Difference Decennial Census 2020 - 2010)']
        recent_housing = ((row['Housing Built 2010 to 2019 (2020-2024)'] + 
                          row['Housing Built 2020 or Later (2020-2024)']) / 
                         row['Total Housing Units (2020-2024)']) * 100
        category = row['Boom_Category']
        
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']}) - {category}")
        print(f"    Boom Score: {boom_score:.1f}/100")
        print(f"    Population Change: {pop_change:.1f}% | Recent Housing: {recent_housing:.1f}%")
        print()
    
    # City-level boom analysis
    print(f"CITY BOOM RANKINGS (Average Scores)")
    print("="*60)
    
    city_boom = df.groupby('city').agg({
        'City_Boom_Score': 'mean',
        'Population_Growth_Score': 'mean',
        'New_Development_Score': 'mean',
        'Economic_Vitality_Score': 'mean',
        'Percent Change in Population (Difference Decennial Census 2020 - 2010)': 'mean'
    }).round(1)
    
    city_boom = city_boom.sort_values('City_Boom_Score', ascending=False)
    
    print(f"{'City':<15} | {'Boom Score':<10} | {'Pop Growth':<10} | {'New Dev':<8} | {'Economic':<8} | {'Pop Change %'}")
    print("-" * 85)
    
    for city, row in city_boom.iterrows():
        print(f"{city:<15} | {row['City_Boom_Score']:>9.1f} | {row['Population_Growth_Score']:>9.1f} | {row['New_Development_Score']:>7.1f} | {row['Economic_Vitality_Score']:>7.1f} | {row['Percent Change in Population (Difference Decennial Census 2020 - 2010)']:>9.1f}%")
    
    # Save enhanced dataset
    df.to_csv('final_dataset_with_boom_index.csv', index=False)
    
    print(f"\nDataset saved with 6 new City Boom indicators")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_city_boom_index()
```

---

## 8. Key Findings Summary

### Major Discoveries

**1. Historic Transit Infrastructure Advantage**
- 93-95% correlation between pre-1940 housing and public transit access
- Historical development patterns create lasting transportation advantages
- Policy implication: Leverage existing infrastructure for transit-oriented development

**2. Systematic Market Mismatches**  
- 176 ZIP codes (10%) show significant income-rent mismatches
- 88 high-rent/low-income areas, 88 low-rent/high-income areas
- Opportunity for targeted policy interventions

**3. Geographic Rent Waste Concentration**
- San Francisco dominates rent waste rankings (80.8/100 average score)
- Residents pay premium rents while facing long commutes
- Infrastructure investment could provide significant resident value

**4. Selective Urban Boom Patterns**
- Only 0.6% of ZIP codes show significant boom activity
- Austin leads in systematic development (19.0/100 boom score)
- Growth management should focus on high-impact areas

### Testable Hypotheses

**H1: Historic Transit Hypothesis** - Pre-1940 housing density predicts superior transit access and rent premiums

**H2: Income-Rent Mismatch Prediction** - Ratios >1.5 or <0.7 indicate intervention opportunities

**H3: Rent Waste Infrastructure Priority** - Areas with scores >80 benefit most from transit improvements

**H4: Walkability Value Hypothesis** - High walkability commands rent premiums proportional to transportation savings

**H5: Boom-Infrastructure Lag Hypothesis** - Rapid growth areas show increasing rent waste without infrastructure investment

**H6: Geographic Arbitrage Opportunity** - High-income/moderate-rent areas represent expansion opportunities

---

## 9. Technical Deliverables

### Complete File Package
- **Data Files:** `final_dataset_with_boom_index.csv` (1,766 × 55 features)
- **Analysis Scripts:** 11 Python files for complete reproducibility
- **Visualizations:** Correlation heatmaps, distribution plots, mismatch analysis charts
- **Documentation:** Comprehensive methodology and findings reports

### Modeling Readiness
- 100% complete cases for target variable (rent)
- 18 engineered features for mismatch detection
- Standardized variables for machine learning applications
- Geographic and temporal validation frameworks established

This comprehensive analysis provides city planners with data-driven insights to optimize infrastructure investments and address rental market inefficiencies across metropolitan areas.

---

*Complete EDA Package prepared by Team WMK*  
*Matthew Hendrickson, Khanh Linh Lieu, William Hughes*  
*CAP 4922 Data Science Capstone Project - March 11, 2026*