# CAP 4922 – Data Science Capstone Project
## Deliverable 3 – Exploratory Data Analysis

**Team name:** WMK

**Team members:** Khanh Linh Lieu, William Hughes, Matthew Hendrickson

**Project title:** Identifying Rental Market Mismatches: Extreme Rent Analysis Across Metropolitan Areas

## Team Project Overview Context

This project leverages comprehensive demographic, housing, and economic data to identify rental market mismatches across 14 major metropolitan areas. Our analysis focuses on detecting ZIP codes where rental costs are disproportionate to local economic conditions, infrastructure quality, and demographic characteristics. 

The primary goal is to provide city planners and policymakers with data-driven insights to identify areas where rent prices create inefficiencies in the housing market. Rather than treating high rents as simple outliers, we frame them as "mismatches" - situations where rental costs don't align with the value proposition of location, transit access, or economic opportunity.

Key variables prioritized in our analysis include median home rent (target variable), transit accessibility, income-rent ratios, commute times, housing age diversity, and population growth patterns. These variables were selected because they directly impact housing affordability and location efficiency for residents.

---

## Dataset Summaries & Descriptive Statistics

### Metadata Summary

**Data Sources:**
1. **Housing Building Age Data** (HousingBuildingAge.zip)
   - Observations: 2,076 ZIP codes
   - Features: 10 housing age categories (1939 or earlier through 2020+)
   
2. **Main Demographic & Economic Data** (Main data.zip)  
   - Observations: 2,076 ZIP codes
   - Features: 18 variables including rent, income, employment, commute data
   
3. **Population Data** (TotalPopulation.zip)
   - Observations: 2,076 ZIP codes  
   - Features: 9 variables including total population and population change

**Merged Dataset Dimensions:**
- **Final Dataset:** 1,766 ZIP codes × 37 original features
- **Enhanced Dataset:** 1,766 ZIP codes × 55 features (after feature engineering)

### Unit of Analysis
Each row represents a **single ZIP code** within one of 14 metropolitan areas. This is a cross-sectional analysis where each ZIP code is a static geographic unit with aggregated demographic, economic, and housing characteristics for the 2020-2024 period.

**Geographic Coverage:** 14 major US metropolitan areas including Austin, Charlotte, Columbus, Denver, Indianapolis, Jacksonville, Louisville, Miami, Nashville, Orlando, Philadelphia, San Antonio, San Francisco, and Tampa.

**Temporal Coverage:** Data spans 2020-2024 for most variables, with population change calculated as the difference between 2020 and 2010 decennial census data.

### Feature Characterization

**Target Variable:**
- Median Home Rent (2020-2024): Continuous variable, primary focus of mismatch analysis

**Demographic Features:**
- Total Population, Population Change %, Per Capita Income, Income distribution across poverty levels

**Housing Features:**  
- Housing age categories (10 variables from pre-1940 to 2020+), Total Housing Units, Vacancy Rates

**Economic Features:**
- Median Household Income, Unemployment Rate, Labor Force Participation Rate, Excessive Housing Costs

**Transportation Features:**
- Commute Mean Travel Time, Public Transit Usage, Vehicle Availability

**Engineered Features:**
- Transit Accessibility Index, Income-Rent Mismatch Ratio, Rent Waste Indicators, City Boom Score

### Variable Classification

**Numerical Continuous (23 variables):**
- Median Home Rent, Median Household Income, Per Capita Income, Commute Time, Population metrics

**Numerical Discrete (14 variables):**  
- Housing unit counts by age category, Total Housing Units, Population counts

**Categorical Nominal (1 variable):**
- City (14 metropolitan areas)

**Engineered Categorical (1 variable):**
- Boom Category (MEGA BOOM, HIGH BOOM, MODERATE BOOM, SLOW GROWTH, STABLE/DECLINE)

### Statistical Summary

**Key Continuous Variables:**

