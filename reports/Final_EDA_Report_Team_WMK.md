# CAP 4922 – Data Science Capstone Project
## Deliverable 3 – Exploratory Data Analysis

---

**Team Name:** WMK

**Team Members:** Khanh Linh Lieu, William Hughes, Matthew Hendrickson

**Project Title:** Identifying Rental Market Mismatches: Extreme Rent Analysis Across Metropolitan Areas

**Date:** March 11, 2026

---

## Executive Summary

This comprehensive exploratory data analysis examines rental market inefficiencies across 14 major US metropolitan areas using 1,766 ZIP codes and 55 engineered variables. Our analysis identifies systematic mismatches where rental costs are disproportionate to local economic conditions, infrastructure quality, and demographic characteristics. Key findings include the discovery of 88 high-rent/low-income mismatch areas, a 93-95% correlation between historic housing and transit access, and the identification of San Francisco as having the highest "rent waste" where residents pay premium prices while still facing long commutes.

---

## 1. Team Project Overview Context

This project leverages comprehensive demographic, housing, and economic data to identify rental market mismatches across 14 major metropolitan areas. Rather than treating high rents as simple outliers, we frame them as "mismatches" - situations where rental costs don't align with the value proposition of location, transit access, or economic opportunity.

**Primary Objective:** Provide city planners and policymakers with data-driven insights to identify areas where rent prices create inefficiencies in the housing market.

**Target End Users:** City planners, urban development authorities, and policy makers seeking to optimize infrastructure investments and housing policy interventions.

**Key Innovation:** Development of comprehensive mismatch detection indexes including Transit Accessibility, Income-Rent Mismatch Ratios, Rent Waste Indicators, and City Boom Scores to quantify market inefficiencies.

---

## 2. Dataset Summaries & Descriptive Statistics

### Metadata Summary

**Original Data Sources:**
1. **HousingBuildingAge.zip**
   - Initial observations: 2,076 ZIP codes
   - Features: 10 housing age categories (1939 or earlier through 2020+)
   - Geographic coverage: 14 metropolitan areas

2. **Main data.zip** 
   - Initial observations: 2,076 ZIP codes
   - Features: 18 demographic and economic variables
   - Includes: rent, income, employment, commute, vacancy data

3. **TotalPopulation.zip**
   - Initial observations: 2,076 ZIP codes
   - Features: 9 population and demographic variables
   - Temporal coverage: 2010-2020 population change data

**Final Merged Dataset Dimensions:**
- **Post-Cleaning:** 1,766 ZIP codes × 37 original features
- **Post-Engineering:** 1,766 ZIP codes × 55 total features
- **Data Completeness:** 100% complete cases after removing 310 ZIP codes with missing rent data

### Unit of Analysis Definition

**Primary Unit:** Each row represents a single ZIP code within one of 14 metropolitan areas.

**Analysis Type:** Cross-sectional analysis with aggregated characteristics for the 2020-2024 period.

**Geographic Scope:** Austin, Charlotte, Columbus, Denver, Indianapolis, Jacksonville, Louisville, Miami, Nashville, Orlando, Philadelphia, San Antonio, San Francisco, Tampa.

**Temporal Coverage:** 
- Primary data: 2020-2024 American Community Survey estimates
- Population change: Decennial Census 2010-2020 difference
- No temporal gaps identified in the dataset

### Feature Characterization by Type

**Target Variable (1):**
- Median Home Rent (2020-2024): Continuous, $485-$3,473 range

**Demographic Features (8):**
- Total Population, Population Change %, Per Capita Income
- Income distribution across 7 poverty level categories

**Housing Characteristics (12):**
- 10 housing age categories (pre-1940 through 2020+)
- Total Housing Units, Rental/Homeowner Vacancy Rates

**Economic Indicators (6):**
- Median Household Income, Unemployment Rate, Labor Force Participation
- Renter/Owner Excessive Housing Cost percentages

**Transportation & Infrastructure (4):**
- Commute Mean Travel Time, Public Transit Usage, Vehicle Availability

**Geographic Identifier (2):**
- City (categorical), geoid (ZIP code identifier)

**Engineered Mismatch Indexes (7):**
- Transit Accessibility Index, Income-Rent Mismatch Ratio
- Walkability Premium Index, Vacancy Quality Score
- Housing Age Diversity Index, Economic Stress Index
- Comprehensive Mismatch Score

**Rent Efficiency Metrics (5):**
- Basic Rent Waste, Rent Per Commute Minute
- Commute-Rent Mismatch, Comprehensive Rent Waste Score
- Time-Value Rent Waste

**Growth & Development Indicators (6):**
- Population Growth Score, New Development Score
- Economic Vitality Score, Ultra-Recent Development Boost
- City Boom Score, Boom Category

