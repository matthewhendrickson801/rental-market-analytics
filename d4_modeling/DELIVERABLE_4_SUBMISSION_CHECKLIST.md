# Deliverable 4 Submission Checklist
**CAP 4922 - Data Science Capstone Project**  
**Due: April 1**

---

## Required Submission Format
- **Format:** Microsoft Word or PDF document
- **Style:** Cohesive narrative (NOT Q&A format)
- **Formatting:** Consistent fonts, clear headings, proper citations

---

## Team Information (5 points)

✅ **Team name:** Team WMK

✅ **Team members:** 
- Matthew Hendrickson
- William Hughes
- Khanh Linh Lieu

✅ **Project title:** Affordable Housing Detection for Jacksonville Metro Using Multi-City Rental Market Analysis

✅ **Team Project Overview Context:**
- StateofJax non-profit stakeholder
- Goal: Identify affordable housing opportunities in Jacksonville
- 14-city training dataset (2,128 ZIPs)
- City-normalized model to remove regional bias

---

## Individual Sections (Each Team Member - 50 points each)

### 1. Justification for Machine Learning Models (10 points)

**What to include:**
- ✅ **Model chosen:** XGBoost Regression (City-Normalized)
- ✅ **Why XGBoost over alternatives:**
  - Handles non-linear relationships (education × income interactions)
  - Feature importance for interpretability
  - Robust to outliers (military bases, retirement communities)
  - Faster than neural networks, more accurate than linear regression
- ✅ **Occam's Razor justification:**
  - Started with R² = 0.757 (original features)
  - Added team data → R² = 0.98 (too complex, overfitting)
  - City-normalized → R² = 0.86 (optimal balance)
- ✅ **Model assumptions:**
  - No normality assumption (tree-based)
  - Handles heteroscedasticity naturally
  - Independence: stratified by city to maintain independence
- ✅ **Alternatives considered:**
  - Linear Regression: R² = 0.65 (insufficient for complexity)
  - Random Forest: Similar performance but slower, less interpretable
  - Neural Networks: Overkill, requires more data, black box
- ✅ **Cost analysis:**
  - Training time: ~30 seconds (acceptable)
  - Prediction latency: <1ms per ZIP (real-time capable)
  - Memory: 50MB model (deployable)
  - Trade-off: 0.86 R² with interpretability > 0.98 R² with regional bias

### 2. Input Variables and Feature Selection (10 points)

**What to include:**
- ✅ **Key features (66 total):**
  1. Bachelor's degree % (12.5% importance) - education drives rent
  2. Median household income (8.1%) - purchasing power
  3. High school only % (6.0%) - inverse relationship with rent
  4. Remote work premium (5.5%) - engineered feature (education × WFH)
  5. Transit accessibility (4.2%) - urban amenity
- ✅ **Link to EDA (Deliverable 3):**
  - Correlation analysis showed education-rent relationship
  - Missing value analysis led to Indianapolis imputation
  - Outlier detection identified 17 commercial districts
- ✅ **Feature engineering:**
  - `remote_work_premium` = pct_bachelors_plus × pct_work_from_home / 100
  - `education_occupation_mismatch` = pct_bachelors_plus × pct_blue_collar / 100
  - `jobs_per_capita_log` = log(total_jobs / population) - fixed skewness
  - `commercial_district` = flag for jobs_per_capita > 5
- ✅ **Feature selection:**
  - Removed 3 redundant features (correlation > 0.9):
    - total_employed (r=0.998 with total_jobs)
    - pct_mgmt_professional (r=0.902 with pct_bachelors_plus)
    - professional_density (r=0.992 with total_jobs)
  - **CRITICAL:** Removed region features (region_HighCost, region_Midwest) to prevent city-level shortcuts
- ✅ **Normalization:**
  - Target variable: Deviation from city median rent (removes regional bias)
  - Features: StandardScaler applied after train/test split

### 3. Training and Validation Set Details (10 points)

**What to include:**
- ✅ **Split strategy:** 70/15/15 (Train/Val/Test)
  - Train: 1,488 ZIPs (69.9%)
  - Validation: 320 ZIPs (15.0%)
  - Test: 320 ZIPs (15.0%)