| Variable | Mean | Median | Std Dev | IQR | Min | Max |
|----------|------|--------|---------|-----|-----|-----|
| Median Home Rent | $1,439 | $1,356 | $485 | $598 | $485 | $3,473 |
| Median Household Income | $69,847 | $65,313 | $28,580 | $35,625 | $19,063 | $250,001 |
| Commute Mean Travel Time | 28.1 min | 27.8 min | 6.8 min | 8.7 min | 3.5 min | 54.6 min |
| Population Change % | 17.8% | 11.2% | 67.4% | 18.1% | -32.7% | 14,775% |

**Skewness Analysis:**
- **Median Home Rent:** Mean ($1,439) > Median ($1,356), indicating right skewness with high-rent outliers
- **Household Income:** Mean ($69,847) > Median ($65,313), showing income inequality with high earners
- **Population Change:** Extreme right skewness due to outlier ZIP codes with massive growth

**High-Cardinality Features:**
- geoid (ZIP code): 1,766 unique values - used as identifier, not for modeling
- feature label: Geographic descriptors - excluded from analysis

**Sparse Features Identified:**
- Housing Built 2020 or Later: 67% of ZIP codes have zero new construction
- Public Transit Usage: 45% of ZIP codes report zero public transit commuting

---

## Visual Analysis

### Univariate Analysis

**Target Variable Distribution (Median Home Rent):**
Our histogram analysis reveals a right-skewed distribution with a clear concentration around $1,200-$1,400, representing typical middle-market rents. The distribution shows a long tail extending to $3,473, with 38 ZIP codes identified as high-rent outliers (>$2,929).

**Key Takeaway:** The skewness suggests that while most areas have moderate rents, a significant minority of ZIP codes command premium prices, justifying our focus on mismatch detection rather than simple outlier removal.

**Box Plot Analysis:**
The five-number summary ($485, $1,058, $1,356, $1,656, $3,473) shows that 50% of ZIP codes fall within a $598 rent range, while the upper quartile extends significantly higher, confirming the presence of distinct market segments.

**City-Level Rent Comparison:**
San Francisco leads with $2,475 average rent, followed by Miami ($1,994) and Denver ($1,880). Louisville shows the lowest average at $1,036, creating a $1,439 gap between highest and lowest markets.

### Bivariate & Multivariate Analysis

**Correlation Heatmap Insights:**
The comprehensive correlation analysis revealed several unexpected relationships:

1. **Historic Housing-Transit Correlation (0.93-0.95):** The strongest correlation in our dataset links pre-1940 housing with public transit usage, suggesting that older urban cores maintain superior transit infrastructure.

2. **Rent-Income Relationships:** Moderate correlation (0.45) between rent and income, but significant variation suggests other factors drive rent premiums.

3. **Commute-Rent Paradox:** Weak negative correlation (-0.12) between rent and commute time challenges assumptions about location premiums.

**Scatter Plot Analysis:**
Income vs. Rent scatter plots reveal distinct clusters:
- High-income, high-rent (luxury markets): San Francisco, Miami premium areas
- Low-income, high-rent (mismatch zones): 88 ZIP codes identified as problematic
- High-income, moderate-rent (value areas): Suburban Indianapolis, Louisville

**Key Takeaway:** The scatter plot's "fan shape" indicates heteroscedasticity, suggesting that rent variability increases with income levels, requiring careful model selection for prediction tasks.

---

## Data Quality Audit

### Missing Value Analysis

**Pre-Cleaning Missing Data:**
- Median Home Rent: 14.93% missing (310 ZIP codes)
- Other variables: <1% missing across all features

**Missing Data Pattern Analysis:**
Missing rent data was not random but systematically related to area characteristics:
- 51.3% rural/low population areas
- 26.8% owner-dominated markets  
- 10.6% commercial/industrial zones
- 4.2% high vacancy areas

**Resolution Strategy:** Complete case analysis was chosen over imputation to maintain data authenticity, removing 310 ZIP codes to achieve 100% complete rent data.

### Outlier Detection

**Statistical Outliers (Z-score > 3):**
- Population Change: ZIP 33122 (Miami) with 14,775% growth
- Median Rent: 38 ZIP codes above $2,929 (2 standard deviations)
- Commute Time: 12 ZIP codes with >45 minute average commutes

**Outlier Treatment Decision:** Outliers were retained as they represent legitimate extreme market conditions rather than data errors, aligning with our mismatch detection objectives.