### Statistical Summary Table

| Variable Category | Key Statistics | Distribution Characteristics |
|------------------|----------------|----------------------------|
| **Median Home Rent** | Mean: $1,439, Median: $1,356, SD: $485 | Right-skewed, 38 high-rent outliers (>$2,929) |
| **Household Income** | Mean: $69,847, Median: $65,313, SD: $28,580 | Right-skewed, income inequality evident |
| **Commute Time** | Mean: 28.1 min, Median: 27.8 min, SD: 6.8 min | Near-normal distribution, range: 3.5-54.6 min |
| **Population Change** | Mean: 17.8%, Median: 11.2%, SD: 67.4% | Extreme right skew, outlier: 14,775% growth |
| **Transit Usage** | Mean: 2.1%, Median: 0.8%, SD: 4.2% | Highly right-skewed, 45% zero values |

**High-Variance Variables Requiring Attention:**
- Population Change (CV = 378%): Extreme outliers require careful handling
- Public Transit Usage (CV = 200%): Sparse feature with many zero values
- Housing Built 2020+ (CV = 156%): Recent construction highly concentrated

**Skewness Analysis:**
- **Moderate Skew (0.5-1.0):** Rent, Income - suitable for log transformation
- **High Skew (>1.0):** Population change, Transit usage - require robust methods
- **Near-Normal (<0.5):** Commute time, Housing age categories

---

## 3. Visual Analysis Results

### Univariate Analysis Key Findings

**Target Variable Distribution (Median Home Rent):**
- **Shape:** Right-skewed with concentration around $1,200-$1,400
- **Outliers:** 38 ZIP codes above $2,929 (2 standard deviations)
- **City Variation:** $1,439 gap between San Francisco ($2,475) and Louisville ($1,036)
- **Interpretation:** Clear market segmentation with distinct premium and standard market tiers

**Box Plot Five-Number Summary:**
- Min: $485, Q1: $1,058, Median: $1,356, Q3: $1,656, Max: $3,473
- **Key Insight:** 50% of markets fall within $598 range, while upper quartile shows significant premium extension

### Bivariate & Multivariate Analysis Discoveries

**Correlation Heatmap Major Findings:**

1. **Historic Housing-Transit Correlation (r = 0.93-0.95)**
   - Strongest relationship in dataset
   - Pre-1940 housing predicts public transit access
   - **Implication:** Historical urban cores maintain infrastructure advantages

2. **Income-Rent Relationship (r = 0.45)**
   - Moderate correlation with significant scatter
   - **Mismatch Identification:** 88 high-rent/low-income ZIP codes, 88 low-rent/high-income ZIP codes
   - **Policy Relevance:** 10% of areas show fundamental supply-demand imbalances

3. **Commute-Rent Paradox (r = -0.12)**
   - Weak negative correlation challenges location premium assumptions
   - **Insight:** Other factors (schools, amenities) may override commute convenience

**Scatter Plot Analysis:**
- **Heteroscedasticity Detected:** Rent variability increases with income levels
- **Market Clusters Identified:** Luxury markets, value areas, mismatch zones
- **Model Implications:** Non-linear methods required for prediction tasks

---

## 4. Data Quality Audit Results

### Missing Value Analysis Resolution

**Pre-Cleaning Missing Data Pattern:**
- Median Home Rent: 14.93% missing (310 ZIP codes)
- All other variables: <1% missing

**Missing Data Systematic Analysis:**
- 51.3% rural/low population density areas
- 26.8% owner-dominated markets (>90% homeownership)
- 10.6% commercial/industrial zones
- 4.2% high vacancy/transitional areas

**Resolution Strategy:** Complete case analysis chosen over imputation
- **Rationale:** Target variable authenticity prioritized for policy applications
- **Result:** 1,766 ZIP codes with 100% complete rent data
- **Trade-off:** Sample size reduction accepted for data integrity

### Outlier Detection & Treatment

**Statistical Outliers Identified:**
- Population Change: ZIP 33122 (Miami) with 14,775% growth
- Median Rent: 38 ZIP codes above $2,929
- Commute Time: 12 ZIP codes with >45 minute averages

**Treatment Decision:** Outliers retained as legitimate extreme conditions
- **Justification:** Extreme values represent real market conditions, not data errors
- **Alignment:** Supports mismatch detection objectives rather than normalization

### Data Consistency Validation

**Geographic Consistency:** 100% ZIP code validation against metropolitan area assignments
**Temporal Consistency:** All 2020-2024 data ranges confirmed
**Data Type Integrity:** No conversion errors or format inconsistencies detected

---

