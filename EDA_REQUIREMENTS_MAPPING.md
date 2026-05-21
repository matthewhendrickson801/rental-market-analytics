# CAP4922-D3-EDA Requirements Mapping
## How We Completed Each Requirement

This document maps each requirement from CAP4922-D3-EDA.txt to the specific code, files, and analysis we completed.

---

## ✅ Team Information

**Requirement:** Team name, members, project title

**How We Completed It:**
- **Team Name:** WMK
- **Team Members:** Khanh Linh Lieu, William Hughes, Matthew Hendrickson
- **Project Title:** "Identifying Rental Market Mismatches: Extreme Rent Analysis Across Metropolitan Areas"

**Where to Find It:**
- All reports in `reports/` directory
- README.md header

---

## ✅ Team Project Overview Context

**Requirement:** Brief overview of project goals and purpose, explain why certain variables are prioritized

**How We Completed It:**
- Focused on rental market inefficiencies for city planning applications
- Prioritized rent (target), transit access, income, commute time
- Framed as "mismatch detection" rather than outlier analysis

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 1
- `reports/Matthew_EDA_Complete_Report.md` - Section 1
- `README.md` - Project Overview section

---

## ✅ Dataset Summaries & Descriptive Statistics

### Metadata Summary

**Requirement:** List data sources, dimensions, unit of analysis, temporal/geographic coverage

**How We Completed It:**

**Script:** `scripts/data_extraction/combine_data.py`

```python
# Extracts 3 ZIP files and merges them
# - HousingBuildingAge.zip: 2,076 rows × 10 columns
# - Main data.zip: 2,076 rows × 18 columns  
# - TotalPopulation.zip: 2,076 rows × 9 columns
# Merged on: geoid (ZIP code)
# Output: combined_city_data.csv (2,076 rows × 37 columns)
```

**How to Run:**
```bash
python3 scripts/data_extraction/combine_data.py
```

**Results:**
- **Unit of Analysis:** Each row = one ZIP code (cross-sectional)
- **Geographic Coverage:** 14 metropolitan areas
- **Temporal Coverage:** 2020-2024 ACS data, 2010-2020 population change
- **Final Dataset:** 1,766 ZIP codes × 55 features (after cleaning + engineering)

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 2
- `data/processed/combined_city_data.csv` - Initial merged data
- `data/final/final_dataset_with_boom_index.csv` - Final enhanced data

---

### Feature Characterization

**Requirement:** Group columns by type, identify target variable, categorize as numerical/categorical

**How We Completed It:**

**Feature Groups:**
- **Target Variable:** Median Home Rent (2020-2024)
- **Demographic:** Population, income, poverty levels (8 features)
- **Housing:** Age categories, units, vacancy (12 features)
- **Economic:** Income, unemployment, labor force (6 features)
- **Transportation:** Commute time, transit, vehicles (4 features)
- **Engineered:** Mismatch indexes, rent waste, boom scores (18 features)

**Variable Types:**
- **Numerical Continuous:** 23 variables (rent, income, commute time)
- **Numerical Discrete:** 14 variables (housing unit counts)
- **Categorical Nominal:** 1 variable (city)
- **Categorical Ordinal:** 1 variable (boom category)

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 2.3
- `README.md` - Data Dictionary section

---

### Statistical Table

**Requirement:** Mean, Median, SD, IQR for continuous; discuss skewness; identify sparse features

**How We Completed It:**

**Script:** `scripts/analysis/generate_eda_statistics.py`

```python
# Generates comprehensive statistics for all key variables
# Calculates: mean, median, std, min, Q1, Q3, max, IQR, skewness
# Identifies high-rent outliers using Z-scores
# City-level comparisons
```

**How to Run:**
```bash
python3 scripts/analysis/generate_eda_statistics.py
```

**Key Results:**
| Variable | Mean | Median | Std Dev | IQR | Skewness |
|----------|------|--------|---------|-----|----------|
| Rent | $1,439 | $1,356 | $485 | $598 | Right-skewed |
| Income | $69,847 | $65,313 | $28,580 | $35,625 | Right-skewed |
| Commute | 28.1 min | 27.8 min | 6.8 min | 8.7 min | Near-normal |

**Sparse Features Identified:**
- Housing Built 2020+: 67% zeros
- Public Transit Usage: 45% zeros

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 2.4
- Console output from running the script

---

## ✅ Visual Analysis

### Univariate Analysis

**Requirement:** Histograms, box plots for target and key predictors; discuss skewness and outliers

**How We Completed It:**

**Script:** `scripts/analysis/univariate_analysis.py`

```python
# Creates 6-panel visualization:
# 1. Rent histogram with mean/median lines
# 2. Rent box plot (five-number summary)
# 3. City comparison bar chart
# 4. Income distribution
# 5. Commute time distribution
# 6. Population change distribution
```

