"""
Generate StateofJax Report - Duval County Only
Top overpriced and underpriced ZIPs
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RESULTS_DIR = BASE_DIR / 'results'

# Duval County ZIP codes (official list from previous context)
DUVAL_ZIPS = [
    '32218', '32210', '32244', '32246', '32256', '32225', '32224', '32257',
    '32216', '32211', '32207', '32209', '32208', '32258', '32277', '32221',
    '32205', '32250', '32223', '32233', '32217', '32226', '32206', '32222',
    '32254', '32219', '32220', '32234', '32204', '32266', '32202', '32276',
    '32267', '32099', '32215', '32230', '32237', '32201', '32203', '32214',
    '32228', '32229', '32232', '32231', '32236', '32235', '32238', '32240',
    '32239', '32241', '32245', '32247', '32255'
]

print("=" * 80)
print("STATEOFJAX AFFORDABLE HOUSING REPORT")
print("Duval County, Florida")
print("=" * 80)

# Load predictions (city-normalized model)
df = pd.read_csv(DATA_DIR / 'predictions_city_normalized.csv')
df['predicted_rent'] = df['predicted_rent_normalized']
df['residual'] = df['residual_normalized']

# Filter for Duval County only
df['geoid'] = df['geoid'].astype(str)
duval = df[df['geoid'].isin(DUVAL_ZIPS)].copy()

print(f"\nTotal Duval County ZIPs in dataset: {len(duval)}")

if len(duval) == 0:
    print("ERROR: No Duval County ZIPs found in dataset")
    exit(1)

# Sort by residual
duval_sorted = duval.sort_values('residual')

# Get top underpriced (best deals)
top_underpriced = duval_sorted.head(10)

# Get top overpriced
top_overpriced = duval_sorted.tail(10).sort_values('residual', ascending=False)

# Market statistics
avg_actual = duval['Median Home Rent (2020-2024)'].mean()
avg_predicted = duval['predicted_rent'].mean()
market_efficiency = (1 - abs(avg_actual - avg_predicted) / avg_predicted) * 100

# Generate markdown report
report = f"""# StateofJax Affordable Housing Report
**Duval County, Florida**

*Generated: {datetime.now().strftime('%B %d, %Y')}*

---

## Executive Summary

This report identifies rental housing opportunities in Duval County by comparing actual median rents to model-predicted market rates. ZIPs where actual rent is below predicted represent potential affordable housing opportunities.

**Key Findings:**
- **Total ZIPs Analyzed:** {len(duval)}
- **Average Actual Rent:** ${avg_actual:,.0f}/month
- **Average Predicted Rent:** ${avg_predicted:,.0f}/month
- **Market Efficiency:** {market_efficiency:.1f}%

---

## Top 10 Underpriced ZIPs (Best Affordable Housing Opportunities)

These ZIP codes have actual rents significantly below what the model predicts based on demographics, employment, and housing characteristics. They represent the best value for renters.

| Rank | ZIP Code | Actual Rent | Predicted Rent | Monthly Savings | % Below Market |
|------|----------|-------------|----------------|-----------------|----------------|
"""

for i, (_, row) in enumerate(top_underpriced.iterrows(), 1):
    actual = row['Median Home Rent (2020-2024)']
    predicted = row['predicted_rent']
    savings = predicted - actual
    pct_below = (savings / predicted) * 100
    
    report += f"| {i} | {row['geoid']} | ${actual:,.0f} | ${predicted:,.0f} | ${savings:,.0f} | {pct_below:.1f}% |\n"

report += f"""
**Interpretation:**
- ZIP codes with negative residuals (actual < predicted) indicate areas where rent is below market expectations
- These areas may offer better value for renters seeking affordable housing
- Savings range from ${top_underpriced.iloc[-1]['predicted_rent'] - top_underpriced.iloc[-1]['Median Home Rent (2020-2024)']:,.0f} to ${top_underpriced.iloc[0]['predicted_rent'] - top_underpriced.iloc[0]['Median Home Rent (2020-2024)']:,.0f} per month

---

## Top 10 Overpriced ZIPs (Above Market Rate)

These ZIP codes have actual rents significantly above model predictions, indicating premium pricing or high demand.

| Rank | ZIP Code | Actual Rent | Predicted Rent | Monthly Premium | % Above Market |
|------|----------|-------------|----------------|-----------------|----------------|
"""

for i, (_, row) in enumerate(top_overpriced.iterrows(), 1):
    actual = row['Median Home Rent (2020-2024)']
    predicted = row['predicted_rent']
    premium = actual - predicted
    pct_above = (premium / predicted) * 100
    
    report += f"| {i} | {row['geoid']} | ${actual:,.0f} | ${predicted:,.0f} | ${premium:,.0f} | {pct_above:.1f}% |\n"

report += f"""
**Interpretation:**
- ZIP codes with positive residuals (actual > predicted) indicate areas where rent exceeds market expectations
- These areas may have premium amenities, high demand, or limited supply
- Premium ranges from ${top_overpriced.iloc[-1]['Median Home Rent (2020-2024)'] - top_overpriced.iloc[-1]['predicted_rent']:,.0f} to ${top_overpriced.iloc[0]['Median Home Rent (2020-2024)'] - top_overpriced.iloc[0]['predicted_rent']:,.0f} per month

