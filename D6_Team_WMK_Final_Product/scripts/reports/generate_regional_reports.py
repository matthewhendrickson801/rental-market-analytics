"""
Generate three regional reports:
1. Duval County (Jacksonville city proper)
2. Jacksonville Metro (all Jacksonville ZIPs)
3. Florida (Miami, Tampa, Orlando, Jacksonville)
"""

import pandas as pd
import numpy as np

# Load predictions
preds = pd.read_csv('d4_modeling/results/all_predictions.csv')

print("=" * 80)
print("GENERATING REGIONAL REPORTS")
print("=" * 80)

# ============================================================================
# REPORT 1: DUVAL COUNTY (Jacksonville City Proper)
# ============================================================================

print("\n[1/3] Duval County Report...")

# Jacksonville ZIPs are Duval County
duval = preds[preds['city'] == 'Jacksonville'].copy()
duval_sorted = duval.sort_values('residual', ascending=False)

report1 = []
report1.append("# Duval County Affordable Housing Analysis")
report1.append("## StateofJax - Model Predictions for Duval County")
report1.append("")
report1.append("---")
report1.append("")
report1.append("## Executive Summary")
report1.append("")
report1.append(f"**Total ZIP Codes Analyzed**: {len(duval)}")
report1.append(f"**Average Median Rent**: ${duval['actual_rent'].mean():.0f}")
report1.append(f"**Model Prediction Accuracy**: ±${duval['abs_residual'].mean():.0f} (MAE)")
report1.append(f"**Rent Range**: ${duval['actual_rent'].min():.0f} - ${duval['actual_rent'].max():.0f}")
report1.append("")
report1.append("### Key Findings")
report1.append("")
report1.append(f"- **{len(duval[duval['residual'] > 0])} ZIPs** identified as underpriced opportunities")
report1.append(f"- **{len(duval[duval['residual'] < 0])} ZIPs** identified as premium/overpriced")
report1.append(f"- **{len(duval[duval['beach_proximity'] >= 1])} ZIPs** with beach proximity (score ≥ 1.0)")
report1.append(f"- Average household income: ${duval['median_income'].mean():.0f}")
report1.append(f"- Average bachelor's degree attainment: {duval['bachelors_plus'].mean():.1f}%")
report1.append("")
report1.append("---")
report1.append("")
report1.append("## Top 10 Affordable Housing Opportunities")
report1.append("")
report1.append("These ZIP codes show the greatest potential for affordable housing investment:")
report1.append("")
report1.append("| Rank | ZIP | Actual Rent | Predicted Rent | Opportunity | Population | Education | Income | Type |")
report1.append("|------|-----|-------------|----------------|-------------|------------|-----------|--------|------|")

for i, (_, row) in enumerate(duval_sorted[duval_sorted['residual'] > 0].head(10).iterrows(), 1):
    report1.append(f"| {i} | {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | **+${row['residual']:.0f}** | {row['population']:.0f} | {row['bachelors_plus']:.1f}% | ${row['median_income']:.0f} | {row['urban_rural']} |")

report1.append("")
report1.append("---")
report1.append("")
report1.append("## All Duval County ZIPs")
report1.append("")
report1.append("| ZIP | Actual Rent | Predicted | Opportunity | Pop | Education | Income | Type | Beach |")
report1.append("|-----|-------------|-----------|-------------|-----|-----------|--------|------|-------|")

for _, row in duval_sorted.iterrows():
    opp_sign = "+" if row['residual'] > 0 else ""
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report1.append(f"| {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | {opp_sign}${row['residual']:.0f} | {row['population']:.0f} | {row['bachelors_plus']:.1f}% | ${row['median_income']:.0f} | {row['urban_rural']} | {beach_icon} {row['beach_proximity']:.1f} |")

# Save Report 1
with open('d4_modeling/results/Duval_County_Report.md', 'w') as f:
    f.write('\n'.join(report1))
print(f"   ✅ Saved: Duval_County_Report.md")

# ============================================================================
# REPORT 2: JACKSONVILLE METRO (Same as Duval in our dataset)
# ============================================================================

print("\n[2/3] Jacksonville Metro Report...")

# In our dataset, Jacksonville = entire metro
metro = duval.copy()  # Same as Duval
metro_sorted = metro.sort_values('residual', ascending=False)