**How to Run:**
```bash
python3 scripts/analysis/univariate_analysis.py
```

**Output:** `visualizations/univariate_rent_analysis.png`

**Key Findings:**
- Rent: Right-skewed, 38 high-rent outliers identified
- City gap: $1,439 between San Francisco and Louisville
- Mean > Median confirms positive skew

**Where to Find It:**
- `visualizations/univariate_rent_analysis.png`
- `reports/Final_EDA_Report_Team_WMK.md` - Section 3.1

---

### Bivariate & Multivariate Analysis

**Requirement:** Correlation heatmap, scatter plots, identify relationships and heteroscedasticity

**How We Completed It:**

**Script 1:** `scripts/analysis/bivariate_analysis.py`

```python
# Creates 6-panel bivariate analysis:
# 1. Rent vs Income scatter with trend line
# 2. Income-Rent mismatch identification (88 high/88 low)
# 3. Rent vs Commute scatter
# 4. Historic Housing vs Transit (r=0.93-0.95!)
# 5. City-wise rent box plots
# 6. Population growth vs Rent
```

**How to Run:**
```bash
python3 scripts/analysis/bivariate_analysis.py
```

**Output:** `visualizations/bivariate_mismatch_analysis.png`

**Script 2:** `scripts/analysis/comprehensive_heatmap.py`

```python
# Creates full correlation matrix (32 variables)
# Identifies strongest correlations
# Creates rent-focused heatmap
```

**How to Run:**
```bash
python3 scripts/analysis/comprehensive_heatmap.py
```

**Output:** 
- `visualizations/comprehensive_correlation_heatmap.png`
- `visualizations/rent_focused_correlation_heatmap.png`

**Key Findings:**
- **Strongest correlation:** Historic housing ↔ Transit (0.93-0.95)
- **Heteroscedasticity detected:** Rent variance increases with income
- **Mismatch areas:** 176 ZIP codes (10%) show income-rent imbalances

**Where to Find It:**
- `visualizations/bivariate_mismatch_analysis.png`
- `visualizations/comprehensive_correlation_heatmap.png`
- `reports/Final_EDA_Report_Team_WMK.md` - Section 3.2

---

## ✅ Data Quality Audit

### Missing Value Analysis

**Requirement:** Table/chart showing % missing, visualize missingness patterns

**How We Completed It:**

**Script:** `scripts/data_extraction/missing_values_analysis.py`

```python
# Calculates missing % for each column
# Creates bar chart visualization
# Generates summary CSV
```

**How to Run:**
```bash
python3 scripts/data_extraction/missing_values_analysis.py
```

**Output:** 
- `visualizations/missing_values_analysis.png`
- `data/processed/missing_values_summary.csv`

**Key Findings:**
- Overall: 0.98% missing data
- Median Home Rent: 14.93% missing (310 ZIP codes)
- All other variables: <7% missing

**Script 2:** `scripts/data_extraction/analyze_missing_rent.py`

```python
# Categorizes 310 missing rent ZIP codes:
# - 51.3% rural/low population
# - 26.8% owner-dominated markets
# - 10.6% commercial/industrial
# - 4.2% high vacancy
```

**How to Run:**
```bash
python3 scripts/data_extraction/analyze_missing_rent.py
```

**Output:** `data/processed/missing_rent_analysis.csv`

**Where to Find It:**
- `visualizations/missing_values_analysis.png`
- `data/processed/missing_rent_analysis.csv`
- `reports/Final_EDA_Report_Team_WMK.md` - Section 4

---

### Outlier Detection

**Requirement:** Use Z-scores or IQR method, justify outlier classification

**How We Completed It:**

**Method:** Z-score approach (μ + 2σ threshold)

**In Script:** `scripts/analysis/generate_eda_statistics.py`

```python
# Identifies outliers using Z-score > 2
# Rent threshold: $2,929
# Found: 38 high-rent outliers
# Decision: RETAINED (legitimate extreme markets, not errors)
```

**Justification:** Outliers represent real market conditions (San Francisco luxury areas) rather than data errors. Aligned with "mismatch detection" objectives.

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 4.2

---

### Consistency Checks

**Requirement:** Check for duplicates, data type mismatches

**How We Completed It:**

**Checks Performed:**
- ✅ No duplicate ZIP codes found
- ✅ All data types validated (no string-to-number issues)
- ✅ Geographic consistency verified (ZIP codes match assigned cities)
- ✅ Temporal consistency confirmed (2020-2024 ranges valid)

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 4.3

---

## ✅ Data Cleaning & Preprocessing

### Imputation Strategy

**Requirement:** Explain logic for handling missing values, justify approach

**How We Completed It:**

**Script:** `scripts/data_extraction/remove_missing_rent_zips.py`

