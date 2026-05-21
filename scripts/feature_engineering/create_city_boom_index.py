import pandas as pd
import numpy as np

def create_city_boom_index():
    """Create City Boom Index - identifies rapidly growing/developing areas"""
    
    # Load the enhanced dataset
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
    
    # Component 1: Population Growth Score (0-100)
    print(f"\n1. POPULATION GROWTH SCORE")
    print("-" * 40)
    
    # Convert population change to 0-100 scale (negative growth = 0, high growth = 100)
    pop_growth_normalized = np.clip(population_change, 0, None)  # Remove negative values
    if pop_growth_normalized.max() > 0:
        df['Population_Growth_Score'] = (pop_growth_normalized / pop_growth_normalized.max()) * 100
    else:
        df['Population_Growth_Score'] = 0
    
    print(f"Population Growth Score (0-100):")
    print(f"  Range: {df['Population_Growth_Score'].min():.1f} - {df['Population_Growth_Score'].max():.1f}")
    print(f"  Mean: {df['Population_Growth_Score'].mean():.1f}")
    
    # Component 2: New Development Score (0-100)
    print(f"\n2. NEW DEVELOPMENT SCORE")
    print("-" * 40)
    
    # Calculate percentage of housing built in last 15 years (2010+)
    recent_housing = new_housing_2010_2019 + new_housing_2020_later
    recent_housing_pct = (recent_housing / total_housing) * 100
    recent_housing_pct = recent_housing_pct.fillna(0)
    
    # Normalize to 0-100 scale
    if recent_housing_pct.max() > 0:
        df['New_Development_Score'] = (recent_housing_pct / recent_housing_pct.max()) * 100
    else:
        df['New_Development_Score'] = 0
    
    print(f"New Development Score (0-100):")
    print(f"  Range: {df['New_Development_Score'].min():.1f} - {df['New_Development_Score'].max():.1f}")
    print(f"  Mean: {df['New_Development_Score'].mean():.1f}")
    print(f"  Based on % housing built 2010+: {recent_housing_pct.min():.1f}% - {recent_housing_pct.max():.1f}%")
    
    # Component 3: Economic Vitality Score (0-100)
    print(f"\n3. ECONOMIC VITALITY SCORE")
    print("-" * 40)
    
    # Use rent-to-income ratio as proxy for economic demand
    # Higher rent relative to income suggests high demand/economic activity
    rent_income_ratio = rent / income
    rent_income_ratio = rent_income_ratio.fillna(rent_income_ratio.median())
    
    # Normalize to 0-100 (higher ratio = more economic pressure/demand)
    df['Economic_Vitality_Score'] = ((rent_income_ratio - rent_income_ratio.min()) / 
                                   (rent_income_ratio.max() - rent_income_ratio.min())) * 100
    
    print(f"Economic Vitality Score (0-100):")
    print(f"  Range: {df['Economic_Vitality_Score'].min():.1f} - {df['Economic_Vitality_Score'].max():.1f}")
    print(f"  Mean: {df['Economic_Vitality_Score'].mean():.1f}")
    print(f"  Based on rent/income ratio: {rent_income_ratio.min():.3f} - {rent_income_ratio.max():.3f}")
    
    # Component 4: Ultra-Recent Development Boost (0-50)
    print(f"\n4. ULTRA-RECENT DEVELOPMENT BOOST")
    print("-" * 40)
    
    # Extra points for housing built 2020 or later (very recent boom indicator)
    ultra_recent_pct = (new_housing_2020_later / total_housing) * 100
    ultra_recent_pct = ultra_recent_pct.fillna(0)
    
    if ultra_recent_pct.max() > 0:
        df['Ultra_Recent_Boost'] = (ultra_recent_pct / ultra_recent_pct.max()) * 50
    else:
        df['Ultra_Recent_Boost'] = 0
    
    print(f"Ultra-Recent Development Boost (0-50):")
    print(f"  Range: {df['Ultra_Recent_Boost'].min():.1f} - {df['Ultra_Recent_Boost'].max():.1f}")
    print(f"  Mean: {df['Ultra_Recent_Boost'].mean():.1f}")
    print(f"  Based on % housing built 2020+: {ultra_recent_pct.min():.1f}% - {ultra_recent_pct.max():.1f}%")
    
    # Component 5: Comprehensive City Boom Score (0-100)
    print(f"\n5. COMPREHENSIVE CITY BOOM SCORE")
    print("-" * 40)
    
    # Weighted combination of all boom indicators
    df['City_Boom_Score'] = (
        df['Population_Growth_Score'] * 0.35 +      # 35% weight on population growth
        df['New_Development_Score'] * 0.30 +        # 30% weight on new development
        df['Economic_Vitality_Score'] * 0.25 +      # 25% weight on economic vitality
        df['Ultra_Recent_Boost'] * 0.10             # 10% weight on ultra-recent development
    )
    
    # Ensure score stays within 0-100 range
    df['City_Boom_Score'] = np.clip(df['City_Boom_Score'], 0, 100)
    
    print(f"Comprehensive City Boom Score (0-100):")
    print(f"  Range: {df['City_Boom_Score'].min():.1f} - {df['City_Boom_Score'].max():.1f}")
    print(f"  Mean: {df['City_Boom_Score'].mean():.1f}")
    
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
    
    # Identify the top booming areas
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
        print(f"    Rent: ${row['Median Home Rent (2020-2024)']:,.0f} | Income: ${row['Median Household Income (2020-2024)']:,.0f}")
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
    
    # Boom category distribution
    print(f"\n" + "="*60)
    print("BOOM CATEGORY DISTRIBUTION")
    print("="*60)
    
    boom_dist = df['Boom_Category'].value_counts()
    total_zips = len(df)
    
    for category, count in boom_dist.items():
        pct = (count / total_zips) * 100
        print(f"{category:<15}: {count:>4} ZIP codes ({pct:>5.1f}%)")
    
    # Correlation with rent waste
    print(f"\n" + "="*60)
    print("BOOM vs RENT WASTE CORRELATION")
    print("="*60)
    
    boom_waste_corr = df['City_Boom_Score'].corr(df['Comprehensive_Rent_Waste_Score'])
    print(f"Correlation between City Boom and Rent Waste: {boom_waste_corr:.3f}")
    
    if boom_waste_corr > 0.3:
        print("INSIGHT: Booming areas tend to have higher rent waste (growth outpacing infrastructure)")
    elif boom_waste_corr < -0.3:
        print("INSIGHT: Booming areas tend to have lower rent waste (efficient development)")
    else:
        print("INSIGHT: Boom and rent waste are not strongly correlated")
    
    # Save enhanced dataset
    df.to_csv('final_dataset_with_boom_index.csv', index=False)
    
    print(f"\nDataset saved with 6 new City Boom indicators:")
    print(f"  1. Population_Growth_Score (0-100)")
    print(f"  2. New_Development_Score (0-100)")
    print(f"  3. Economic_Vitality_Score (0-100)")
    print(f"  4. Ultra_Recent_Boost (0-50)")
    print(f"  5. City_Boom_Score (0-100) - Comprehensive metric")
    print(f"  6. Boom_Category (MEGA BOOM to STABLE/DECLINE)")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_city_boom_index()