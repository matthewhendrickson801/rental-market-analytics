# Executive Summary
## Affordable Housing Detection in Jacksonville Using Multi-City Rental Market Analysis

**Team WMK:** Matthew Hendrickson, William Hughes, Khanh Linh Lieu  
**Stakeholder:** StateofJax (Non-Profit Organization)  
**Date:** April 1, 2026

---

## Project Overview

StateofJax provided Team WMK with rental market data from 14 U.S. cities to develop a machine learning model that identifies affordable housing opportunities in Jacksonville, Florida. By training on 1,738 ZIP codes across comparable metros (Charlotte, Nashville, Tampa, Orlando, and others), we built a predictive model that establishes baseline rent expectations and identifies Jacksonville neighborhoods offering genuine affordability.

---

## Key Findings

### Jacksonville Market Efficiency: 97.5%

Jacksonville's rental market is remarkably efficient, with actual rents averaging only 2.5% above model predictions. This indicates a transparent, well-functioning market where rents closely match economic fundamentals.

**55 Jacksonville ZIP Codes Analyzed:**
- **9 Affordable ZIPs** (16.4%): Rent 5-21% below predicted
- **29 Fair Value ZIPs** (52.7%): Rent within ±5% of predicted  
- **17 Overpriced ZIPs** (30.9%): Rent 5-29% above predicted

### Top Affordable Opportunities

1. **32068 (Middleburg)**: $1,391 actual vs. $1,763 predicted (21.1% underpriced, $372/month savings)
2. **32091 (Starke)**: $830 actual vs. $1,015 predicted (18.2% underpriced, $185/month savings)
3. **32217 (Arlington)**: $1,261 actual vs. $1,473 predicted (14.4% underpriced, $212/month savings)

### Areas of Concern (Overpriced)

St. Augustine area shows consistent overpricing (26-29% above predicted):
- **32095, 32092, 32080**: Tourist destination premium, coastal location
- **32145 (Palatka)**: 28.7% overpriced, potential policy intervention target

---

## Model Performance

**XGBoost Gradient Boosted Trees** selected after comprehensive evaluation:

| Metric | Training | Validation | Test | Interpretation |
|--------|----------|------------|------|----------------|
| R² | 0.965 | 0.757 | 0.746 | Explains 75.7% of rent variation |
| RMSE | $100 | $241 | $273 | Average error $241-273 |
| MAE | $75 | $182 | $205 | Typical error $182-205 |
| MAPE | - | 10.0% | 9.3% | Median error ~10% |

**Jacksonville-Specific Accuracy:**
- Mean Absolute Error: $108
- Median Absolute Error: $57 (3.8% of median rent)
- Model performs exceptionally well on Jacksonville data

---

## Methodology

### Data Sources
U.S. Census Bureau American Community Survey (ACS) 5-Year Estimates (2020-2024):
- 38 features across 8 categories (housing age, income, employment, population, transit)
- 1,738 ZIP codes across 14 cities
- 28 anomalous ZIPs excluded (16 military bases, 12 retirement communities)

### Why These 14 Cities?
StateofJax selected comparable metros for training:
- **Southern region**: Charlotte, Nashville, Tampa, Orlando, San Antonio
- **Similar size**: Mid-sized metros with diverse economies
- **Growth markets**: Population growth and economic development patterns
- **Data quality**: Complete Census data availability

### Model Selection Rationale
- **Linear Regression**: Failed catastrophically (R² = -75.56)
- **Ridge Regression**: Still failed (R² = -67.62)
- **Random Forest**: Good performance (R² = 0.709)
- **XGBoost**: Best performance (R² = 0.757) ← Selected

XGBoost handles non-linear relationships, feature interactions, and outliers effectively—critical for rental market dynamics where income × region × urban type create complex patterns.

---

## Strategic Implications for StateofJax

### 1. Market Education Over Arbitrage Hunting

