# Rental Market Mismatch Analysis - EDA Project
## CAP 4922 Data Science Capstone - Team WMK

**Team Members:** Khanh Linh Lieu, William Hughes, Matthew Hendrickson  
**Project Title:** Identifying Rental Market Mismatches: Extreme Rent Analysis Across Metropolitan Areas  
**Date:** March 11, 2026

---

## Project Overview

This project analyzes rental market inefficiencies across 14 major US metropolitan areas using comprehensive demographic, housing, and economic data. We identify systematic mismatches where rental costs are disproportionate to local economic conditions, infrastructure quality, and demographic characteristics.

**Key Innovation:** Rather than treating high rents as simple outliers, we frame them as "mismatches" - situations where rental costs don't align with the value proposition of location, transit access, or economic opportunity.

**Target Users:** City planners, urban development authorities, and policy makers seeking data-driven insights for infrastructure investments and housing policy interventions.

---

## 📋 Assignment Completion Guide

This project fulfills all requirements from **CAP4922-D3-EDA.txt**. Here's how:

**✅ All Required Sections Completed:**
- Team Information & Project Overview
- Dataset Summaries & Descriptive Statistics (Metadata, Feature Characterization, Statistical Tables)
- Visual Analysis (Univariate, Bivariate, Multivariate with 6 visualizations)
- Data Quality Audit (Missing values, Outliers, Consistency checks)
- Data Cleaning & Preprocessing (Complete case analysis, Feature engineering)
- Key Insights & Hypotheses (5 discoveries, 6 testable hypotheses)
- Modeling Strategy & Technical Roadmap

**📄 Detailed Mapping:** See `EDA_REQUIREMENTS_MAPPING.md` for complete requirement-to-code mapping

**🎯 For Fellow Students:** 
- All code is reproducible - run scripts in order (see "How to Run" below)
- Or use pre-generated results (all analysis already complete)
- Reports contain all required sections with proper formatting

---

## Project Structure

```
.
├── scripts/
│   ├── data_extraction/          # Data loading and cleaning scripts
│   │   ├── combine_data.py       # Extract and merge 3 ZIP files
│   │   ├── missing_values_analysis.py
│   │   ├── analyze_missing_rent.py
│   │   └── remove_missing_rent_zips.py
│   ├── analysis/                 # Statistical and visual analysis
│   │   ├── generate_eda_statistics.py
│   │   ├── univariate_analysis.py
│   │   ├── bivariate_analysis.py
│   │   ├── comprehensive_heatmap.py
│   │   └── deep_insights_analysis.py
│   └── feature_engineering/      # Advanced feature creation
│       ├── create_mismatch_indexes.py
│       ├── create_rent_waste_index.py
│       └── create_city_boom_index.py
├── data/
│   ├── raw/                      # Original ZIP files
│   ├── processed/                # Cleaned intermediate data
│   └── final/                    # Final enhanced datasets
├── visualizations/               # All generated charts and plots
├── reports/                      # Final EDA reports and documentation
└── README.md                     # This file
```

---

## Data Sources

### Original Data (3 ZIP files)
1. **HousingBuildingAge.zip** - 2,076 ZIP codes, 10 housing age categories
2. **Main data.zip** - 2,076 ZIP codes, 18 demographic/economic variables
3. **TotalPopulation.zip** - 2,076 ZIP codes, 9 population variables

### Geographic Coverage
14 metropolitan areas: Austin, Charlotte, Columbus, Denver, Indianapolis, Jacksonville, Louisville, Miami, Nashville, Orlando, Philadelphia, San Antonio, San Francisco, Tampa

### Temporal Coverage
- Primary data: 2020-2024 American Community Survey estimates
- Population change: Decennial Census 2010-2020 difference

---

## Methodology & Workflow

### Phase 1: Data Extraction & Cleaning
**Scripts:** `scripts/data_extraction/`

1. **combine_data.py** - Extract 3 ZIP files and merge on geoid (ZIP code)
   - Output: `combined_city_data.csv` (2,076 ZIP codes × 37 features)

2. **missing_values_analysis.py** - Comprehensive missing data assessment
   - Output: `missing_values_summary.csv`, `missing_values_analysis.png`
   - Finding: 14.93% missing rent data (310 ZIP codes)

3. **analyze_missing_rent.py** - Categorize reasons for missing rent data
   - Output: `missing_rent_analysis.csv`
   - Categories: Rural (51.3%), Owner-dominated (26.8%), Commercial (10.6%), High vacancy (4.2%)

