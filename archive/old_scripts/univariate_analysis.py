import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_univariate_analysis():
    """Create univariate analysis visualizations for median home rent"""
    
    # Load the data
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Univariate Analysis: Median Home Rent Distribution', fontsize=16, fontweight='bold')
    
    rent_data = df['Median Home Rent (2020-2024)']
    
    # 1. Histogram - Distribution Shape
    axes[0, 0].hist(rent_data, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].axvline(rent_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${rent_data.mean():.0f}')
    axes[0, 0].axvline(rent_data.median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${rent_data.median():.0f}')
    axes[0, 0].set_xlabel('Median Home Rent ($)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Rent Distribution - Identifying Extreme Values')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Box Plot - Outlier Detection
    box_plot = axes[0, 1].boxplot(rent_data, patch_artist=True)
    box_plot['boxes'][0].set_facecolor('lightcoral')
    axes[0, 1].set_ylabel('Median Home Rent ($)')
    axes[0, 1].set_title('Box Plot - Outlier Detection')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Add statistics text
    q1 = rent_data.quantile(0.25)
    q3 = rent_data.quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    
    stats_text = f'Q1: ${q1:.0f}\nQ3: ${q3:.0f}\nIQR: ${iqr:.0f}\nLower Fence: ${lower_fence:.0f}\nUpper Fence: ${upper_fence:.0f}'
    axes[0, 1].text(1.1, rent_data.median(), stats_text, transform=axes[0, 1].transData, 
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
    
    # 3. Rent by City - Box Plots
    city_order = df.groupby('city')['Median Home Rent (2020-2024)'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x='city', y='Median Home Rent (2020-2024)', order=city_order, ax=axes[1, 0])
    axes[1, 0].set_xticklabels(city_order, rotation=45, ha='right')
    axes[1, 0].set_xlabel('City')
    axes[1, 0].set_ylabel('Median Home Rent ($)')
    axes[1, 0].set_title('Rent Distribution by City - Identifying City-Level Mismatches')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Rent by City - Mean Values Bar Chart
    city_means = df.groupby('city')['Median Home Rent (2020-2024)'].mean().sort_values(ascending=False)
    bars = axes[1, 1].bar(range(len(city_means)), city_means.values, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[1, 1].set_xlabel('City')
    axes[1, 1].set_ylabel('Mean Rent ($)')
    axes[1, 1].set_title('Average Rent by City')
    axes[1, 1].set_xticks(range(len(city_means)))
    axes[1, 1].set_xticklabels(city_means.index, rotation=45, ha='right')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 20,
                        f'${height:.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('univariate_rent_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Generate detailed statistics for interpretation
    print("="*60)
    print("UNIVARIATE ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\nRENT DISTRIBUTION STATISTICS:")
    print(f"Mean: ${rent_data.mean():,.0f}")
    print(f"Median: ${rent_data.median():,.0f}")
    print(f"Standard Deviation: ${rent_data.std():,.0f}")
    print(f"Range: ${rent_data.min():,.0f} - ${rent_data.max():,.0f}")
    print(f"Coefficient of Variation: {rent_data.std()/rent_data.mean():.3f}")
    
    # Identify potential outliers
    outliers_low = rent_data[rent_data < lower_fence]
    outliers_high = rent_data[rent_data > upper_fence]
    
    print(f"\nOUTLIER ANALYSIS:")
    print(f"Lower fence: ${lower_fence:.0f}")
    print(f"Upper fence: ${upper_fence:.0f}")
    print(f"Low outliers: {len(outliers_low)} zip codes (rent < ${lower_fence:.0f})")
    print(f"High outliers: {len(outliers_high)} zip codes (rent > ${upper_fence:.0f})")
    
    if len(outliers_low) > 0:
        print(f"Lowest rents: ${outliers_low.min():.0f} - ${outliers_low.max():.0f}")
    if len(outliers_high) > 0:
        print(f"Highest rents: ${outliers_high.min():.0f} - ${outliers_high.max():.0f}")
    
    print(f"\nCITY-LEVEL ANALYSIS:")
    print("Cities ranked by median rent:")
    city_stats = df.groupby('city')['Median Home Rent (2020-2024)'].agg(['count', 'mean', 'median', 'std']).round(0)
    city_stats = city_stats.sort_values('median', ascending=False)
    
    for city, stats in city_stats.iterrows():
        print(f"{city:<15}: Median ${stats['median']:>4.0f}, Mean ${stats['mean']:>4.0f}, Std ${stats['std']:>3.0f} ({stats['count']:>3.0f} zips)")
    
    # Identify extreme cities
    highest_city = city_stats.index[0]
    lowest_city = city_stats.index[-1]
    
    print(f"\nEXTREME CITIES:")
    print(f"Highest rent city: {highest_city} (median: ${city_stats.loc[highest_city, 'median']:.0f})")
    print(f"Lowest rent city: {lowest_city} (median: ${city_stats.loc[lowest_city, 'median']:.0f})")
    print(f"City rent gap: ${city_stats.loc[highest_city, 'median'] - city_stats.loc[lowest_city, 'median']:.0f}")
    
    return df, outliers_low, outliers_high

if __name__ == "__main__":
    df, low_outliers, high_outliers = create_univariate_analysis()