## 5. Data Cleaning & Preprocessing Methodology

### Comprehensive Cleaning Strategy

**Missing Data Resolution:**
- **Approach:** Complete case analysis for target variable
- **Justification:** Policy decisions require authentic rent data
- **Impact:** 310 ZIP codes removed, 1,766 retained with 100% completeness

**Dataset Integration:**
- **Method:** Inner join on geoid (ZIP code) across three data sources
- **Validation:** 100% match rate confirmed data consistency
- **Result:** Seamless integration of housing, demographic, and population data

### Advanced Feature Engineering

**Mismatch Detection Indexes Created:**

1. **Transit Accessibility Index**
   - Formula: Combines public transit usage + vehicle availability metrics
   - Purpose: Quantifies transportation infrastructure quality

2. **Income-Rent Mismatch Ratio**
   - Formula: (Actual Rent / Expected Rent from Income) 
   - Interpretation: >1.5 = overpriced, <0.7 = underpriced markets

3. **Rent Waste Indicators (5 metrics)**
   - Comprehensive Rent Waste Score: Weighted combination of rent level, commute time, and efficiency
   - Time-Value Rent Waste: Economic cost including $25/hour time valuation
   - Purpose: Identify inefficient location choices

4. **City Boom Score**
   - Components: Population growth (35%) + New development (30%) + Economic vitality (25%) + Ultra-recent construction (10%)
   - Categories: MEGA BOOM, HIGH BOOM, MODERATE BOOM, SLOW GROWTH, STABLE/DECLINE

**Scaling & Normalization:**
- Standardization applied for correlation analysis
- Min-max scaling used for index creation (0-100 scales)
- Categorical variables retained for geographic analysis

---

## 6. Key Insights & Hypothesis Synthesis

### Major Discoveries

**Discovery 1: Historic Transit Infrastructure Advantage**
- **Finding:** 93-95% correlation between pre-1940 housing and public transit access
- **Implication:** Historical development patterns create lasting transportation advantages
- **Policy Relevance:** Investment in transit-oriented development should leverage existing infrastructure

**Discovery 2: Systematic Market Mismatches**
- **Finding:** 176 ZIP codes (10%) show significant income-rent mismatches
- **Breakdown:** 88 high-rent/low-income areas, 88 low-rent/high-income areas
- **Opportunity:** Targeted interventions can address supply-demand imbalances

**Discovery 3: Geographic Concentration of Rent Waste**
- **Finding:** San Francisco dominates rent waste rankings (80.8/100 average score)
- **Problem:** Residents pay premium rents while facing long commutes
- **Solution Pathway:** Infrastructure investment could provide significant resident value

**Discovery 4: Selective Urban Boom Patterns**
- **Finding:** Only 0.6% of ZIP codes show significant boom activity
- **Leader:** Austin leads in systematic development (19.0/100 boom score)
- **Strategy Implication:** Growth management should focus on high-impact areas

**Discovery 5: Commute-Rent Value Paradox**
- **Finding:** Longer commutes don't consistently correlate with lower rents
- **Explanation:** Quality factors (schools, amenities) may override location convenience
- **Research Need:** Additional quality-of-life variables could improve model explanatory power

### Testable Hypotheses Formulated

**H1: Historic Transit Hypothesis**
*If a ZIP code has high pre-1940 housing density, then it will have superior public transit access and command rent premiums, because historical urban development concentrated around transportation hubs.*

**H2: Income-Rent Mismatch Prediction**
*If we identify ZIP codes with Income-Rent Mismatch Ratios >1.5 or <0.7, then we can predict areas needing affordable housing interventions or luxury development opportunities, because these ratios indicate supply-demand imbalances.*

**H3: Rent Waste Infrastructure Priority**
*If a ZIP code has Comprehensive Rent Waste Score >80, then targeted transit improvements will provide higher resident value than lower-scoring areas, because residents already pay premium rents while accepting poor location efficiency.*

**H4: Walkability Value Hypothesis**
*If an area has high walkability (low vehicle dependency + short commutes), then it will command rent premiums proportional to transportation cost savings, because residents value reduced transportation expenses.*

**H5: Boom-Infrastructure Lag Hypothesis**
*If a ZIP code has City Boom Score >50, then it will show increasing rent waste over time unless infrastructure investments keep pace, because rapid growth outpaces infrastructure development.*

**H6: Geographic Arbitrage Opportunity**
*If we identify ZIP codes with high incomes but moderate rents (Mismatch Ratio <0.7), then these areas represent expansion opportunities, because they offer economic advantages without proportional cost increases.*

---

## 7. Modeling Strategy & Technical Roadmap

### Model Architecture Strategy

