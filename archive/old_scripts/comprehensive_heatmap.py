import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_comprehensive_heatmap():
    """Create comprehensive correlation heatmap for all variables"""
    
    # Load the data
    df = pd.read_csv('final_rent_dataset_complete_cases_only.csv')
    
    # Select numeric variables for correlation analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Remove ID columns and data source tracking
    exclude_cols = ['geoid', 'data_source']
    numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    print("="*80)
    print("COMPREHENSIVE CORRELATION HEATMAP ANALYSIS")
    print("="*80)
    print(f"Analyzing correlations between {len(numeric_cols)} variables")
    
    # Create the heatmap
    plt.figure(figsize=(20, 16))
    
    # Create mask for upper triangle to avoid redundancy
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Create custom colormap
    cmap = sns.diverging_palette(250, 10, as_cmap=True)
    
    # Create the heatmap
    heatmap = sns.heatmap(corr_matrix, 
                         mask=mask,
                         cmap=cmap, 
                         center=0,
                         square=True, 
                         linewidths=0.5,
                         cbar_kws={"shrink": 0.8},
                         annot=True,
                         fmt='.2f',
                         annot_kws={'size': 6})
    
    plt.title('Comprehensive Correlation Heatmap: All Variables\nIdentifying Rental Market Patterns and Mismatches', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig('comprehensive_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Analyze the most interesting correlations
    print(f"\nTOP CORRELATIONS ANALYSIS:")
    print("="*50)
    
    # Get all correlations in a flat format
    correlations = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            var1 = corr_matrix.columns[i]
            var2 = corr_matrix.columns[j]
            corr_val = corr_matrix.iloc[i, j]
            correlations.append((var1, var2, corr_val))
    
    # Sort by absolute correlation value
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print(f"\nTOP 10 STRONGEST CORRELATIONS:")
    print("-" * 70)
    
    for i, (var1, var2, corr) in enumerate(correlations[:10], 1):
        # Shorten variable names for display
        var1_short = var1.replace(' (2020-2024)', '').replace('Housing Built ', '')
        var2_short = var2.replace(' (2020-2024)', '').replace('Housing Built ', '')
        
        print(f"{i:2d}. {var1_short:<30} ↔ {var2_short:<30} | {corr:>6.3f}")
        
        # Add interpretation for surprising correlations
        if abs(corr) > 0.8:
            print(f"    🔥 VERY STRONG: {abs(corr):.1%} shared variance")
        elif abs(corr) > 0.5:
            print(f"    💪 STRONG: {abs(corr):.1%} shared variance")
    
    # Focus on rent-related correlations
    print(f"\nRENT-RELATED CORRELATIONS (sorted by strength):")
    print("-" * 70)
    
    rent_corrs = corr_matrix['Median Home Rent (2020-2024)'].sort_values(key=abs, ascending=False)
    
    for i, (var, corr) in enumerate(rent_corrs.items(), 1):
        if var != 'Median Home Rent (2020-2024)' and abs(corr) > 0.05:  # Skip weak correlations
            var_short = var.replace(' (2020-2024)', '').replace('Housing Built ', '')
            
            direction = "↗️" if corr > 0 else "↘️"
            strength = "🔥" if abs(corr) > 0.5 else "💪" if abs(corr) > 0.3 else "📊"
            
            print(f"{i:2d}. {var_short:<40} | {corr:>6.3f} {direction} {strength}")
            
            if i <= 15:  # Show top 15 rent correlations
                continue
            else:
                break
    
    # Identify surprising patterns
    print(f"\n" + "="*80)
    print("SURPRISING PATTERN DETECTION")
    print("="*80)
    
    surprising_patterns = []
    
    # Look for counterintuitive correlations
    for var1, var2, corr in correlations:
        # Housing age patterns
        if 'Housing Built 1939' in var1 and 'Housing Built 2020' in var2:
            if abs(corr) > 0.1:
                surprising_patterns.append((var1, var2, corr, "Old vs New Housing"))
        
        # Economic contradictions
        if 'Income' in var1 and 'Unemployment' in var2:
            if corr > -0.5:  # Should be strongly negative
                surprising_patterns.append((var1, var2, corr, "Income-Unemployment Paradox"))
        
        # Transit patterns
        if 'Transit' in var1 or 'Transit' in var2:
            if abs(corr) > 0.3:
                surprising_patterns.append((var1, var2, corr, "Transit Relationship"))
        
        # Vacancy patterns
        if 'Vacancy' in var1 and 'Rent' in var2:
            if corr > 0:  # Positive is counterintuitive
                surprising_patterns.append((var1, var2, corr, "Vacancy Paradox"))
    
    if surprising_patterns:
        print(f"\nSURPRISING PATTERNS FOUND:")
        for var1, var2, corr, pattern_type in surprising_patterns[:5]:
            var1_short = var1.replace(' (2020-2024)', '')
            var2_short = var2.replace(' (2020-2024)', '')
            print(f"• {pattern_type}: {var1_short} ↔ {var2_short} ({corr:.3f})")
    
    # Create focused rent heatmap
    create_rent_focused_heatmap(df, corr_matrix)
    
    return corr_matrix, correlations

def create_rent_focused_heatmap(df, full_corr_matrix):
    """Create a focused heatmap showing rent correlations"""
    
    # Select key variables for rent analysis
    rent_focus_vars = [
        'Median Home Rent (2020-2024)',
        'Median Household Income (2020-2024)',
        'Per Capita Income (2020-2024)',
        'Total Population (2020-2024)',
        'Total Housing Units (2020-2024)',
        'Housing Built 1939 or Earlier (2020-2024)',
        'Housing Built 2020 or Later (2020-2024)',
        'Rental Vacancy Rate (2020-2024)',
        'Homeowner Vacancy Rate (2020-2024)',
        'Unemployment Rate (2020-2024)',
        'Commute Mean Travel Time (2020-2024)',
        'Commute Transportation by Public Transit (2020-2024)',
        'No Vehicles Available (2020-2024)'
    ]
    
    # Filter to available variables
    available_vars = [var for var in rent_focus_vars if var in df.columns]
    
    # Create focused correlation matrix
    focused_corr = df[available_vars].corr()
    
    # Create the focused heatmap
    plt.figure(figsize=(12, 10))
    
    # Custom colormap for better contrast
    cmap = sns.diverging_palette(10, 250, as_cmap=True)
    
    sns.heatmap(focused_corr, 
                annot=True, 
                fmt='.3f',
                cmap=cmap,
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
                annot_kws={'size': 8})
    
    plt.title('Rent-Focused Correlation Analysis\nKey Variables for Rental Market Mismatch Detection', 
              fontsize=14, fontweight='bold')
    
    # Shorten labels
    labels = [label.replace(' (2020-2024)', '').replace('Housing Built ', '') for label in available_vars]
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.yticks(range(len(labels)), labels, rotation=0)
    
    plt.tight_layout()
    plt.savefig('rent_focused_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nRent-focused heatmap created with {len(available_vars)} key variables")

if __name__ == "__main__":
    corr_matrix, all_correlations = create_comprehensive_heatmap()