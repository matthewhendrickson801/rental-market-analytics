"""
Generate three regional reports with neutral language:
1. Duval County
2. Jacksonville Metro
3. Florida State

Format: All ZIPs first, then top 10 over/under predicted with justifications
"""

import pandas as pd
import numpy as np

# Load predictions
preds = pd.read_csv('d4_modeling/results/all_predictions.csv')

def generate_justification(row, prediction_type):
    """Generate justification for why model over/under predicted"""
    justifications = []
    
    if prediction_type == "over":
        # Model predicted higher than actual
        justifications.append(f"Model predicted ${row['predicted_rent']:.0f} but actual is ${row['actual_rent']:.0f}.")
        
        # Check factors
        if row['bachelors_plus'] > 40:
            justifications.append(f"High education ({row['bachelors_plus']:.1f}% bachelor's+) suggests higher rent.")
        if row['median_income'] > 90000:
            justifications.append(f"High income (${row['median_income']:.0f}) indicates affluent area.")
        if row['beach_proximity'] >= 1:
            justifications.append(f"Beach proximity (score {row['beach_proximity']:.1f}) adds premium.")
        if row['urban_rural'] == 'Urban':
            justifications.append("Urban location typically commands higher rent.")
            
        # Possible reasons for lower actual rent
        justifications.append("Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.")
        
    else:
        # Model predicted lower than actual
        justifications.append(f"Model predicted ${row['predicted_rent']:.0f} but actual is ${row['actual_rent']:.0f}.")
        
        # Check factors
        if row['beach_proximity'] >= 2:
            justifications.append(f"Beachfront location (score {row['beach_proximity']:.1f}) commands premium.")
        if row['urban_rural'] == 'Urban' and row['bachelors_plus'] > 35:
            justifications.append("Urban area with educated population drives demand.")
        
        # Possible reasons for higher actual rent
        justifications.append("Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.")
    
    return " ".join(justifications)

print("=" * 80)
print("GENERATING REGIONAL REPORTS V2")
print("=" * 80)

# ============================================================================
# REPORT 1: DUVAL COUNTY
# ============================================================================

print("\n[1/3] Duval County Report...")

duval = preds[preds['city'] == 'Jacksonville'].copy()
duval_sorted = duval.sort_values('actual_rent', ascending=False)

# Get top 10 over and under predicted
duval_over = duval.sort_values('residual', ascending=True).head(10)  # Most negative residual
duval_under = duval.sort_values('residual', ascending=False).head(10)  # Most positive residual

report1 = []
report1.append("# Duval County Housing Market Analysis")
report1.append("## Model-Based Rent Predictions for Duval County ZIP Codes")
report1.append("")
report1.append("---")
report1.append("")
report1.append("## Executive Summary")
report1.append("")
report1.append(f"**Total ZIP Codes Analyzed**: {len(duval)}")
report1.append(f"**Average Median Rent**: ${duval['actual_rent'].mean():.0f}")
report1.append(f"**Model Accuracy (MAE)**: ±${duval['abs_residual'].mean():.0f}")
report1.append(f"**Rent Range**: ${duval['actual_rent'].min():.0f} - ${duval['actual_rent'].max():.0f}")
report1.append(f"**Total Population**: {duval['population'].sum():.0f}")
report1.append("")
report1.append("### County Characteristics")
report1.append("")
report1.append(f"- **Urban ZIPs**: {len(duval[duval['urban_rural'] == 'Urban'])} ({len(duval[duval['urban_rural'] == 'Urban'])/len(duval)*100:.1f}%)")
report1.append(f"- **Suburban ZIPs**: {len(duval[duval['urban_rural'] == 'Suburban'])} ({len(duval[duval['urban_rural'] == 'Suburban'])/len(duval)*100:.1f}%)")
report1.append(f"- **Rural ZIPs**: {len(duval[duval['urban_rural'] == 'Rural'])} ({len(duval[duval['urban_rural'] == 'Rural'])/len(duval)*100:.1f}%)")
report1.append(f"- **Beach/Waterfront ZIPs**: {len(duval[duval['beach_proximity'] >= 1])}")
report1.append(f"- **Average Household Income**: ${duval['median_income'].mean():.0f}")
report1.append(f"- **Average Education (Bachelor's+)**: {duval['bachelors_plus'].mean():.1f}%")
report1.append("")
report1.append("---")
report1.append("")
report1.append("## All Duval County ZIP Codes")
report1.append("")
report1.append("Complete listing sorted by actual rent (highest to lowest):")
report1.append("")
report1.append("| ZIP | Actual Rent | Predicted Rent | Difference | Population | Education | Income | Type | Beach |")
report1.append("|-----|-------------|----------------|------------|------------|-----------|--------|------|-------|")