```python
# DECISION: Complete Case Analysis (no imputation)
# Removed 310 ZIP codes with missing rent data
# Prioritized data authenticity over sample size
# Final: 1,766 ZIP codes with 100% authentic rent data
```

**How to Run:**
```bash
python3 scripts/data_extraction/remove_missing_rent_zips.py
```

**Output:** `data/processed/final_rent_dataset_complete_cases_only.csv`

**Justification:**
- Target variable (rent) requires authenticity for policy applications
- Missing data was systematic (not random) - represents non-rental markets
- City planners need real market conditions, not estimates

**Where to Find It:**
- `data/processed/final_rent_dataset_complete_cases_only.csv`
- `reports/data_cleaning_methodology_report_FINAL.txt`
- `reports/Final_EDA_Report_Team_WMK.md` - Section 5.1

---

### Structural Cleaning

**Requirement:** Document filtering, merging, duplicate handling

**How We Completed It:**

**Merging:** `scripts/data_extraction/combine_data.py`
- Inner join on geoid (ZIP code) across 3 datasets
- 100% match rate confirmed

**Filtering:** `scripts/data_extraction/remove_missing_rent_zips.py`
- Removed 310 non-residential ZIP codes
- Focused on active rental markets only

**Duplicates:** None found (verified in merge process)

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 5.2

---

### Initial Feature Engineering

**Requirement:** Document new variables, explain value-add, describe encoding/scaling

**How We Completed It:**

**Script 1:** `scripts/feature_engineering/create_mismatch_indexes.py`

```python
# Creates 7 mismatch detection indexes:
# 1. Transit Accessibility Index (0-100)
# 2. Income-Rent Mismatch Ratio
# 3. Walkability Premium Index
# 4. Vacancy Quality Score
# 5. Housing Age Diversity Index
# 6. Economic Stress Index
# 7. Comprehensive Mismatch Score
```

**How to Run:**
```bash
python3 scripts/feature_engineering/create_mismatch_indexes.py
```

**Output:** `data/final/final_dataset_with_mismatch_indexes.csv`

**Script 2:** `scripts/feature_engineering/create_rent_waste_index.py`

```python
# Creates 5 rent efficiency metrics:
# 1. Basic Rent Waste (0-100)
# 2. Rent Per Commute Minute ($/min)
# 3. Commute-Rent Mismatch ($)
# 4. Comprehensive Rent Waste Score (0-100)
# 5. Time-Value Rent Waste ($)
```

**How to Run:**
```bash
python3 scripts/feature_engineering/create_rent_waste_index.py
```

**Output:** `data/final/final_dataset_with_rent_waste.csv`

**Script 3:** `scripts/feature_engineering/create_city_boom_index.py`

```python
# Creates 6 growth indicators:
# 1. Population Growth Score (0-100)
# 2. New Development Score (0-100)
# 3. Economic Vitality Score (0-100)
# 4. Ultra-Recent Development Boost (0-50)
# 5. City Boom Score (0-100)
# 6. Boom Category (ordinal)
```

**How to Run:**
```bash
python3 scripts/feature_engineering/create_city_boom_index.py
```

**Output:** `data/final/final_dataset_with_boom_index.csv` ⭐ **FINAL DATASET**

**Encoding/Scaling:**
- Min-Max Scaling: Used for index creation (0-100 scales)
- Standardization: Applied for correlation analysis
- Categorical: City retained as-is, Boom Category ordinally encoded

**Where to Find It:**
- `data/final/final_dataset_with_boom_index.csv` (1,766 × 55 features)
- `reports/Final_EDA_Report_Team_WMK.md` - Section 5.3

---

## ✅ Key Insights & Hypotheses

### Synthesis of Findings

**Requirement:** 3-5 key discoveries, strongest correlations, hidden subgroups

**How We Completed It:**

**5 Major Discoveries:**

1. **Historic Transit Infrastructure Advantage**
   - 93-95% correlation between pre-1940 housing and transit
   - Discovered in: `scripts/analysis/comprehensive_heatmap.py`

2. **Systematic Market Mismatches**
   - 176 ZIP codes (10%) show income-rent imbalances
   - Discovered in: `scripts/analysis/bivariate_analysis.py`

3. **Geographic Rent Waste Concentration**
   - San Francisco: 80.8/100 average rent waste score
   - Discovered in: `scripts/feature_engineering/create_rent_waste_index.py`

4. **Selective Urban Boom Patterns**
   - Only 0.6% of ZIP codes show significant boom
   - Discovered in: `scripts/feature_engineering/create_city_boom_index.py`

5. **Commute-Rent Value Paradox**
   - Weak correlation (-0.12) challenges assumptions
   - Discovered in: `scripts/analysis/bivariate_analysis.py`

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 6.1

---

### Hypothesis Formulation

