import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def find_deep_insights():
    """Find surprising correlations that reveal hidden patterns"""
    
    # Load the data
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    print("="*80)
    print("DEEP INSIGHTS: SURPRISING CORRELATIONS ANALYSIS")
    print("="*80)
    
    # Calculate correlation matrix for all numeric variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != 'geoid']  # Remove ID column
    
    corr_matrix = df[numeric_cols].corr()
    
    # Focus on rent correlations first
    rent_corrs = corr_matrix['Median Home Rent (2020-2024)'].sort_values(key=abs, ascending=False)
    
    print("PART 1: 5 SURPRISING RENT CORRELATIONS")
    print("="*50)
    
    # Skip the self-correlation (1.0) and find interesting ones
    rent_insights = []
    
    for var, corr in rent_corrs.items():
        if var != 'Median Home Rent (2020-2024)' and abs(corr) > 0.1:  # Skip weak correlations
            rent_insights.append((var, corr))
    
    # Analyze the most surprising rent correlations
    surprising_rent = [
        ('Housing Built 1939 or Earlier (2020-2024)', rent_corrs.get('Housing Built 1939 or Earlier (2020-2024)', 0)),
        ('Housing Built 2020 or Later (2020-2024)', rent_corrs.get('Housing Built 2020 or Later (2020-2024)', 0)),
        ('Rental Vacancy Rate (2020-2024)', rent_corrs.get('Rental Vacancy Rate (2020-2024)', 0)),
        ('No Vehicles Available (2020-2024)', rent_corrs.get('No Vehicles Available (2020-2024)', 0)),
        ('Income 200% and Over the Poverty Level (2020-2024)', rent_corrs.get('Income 200% and Over the Poverty Level (2020-2024)', 0))
    ]
    
    for i, (var, corr) in enumerate(surprising_rent, 1):
        print(f"\n{i}. {var}")
        print(f"   Correlation with Rent: {corr:.3f}")
        
        # Provide insight interpretation
        if 'Housing Built 1939' in var:
            if corr > 0:
                print(f"   💡 INSIGHT: Older housing (pre-1940) correlates with HIGHER rent!")
                print(f"      This suggests historic/character neighborhoods command premium pricing.")
            else:
                print(f"   💡 INSIGHT: Older housing (pre-1940) correlates with LOWER rent.")
                print(f"      This suggests aging infrastructure reduces rental value.")
        
        elif 'Housing Built 2020' in var:
            if corr > 0:
                print(f"   💡 INSIGHT: Brand new housing correlates with HIGHER rent.")
                print(f"      New construction commands premium in rental market.")
            else:
                print(f"   💡 INSIGHT: Surprisingly, new housing correlates with LOWER rent!")
                print(f"      New developments may be in emerging/cheaper areas.")
        
        elif 'Rental Vacancy' in var:
            if corr > 0:
                print(f"   💡 INSIGHT: Higher vacancy rates correlate with HIGHER rent!")
                print(f"      Counterintuitive - suggests luxury markets have higher turnover.")
            else:
                print(f"   💡 INSIGHT: Higher vacancy rates correlate with LOWER rent.")
                print(f"      Expected - oversupply drives down rental prices.")
        
        elif 'No Vehicles' in var:
            if corr > 0:
                print(f"   💡 INSIGHT: More car-free households correlate with HIGHER rent!")
                print(f"      Urban, walkable areas command premium despite car dependency.")
            else:
                print(f"   💡 INSIGHT: More car-free households correlate with LOWER rent.")
                print(f"      Car-free areas may lack accessibility/amenities.")
        
        elif 'Income 200%' in var:
            if corr > 0:
                print(f"   💡 INSIGHT: Wealthy populations correlate with HIGHER rent.")
                print(f"      Expected - affluent areas drive up rental demand.")
    
    print(f"\n" + "="*80)
    print("PART 2: 5 SURPRISING NON-RENT CORRELATIONS")
    print("="*50)
    
    # Find surprising correlations between other variables
    surprising_pairs = []
    
    # Look for unexpected relationships
    variables_of_interest = [
        'Housing Built 1939 or Earlier (2020-2024)',
        'Housing Built 2020 or Later (2020-2024)',
        'Commute Transportation by Public Transit (2020-2024)',
        'No Vehicles Available (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Rental Vacancy Rate (2020-2024)',
        'Total Population (2020-2024)',
        'Labor Force Participation Rate (2020-2024)'
    ]
    
    # Calculate specific surprising correlations
    insights = []
    
    # 1. Old housing vs Public Transit
    if all(var in df.columns for var in ['Housing Built 1939 or Earlier (2020-2024)', 'Commute Transportation by Public Transit (2020-2024)']):
        corr1 = df['Housing Built 1939 or Earlier (2020-2024)'].corr(df['Commute Transportation by Public Transit (2020-2024)'])
        insights.append(('Old Housing vs Public Transit Use', corr1, 
                        "Historic neighborhoods and transit usage relationship"))
    
    # 2. New housing vs Car ownership
    if all(var in df.columns for var in ['Housing Built 2020 or Later (2020-2024)', 'No Vehicles Available (2020-2024)']):
        corr2 = df['Housing Built 2020 or Later (2020-2024)'].corr(df['No Vehicles Available (2020-2024)'])
        insights.append(('New Housing vs Car-Free Living', corr2,
                        "New developments and car dependency patterns"))
    
    # 3. Vacancy vs Unemployment
    if all(var in df.columns for var in ['Rental Vacancy Rate (2020-2024)', 'Unemployment Rate (2020-2024)']):
        corr3 = df['Rental Vacancy Rate (2020-2024)'].corr(df['Unemployment Rate (2020-2024)'])
        insights.append(('Rental Vacancy vs Unemployment', corr3,
                        "Housing market and economic distress relationship"))
    
    # 4. Population vs Labor Force Participation
    if all(var in df.columns for var in ['Total Population (2020-2024)', 'Labor Force Participation Rate (2020-2024)']):
        corr4 = df['Total Population (2020-2024)'].corr(df['Labor Force Participation Rate (2020-2024)'])
        insights.append(('Population Size vs Work Participation', corr4,
                        "Urban density and employment engagement"))
    
    # 5. Income vs Public Transit (counterintuitive)
    if all(var in df.columns for var in ['Per Capita Income (2020-2024)', 'Commute Transportation by Public Transit (2020-2024)']):
        corr5 = df['Per Capita Income (2020-2024)'].corr(df['Commute Transportation by Public Transit (2020-2024)'])
        insights.append(('Income vs Public Transit Use', corr5,
                        "Wealth and transportation choice patterns"))
    
    # Display the insights
    for i, (relationship, corr, description) in enumerate(insights, 1):
        print(f"\n{i}. {relationship}")
        print(f"   Correlation: {corr:.3f}")
        print(f"   Context: {description}")
        
        # Provide deep insight
        if 'Old Housing vs Public Transit' in relationship:
            if corr > 0.2:
                print(f"   💡 DEEP INSIGHT: Historic neighborhoods have MORE public transit!")
                print(f"      Cities built before cars have better transit infrastructure.")
            elif corr < -0.2:
                print(f"   💡 DEEP INSIGHT: Historic neighborhoods have LESS public transit!")
                print(f"      Old areas may lack modern transit investment.")
            else:
                print(f"   💡 DEEP INSIGHT: Housing age doesn't predict transit access.")
        
        elif 'New Housing vs Car-Free' in relationship:
            if corr > 0.2:
                print(f"   💡 DEEP INSIGHT: New developments are more car-free friendly!")
                print(f"      Modern planning emphasizes walkability and transit.")
            elif corr < -0.2:
                print(f"   💡 DEEP INSIGHT: New developments increase car dependency!")
                print(f"      Suburban sprawl pattern in new construction.")
        
        elif 'Vacancy vs Unemployment' in relationship:
            if corr > 0.3:
                print(f"   💡 DEEP INSIGHT: High unemployment = high rental vacancy!")
                print(f"      Economic distress directly impacts housing demand.")
            elif corr < -0.1:
                print(f"   💡 DEEP INSIGHT: High unemployment = low rental vacancy!")
                print(f"      Economic stress forces people into cheaper rentals.")
        
        elif 'Population Size vs Work' in relationship:
            if corr > 0.1:
                print(f"   💡 DEEP INSIGHT: Larger populations = higher work participation!")
                print(f"      Urban areas provide more employment opportunities.")
            elif corr < -0.1:
                print(f"   💡 DEEP INSIGHT: Larger populations = lower work participation!")
                print(f"      Urban areas may have more retirees/students.")
        
        elif 'Income vs Public Transit' in relationship:
            if corr > 0.2:
                print(f"   💡 DEEP INSIGHT: Wealthier people use MORE public transit!")
                print(f"      High-income urban professionals choose transit over cars.")
            elif corr < -0.2:
                print(f"   💡 DEEP INSIGHT: Wealthier people use LESS public transit!")
                print(f"      Income enables car ownership and private transportation.")
    
    # Create visualization of key insights
    create_insights_visualization(df, insights)
    
    return insights

def create_insights_visualization(df, insights):
    """Create visualization of the most surprising correlations"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Deep Insights: Surprising Data Correlations', fontsize=16, fontweight='bold')
    
    # Plot rent correlations
    rent_vars = [
        'Housing Built 1939 or Earlier (2020-2024)',
        'Rental Vacancy Rate (2020-2024)',
        'No Vehicles Available (2020-2024)'
    ]
    
    for i, var in enumerate(rent_vars):
        if var in df.columns:
            axes[0, i].scatter(df[var], df['Median Home Rent (2020-2024)'], alpha=0.6)
            axes[0, i].set_xlabel(var.replace(' (2020-2024)', ''))
            axes[0, i].set_ylabel('Median Rent ($)')
            
            corr = df[var].corr(df['Median Home Rent (2020-2024)'])
            axes[0, i].set_title(f'Correlation: {corr:.3f}')
            axes[0, i].grid(True, alpha=0.3)
    
    # Plot other surprising correlations
    if len(insights) >= 3:
        # This would need specific variable pairs from insights
        pass
    
    plt.tight_layout()
    plt.savefig('deep_insights_correlations.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    insights = find_deep_insights()