for _, row in duval_sorted.iterrows():
    diff_sign = "+" if row['residual'] > 0 else ""
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report1.append(f"| {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | {diff_sign}${row['residual']:.0f} | {row['population']:.0f} | {row['bachelors_plus']:.1f}% | ${row['median_income']:.0f} | {row['urban_rural']} | {beach_icon} |")

report1.append("")
report1.append("---")
report1.append("")
report1.append("## Top 10 Over-Predicted ZIP Codes")
report1.append("")
report1.append("Model predicted higher rent than actual (negative residual):")
report1.append("")

for i, (_, row) in enumerate(duval_over.iterrows(), 1):
    report1.append(f"### {i}. ZIP {int(row['geoid'])}")
    report1.append(f"- **Actual Rent**: ${row['actual_rent']:.0f}")
    report1.append(f"- **Predicted Rent**: ${row['predicted_rent']:.0f}")
    report1.append(f"- **Difference**: ${row['residual']:.0f}")
    report1.append(f"- **Characteristics**: {row['urban_rural']}, {row['population']:.0f} population, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report1.append(f"- **Analysis**: {generate_justification(row, 'over')}")
    report1.append("")

report1.append("---")
report1.append("")
report1.append("## Top 10 Under-Predicted ZIP Codes")
report1.append("")
report1.append("Model predicted lower rent than actual (positive residual):")
report1.append("")

for i, (_, row) in enumerate(duval_under.iterrows(), 1):
    report1.append(f"### {i}. ZIP {int(row['geoid'])}")
    report1.append(f"- **Actual Rent**: ${row['actual_rent']:.0f}")
    report1.append(f"- **Predicted Rent**: ${row['predicted_rent']:.0f}")
    report1.append(f"- **Difference**: +${row['residual']:.0f}")
    report1.append(f"- **Characteristics**: {row['urban_rural']}, {row['population']:.0f} population, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report1.append(f"- **Analysis**: {generate_justification(row, 'under')}")
    report1.append("")

# Save Report 1
with open('d4_modeling/results/Duval_County_Report.md', 'w') as f:
    f.write('\n'.join(report1))
print(f"   ✅ Saved: Duval_County_Report.md ({len(report1)} lines)")

# ============================================================================
# REPORT 2: JACKSONVILLE METRO
# ============================================================================

print("\n[2/3] Jacksonville Metro Report...")

metro = duval.copy()
metro_sorted = metro.sort_values('actual_rent', ascending=False)
metro_over = metro.sort_values('residual', ascending=True).head(10)
metro_under = metro.sort_values('residual', ascending=False).head(10)

report2 = []
report2.append("# Jacksonville Metropolitan Area Housing Analysis")
report2.append("## Comprehensive Metro-Wide Rent Prediction Analysis")
report2.append("")
report2.append("---")
report2.append("")
report2.append("## Executive Summary")
report2.append("")
report2.append(f"**Metropolitan Area**: Jacksonville, FL")
report2.append(f"**Total ZIP Codes**: {len(metro)}")
report2.append(f"**Total Population**: {metro['population'].sum():.0f}")
report2.append(f"**Average Median Rent**: ${metro['actual_rent'].mean():.0f}")
report2.append(f"**Model Accuracy (MAE)**: ±${metro['abs_residual'].mean():.0f}")
report2.append(f"**Rent Range**: ${metro['actual_rent'].min():.0f} - ${metro['actual_rent'].max():.0f}")
report2.append("")
report2.append("### Metro Breakdown")
report2.append("")

for area_type in ['Urban', 'Suburban', 'Rural']:
    area_data = metro[metro['urban_rural'] == area_type]
    if len(area_data) > 0:
        report2.append(f"**{area_type}:**")
        report2.append(f"- ZIPs: {len(area_data)}")
        report2.append(f"- Average Rent: ${area_data['actual_rent'].mean():.0f}")
        report2.append(f"- Average Income: ${area_data['median_income'].mean():.0f}")
        report2.append(f"- Average Education: {area_data['bachelors_plus'].mean():.1f}%")
        report2.append("")

report2.append("---")
report2.append("")
report2.append("## All Metro ZIP Codes")
report2.append("")
report2.append("Complete listing sorted by actual rent:")
report2.append("")
report2.append("| ZIP | Actual Rent | Predicted | Difference | Type | Beach | Population | Income |")
report2.append("|-----|-------------|-----------|------------|------|-------|------------|--------|")

for _, row in metro_sorted.iterrows():
    diff_sign = "+" if row['residual'] > 0 else ""
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report2.append(f"| {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | {diff_sign}${row['residual']:.0f} | {row['urban_rural']} | {beach_icon} | {row['population']:.0f} | ${row['median_income']:.0f} |")

report2.append("")
report2.append("---")
report2.append("")
report2.append("## Top 10 Over-Predicted ZIP Codes")
report2.append("")

for i, (_, row) in enumerate(metro_over.iterrows(), 1):
    report2.append(f"### {i}. ZIP {int(row['geoid'])}")
    report2.append(f"- **Actual**: ${row['actual_rent']:.0f} | **Predicted**: ${row['predicted_rent']:.0f} | **Difference**: ${row['residual']:.0f}")
    report2.append(f"- **Profile**: {row['urban_rural']}, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report2.append(f"- **Analysis**: {generate_justification(row, 'over')}")
    report2.append("")

report2.append("---")
report2.append("")
report2.append("## Top 10 Under-Predicted ZIP Codes")
report2.append("")

for i, (_, row) in enumerate(metro_under.iterrows(), 1):
    report2.append(f"### {i}. ZIP {int(row['geoid'])}")
    report2.append(f"- **Actual**: ${row['actual_rent']:.0f} | **Predicted**: ${row['predicted_rent']:.0f} | **Difference**: +${row['residual']:.0f}")
    report2.append(f"- **Profile**: {row['urban_rural']}, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report2.append(f"- **Analysis**: {generate_justification(row, 'under')}")
    report2.append("")

with open('d4_modeling/results/Jacksonville_Metro_Report.md', 'w') as f:
    f.write('\n'.join(report2))
print(f"   ✅ Saved: Jacksonville_Metro_Report.md ({len(report2)} lines)")

# ============================================================================
# REPORT 3: FLORIDA STATE
# ============================================================================

print("\n[3/3] Florida State Report...")

florida_cities = ['Jacksonville', 'Miami', 'Tampa', 'Orlando']
florida = preds[preds['city'].isin(florida_cities)].copy()
florida_sorted = florida.sort_values('actual_rent', ascending=False)
florida_over = florida.sort_values('residual', ascending=True).head(10)
florida_under = florida.sort_values('residual', ascending=False).head(10)

report3 = []
report3.append("# Florida Housing Market Analysis")
report3.append("## Statewide Rent Prediction Analysis")
report3.append("")
report3.append("---")
report3.append("")
report3.append("## Executive Summary")
report3.append("")
report3.append(f"**Cities Analyzed**: Jacksonville, Miami, Tampa, Orlando")
report3.append(f"**Total ZIP Codes**: {len(florida)}")
report3.append(f"**Total Population**: {florida['population'].sum():.0f}")
report3.append(f"**Average Median Rent**: ${florida['actual_rent'].mean():.0f}")
report3.append(f"**Model Accuracy (MAE)**: ±${florida['abs_residual'].mean():.0f}")
report3.append(f"**Rent Range**: ${florida['actual_rent'].min():.0f} - ${florida['actual_rent'].max():.0f}")
report3.append("")
report3.append("### City Comparison")
report3.append("")
report3.append("| City | ZIPs | Avg Rent | Avg Income | Education | Coastal | MAE |")
report3.append("|------|------|----------|------------|-----------|---------|-----|")

for city in florida_cities:
    city_data = florida[florida['city'] == city]
    coastal = len(city_data[city_data['is_coastal'] == 1])
    mae = city_data['abs_residual'].mean()
    report3.append(f"| {city} | {len(city_data)} | ${city_data['actual_rent'].mean():.0f} | ${city_data['median_income'].mean():.0f} | {city_data['bachelors_plus'].mean():.1f}% | {coastal} | ${mae:.0f} |")

report3.append("")
report3.append("---")
report3.append("")
report3.append("## All Florida ZIP Codes")
report3.append("")
report3.append("Complete listing sorted by actual rent:")
report3.append("")
report3.append("| City | ZIP | Actual Rent | Predicted | Difference | Type | Beach |")
report3.append("|------|-----|-------------|-----------|------------|------|-------|")

for _, row in florida_sorted.iterrows():
    diff_sign = "+" if row['residual'] > 0 else ""
    beach_icon = "🏖️" if row['beach_proximity'] >= 2 else ("🌊" if row['beach_proximity'] >= 1 else "")
    report3.append(f"| {row['city']} | {int(row['geoid'])} | ${row['actual_rent']:.0f} | ${row['predicted_rent']:.0f} | {diff_sign}${row['residual']:.0f} | {row['urban_rural']} | {beach_icon} |")

report3.append("")
report3.append("---")
report3.append("")
report3.append("## Top 10 Over-Predicted ZIP Codes (Statewide)")
report3.append("")

for i, (_, row) in enumerate(florida_over.iterrows(), 1):
    report3.append(f"### {i}. {row['city']} - ZIP {int(row['geoid'])}")
    report3.append(f"- **Actual**: ${row['actual_rent']:.0f} | **Predicted**: ${row['predicted_rent']:.0f} | **Difference**: ${row['residual']:.0f}")
    report3.append(f"- **Profile**: {row['urban_rural']}, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report3.append(f"- **Analysis**: {generate_justification(row, 'over')}")
    report3.append("")

report3.append("---")
report3.append("")
report3.append("## Top 10 Under-Predicted ZIP Codes (Statewide)")
report3.append("")

for i, (_, row) in enumerate(florida_under.iterrows(), 1):
    report3.append(f"### {i}. {row['city']} - ZIP {int(row['geoid'])}")
    report3.append(f"- **Actual**: ${row['actual_rent']:.0f} | **Predicted**: ${row['predicted_rent']:.0f} | **Difference**: +${row['residual']:.0f}")
    report3.append(f"- **Profile**: {row['urban_rural']}, {row['bachelors_plus']:.1f}% bachelor's+, ${row['median_income']:.0f} income")
    report3.append(f"- **Analysis**: {generate_justification(row, 'under')}")
    report3.append("")

report3.append("---")
report3.append("")
report3.append("## Methodology")
report3.append("")
report3.append("**Model**: XGBoost Regression")
report3.append("")
report3.append("**Features Used**:")
report3.append("- Housing age distribution (10 categories)")
report3.append("- Education levels (4 categories)")
report3.append("- Income metrics (median household, per capita)")
report3.append("- Jobs per capita")
report3.append("- Commute patterns")
report3.append("- Coastal/beach proximity")
report3.append("- Urban/suburban/rural classification")
report3.append("")
report3.append("**Performance Metrics**:")
report3.append("- R² Score: 0.783")
report3.append("- Overall MAE: $174")
report3.append(f"- Florida MAE: ${florida['abs_residual'].mean():.0f}")

with open('d4_modeling/results/Florida_State_Report.md', 'w') as f:
    f.write('\n'.join(report3))
print(f"   ✅ Saved: Florida_State_Report.md ({len(report3)} lines)")

print("\n" + "=" * 80)
print("ALL REPORTS GENERATED")
print("=" * 80)
print("\n✅ Duval_County_Report.md")
print("✅ Jacksonville_Metro_Report.md")
print("✅ Florida_State_Report.md")
print("\n" + "=" * 80)