report2 = []
report2.append("# Jacksonville Metropolitan Area Housing Analysis")
report2.append("## Comprehensive Metro-Wide Affordable Housing Report")
report2.append("")
report2.append("---")
report2.append("")
report2.append("## Executive Summary")
report2.append("")
report2.append(f"**Metropolitan Area**: Jacksonville, FL (Duval County)")
report2.append(f"**Total ZIP Codes**: {len(metro)}")
report2.append(f"**Total Population**: {metro['population'].sum():.0f}")
report2.append(f"**Average Median Rent**: ${metro['actual_rent'].mean():.0f}")
report2.append(f"**Rent Range**: ${metro['actual_rent'].min():.0f} - ${metro['actual_rent'].max():.0f}")
report2.append("")
report2.append("### Metro Characteristics")
report2.append("")
report2.append(f"- **Urban ZIPs**: {len(metro[metro['urban_rural'] == 'Urban'])} ({len(metro[metro['urban_rural'] == 'Urban'])/len(metro)*100:.1f}%)")
report2.append(f"- **Suburban ZIPs**: {len(metro[metro['urban_rural'] == 'Suburban'])} ({len(metro[metro['urban_rural'] == 'Suburban'])/len(metro)*100:.1f}%)")
report2.append(f"- **Rural ZIPs**: {len(metro[metro['urban_rural'] == 'Rural'])} ({len(metro[metro['urban_rural'] == 'Rural'])/len(metro)*100:.1f}%)")
report2.append(f"- **Coastal/Beach ZIPs**: {len(metro[metro['beach_proximity'] >= 1])}")
report2.append("")
report2.append("### Economic Profile")
report2.append("")
report2.append(f"- **Average Household Income**: ${metro['median_income'].mean():.0f}")
report2.append(f"- **Income Range**: ${metro['median_income'].min():.0f} - ${metro['median_income'].max():.0f}")
report2.append(f"- **Average Education (Bachelor's+)**: {metro['bachelors_plus'].mean():.1f}%")
report2.append(f"- **Education Range**: {metro['bachelors_plus'].min():.1f}% - {metro['bachelors_plus'].max():.1f}%")
report2.append("")
report2.append("---")
report2.append("")
report2.append("## Affordable Housing Opportunities by Area Type")
report2.append("")

for area_type in ['Urban', 'Suburban', 'Rural']:
    area_data = metro[metro['urban_rural'] == area_type]
    if len(area_data) > 0:
        opportunities = area_data[area_data['residual'] > 0]
        report2.append(f"### {area_type} Areas")
        report2.append("")
        report2.append(f"- **Total ZIPs**: {len(area_data)}")
        report2.append(f"- **Opportunities**: {len(opportunities)}")
        report2.append(f"- **Average Rent**: ${area_data['actual_rent'].mean():.0f}")
        report2.append(f"- **Average Income**: ${area_data['median_income'].mean():.0f}")
        report2.append("")
        
        if len(opportunities) > 0:
            report2.append(f"**Top 3 {area_type} Opportunities:**")
            report2.append("")
            for _, row in opportunities.sort_values('residual', ascending=False).head(3).iterrows():
                report2.append(f"- **ZIP {int(row['geoid'])}**: ${row['actual_rent']:.0f} actual, ${row['predicted_rent']:.0f} predicted (+${row['residual']:.0f} opportunity)")
            report2.append("")

report2.append("---")
report2.append("")
report2.append("## Complete Metro ZIP Code Listing")
report2.append("")
report2.append("| ZIP | Rent | Predicted | Opportunity | Type | Beach | Population | Income |")
report2.append("|-----|------|-----------|-------------|------|-------|------------|--------|")

for _, row in metro_sorted.iterrows():
    opp_sign = "+" if row['residual'] > 0 else ""
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report2.append(f"| {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | {opp_sign}${row['residual']:.0f} | {row['urban_rural']} | {beach_icon} | {row['population']:.0f} | ${row['median_income']:.0f} |")

# Save Report 2
with open('d4_modeling/results/Jacksonville_Metro_Report.md', 'w') as f:
    f.write('\n'.join(report2))
print(f"   ✅ Saved: Jacksonville_Metro_Report.md")

# ============================================================================
# REPORT 3: FLORIDA STATE
# ============================================================================

print("\n[3/3] Florida State Report...")

# Florida cities in our dataset
florida_cities = ['Jacksonville', 'Miami', 'Tampa', 'Orlando']
florida = preds[preds['city'].isin(florida_cities)].copy()
florida_sorted = florida.sort_values('residual', ascending=False)

