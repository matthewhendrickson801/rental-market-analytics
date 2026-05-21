import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

def create_bivariate_analysis():
    """Create bivariate analysis to identify rental market mismatches"""
    
    # Load the data
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Bivariate Analysis: Identifying Rental Market Mismatches', fontsize=16, fontweight='bold')
    
    rent = df['Median Home Rent (2020-2024)']
    
    # 1. Rent vs Median Household Income - Income-Rent Mismatch Detection
    income = df['Median Household Income (2020-2024)'].dropna()
    rent_income = df[df['Median Household Income (2020-2024)'].notna()]
    
    scatter1 = axes[0, 0].scatter(rent_income['Median Household Income (2020-2024)'], 
                                  rent_income['Median Home Rent (2020-2024)'], 
                                  alpha=0.6, c=range(len(rent_income)), cmap='viridis')
    
    # Add trend line
    z = np.polyfit(rent_income['Median Household Income (2020-2024)'], 
                   rent_income['Median Home Rent (2020-2024)'], 1)
    p = np.poly1d(z)
    axes[0, 0].plot(rent_income['Median Household Income (2020-2024)'], 
                    p(rent_income['Median Household Income (2020-2024)']), "r--", alpha=0.8)
    
    axes[0, 0].set_xlabel('Median Household Income ($)')
    axes[0, 0].set_ylabel('Median Home Rent ($)')
    axes[0, 0].set_title('Rent vs Income - Mismatch Detection')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Calculate correlation
    corr_income = rent_income['Median Home Rent (2020-2024)'].corr(rent_income['Median Household Income (2020-2024)'])
    axes[0, 0].text(0.05, 0.95, f'Correlation: {corr_income:.3f}', transform=axes[0, 0].transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
    
    # 2. Rent vs Commute Time - Transit Hypothesis Testing
    commute_data = df[df['Commute Mean Travel Time (2020-2024)'].notna()]
    
    scatter2 = axes[0, 1].scatter(commute_data['Commute Mean Travel Time (2020-2024)'], 
                                  commute_data['Median Home Rent (2020-2024)'], 
                                  alpha=0.6, c=range(len(commute_data)), cmap='plasma')
    
    # Add trend line
    z2 = np.polyfit(commute_data['Commute Mean Travel Time (2020-2024)'], 
                    commute_data['Median Home Rent (2020-2024)'], 1)
    p2 = np.poly1d(z2)
    axes[0, 1].plot(commute_data['Commute Mean Travel Time (2020-2024)'], 
                    p2(commute_data['Commute Mean Travel Time (2020-2024)']), "r--", alpha=0.8)
    
    axes[0, 1].set_xlabel('Commute Mean Travel Time (minutes)')
    axes[0, 1].set_ylabel('Median Home Rent ($)')
    axes[0, 1].set_title('Rent vs Commute Time - Transit Impact Analysis')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Calculate correlation
    corr_commute = commute_data['Median Home Rent (2020-2024)'].corr(commute_data['Commute Mean Travel Time (2020-2024)'])
    axes[0, 1].text(0.05, 0.95, f'Correlation: {corr_commute:.3f}', transform=axes[0, 1].transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
    
    # 3. Rent vs Population Density - Density-Price Mismatch
    pop_data = df[df['Total Population (2020-2024)'].notna()]
    
    scatter3 = axes[1, 0].scatter(pop_data['Total Population (2020-2024)'], 
                                  pop_data['Median Home Rent (2020-2024)'], 
                                  alpha=0.6, c=range(len(pop_data)), cmap='coolwarm')
    
    axes[1, 0].set_xlabel('Total Population')
    axes[1, 0].set_ylabel('Median Home Rent ($)')
    axes[1, 0].set_title('Rent vs Population - Density Mismatch Detection')
    axes[1, 0].set_xscale('log')  # Log scale for better visualization
    axes[1, 0].grid(True, alpha=0.3)
    
    # Calculate correlation
    corr_pop = pop_data['Median Home Rent (2020-2024)'].corr(pop_data['Total Population (2020-2024)'])
    axes[1, 0].text(0.05, 0.95, f'Correlation: {corr_pop:.3f}', transform=axes[1, 0].transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
    
    # 4. Rent vs Unemployment Rate - Economic Mismatch
    unemp_data = df[df['Unemployment Rate (2020-2024)'].notna()]
    
    scatter4 = axes[1, 1].scatter(unemp_data['Unemployment Rate (2020-2024)'], 
                                  unemp_data['Median Home Rent (2020-2024)'], 
                                  alpha=0.6, c=range(len(unemp_data)), cmap='RdYlBu')
    
    # Add trend line
    z4 = np.polyfit(unemp_data['Unemployment Rate (2020-2024)'], 
                    unemp_data['Median Home Rent (2020-2024)'], 1)
    p4 = np.poly1d(z4)
    axes[1, 1].plot(unemp_data['Unemployment Rate (2020-2024)'], 
                    p4(unemp_data['Unemployment Rate (2020-2024)']), "r--", alpha=0.8)
    
    axes[1, 1].set_xlabel('Unemployment Rate (%)')
    axes[1, 1].set_ylabel('Median Home Rent ($)')
    axes[1, 1].set_title('Rent vs Unemployment - Economic Mismatch Detection')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Calculate correlation
    corr_unemp = unemp_data['Median Home Rent (2020-2024)'].corr(unemp_data['Unemployment Rate (2020-2024)'])
    axes[1, 1].text(0.05, 0.95, f'Correlation: {corr_unemp:.3f}', transform=axes[1, 1].transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('bivariate_mismatch_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Identify specific mismatches
    print("="*70)
    print("BIVARIATE MISMATCH ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\nCORRELATION ANALYSIS:")
    print(f"Rent vs Income: {corr_income:.3f} ({'Strong' if abs(corr_income) > 0.7 else 'Moderate' if abs(corr_income) > 0.3 else 'Weak'} correlation)")
    print(f"Rent vs Commute Time: {corr_commute:.3f} ({'Strong' if abs(corr_commute) > 0.7 else 'Moderate' if abs(corr_commute) > 0.3 else 'Weak'} correlation)")
    print(f"Rent vs Population: {corr_pop:.3f} ({'Strong' if abs(corr_pop) > 0.7 else 'Moderate' if abs(corr_pop) > 0.3 else 'Weak'} correlation)")
    print(f"Rent vs Unemployment: {corr_unemp:.3f} ({'Strong' if abs(corr_unemp) > 0.7 else 'Moderate' if abs(corr_unemp) > 0.3 else 'Weak'} correlation)")
    
    # Identify income-rent mismatches
    print(f"\nINCOME-RENT MISMATCH DETECTION:")
    
    # Calculate residuals from income-rent relationship
    predicted_rent = p(rent_income['Median Household Income (2020-2024)'])
    residuals = rent_income['Median Home Rent (2020-2024)'] - predicted_rent
    
    # Find extreme mismatches (high residuals)
    high_rent_mismatch = rent_income[residuals > residuals.quantile(0.95)]
    low_rent_mismatch = rent_income[residuals < residuals.quantile(0.05)]
    
    print(f"High-rent mismatches (rent higher than income suggests): {len(high_rent_mismatch)} zip codes")
    print(f"Low-rent mismatches (rent lower than income suggests): {len(low_rent_mismatch)} zip codes")
    
    if len(high_rent_mismatch) > 0:
        print(f"\nTop 5 HIGH-RENT mismatches:")
        top_high = high_rent_mismatch.nlargest(5, 'Median Home Rent (2020-2024)')
        for _, row in top_high.iterrows():
            print(f"  ZIP {row['geoid']} ({row['city']}): Rent ${row['Median Home Rent (2020-2024)']:,.0f}, Income ${row['Median Household Income (2020-2024)']:,.0f}")
    
    if len(low_rent_mismatch) > 0:
        print(f"\nTop 5 LOW-RENT mismatches:")
        top_low = low_rent_mismatch.nsmallest(5, 'Median Home Rent (2020-2024)')
        for _, row in top_low.iterrows():
            print(f"  ZIP {row['geoid']} ({row['city']}): Rent ${row['Median Home Rent (2020-2024)']:,.0f}, Income ${row['Median Household Income (2020-2024)']:,.0f}")
    
    # Commute time analysis
    print(f"\nCOMMUTE TIME ANALYSIS:")
    if corr_commute > 0:
        print("Positive correlation suggests longer commutes = higher rents (accessibility premium)")
    else:
        print("Negative correlation suggests longer commutes = lower rents (distance penalty)")
    
    # Extreme commute cases
    long_commute_high_rent = commute_data[
        (commute_data['Commute Mean Travel Time (2020-2024)'] > commute_data['Commute Mean Travel Time (2020-2024)'].quantile(0.9)) &
        (commute_data['Median Home Rent (2020-2024)'] > commute_data['Median Home Rent (2020-2024)'].quantile(0.9))
    ]
    
    if len(long_commute_high_rent) > 0:
        print(f"\nLong commute + High rent mismatches: {len(long_commute_high_rent)} zip codes")
        print("Top 3 cases:")
        for _, row in long_commute_high_rent.head(3).iterrows():
            print(f"  ZIP {row['geoid']} ({row['city']}): Rent ${row['Median Home Rent (2020-2024)']:,.0f}, Commute {row['Commute Mean Travel Time (2020-2024)']:.1f} min")
    
    return df, high_rent_mismatch, low_rent_mismatch, long_commute_high_rent

if __name__ == "__main__":
    df, high_mismatches, low_mismatches, commute_mismatches = create_bivariate_analysis()