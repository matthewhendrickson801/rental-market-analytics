import pandas as pd
import numpy as np

def analyze_missing_rent_zipcodes():
    """Analyze zip codes with missing median home rent data to understand why"""
    
    # Load the data
    df = pd.read_csv("combined_city_data.csv")
    
    # Filter to zip codes with missing median home rent
    missing_rent = df[df['Median Home Rent (2020-2024)'].isnull()].copy()
    
    print("="*80)
    print("ANALYSIS OF ZIP CODES WITH MISSING MEDIAN HOME RENT DATA")
    print("="*80)
    print(f"Total zip codes with missing rent data: {len(missing_rent)}")
    print(f"Percentage of total dataset: {len(missing_rent)/len(df)*100:.1f}%")
    
    # Group by city to see distribution
    print(f"\nMissing rent data by city:")
    city_missing = missing_rent.groupby('city').size().sort_values(ascending=False)
    for city, count in city_missing.items():
        total_city_zips = len(df[df['city'] == city])
        pct = count/total_city_zips*100
        print(f"  {city:<15}: {count:>3} out of {total_city_zips:>3} zip codes ({pct:>5.1f}%)")
    
    # Analyze characteristics of missing rent zip codes
    print(f"\n" + "="*80)
    print("CHARACTERISTICS ANALYSIS OF MISSING RENT ZIP CODES")
    print("="*80)
    
    # Look at population characteristics
    print("\n1. POPULATION ANALYSIS:")
    pop_stats = missing_rent['Total Population (2020-2024)'].describe()
    print(f"Population statistics for missing rent zip codes:")
    print(f"  Mean population: {pop_stats['mean']:,.0f}")
    print(f"  Median population: {pop_stats['50%']:,.0f}")
    print(f"  Min population: {pop_stats['min']:,.0f}")
    print(f"  Max population: {pop_stats['max']:,.0f}")
    
    # Compare to overall population
    overall_pop = df['Total Population (2020-2024)'].describe()
    print(f"\nComparison to all zip codes:")
    print(f"  Overall mean population: {overall_pop['mean']:,.0f}")
    print(f"  Overall median population: {overall_pop['50%']:,.0f}")
    
    # Low population zip codes (likely rural/special use)
    low_pop_threshold = 1000
    low_pop_missing = missing_rent[missing_rent['Total Population (2020-2024)'] < low_pop_threshold]
    print(f"\nZip codes with missing rent AND population < {low_pop_threshold:,}:")
    print(f"  Count: {len(low_pop_missing)} ({len(low_pop_missing)/len(missing_rent)*100:.1f}% of missing rent zips)")
    
    # Look at housing units
    print(f"\n2. HOUSING UNITS ANALYSIS:")
    housing_stats = missing_rent['Total Housing Units (2020-2024)'].describe()
    print(f"Housing units statistics for missing rent zip codes:")
    print(f"  Mean housing units: {housing_stats['mean']:,.0f}")
    print(f"  Median housing units: {housing_stats['50%']:,.0f}")
    print(f"  Min housing units: {housing_stats['min']:,.0f}")
    print(f"  Max housing units: {housing_stats['max']:,.0f}")
    
    # Low housing units (likely commercial/industrial/special use)
    low_housing_threshold = 500
    low_housing_missing = missing_rent[missing_rent['Total Housing Units (2020-2024)'] < low_housing_threshold]
    print(f"\nZip codes with missing rent AND housing units < {low_housing_threshold:,}:")
    print(f"  Count: {len(low_housing_missing)} ({len(low_housing_missing)/len(missing_rent)*100:.1f}% of missing rent zips)")
    
    # Look at vacancy rates
    print(f"\n3. VACANCY RATE ANALYSIS:")
    rental_vacancy = missing_rent['Rental Vacancy Rate (2020-2024)']
    homeowner_vacancy = missing_rent['Homeowner Vacancy Rate (2020-2024)']
    
    print(f"Rental vacancy rate statistics:")
    print(f"  Mean: {rental_vacancy.mean():.2f}%")
    print(f"  Median: {rental_vacancy.median():.2f}%")
    print(f"  Max: {rental_vacancy.max():.2f}%")
    
    # High vacancy rates (might indicate special circumstances)
    high_vacancy = missing_rent[missing_rent['Rental Vacancy Rate (2020-2024)'] > 20]
    print(f"\nZip codes with missing rent AND rental vacancy > 20%:")
    print(f"  Count: {len(high_vacancy)} ({len(high_vacancy)/len(missing_rent)*100:.1f}% of missing rent zips)")
    
    # Create detailed analysis for each missing rent zip code
    print(f"\n" + "="*80)
    print("DETAILED ANALYSIS OF EACH MISSING RENT ZIP CODE")
    print("="*80)
    
    # Add analysis columns
    missing_rent['likely_reason'] = ''
    missing_rent['confidence'] = ''
    
    for idx, row in missing_rent.iterrows():
        zip_code = row['geoid']
        city = row['city']
        population = row['Total Population (2020-2024)']
        housing_units = row['Total Housing Units (2020-2024)']
        rental_vacancy = row['Rental Vacancy Rate (2020-2024)']
        homeowner_vacancy = row['Homeowner Vacancy Rate (2020-2024)']
        
        # Make educated guesses based on characteristics
        reasons = []
        confidence = "Medium"
        
        if population < 100:
            reasons.append("Very low population - likely industrial/commercial area")
            confidence = "High"
        elif population < 500:
            reasons.append("Low population - possibly rural or special use area")
            confidence = "High"
        
        if housing_units < 50:
            reasons.append("Very few housing units - likely commercial/industrial zone")
            confidence = "High"
        elif housing_units < 200:
            reasons.append("Limited housing - possibly mixed-use or institutional area")
        
        if rental_vacancy > 50:
            reasons.append("Extremely high rental vacancy - area in transition or special circumstances")
            confidence = "High"
        elif rental_vacancy > 20:
            reasons.append("High rental vacancy - economic distress or redevelopment")
        
        # Population to housing ratio analysis
        if housing_units > 0:
            people_per_unit = population / housing_units
            if people_per_unit < 1:
                reasons.append("Low occupancy rate - possible vacation homes or investment properties")
            elif people_per_unit > 4:
                reasons.append("High occupancy - possible group housing or institutional")
        
        # Income analysis
        median_income = row['Median Household Income (2020-2024)']
        if pd.notna(median_income):
            if median_income < 20000:
                reasons.append("Very low income area - possible institutional or transitional housing")
            elif median_income > 150000:
                reasons.append("High income area - possible luxury/custom housing market")
        
        # Combine reasons
        if not reasons:
            reasons.append("Insufficient rental market data - possibly owner-dominated area")
            confidence = "Low"
        
        missing_rent.at[idx, 'likely_reason'] = "; ".join(reasons)
        missing_rent.at[idx, 'confidence'] = confidence
    
    # Display results
    display_cols = ['city', 'geoid', 'Total Population (2020-2024)', 'Total Housing Units (2020-2024)', 
                   'Rental Vacancy Rate (2020-2024)', 'Median Household Income (2020-2024)', 
                   'likely_reason', 'confidence']
    
    result_df = missing_rent[display_cols].copy()
    result_df = result_df.sort_values(['city', 'geoid'])
    
    print(f"\nDetailed analysis of all {len(missing_rent)} zip codes with missing rent data:")
    print("-" * 120)
    
    for _, row in result_df.iterrows():
        print(f"\nZIP {row['geoid']} ({row['city']}):")
        print(f"  Population: {row['Total Population (2020-2024)']:,}")
        print(f"  Housing Units: {row['Total Housing Units (2020-2024)']:,}")
        print(f"  Rental Vacancy: {row['Rental Vacancy Rate (2020-2024)']:.1f}%")
        print(f"  Median Income: ${row['Median Household Income (2020-2024)']:,.0f}" if pd.notna(row['Median Household Income (2020-2024)']) else "  Median Income: Not Available")
        print(f"  Likely Reason: {row['likely_reason']}")
        print(f"  Confidence: {row['confidence']}")
    
    # Summary by reason categories
    print(f"\n" + "="*80)
    print("SUMMARY OF LIKELY REASONS FOR MISSING RENT DATA")
    print("="*80)
    
    reason_categories = {
        'Low Population/Rural': 0,
        'Commercial/Industrial': 0,
        'High Vacancy/Economic Distress': 0,
        'Owner-Dominated Market': 0,
        'Institutional/Special Use': 0,
        'Other/Unknown': 0
    }
    
    for _, row in missing_rent.iterrows():
        reason = row['likely_reason'].lower()
        if 'low population' in reason or 'rural' in reason:
            reason_categories['Low Population/Rural'] += 1
        elif 'commercial' in reason or 'industrial' in reason:
            reason_categories['Commercial/Industrial'] += 1
        elif 'vacancy' in reason or 'economic' in reason:
            reason_categories['High Vacancy/Economic Distress'] += 1
        elif 'owner-dominated' in reason or 'insufficient rental' in reason:
            reason_categories['Owner-Dominated Market'] += 1
        elif 'institutional' in reason or 'group housing' in reason:
            reason_categories['Institutional/Special Use'] += 1
        else:
            reason_categories['Other/Unknown'] += 1
    
    for category, count in reason_categories.items():
        if count > 0:
            pct = count/len(missing_rent)*100
            print(f"  {category:<30}: {count:>3} zip codes ({pct:>5.1f}%)")
    
    # Save detailed results
    result_df.to_csv('missing_rent_analysis.csv', index=False)
    print(f"\nDetailed analysis saved to 'missing_rent_analysis.csv'")
    
    return result_df

if __name__ == "__main__":
    analysis_df = analyze_missing_rent_zipcodes()