### Consistency Checks

**Data Type Validation:** All numerical variables properly formatted, no string-to-number conversion issues identified.

**Geographic Consistency:** All ZIP codes validated against their assigned metropolitan areas with no misclassifications found.

**Temporal Consistency:** 2020-2024 data ranges confirmed across all variables with no anachronistic entries.

---

## Data Cleaning & Preprocessing

### Imputation Strategy

**Complete Case Analysis Approach:**
Rather than imputing missing rent values, we removed 310 ZIP codes lacking rent data to ensure analytical integrity. This decision prioritized data authenticity over sample size, maintaining 1,766 ZIP codes with 100% complete rent information.

**Justification:** Given that rent is our target variable and missing patterns were systematic (not random), imputation would introduce bias. City planning decisions require authentic rent data, making complete case analysis the appropriate choice.

### Structural Cleaning

**Dataset Merging:** Three separate ZIP-level datasets were successfully merged on geoid (ZIP code) as the common key, with 100% match rates confirming data consistency.

**Duplicate Removal:** No duplicate ZIP codes identified across the merged dataset.

**Geographic Filtering:** Analysis focused on residential ZIP codes only, with commercial and industrial areas removed during the missing data cleaning process.

### Initial Feature Engineering

**Mismatch Detection Indexes:**
1. **Transit Accessibility Index:** Combines public transit usage and vehicle availability
2. **Income-Rent Mismatch Ratio:** Identifies areas where rent exceeds income capacity  
3. **Walkability Premium Index:** Measures rent premiums for pedestrian-friendly areas
4. **Economic Stress Index:** Composite measure of unemployment and housing cost burden

**Rent Efficiency Metrics:**
1. **Rent Waste Index:** Quantifies inefficient location choices (high rent + long commute)
2. **Time-Value Rent Waste:** Economic cost including $25/hour time valuation

**Growth Indicators:**
1. **City Boom Score:** Combines population growth, new development, and economic vitality
2. **Housing Age Diversity Index:** Measures neighborhood development patterns

**Encoding Strategy:**
- City variable: Retained as categorical for geographic analysis
- Boom categories: Ordinal encoding for modeling applications
- All continuous variables: Standardized for correlation analysis

---

## Key Insights & Hypotheses

### Synthesis of Findings

**Key Discovery 1: Historic Transit Advantage**
The 93-95% correlation between pre-1940 housing and public transit usage reveals that older urban cores maintain superior infrastructure. This relationship is the strongest predictor in our dataset, suggesting that historical development patterns create lasting transportation advantages.

**Key Discovery 2: Income-Rent Mismatch Prevalence**  
88 ZIP codes show high-rent/low-income mismatches, while 88 others show low-rent/high-income patterns. This 10% mismatch rate indicates significant market inefficiencies that city planners can address through targeted interventions.

**Key Discovery 3: Rent Waste Geographic Concentration**
San Francisco dominates rent waste rankings (80.8/100 average score), with residents paying premium rents while still facing long commutes. This suggests infrastructure investment opportunities could provide significant resident value.

**Key Discovery 4: Selective Boom Patterns**
Only 0.6% of ZIP codes show significant boom activity, with Austin leading in systematic development. This concentration suggests that growth management strategies should focus on specific high-impact areas rather than broad regional approaches.

**Key Discovery 5: Commute-Rent Paradox**
Contrary to expectations, longer commutes don't consistently correlate with lower rents, suggesting that other factors (schools, amenities, housing quality) may override location convenience in pricing decisions.

### Problem Context Refinement

**Data Sufficiency Assessment:** The dataset provides robust coverage for mismatch detection with 1,766 complete cases across 37 variables. The 14-city scope offers sufficient geographic diversity for generalizable insights.

**Scope Adjustment:** Initial focus on simple outlier detection evolved into comprehensive mismatch analysis, better serving city planning applications. The addition of efficiency metrics (rent waste, boom indicators) enhances practical utility.

**Limitation Acknowledgment:** Lack of school quality, crime rates, and amenity data may limit explanation of rent premiums in some areas. Future analysis could benefit from incorporating these quality-of-life factors.