4. **remove_missing_rent_zips.py** - Complete case analysis implementation
   - Output: `final_rent_dataset_complete_cases_only.csv` (1,766 ZIP codes)
   - Decision: Prioritize data authenticity over sample size

**Key Decision:** Complete case analysis chosen over imputation to maintain data integrity for policy applications.

### Phase 2: Statistical Analysis
**Scripts:** `scripts/analysis/`

5. **generate_eda_statistics.py** - Comprehensive statistical summaries
   - Rent range: $485 - $3,473 (Mean: $1,439, Median: $1,356)
   - Income range: $19,063 - $250,001 (Mean: $69,847)
   - Identified 38 high-rent outliers (>$2,929)

6. **univariate_analysis.py** - Distribution analysis and visualization
   - Output: `univariate_rent_analysis.png`
   - Finding: Right-skewed rent distribution with clear market segmentation
   - City gap: $1,439 between San Francisco ($2,475) and Louisville ($1,036)

7. **bivariate_analysis.py** - Correlation and relationship analysis
   - Output: `bivariate_mismatch_analysis.png`
   - Finding: 176 mismatch areas (10% of dataset)
     - 88 high-rent/low-income ZIP codes
     - 88 low-rent/high-income ZIP codes

8. **comprehensive_heatmap.py** - Full correlation matrix analysis
   - Output: `comprehensive_correlation_heatmap.png`, `rent_focused_correlation_heatmap.png`
   - Major discovery: 93-95% correlation between pre-1940 housing and public transit usage

9. **deep_insights_analysis.py** - Advanced correlation discovery
   - Output: `deep_insights_correlations.png`
   - Counterintuitive findings: Weak rent-commute correlation (-0.12)

### Phase 3: Feature Engineering
**Scripts:** `scripts/feature_engineering/`

10. **create_mismatch_indexes.py** - 7 mismatch detection indexes
    - Output: `final_dataset_with_mismatch_indexes.csv` (1,766 × 44 features)
    - Indexes created:
      1. Transit Accessibility Index (0-100)
      2. Income-Rent Mismatch Ratio
      3. Walkability Premium Index
      4. Vacancy Quality Score
      5. Housing Age Diversity Index
      6. Economic Stress Index
      7. Comprehensive Mismatch Score

11. **create_rent_waste_index.py** - 5 rent efficiency metrics
    - Output: `final_dataset_with_rent_waste.csv` (1,766 × 49 features)
    - Metrics created:
      1. Basic Rent Waste (0-100)
      2. Rent Per Commute Minute ($/minute)
      3. Commute-Rent Mismatch ($)
      4. Comprehensive Rent Waste Score (0-100)
      5. Time-Value Rent Waste ($, includes $25/hour time valuation)
    - Finding: San Francisco dominates rent waste (80.8/100 average score)

12. **create_city_boom_index.py** - 6 growth indicators
    - Output: `final_dataset_with_boom_index.csv` (1,766 × 55 features)
    - Indicators created:
      1. Population Growth Score (0-100)
      2. New Development Score (0-100)
      3. Economic Vitality Score (0-100)
      4. Ultra-Recent Development Boost (0-50)
      5. City Boom Score (0-100)
      6. Boom Category (MEGA BOOM to STABLE/DECLINE)
    - Finding: Only 0.6% of ZIP codes show significant boom activity
    - Leader: Austin (19.0/100 boom score)

---

## Key Findings

### Major Discoveries

**1. Historic Transit Infrastructure Advantage**
- **Correlation:** 93-95% between pre-1940 housing and public transit access
- **Insight:** Historical development patterns create lasting transportation advantages
- **Policy Implication:** Leverage existing infrastructure for transit-oriented development

**2. Systematic Market Mismatches**
- **Scale:** 176 ZIP codes (10%) show significant income-rent mismatches
- **Breakdown:** 88 high-rent/low-income, 88 low-rent/high-income
- **Opportunity:** Targeted interventions can address supply-demand imbalances

**3. Geographic Rent Waste Concentration**
- **Leader:** San Francisco (80.8/100 average rent waste score)
- **Problem:** Residents pay premium rents while facing long commutes
- **Solution:** Infrastructure investment could provide significant resident value

**4. Selective Urban Boom Patterns**
- **Concentration:** Only 0.6% of ZIP codes show significant boom activity
- **Leader:** Austin leads in systematic development
- **Strategy:** Growth management should focus on high-impact areas