**Requirement:** Minimum 3 testable hypotheses in If/Then/Because format

**How We Completed It:**

**6 Testable Hypotheses:**

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

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 6.3

---

## ✅ Modeling Strategy & Technical Roadmap

**Requirement:** Model selection based on distributions, evaluation metrics, red flags

**How We Completed It:**

**Model Selection:**
- **Primary:** Random Forest / Gradient Boosting (non-linear relationships favor tree-based)
- **Secondary:** K-means Clustering (market segmentation validation)

**Target:** Multi-class mismatch classification (High-Rent/Low-Income, Low-Rent/High-Income, Balanced)

**Evaluation Metrics:**
- **Primary:** Macro-averaged F1-Score (equal importance across categories)
- **Secondary:** Precision for High-Rent/Low-Income class (policy priority)

**Red Flags Identified:**
- Geographic bias monitoring (validate by metro area)
- Socioeconomic bias prevention (focus on infrastructure, not displacement)
- Temporal stability (no future information leakage)

**Implementation Roadmap:**
1. Mismatch classification model development
2. Geographic clustering analysis
3. Policy recommendation framework
4. Interactive dashboard for city planners

**Where to Find It:**
- `reports/Final_EDA_Report_Team_WMK.md` - Section 7

---

## Complete Workflow for Fellow Students

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### Step-by-Step Execution

**Phase 1: Data Extraction & Cleaning (15 minutes)**
```bash
# 1. Extract and merge 3 ZIP files
python3 scripts/data_extraction/combine_data.py

# 2. Analyze missing values
python3 scripts/data_extraction/missing_values_analysis.py

# 3. Investigate missing rent data
python3 scripts/data_extraction/analyze_missing_rent.py

# 4. Remove missing rent ZIP codes (complete case analysis)
python3 scripts/data_extraction/remove_missing_rent_zips.py
```

**Phase 2: Statistical Analysis (20 minutes)**
```bash
# 5. Generate comprehensive statistics
python3 scripts/analysis/generate_eda_statistics.py

# 6. Create univariate visualizations
python3 scripts/analysis/univariate_analysis.py

# 7. Perform bivariate analysis
python3 scripts/analysis/bivariate_analysis.py

# 8. Generate correlation heatmaps
python3 scripts/analysis/comprehensive_heatmap.py

# 9. Deep insights analysis (optional)
python3 scripts/analysis/deep_insights_analysis.py
```

**Phase 3: Feature Engineering (15 minutes)**
```bash
# 10. Create mismatch detection indexes
python3 scripts/feature_engineering/create_mismatch_indexes.py

# 11. Create rent waste metrics
python3 scripts/feature_engineering/create_rent_waste_index.py

# 12. Create city boom indicators
python3 scripts/feature_engineering/create_city_boom_index.py
```

**Total Time:** ~50 minutes for complete analysis

### Quick Verification

Check that all outputs were created:
```bash
# Data files
ls data/processed/combined_city_data.csv
ls data/processed/final_rent_dataset_complete_cases_only.csv
ls data/final/final_dataset_with_boom_index.csv

# Visualizations
ls visualizations/*.png

# Should see 6 PNG files
```

### Final Outputs

**For Submission:**
- **Main Report:** `reports/Matthew_EDA_Complete_Report.md`
- **Executive Summary:** `reports/Final_EDA_Report_Team_WMK.md`
- **Final Dataset:** `data/final/final_dataset_with_boom_index.csv`
- **All Visualizations:** `visualizations/*.png`

---

## Summary: Requirements Coverage

| Requirement | Script(s) | Output | Status |
|-------------|-----------|--------|--------|
| Metadata Summary | combine_data.py | combined_city_data.csv | ✅ |
| Feature Characterization | (documented in reports) | N/A | ✅ |
| Statistical Table | generate_eda_statistics.py | Console output | ✅ |
| Univariate Analysis | univariate_analysis.py | univariate_rent_analysis.png | ✅ |
| Bivariate Analysis | bivariate_analysis.py | bivariate_mismatch_analysis.png | ✅ |
| Correlation Heatmap | comprehensive_heatmap.py | 2 PNG files | ✅ |
| Missing Value Analysis | missing_values_analysis.py | missing_values_analysis.png | ✅ |
| Outlier Detection | generate_eda_statistics.py | Console output | ✅ |
| Imputation Strategy | remove_missing_rent_zips.py | final_rent_dataset.csv | ✅ |
| Feature Engineering | 3 scripts in feature_engineering/ | 3 CSV files | ✅ |
| Key Insights | (synthesized in reports) | N/A | ✅ |
| Hypotheses | (documented in reports) | N/A | ✅ |
| Modeling Strategy | (documented in reports) | N/A | ✅ |

**All Requirements Met:** ✅ 100%

---

*Last Updated: March 11, 2026*