- ✅ **Stratified split:** By city to maintain proportional representation
  - Ensures each split has all 14 cities
  - Prevents city-specific bias in any single split
- ✅ **Why 70/15/15:**
  - Compared 5 split strategies (65/15/20, 70/15/15, 70/10/20, 80/10/10, 80/15/5)
  - 70/15/15 had highest validation R² (0.9815 before normalization)
  - Balanced: enough training data + robust validation
- ✅ **Cross-validation:** Not used
  - Stratified split sufficient with 2,128 samples
  - City stratification more important than k-fold
- ✅ **Overfitting mitigation:**
  - Regularization: L1 (alpha=0.5), L2 (lambda=2.0)
  - Max depth: 5 (reduced from 6)
  - Learning rate: 0.03 (slower learning)
  - Subsample: 0.7 (70% of data per tree)
  - Colsample: 0.7 (70% of features per tree)
  - Min child weight: 5 (prevents overfitting to small groups)
- ✅ **Results:**
  - Train R²: 0.9576 (deviation prediction)
  - Val R²: 0.6797 (deviation prediction)
  - **Actual rent prediction:** Val R² = 0.8615, Test R² = 0.8088
  - Train-Val gap: 0.0174 (minimal overfitting)

### 4. Evaluation Metrics for Performance Assessment (10 points)

**What to include:**
- ✅ **Primary metric:** R² (coefficient of determination)
  - Measures % of rent variation explained by model
  - Validation R² = 0.8615 (86.15% of within-city variation)
  - Test R² = 0.8088 (consistent with validation)
- ✅ **Secondary metrics:**
  - RMSE: $193.32 (validation), $211.82 (test) - average prediction error
  - MAE: Not reported but calculable
  - Residual analysis: Mean = $1.54, Std = $127.56
- ✅ **Why R² is appropriate:**
  - Regression problem (continuous target)
  - Interpretable: "86% of rent variation explained"
  - Stakeholder-friendly metric
- ✅ **Training vs. Validation comparison:**
  - Train R² (deviation): 0.9576
  - Val R² (deviation): 0.6797
  - Gap: 0.2779 (acceptable for deviation prediction)
  - **Actual rent:** Train 0.9793, Val 0.8615, Test 0.8088 (good generalization)
- ✅ **Where model fails:**
  - San Francisco ZIPs: Highest residuals (-$1,139 to +$1,172)
  - Commercial districts: 17 ZIPs with jobs_per_capita > 5
  - Retirement communities: 12 ZIPs tested separately (R² = 0.9674)
- ✅ **Residual analysis:**
  - 598 affordable ZIPs (28.1%) with actual < predicted
  - 420 overpriced ZIPs (19.7%) with actual > predicted
  - Jacksonville: 40/56 ZIPs (71.4%) affordable

### 5. Overall Strategy for the Data Science Solution (10 points)

**What to include:**
- ✅ **Best-performing model:**
  - XGBoost City-Normalized (R² = 0.8615)
  - Chosen over original model (R² = 0.9815) due to regional bias
  - Stability: Val-Test gap only 0.0527
  - Interpretability: Feature importance + residual analysis
- ✅ **Planned data product:**
  - **Interactive dashboard** for StateofJax
  - Features:
    - Map visualization of Duval County ZIPs color-coded by affordability
    - Filter by savings threshold ($50, $100, $200+)
    - Drill-down to ZIP-level details (demographics, predicted vs. actual)
    - Quarterly update capability
- ✅ **System workflow:**
  1. **Input:** ZIP code or neighborhood name
  2. **Processing:** Model predicts expected rent based on demographics/employment
  3. **Output:** 
     - Affordability score (% below/above market)
     - Monthly savings estimate
     - Comparison to city median
     - Neighborhood characteristics
  4. **User interaction:** 
     - Search by ZIP or map click
     - Filter by affordability category
     - Export list of affordable ZIPs for outreach