**Primary Approach: Ensemble Classification**
- **Method:** Random Forest and Gradient Boosting for mismatch category prediction
- **Justification:** Non-linear relationships and interaction effects favor tree-based methods
- **Target:** Multi-class classification (High-Rent/Low-Income, Low-Rent/High-Income, Balanced)

**Secondary Approach: Unsupervised Clustering**
- **Method:** K-means clustering on engineered mismatch indexes
- **Purpose:** Validate hypothesis-driven categories and discover additional patterns
- **Application:** Market segmentation for targeted policy interventions

### Evaluation Framework

**Primary Metric: Macro-Averaged F1-Score**
- **Rationale:** Equal importance across all mismatch categories for policy applications
- **Focus:** Balanced performance across minority and majority classes

**Secondary Metrics:**
- Precision for High-Rent/Low-Income class (intervention priority)
- Geographic clustering validation using silhouette scores
- Feature importance rankings to validate hypothesis-driven variables

### Implementation Roadmap

**Phase 1: Mismatch Classification Model (Weeks 1-2)**
- Develop and validate multi-class classification models
- Feature importance analysis to confirm hypothesis-driven variable selection
- Cross-validation by metropolitan area to ensure geographic generalizability

**Phase 2: Geographic Market Segmentation (Week 3)**
- Unsupervised clustering analysis for natural market groupings
- Validation against known geographic and economic patterns
- Integration with mismatch classification results

**Phase 3: Policy Recommendation Framework (Week 4)**
- Decision tree development for intervention type selection
- Cost-benefit analysis framework for infrastructure investments
- Risk assessment for displacement and gentrification concerns

**Phase 4: Interactive Decision Support System (Week 5)**
- Dashboard development for city planner use
- Real-time mismatch scoring for new areas
- Scenario modeling for policy impact assessment

### Risk Mitigation & Bias Prevention

**Geographic Bias Monitoring:**
- Separate model validation by metropolitan area
- Ensure recommendations aren't biased toward specific regional characteristics

**Socioeconomic Bias Prevention:**
- Focus recommendations on infrastructure improvements rather than displacement
- Monitor for inadvertent penalization of low-income areas

**Temporal Stability Validation:**
- Test model robustness across different time periods
- Establish monitoring framework for changing market conditions

---

## 8. Technical Deliverables Summary

### Analysis Files Created
1. `combine_data.py` - Data extraction and merging
2. `missing_values_analysis.py` - Comprehensive missing data assessment
3. `analyze_missing_rent.py` - Detailed rent data investigation
4. `remove_missing_rent_zips.py` - Complete case analysis implementation
5. `generate_eda_statistics.py` - Statistical summary generation
6. `univariate_analysis.py` - Distribution analysis and visualization
7. `bivariate_analysis.py` - Correlation and relationship analysis
8. `comprehensive_heatmap.py` - Full correlation matrix analysis
9. `create_mismatch_indexes.py` - Advanced feature engineering
10. `create_rent_waste_index.py` - Efficiency metric development
11. `create_city_boom_index.py` - Growth indicator creation

### Key Output Files
- `final_dataset_with_boom_index.csv` - Complete enhanced dataset (1,766 × 55)
- `data_cleaning_methodology_report_FINAL.txt` - Comprehensive methodology documentation
- `comprehensive_correlation_heatmap.png` - Visual correlation analysis
- `univariate_rent_analysis.png` - Distribution visualizations
- `bivariate_mismatch_analysis.png` - Relationship analysis charts

### Methodology Documentation
- Complete data cleaning rationale and impact assessment
- Feature engineering mathematical formulations
- Statistical validation of all derived metrics
- Geographic and temporal scope limitations

---

## 9. Conclusions & Next Steps

This comprehensive EDA has successfully transformed raw demographic and housing data into actionable insights for urban planning applications. The identification of systematic market mismatches, development of efficiency metrics, and formulation of testable hypotheses provides a robust foundation for predictive modeling and policy recommendation development.

**Key Achievements:**
- 100% complete dataset with authentic rent data
- 18 engineered features quantifying market efficiency
- 6 testable hypotheses linking infrastructure to housing costs
- Comprehensive mismatch detection framework

**Immediate Next Steps:**
- Implement multi-class classification models for mismatch prediction
- Develop geographic clustering analysis for market segmentation
- Create policy recommendation framework based on mismatch types
- Design interactive dashboard for city planner decision support

**Long-term Impact:**
This analysis framework can be extended to additional metropolitan areas and updated with new data to provide ongoing market efficiency monitoring for urban planning authorities nationwide.

---

*Report prepared by Team WMK for CAP 4922 Data Science Capstone Project*
*Analysis period: 2020-2024 data, Report date: March 11, 2026*