**5. Commute-Rent Value Paradox**
- **Finding:** Weak correlation (-0.12) between rent and commute time
- **Explanation:** Quality factors (schools, amenities) may override location convenience
- **Research Need:** Additional quality-of-life variables could improve explanatory power

### Statistical Highlights

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Dataset Size | 1,766 ZIP codes | 100% complete rent data |
| Features | 55 total (37 original + 18 engineered) | Comprehensive coverage |
| Rent Range | $485 - $3,473 | $2,988 spread |
| High-Rent Outliers | 38 ZIP codes | >$2,929 threshold |
| Mismatch Rate | 10% | 176 problematic areas |
| Strongest Correlation | 0.93-0.95 | Historic housing ↔ Transit |

---

## Testable Hypotheses

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

## How to Run the Analysis

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Option 1: Run Complete Analysis (~50 minutes)

All scripts must be run from the project root directory. They will read from and write to the appropriate subdirectories.

**Phase 1: Data Extraction & Cleaning (15 minutes)**
```bash
# Step 1: Extract and merge 3 ZIP files (2,076 ZIP codes → 37 features)
python3 scripts/data_extraction/combine_data.py
# Output: data/processed/combined_city_data.csv

# Step 2: Analyze missing values (identifies 14.93% missing rent data)
python3 scripts/data_extraction/missing_values_analysis.py
# Output: visualizations/missing_values_analysis.png

# Step 3: Investigate missing rent data (categorizes 310 ZIP codes)
python3 scripts/data_extraction/analyze_missing_rent.py
# Output: data/processed/missing_rent_analysis.csv

# Step 4: Remove missing rent ZIP codes (complete case analysis)
python3 scripts/data_extraction/remove_missing_rent_zips.py
# Output: data/processed/final_rent_dataset_complete_cases_only.csv (1,766 ZIP codes)
```

**Phase 2: Statistical Analysis (20 minutes)**
```bash
# Step 5: Generate comprehensive statistics
python3 scripts/analysis/generate_eda_statistics.py
# Output: Console output with detailed statistics

# Step 6: Create univariate visualizations
python3 scripts/analysis/univariate_analysis.py
# Output: visualizations/univariate_rent_analysis.png

# Step 7: Perform bivariate analysis (identifies 176 mismatch areas)
python3 scripts/analysis/bivariate_analysis.py
# Output: visualizations/bivariate_mismatch_analysis.png

# Step 8: Generate correlation heatmaps (discovers 0.93-0.95 transit correlation)
python3 scripts/analysis/comprehensive_heatmap.py
# Output: visualizations/comprehensive_correlation_heatmap.png
#         visualizations/rent_focused_correlation_heatmap.png
```

**Phase 3: Feature Engineering (15 minutes)**
```bash
# Step 9: Create 7 mismatch detection indexes
python3 scripts/feature_engineering/create_mismatch_indexes.py
# Output: data/final/final_dataset_with_mismatch_indexes.csv (1,766 × 44 features)

# Step 10: Create 5 rent waste efficiency metrics
python3 scripts/feature_engineering/create_rent_waste_index.py
# Output: data/final/final_dataset_with_rent_waste.csv (1,766 × 49 features)

# Step 11: Create 6 city boom growth indicators
python3 scripts/feature_engineering/create_city_boom_index.py
# Output: data/final/final_dataset_with_boom_index.csv (1,766 × 55 features) ⭐ FINAL
```

### Option 2: Use Pre-Generated Results (Instant)

All analysis has already been completed! You can skip running scripts and use:

**Final Dataset:**
```
data/final/final_dataset_with_boom_index.csv
```
- 1,766 ZIP codes × 55 features
- 100% complete rent data
- Ready for modeling

**All Visualizations:**
```
visualizations/
├── missing_values_analysis.png
├── univariate_rent_analysis.png
├── bivariate_mismatch_analysis.png
├── comprehensive_correlation_heatmap.png
├── rent_focused_correlation_heatmap.png
└── deep_insights_correlations.png
```

**Complete Reports:**
```
reports/
├── Matthew_EDA_Complete_Report.md      ⭐ Main report with all code
├── Final_EDA_Report_Team_WMK.md        Executive summary
├── data_cleaning_methodology_report_FINAL.txt
└── CAP4922-D3-EDA.txt                  Original requirements
```

### Verification

Check that all outputs exist:
```bash
# Verify data files
ls data/processed/combined_city_data.csv
ls data/processed/final_rent_dataset_complete_cases_only.csv
ls data/final/final_dataset_with_boom_index.csv

# Verify visualizations (should see 6 PNG files)
ls visualizations/*.png

# Verify reports
ls reports/*.md
```

