# StateofJax Affordable Housing Report
**Duval County, Florida**

*Generated: April 06, 2026*

---

## Executive Summary

This report identifies rental housing opportunities in Duval County by comparing actual median rents to model-predicted market rates. ZIPs where actual rent is below predicted represent potential affordable housing opportunities.

**Key Findings:**
- **Total ZIPs Analyzed:** 30
- **Average Actual Rent:** $1,434/month
- **Average Predicted Rent:** $1,499/month
- **Market Efficiency:** 95.7%

---

## Top 10 Underpriced ZIPs (Best Affordable Housing Opportunities)

These ZIP codes have actual rents significantly below what the model predicts based on demographics, employment, and housing characteristics. They represent the best value for renters.

| Rank | ZIP Code | Actual Rent | Predicted Rent | Monthly Savings | % Below Market |
|------|----------|-------------|----------------|-----------------|----------------|
| 1 | 32207 | $1,266 | $1,541 | $275 | 17.9% |
| 2 | 32217 | $1,261 | $1,500 | $239 | 15.9% |
| 3 | 32205 | $1,263 | $1,473 | $210 | 14.3% |
| 4 | 32206 | $860 | $975 | $115 | 11.8% |
| 5 | 32216 | $1,364 | $1,470 | $106 | 7.2% |
| 6 | 32234 | $1,096 | $1,202 | $106 | 8.8% |
| 7 | 32256 | $1,698 | $1,802 | $104 | 5.8% |
| 8 | 32258 | $1,928 | $2,028 | $100 | 4.9% |
| 9 | 32204 | $1,167 | $1,265 | $98 | 7.8% |
| 10 | 32218 | $1,503 | $1,593 | $90 | 5.6% |

**Interpretation:**
- ZIP codes with negative residuals (actual < predicted) indicate areas where rent is below market expectations
- These areas may offer better value for renters seeking affordable housing
- Savings range from $90 to $275 per month

---

## Top 10 Overpriced ZIPs (Above Market Rate)

These ZIP codes have actual rents significantly above model predictions, indicating premium pricing or high demand.

| Rank | ZIP Code | Actual Rent | Predicted Rent | Monthly Premium | % Above Market |
|------|----------|-------------|----------------|-----------------|----------------|
| 1 | 32250 | $1,787 | $1,724 | $63 | 3.6% |
| 2 | 32221 | $1,708 | $1,657 | $51 | 3.0% |
| 3 | 32233 | $1,681 | $1,651 | $30 | 1.8% |
| 4 | 32225 | $1,729 | $1,716 | $13 | 0.8% |
| 5 | 32244 | $1,470 | $1,460 | $10 | 0.7% |
| 6 | 32220 | $1,330 | $1,341 | $-11 | -0.8% |
| 7 | 32266 | $1,763 | $1,779 | $-16 | -0.9% |
| 8 | 32246 | $1,761 | $1,779 | $-18 | -1.0% |
| 9 | 32223 | $1,587 | $1,615 | $-28 | -1.7% |
| 10 | 32222 | $1,795 | $1,827 | $-32 | -1.8% |

**Interpretation:**
- ZIP codes with positive residuals (actual > predicted) indicate areas where rent exceeds market expectations
- These areas may have premium amenities, high demand, or limited supply
- Premium ranges from $-32 to $63 per month

---

## Market Distribution

**Affordability Categories:**

- **Highly Affordable** (>$100 below predicted): 8 ZIPs (26.7%)
- **Affordable** ($50-$100 below predicted): 7 ZIPs (23.3%)
- **Market Rate** (±$50 of predicted): 13 ZIPs (43.3%)
- **Overpriced** ($50-$100 above predicted): 2 ZIPs (6.7%)
- **Highly Overpriced** (>$100 above predicted): 0 ZIPs (0.0%)

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