---

## Market Distribution

**Affordability Categories:**
"""

# Calculate categories
highly_affordable = (duval['residual'] < -100).sum()
affordable = ((duval['residual'] >= -100) & (duval['residual'] < -50)).sum()
market_rate = ((duval['residual'] >= -50) & (duval['residual'] <= 50)).sum()
overpriced = ((duval['residual'] > 50) & (duval['residual'] <= 100)).sum()
highly_overpriced = (duval['residual'] > 100).sum()

report += f"""
- **Highly Affordable** (>$100 below predicted): {highly_affordable} ZIPs ({highly_affordable/len(duval)*100:.1f}%)
- **Affordable** ($50-$100 below predicted): {affordable} ZIPs ({affordable/len(duval)*100:.1f}%)
- **Market Rate** (±$50 of predicted): {market_rate} ZIPs ({market_rate/len(duval)*100:.1f}%)
- **Overpriced** ($50-$100 above predicted): {overpriced} ZIPs ({overpriced/len(duval)*100:.1f}%)
- **Highly Overpriced** (>$100 above predicted): {highly_overpriced} ZIPs ({highly_overpriced/len(duval)*100:.1f}%)

---

## Methodology

**Model Details:**
- **Algorithm:** XGBoost Regression (City-Normalized)
- **Training Data:** 14 comparable Southern U.S. cities (2,128 ZIP codes)
- **Target Variable:** Deviation from city median rent (removes regional bias)
- **Validation R²:** 0.8615 (86.15% of within-city rent variation explained)
- **Test R²:** 0.8088
- **Features:** 66 variables including demographics, employment, education, housing age, and economic indicators
- **Regional Features:** REMOVED to prevent model from learning city-level shortcuts

**Key Predictive Features:**
1. Bachelor's degree percentage (12.5% importance)
2. Median household income (8.1% importance)
3. High school education percentage (6.0% importance)
4. Remote work premium (5.5% importance)
5. Transit accessibility index (4.2% importance)

**Why City-Normalized?**
The model predicts how much a ZIP's rent deviates from its city's median, rather than absolute rent. This ensures the model learns true housing economics (education, income, transit access) instead of simply memorizing "San Francisco is expensive, Louisville is cheap." The residuals now represent genuine within-city affordable housing opportunities.

**Residual Calculation:**
- Residual = Actual Rent - Predicted Rent
- Negative residual = Underpriced (affordable opportunity)
- Positive residual = Overpriced (premium market)

---

## Recommendations for StateofJax

1. **Focus on Top 10 Underpriced ZIPs** for affordable housing initiatives
2. **Investigate why these ZIPs are underpriced** - may indicate hidden value or development opportunities
3. **Monitor overpriced ZIPs** for potential market corrections or gentrification trends
4. **Use this analysis quarterly** to track market changes and identify emerging opportunities

---

## Data Sources

- U.S. Census Bureau American Community Survey (2020-2024)
- Employment and occupation data from team research
- Housing characteristics and vacancy rates
- Commute patterns and transportation data

---

*Report prepared for StateofJax by Team WMK*  
*Model Version: City-Normalized (R² = 0.86, removes regional bias)*  
*Contact: [Your contact information]*
"""

# Save report
report_path = RESULTS_DIR / 'StateofJax_Duval_County_Report.md'
with open(report_path, 'w') as f:
    f.write(report)

print(f"\n✓ Report saved to: {report_path}")

# Also save detailed data
detail_path = RESULTS_DIR / 'duval_county_detailed.csv'
duval_export = duval[['geoid', 'Median Home Rent (2020-2024)', 'predicted_rent', 
                      'residual']].copy()
duval_export.columns = ['ZIP', 'Actual_Rent', 'Predicted_Rent', 'Residual']
duval_export['Residual_Pct'] = (duval_export['Residual'] / duval_export['Predicted_Rent'] * 100).round(1)
duval_export = duval_export.sort_values('Residual')
duval_export.to_csv(detail_path, index=False)

print(f"✓ Detailed data saved to: {detail_path}")

# Print summary to console
print("\n" + "=" * 80)
print("REPORT SUMMARY")
print("=" * 80)
print(f"\nTop 3 Affordable ZIPs:")
for i, (_, row) in enumerate(top_underpriced.head(3).iterrows(), 1):
    savings = row['predicted_rent'] - row['Median Home Rent (2020-2024)']
    print(f"  {i}. ZIP {row['geoid']}: ${savings:,.0f}/month below market")

print(f"\nTop 3 Overpriced ZIPs:")
for i, (_, row) in enumerate(top_overpriced.head(3).iterrows(), 1):
    premium = row['Median Home Rent (2020-2024)'] - row['predicted_rent']
    print(f"  {i}. ZIP {row['geoid']}: ${premium:,.0f}/month above market")

print("\n" + "=" * 80)