### Hypothesis Formulation

**Hypothesis 1: Historic Transit Hypothesis**
If a ZIP code has high pre-1940 housing density, then it will have superior public transit access and command rent premiums, because historical urban development concentrated around transportation hubs that remain relevant today.

**Hypothesis 2: Income-Rent Mismatch Prediction**  
If we can identify ZIP codes with Income-Rent Mismatch Ratios >1.5 or <0.7, then we can predict areas needing affordable housing interventions or luxury development opportunities, because these ratios indicate fundamental supply-demand imbalances.

**Hypothesis 3: Rent Waste Infrastructure Priority**
If a ZIP code has a Comprehensive Rent Waste Score >80, then targeted transit improvements will provide higher resident value than in lower-scoring areas, because residents are already paying premium rents while accepting poor location efficiency.

**Hypothesis 4: Walkability Value Hypothesis**
If an area has high walkability (low vehicle dependency + short commutes), then it will command rent premiums proportional to transportation cost savings, because residents value reduced transportation expenses and time.

**Hypothesis 5: Boom-Infrastructure Lag Hypothesis**
If a ZIP code has a City Boom Score >50, then it will show increasing rent waste over time unless infrastructure investments keep pace, because rapid growth typically outpaces infrastructure development.

**Hypothesis 6: Geographic Arbitrage Opportunity**
If we identify ZIP codes with high incomes but moderate rents (Income-Rent Mismatch Ratio <0.7), then these areas represent expansion opportunities for businesses and residents, because they offer economic advantages without proportional cost increases.

---

## Modeling Strategy & Technical Roadmap

### Model Selection Strategy

**Primary Approach: Ensemble Methods**
Given the non-linear relationships discovered (rent-income heteroscedasticity, transit-housing age interactions), Random Forest and Gradient Boosting models are prioritized over linear approaches. The complex interaction patterns between geographic, economic, and infrastructure variables favor tree-based methods.

**Secondary Approach: Clustering Analysis**
K-means clustering will identify natural market segments based on our engineered mismatch indexes. This unsupervised approach will validate our hypothesis-driven mismatch categories and potentially reveal additional market patterns.

### Imbalanced Data Strategy

**Mismatch Detection Focus:** Rather than predicting continuous rent values, we'll classify ZIP codes into mismatch categories (High-Rent/Low-Income, Low-Rent/High-Income, Balanced). This classification approach better serves city planning applications.

**Class Balance Assessment:** Current mismatch distribution shows 10% problematic areas, which is manageable without resampling techniques. We'll monitor precision/recall for minority classes during model evaluation.

### Evaluation Metrics

**Primary Metric: F1-Score (Macro-Averaged)**
Given the multi-class mismatch classification and the importance of identifying all mismatch types equally, macro-averaged F1-score provides balanced evaluation across all categories.

**Secondary Metrics:**
- Precision for High-Rent/Low-Income class (policy intervention priority)
- Geographic clustering validation using silhouette scores
- Feature importance rankings to validate hypothesis-driven variable selection

### Red Flags & Bias Monitoring

**Temporal Leakage Prevention:** All variables represent 2020-2024 conditions, avoiding future information leakage. Population change uses historical (2010-2020) data appropriately.

**Geographic Bias Considerations:** Model performance will be evaluated separately by metropolitan area to ensure recommendations aren't biased toward specific regional characteristics or economic conditions.

**Socioeconomic Bias Monitoring:** Income-based mismatch detection could inadvertently penalize low-income areas. We'll validate that recommendations focus on infrastructure improvements rather than displacement-inducing interventions.

**Data Representativeness:** The 14-city sample covers diverse geographic regions and economic conditions, but recommendations should be tested before applying to metropolitan areas with significantly different characteristics.

### Implementation Roadmap

**Phase 1:** Mismatch classification model development and validation
**Phase 2:** Geographic clustering analysis for market segmentation  
**Phase 3:** Policy recommendation framework based on mismatch types
**Phase 4:** Interactive dashboard for city planner decision support

This technical roadmap positions our analysis to provide actionable insights for urban planning while maintaining rigorous data science standards and ethical considerations.