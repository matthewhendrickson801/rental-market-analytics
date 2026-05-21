import pandas as pd
import numpy as np

def create_rent_waste_index():
    """Create Rent Waste Index - high rent + long commute = wasted money"""
    
    # Load the enhanced dataset
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
    
    # Method 1: Simple Rent Waste = Rent * Commute Time
    print(f"\n1. BASIC RENT WASTE CALCULATION")
    print("-" * 40)
    
    # Normalize both variables to 0-1 scale for fair combination
    rent_normalized = (rent - rent.min()) / (rent.max() - rent.min())
    commute_normalized = (commute_time - commute_time.min()) / (commute_time.max() - commute_time.min())
    
    # Basic Rent Waste: Higher rent + Longer commute = More waste
    df['Basic_Rent_Waste'] = rent_normalized * commute_normalized * 100
    
    print(f"Basic Rent Waste Index (0-100):")
    print(f"  Range: {df['Basic_Rent_Waste'].min():.1f} - {df['Basic_Rent_Waste'].max():.1f}")
    print(f"  Mean: {df['Basic_Rent_Waste'].mean():.1f}")
    
    # Method 2: Rent Per Commute Minute ($/minute of daily commute)
    print(f"\n2. RENT PER COMMUTE MINUTE")
    print("-" * 40)
    
    # Calculate monthly cost per minute of daily commute
    # Assuming 22 working days per month, 2 trips per day
    monthly_commute_minutes = commute_time * 22 * 2
    df['Rent_Per_Commute_Minute'] = rent / monthly_commute_minutes
    
    print(f"Rent Per Commute Minute ($/minute):")
    print(f"  Range: ${df['Rent_Per_Commute_Minute'].min():.2f} - ${df['Rent_Per_Commute_Minute'].max():.2f}")
    print(f"  Mean: ${df['Rent_Per_Commute_Minute'].mean():.2f}")
    
    # Method 3: Advanced Rent Waste Index (considers efficiency)
    print(f"\n3. ADVANCED RENT WASTE INDEX")
    print("-" * 40)
    
    # Calculate "efficient" rent based on commute time
    # Assumption: Shorter commutes should command premium, longer commutes should be cheaper
    
    # Invert commute time (shorter commute = higher efficiency score)
    max_commute = commute_time.max()
    commute_efficiency = (max_commute - commute_time) / max_commute
    
    # Expected rent based on commute efficiency (shorter commute = higher expected rent)
    min_rent, max_rent = rent.min(), rent.max()
    expected_rent_from_commute = min_rent + (commute_efficiency * (max_rent - min_rent))
    
    # Rent Waste = Actual rent - Expected rent based on commute
    # Positive = paying too much for the commute you get
    # Negative = getting good value (short commute for the rent)
    df['Commute_Rent_Mismatch'] = rent - expected_rent_from_commute
    
    print(f"Commute-Rent Mismatch ($):")
    print(f"  Range: ${df['Commute_Rent_Mismatch'].min():,.0f} - ${df['Commute_Rent_Mismatch'].max():,.0f}")
    print(f"  Mean: ${df['Commute_Rent_Mismatch'].mean():.0f}")
    
    # Method 4: Comprehensive Rent Waste Score
    print(f"\n4. COMPREHENSIVE RENT WASTE SCORE")
    print("-" * 40)
    
    # Combine multiple factors:
    # 1. High rent penalty
    # 2. Long commute penalty  
    # 3. Rent-commute mismatch penalty
    
    # Standardize components
    rent_percentile = rent.rank(pct=True)  # 0-1, higher = more expensive
    commute_percentile = commute_time.rank(pct=True)  # 0-1, higher = longer commute
    mismatch_percentile = df['Commute_Rent_Mismatch'].rank(pct=True)  # 0-1, higher = worse mismatch
    
    # Comprehensive Rent Waste Score (0-100, higher = more waste)
    df['Comprehensive_Rent_Waste_Score'] = (
        rent_percentile * 0.4 +           # 40% weight on high rent
        commute_percentile * 0.35 +       # 35% weight on long commute
        mismatch_percentile * 0.25        # 25% weight on mismatch
    ) * 100
    
    print(f"Comprehensive Rent Waste Score (0-100):")
    print(f"  Range: {df['Comprehensive_Rent_Waste_Score'].min():.1f} - {df['Comprehensive_Rent_Waste_Score'].max():.1f}")
    print(f"  Mean: {df['Comprehensive_Rent_Waste_Score'].mean():.1f}")
    
    # Method 5: Time-Value Rent Waste (Economic approach)
    print(f"\n5. TIME-VALUE RENT WASTE")
    print("-" * 40)
    
    # Calculate the economic cost of commute time
    # Assume $25/hour value of time (conservative estimate)
    hourly_time_value = 25
    monthly_commute_hours = (commute_time * 22 * 2) / 60  # Convert to hours
    monthly_time_cost = monthly_commute_hours * hourly_time_value
    
    # Total monthly location cost = Rent + Time cost
    df['Total_Monthly_Location_Cost'] = rent + monthly_time_cost
    
    # Rent waste = How much extra you pay compared to shortest commute areas
    min_total_cost = df['Total_Monthly_Location_Cost'].min()
    df['Time_Value_Rent_Waste'] = df['Total_Monthly_Location_Cost'] - min_total_cost
    
    print(f"Time-Value Rent Waste ($):")
    print(f"  Range: ${df['Time_Value_Rent_Waste'].min():.0f} - ${df['Time_Value_Rent_Waste'].max():.0f}")
    print(f"  Mean: ${df['Time_Value_Rent_Waste'].mean():.0f}")
    print(f"  Monthly commute time cost range: ${monthly_time_cost.min():.0f} - ${monthly_time_cost.max():.0f}")
    
    # Identify the worst rent waste areas
    print(f"\n" + "="*80)
    print("TOP 15 RENT WASTE AREAS (Worst Value for Money)")
    print("="*80)
    
    # Sort by comprehensive rent waste score
    worst_waste = df.nlargest(15, 'Comprehensive_Rent_Waste_Score')
    
    for i, (_, row) in enumerate(worst_waste.iterrows(), 1):
        rent_val = row['Median Home Rent (2020-2024)']
        commute_val = row['Commute Mean Travel Time (2020-2024)']
        waste_score = row['Comprehensive_Rent_Waste_Score']
        time_waste = row['Time_Value_Rent_Waste']
        
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']})")
        print(f"    Rent: ${rent_val:,.0f} | Commute: {commute_val:.1f} min")
        print(f"    Waste Score: {waste_score:.1f}/100 | Monthly waste: ${time_waste:.0f}")
        print(f"    Problem: Paying ${rent_val:,.0f} rent for {commute_val:.1f} min commute")
        print()
    
    # Identify the best value areas (low waste)
    print(f"TOP 10 BEST VALUE AREAS (Efficient Rent-Commute Balance)")
    print("="*60)
    
    best_value = df.nsmallest(10, 'Comprehensive_Rent_Waste_Score')
    
    for i, (_, row) in enumerate(best_value.iterrows(), 1):
        rent_val = row['Median Home Rent (2020-2024)']
        commute_val = row['Commute Mean Travel Time (2020-2024)']
        waste_score = row['Comprehensive_Rent_Waste_Score']
        
        print(f"{i:2d}. ZIP {row['geoid']} ({row['city']})")
        print(f"    Rent: ${rent_val:,.0f} | Commute: {commute_val:.1f} min | Waste: {waste_score:.1f}")
    
    # City-level analysis
    print(f"\n" + "="*80)
    print("RENT WASTE BY CITY (Average Scores)")
    print("="*80)
    
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
    
    print(f"\nDataset saved with 5 new Rent Waste indicators:")
    print(f"  1. Basic_Rent_Waste (0-100 scale)")
    print(f"  2. Rent_Per_Commute_Minute ($/minute)")
    print(f"  3. Commute_Rent_Mismatch ($)")
    print(f"  4. Comprehensive_Rent_Waste_Score (0-100 scale)")
    print(f"  5. Time_Value_Rent_Waste ($)")
    
    return df

if __name__ == "__main__":
    enhanced_df = create_rent_waste_index()