### Troubleshooting

**"File not found" errors:**
- Make sure you're running from the project root directory
- Check that data files exist in `data/raw/` (3 ZIP files)

**"Module not found" errors:**
```bash
pip install pandas numpy matplotlib seaborn scipy
```

**Scripts take too long:**
- Use Option 2 (pre-generated results)
- All analysis is already complete in the reports

---

## Visualizations

All visualizations are saved in `visualizations/` directory:

1. **missing_values_analysis.png** - Missing data patterns
2. **univariate_rent_analysis.png** - Rent distributions and city comparisons
3. **bivariate_mismatch_analysis.png** - Income-rent relationships and mismatch identification
4. **comprehensive_correlation_heatmap.png** - Full correlation matrix (32 variables)
5. **rent_focused_correlation_heatmap.png** - Rent-specific correlations
6. **deep_insights_correlations.png** - Surprising correlation discoveries

---

## Reports & Documentation

### Main Reports (in `reports/` directory)

1. **Matthew_EDA_Complete_Report.md** - Comprehensive EDA with embedded code
   - All analysis scripts included
   - Complete methodology documentation
   - Ready for professor review

2. **Final_EDA_Report_Team_WMK.md** - Executive summary format
   - Structured for academic submission
   - Follows CAP4922-D3-EDA requirements
   - Professional presentation

3. **data_cleaning_methodology_report_FINAL.txt** - Detailed cleaning documentation
   - Complete case analysis rationale
   - Missing data categorization
   - Data integrity decisions

4. **CAP4922-D3-EDA.txt** - Original assignment requirements
   - Reference for all required sections
   - Grading criteria

---

## Modeling Strategy & Next Steps

### Recommended Approach

**Primary Model:** Random Forest / Gradient Boosting Classification
- **Target:** Multi-class mismatch categories (High-Rent/Low-Income, Low-Rent/High-Income, Balanced)
- **Rationale:** Non-linear relationships and interaction effects favor tree-based methods

**Secondary Model:** K-means Clustering
- **Purpose:** Validate hypothesis-driven categories and discover additional patterns
- **Application:** Market segmentation for targeted policy interventions

### Evaluation Metrics
- **Primary:** Macro-averaged F1-Score (equal importance across all mismatch categories)
- **Secondary:** Precision for High-Rent/Low-Income class (intervention priority)
- **Validation:** Geographic clustering using silhouette scores

### Implementation Roadmap
1. **Phase 1:** Mismatch classification model development and validation
2. **Phase 2:** Geographic market segmentation analysis
3. **Phase 3:** Policy recommendation framework based on mismatch types
4. **Phase 4:** Interactive dashboard for city planner decision support

---

## Data Dictionary

### Key Variables

**Target Variable:**
- `Median Home Rent (2020-2024)` - Monthly rental cost (continuous, $485-$3,473)

**Demographic Features:**
- `Total Population (2020-2024)` - ZIP code population
- `Percent Change in Population` - 2010-2020 growth rate
- `Per Capita Income (2020-2024)` - Individual income
- `Median Household Income (2020-2024)` - Household income

**Housing Features:**
- `Housing Built [Year Range]` - 10 age categories (pre-1940 through 2020+)
- `Total Housing Units (2020-2024)` - Total housing stock
- `Rental Vacancy Rate (2020-2024)` - Percentage vacant rentals

**Transportation Features:**
- `Commute Mean Travel Time (2020-2024)` - Average commute (minutes)
- `Commute Transportation by Public Transit (2020-2024)` - Transit usage %
- `No Vehicles Available (2020-2024)` - Households without cars

**Engineered Mismatch Indexes:**
- `Transit_Accessibility_Index` - Transit infrastructure quality (0-100)
- `Income_Rent_Mismatch_Ratio` - Rent vs income capacity (>1.5 = overpriced)
- `Comprehensive_Rent_Waste_Score` - Location efficiency (0-100, higher = worse)
- `City_Boom_Score` - Growth and development intensity (0-100)

---

## Contact & Contributions

**Team WMK**
- Matthew Hendrickson
- Khanh Linh Lieu
- William Hughes

**Course:** CAP 4922 - Data Science Capstone Project  
**Institution:** [Your University]  
**Semester:** Spring 2026

---

## License & Usage

This project is submitted as academic work for CAP 4922. The methodology and code are available for educational purposes. For policy applications or commercial use, please contact the team members.

---

*Last Updated: March 11, 2026*