With only 9 affordable ZIPs (16.4% of market), StateofJax should focus on:
- **Tenant education**: Help residents understand fair market values
- **Negotiation tools**: Provide predicted rent data for lease negotiations
- **Regional positioning**: Market Jacksonville's overall affordability vs. Nashville (+5.8%), Tampa (+8.1%)

### 2. Quality-Adjusted Affordability

Our model distinguishes "affordable" from "distressed":
- **32068 Middleburg**: Affordable ($1,391) with strong fundamentals (income $80k+, growth 15%)
- **32091 Starke**: Very cheap ($830) but rural, limited amenities
- **32217 Arlington**: Best balance—affordable ($1,261) with urban amenities

### 3. Policy Advocacy Targets

17 overpriced ZIPs warrant investigation:
- **St. Augustine cluster** (32092, 32095, 32080): 26-29% overpriced, tourist premium
- **32145 Palatka**: 28.7% overpriced, highest concern
- Potential rent control, tenant protection, or supply expansion policies

### 4. Regional Competitive Advantage

Jacksonville offers 5.7% lower rents than Charlotte and 3.3% lower than Nashville for comparable neighborhoods. StateofJax can leverage this for:
- Remote worker recruitment campaigns
- Economic development marketing
- Affordable housing advocacy

---

## Data Exclusions Explained

**28 ZIP Codes Removed (1.6% of dataset):**

**16 Military Bases:**
- Operate under Basic Allowance for Housing (BAH) rates, not market forces
- Transient populations, government-subsidized rents
- Examples: Jacksonville NAS (32212), Mayport (32226)
- **Jacksonville Impact**: 2 military ZIPs excluded, not relevant for StateofJax's civilian housing focus

**12 Retirement Communities:**
- Age-restricted (55+), labor force participation <40%
- Specialized amenities, HOA fees bundled into rent
- Examples: The Villages (32159), Sun City Center (33573)
- **Jacksonville Impact**: 0 retirement ZIPs excluded

**Why Jacksonville Has No Exclusions:**
All 55 Jacksonville ZIPs in the dataset represent normal residential markets relevant to StateofJax's mission. No military bases or retirement communities in the analyzed Jacksonville ZIPs.

---

## Deliverables

### Current (D4)
1. **Predictive Model**: XGBoost with 75.7% accuracy
2. **Interactive Dashboard**: Streamlit app with 55 Jacksonville ZIPs
3. **Affordability Analysis**: Identification of 9 affordable opportunities
4. **Policy Brief**: 17 overpriced ZIPs for advocacy

### Planned (D5)
1. **Public Dashboard**: Deploy to Streamlit Cloud for StateofJax staff and residents
2. **UNF Symposium Presentation**: December 2026, live demo
3. **Tenant Education Materials**: Fair market rent guides
4. **API Integration**: Potential StateofJax website integration

---

## Limitations & Future Enhancements

### Current Limitations
- **Missing factors**: Crime rates, school quality, walkability not included (R² ceiling ~76%)
- **Geographic scope**: Model trained on 14 cities, may not generalize beyond
- **Temporal lag**: Census data updated annually, market changes monthly
- **St. Augustine anomaly**: Tourist premium not fully captured

### Phase 2 Enhancements (2027)
- Integrate Jacksonville-specific data (crime, schools, JTA transit)
- Real-time rent updates from Zillow Rent Index
- Mobile app for residents ("Find Affordable Housing Near Me")
- Expand to all Florida metros

---

## Conclusion

Jacksonville's rental market is efficient and fair, with limited arbitrage opportunities but strong overall affordability compared to regional competitors. StateofJax should leverage this model for tenant education, policy advocacy in overpriced areas, and regional economic development marketing.

**Bottom Line:** Jacksonville offers predictable, fair-market rents—a competitive advantage for attracting residents and businesses.

---

**Next Steps:**
1. Review findings with StateofJax leadership
2. Validate top affordable ZIPs (32068, 32091, 32217) with local knowledge
3. Investigate St. Augustine overpricing (policy intervention?)
4. Prepare UNF Symposium presentation
5. Deploy public dashboard for community access

**Contact:** Team WMK | UNF Computer Science | April 2026