report3 = []
report3.append("# Florida Affordable Housing Analysis")
report3.append("## Statewide Housing Market Assessment")
report3.append("")
report3.append("---")
report3.append("")
report3.append("## Executive Summary")
report3.append("")
report3.append(f"**Cities Analyzed**: Jacksonville, Miami, Tampa, Orlando")
report3.append(f"**Total ZIP Codes**: {len(florida)}")
report3.append(f"**Total Population**: {florida['population'].sum():.0f}")
report3.append(f"**Average Median Rent**: ${florida['actual_rent'].mean():.0f}")
report3.append(f"**Rent Range**: ${florida['actual_rent'].min():.0f} - ${florida['actual_rent'].max():.0f}")
report3.append("")
report3.append("### Statewide Characteristics")
report3.append("")
report3.append(f"- **Coastal ZIPs**: {len(florida[florida['is_coastal'] == 1])} ({len(florida[florida['is_coastal'] == 1])/len(florida)*100:.1f}%)")
report3.append(f"- **Beach/Waterfront ZIPs**: {len(florida[florida['beach_proximity'] >= 2])}")
report3.append(f"- **Average Household Income**: ${florida['median_income'].mean():.0f}")
report3.append(f"- **Average Education (Bachelor's+)**: {florida['bachelors_plus'].mean():.1f}%")
report3.append("")
report3.append("---")
report3.append("")
report3.append("## City-by-City Comparison")
report3.append("")
report3.append("| City | ZIPs | Avg Rent | Avg Income | Education | Opportunities | MAE |")
report3.append("|------|------|----------|------------|-----------|---------------|-----|")

for city in florida_cities:
    city_data = florida[florida['city'] == city]
    opportunities = len(city_data[city_data['residual'] > 0])
    mae = city_data['abs_residual'].mean()
    report3.append(f"| {city} | {len(city_data)} | ${city_data['actual_rent'].mean():.0f} | ${city_data['median_income'].mean():.0f} | {city_data['bachelors_plus'].mean():.1f}% | {opportunities} | ${mae:.0f} |")

report3.append("")
report3.append("---")
report3.append("")
report3.append("## Top 20 Affordable Housing Opportunities in Florida")
report3.append("")
report3.append("| Rank | City | ZIP | Actual Rent | Predicted | Opportunity | Type | Beach |")
report3.append("|------|------|-----|-------------|-----------|-------------|------|-------|")

for i, (_, row) in enumerate(florida_sorted[florida_sorted['residual'] > 0].head(20).iterrows(), 1):
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report3.append(f"| {i} | {row['city']} | {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | **+${row['residual']:.0f}** | {row['urban_rural']} | {beach_icon} |")

report3.append("")
report3.append("---")
report3.append("")
report3.append("## Detailed Analysis by City")
report3.append("")

for city in florida_cities:
    city_data = florida[florida['city'] == city].sort_values('residual', ascending=False)
    opportunities = city_data[city_data['residual'] > 0]
    
    report3.append(f"### {city}")
    report3.append("")
    report3.append(f"**Overview:**")
    report3.append(f"- Total ZIPs: {len(city_data)}")
    report3.append(f"- Opportunities: {len(opportunities)}")
    report3.append(f"- Average Rent: ${city_data['actual_rent'].mean():.0f}")
    report3.append(f"- Rent Range: ${city_data['actual_rent'].min():.0f} - ${city_data['actual_rent'].max():.0f}")
    report3.append(f"- Coastal ZIPs: {len(city_data[city_data['is_coastal'] == 1])}")
    report3.append("")
    
    if len(opportunities) > 0:
        report3.append(f"**Top 5 Opportunities:**")
        report3.append("")
        for _, row in opportunities.head(5).iterrows():
            report3.append(f"- **ZIP {int(row['geoid'])}**: ${row['actual_rent']:.0f} actual, ${row['predicted_rent']:.0f} predicted (+${row['residual']:.0f})")
        report3.append("")

report3.append("---")
report3.append("")
report3.append("## Methodology")
report3.append("")
report3.append("This analysis uses a machine learning model (XGBoost) trained on:")
report3.append("- Housing age distribution")
report3.append("- Education levels (4 categories)")
report3.append("- Income metrics")
report3.append("- Jobs per capita")
report3.append("- Commute patterns")
report3.append("- Coastal/beach proximity")
report3.append("- Urban/suburban/rural classification")
report3.append("")
report3.append(f"**Model Performance:**")
report3.append(f"- R² Score: 0.783")
report3.append(f"- Mean Absolute Error: $174")
report3.append(f"- Florida-specific MAE: ${florida['abs_residual'].mean():.0f}")

# Save Report 3
with open('d4_modeling/results/Florida_State_Report.md', 'w') as f:
    f.write('\n'.join(report3))
print(f"   ✅ Saved: Florida_State_Report.md")

print("\n" + "=" * 80)
print("ALL REPORTS GENERATED")
print("=" * 80)
print("\n1. Duval_County_Report.md")
print("2. Jacksonville_Metro_Report.md")
print("3. Florida_State_Report.md")
print("\n" + "=" * 80)
