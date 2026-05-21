"""
Best and Worst Deals Analysis by Region
Shows top underpriced and overpriced ZIP codes in each region
"""

import pandas as pd

print("=" * 80)
print("BEST & WORST DEALS BY REGION")
print("=" * 80)

# Load dashboard data with predictions
df = pd.read_csv('dashboard/data/dashboard_data.csv')

# Add region mapping
region_mapping = {
    'Columbus': 'Midwest', 'Indianapolis': 'Midwest', 'Louisville': 'Midwest',
    'Charlotte': 'South', 'Nashville': 'South', 'Jacksonville': 'South',
    'SanAntonio': 'South', 'Tampa': 'South', 'Orlando': 'South',
    'Austin': 'HighCost', 'Denver': 'HighCost', 'Miami': 'HighCost',
    'SanFrancisco': 'HighCost', 'Philadelphia': 'HighCost'
}
df['region'] = df['city'].map(region_mapping)

print(f"\n📊 Dataset: {len(df)} ZIP codes across {df['city'].nunique()} cities")
print(f"   Regions: {df['region'].nunique()}")
print(f"   Model R²: 0.739 (XGBoost with 38 features)")

# Define regions
regions = ['Midwest', 'South', 'HighCost']

for region in regions:
    print("\n" + "=" * 80)
    print(f"REGION: {region.upper()}")
    print("=" * 80)
    
    region_df = df[df['region'] == region].copy()
    print(f"\n📍 {len(region_df)} ZIP codes in {region}")
    
    # Sort by discrepancy percentage (negative = underpriced, positive = overpriced)
    region_df = region_df.sort_values('rent_discrepancy_pct')
    
    # Top 10 BEST DEALS (most underpriced)
    print(f"\n🟢 TOP 10 BEST DEALS (Underpriced):")
    print("-" * 80)
    best_deals = region_df.head(10)
    
    for idx, row in best_deals.iterrows():
        print(f"\n{row['geoid']} ({row['city']})")
        print(f"   Actual Rent:    ${row['actual_rent']:>6,.0f}")
        print(f"   Predicted Rent: ${row['predicted_rent']:>6,.0f}")
        print(f"   Discrepancy:    ${row['rent_discrepancy_dollars']:>6,.0f} ({row['rent_discrepancy_pct']:>5.1f}%)")
        print(f"   Median Income:  ${row['median_income']:>6,.0f}")
        print(f"   Poverty Rate:   {row['poverty_rate']:>5.1f}%")
    
    # Top 10 WORST DEALS (most overpriced)
    print(f"\n\n🔴 TOP 10 WORST DEALS (Overpriced):")
    print("-" * 80)
    worst_deals = region_df.tail(10).iloc[::-1]  # Reverse to show highest first
    
    for idx, row in worst_deals.iterrows():
        print(f"\n{row['geoid']} ({row['city']})")
        print(f"   Actual Rent:    ${row['actual_rent']:>6,.0f}")
        print(f"   Predicted Rent: ${row['predicted_rent']:>6,.0f}")
        print(f"   Discrepancy:    ${row['rent_discrepancy_dollars']:>6,.0f} ({row['rent_discrepancy_pct']:>5.1f}%)")
        print(f"   Median Income:  ${row['median_income']:>6,.0f}")
        print(f"   Poverty Rate:   {row['poverty_rate']:>5.1f}%")

# Overall summary
print("\n\n" + "=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)

print(f"\n📊 Model Performance:")
print(f"   Median Absolute Error: {abs(df['rent_discrepancy_pct']).median():.1f}%")
print(f"   Mean Absolute Error: {abs(df['rent_discrepancy_pct']).mean():.1f}%")

print(f"\n🟢 Best Deal Overall:")
best_overall = df.loc[df['rent_discrepancy_pct'].idxmin()]
print(f"   {best_overall['geoid']} ({best_overall['city']}, {best_overall['region']})")
print(f"   Actual: ${best_overall['actual_rent']:,.0f}, Predicted: ${best_overall['predicted_rent']:,.0f}")
print(f"   Underpriced by ${abs(best_overall['rent_discrepancy_dollars']):,.0f} ({abs(best_overall['rent_discrepancy_pct']):.1f}%)")

print(f"\n🔴 Worst Deal Overall:")
worst_overall = df.loc[df['rent_discrepancy_pct'].idxmax()]
print(f"   {worst_overall['geoid']} ({worst_overall['city']}, {worst_overall['region']})")
print(f"   Actual: ${worst_overall['actual_rent']:,.0f}, Predicted: ${worst_overall['predicted_rent']:,.0f}")
print(f"   Overpriced by ${worst_overall['rent_discrepancy_dollars']:,.0f} ({worst_overall['rent_discrepancy_pct']:.1f}%)")

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE")
print("=" * 80)
print(f"\n🌐 Dashboard: http://localhost:8501")
print(f"📁 Data: dashboard/data/dashboard_data.csv")