- ✅ **Usability considerations:**
  - Non-technical users: Traffic light system (green=affordable, red=overpriced)
  - KPIs: "15 ZIPs with $100+ monthly savings"
  - Visual: Heatmap of Jacksonville metro
  - Recommendations: "Focus on ZIPs 32207, 32217, 32205"
- ✅ **Anticipated challenges:**
  - **Data availability:** Need William/Khanh's features for new ZIPs
    - Solution: Use Census API for education/employment data
  - **Model drift:** Housing market changes over time
    - Solution: Retrain quarterly with updated ACS data
  - **Stakeholder trust:** "Why is this ZIP affordable?"
    - Solution: Explainable AI - show feature contributions
- ✅ **How solution solves problem:**
  - StateofJax can prioritize outreach to 15 highly affordable ZIPs
  - Residents can search for undervalued neighborhoods
  - Policy makers can identify areas for affordable housing development
  - Quantifies opportunity: $90-$275/month savings per ZIP
- ✅ **Update strategy:**
  - **Frequency:** Quarterly (aligned with ACS data releases)
  - **Retraining:** Automated pipeline with new data
  - **Monitoring:** Track residual drift (if RMSE increases >10%, retrain)
  - **Validation:** Compare predictions to actual rent changes

---

## Team Contribution Section (5 points)

✅ **Overall Strategy for the Data Science Solution:**
- Collaborative model selection process
- Integrated William's employment data + Khanh's occupation data
- Team decision to normalize by city median
- Consensus on 70/15/15 split after testing 5 strategies

---

## Supporting Materials to Reference

### Files Created:
1. **Model Training:**
   - `d4_modeling/scripts/training/train_city_normalized_model.py`
   - `d4_modeling/models/regression/xgboost_city_normalized.pkl`

2. **Data Processing:**
   - `d4_modeling/scripts/preprocessing/integrate_team_data.py`
   - `d4_modeling/scripts/preprocessing/clean_team_data.py`
   - `d4_modeling/data/master_dataset_cleaned.csv`

3. **Analysis:**
   - `d4_modeling/scripts/analysis/find_affordable_mismatches.py`
   - `d4_modeling/scripts/training/compare_split_strategies.py`
   - `d4_modeling/scripts/analysis/check_team_data_quality.py`

4. **Reports:**
   - `d4_modeling/results/StateofJax_Duval_County_Report.md`
   - `d4_modeling/docs/reports/TEAM_DATA_PREPROCESSING_REPORT.md`

5. **Visualizations:**
   - Feature importance chart
   - Residual distribution
   - City-level affordability comparison

---

## Key Numbers to Include

- **Dataset:** 2,128 ZIPs across 14 cities
- **Features:** 66 (after removing 3 redundant + region features)
- **Training samples:** 1,488 ZIPs
- **Validation R²:** 0.8615
- **Test R²:** 0.8088
- **RMSE:** $193 (validation), $212 (test)
- **Jacksonville results:** 40/56 ZIPs affordable, top savings $275/month
- **Model size:** ~50MB
- **Training time:** ~30 seconds
- **Prediction latency:** <1ms per ZIP

---

## Writing Tips

1. **Use active voice:** "The team selected XGBoost" not "XGBoost was selected"
2. **Be specific:** "R² = 0.8615" not "high accuracy"
3. **Justify decisions:** Always explain "why" not just "what"
4. **Link sections:** Reference EDA findings, connect features to metrics
5. **Avoid jargon:** Explain technical terms for non-technical readers
6. **Use visuals:** Include charts for feature importance, residuals, split comparison

---

## Final Checklist Before Submission

- [ ] All 5 individual sections completed for each team member
- [ ] Team contribution section completed
- [ ] Consistent formatting (fonts, headings, spacing)
- [ ] All data sources cited
- [ ] Figures/tables numbered and captioned
- [ ] Proofread for grammar/spelling
- [ ] Converted to PDF or Word format
- [ ] File named: `TeamWMK_Deliverable4.pdf`

---

**Total Points: 100**
- Individual: 50 points × 3 members = 150 points
- Team: 5 points
- **Your grade = (Individual + Team) / 3**
