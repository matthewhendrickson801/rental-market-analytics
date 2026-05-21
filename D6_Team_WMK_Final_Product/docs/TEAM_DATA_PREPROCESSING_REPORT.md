# Team Data Preprocessing Report
**William & Khanh's Data Integration Analysis**

---

## Executive Summary

This report analyzes the preprocessing applied to William and Khanh's employment/education data before integration into the master dataset.

**Key Finding:** The preprocessing converts raw counts into percentages, but does NOT normalize, standardize, or handle missing values during integration. This could be problematic.

---

## 1. William's Data Processing

### 1.1 Number of Jobs
- **Source:** `NumberofJobs/*_simple.csv`
- **Processing:** None - raw counts used directly
- **Column:** `total_jobs`
- **Issue:** ⚠️ Absolute counts not normalized by population or area

### 1.2 Education Data
- **Source:** `Edu-BlueCollar-Occup-Employment/*_simple.csv`
- **Processing:** 
  - Sums education category columns
  - Calculates percentages: `(category_sum / total_pop_edu) * 100`
- **Columns Created:**
  - `pct_less_than_hs` - % with less than high school
  - `pct_hs_only` - % with only high school degree
  - `pct_some_college` - % with some college/associate
  - `pct_bachelors_plus` - % with bachelor's or higher
- **Issue:** ✅ Percentages are scale-invariant (good)
- **Potential Issue:** ⚠️ No handling of missing categories

### 1.3 Industry Data
- **Source:** `JobsbyWoker&Industry/*_simple.csv`
- **Processing:**
  - Identifies industry columns by keywords
  - Calculates percentages: `(industry_sum / total_jobs) * 100`
- **Columns Created:**
  - `pct_tech_jobs` - % in tech/professional/finance
  - `pct_service_jobs` - % in retail/food/hospitality
  - `pct_manufacturing_jobs` - % in manufacturing/construction
- **Issue:** ✅ Percentages are scale-invariant
- **Potential Issue:** ⚠️ Keyword matching may miss or misclassify industries

---

## 2. Khanh's Data Processing

### 2.1 Occupation Mix
- **Source:** `WorkersbyOccupation/*_simple.csv`
- **Processing:**
  - Sums occupation columns
  - Calculates percentages: `(occupation_sum / total_workers) * 100`
- **Columns Created:**
  - `pct_mgmt_professional` - % in management/business/science
  - `pct_service_occup` - % in service occupations
  - `pct_sales_office` - % in sales/office work
  - `pct_blue_collar` - % in construction/production/transportation
- **Issue:** ✅ Percentages are scale-invariant

### 2.2 Work From Home
- **Source:** `WorkersWhoCommuteorWork/*_simple.csv`
- **Processing:**
  - Identifies WFH columns by keywords
  - Calculates percentage: `(wfh_sum / total_workers_wfh) * 100`
- **Column:** `pct_work_from_home`
- **Issue:** ✅ Percentage is scale-invariant

### 2.3 Employment Status
- **Source:** `EmploymentStatus-TotalEmployed/*_simple.csv`
- **Processing:** None - raw counts used
- **Column:** `total_employed`
- **Issue:** ⚠️ Absolute counts not normalized

---

## 3. Engineered Features

### 3.1 Jobs Per Capita
```python
jobs_per_capita = total_jobs / Total Population
```
- **Issue:** ✅ Normalized by population (good)

### 3.2 Education-Income Ratio
```python
education_income_ratio = pct_bachelors_plus / (Median Household Income / 1000)
```
- **Issue:** ⚠️ Arbitrary division by 1000 - not theoretically justified
- **Interpretation:** Higher ratio = more educated relative to income (undervalued talent?)

### 3.3 High Tech Area (Binary)
```python
high_tech_area = 1 if pct_tech_jobs > median else 0
```
- **Issue:** ✅ Binary flag is fine

### 3.4 Professional Density
```python
professional_density = (pct_mgmt_professional / 100) * Total Population
```
- **Issue:** ⚠️ Absolute count - not normalized by area

### 3.5 High Remote Work (Binary)
```python
high_remote_work = 1 if pct_work_from_home > median else 0
```
- **Issue:** ✅ Binary flag is fine

---

## 4. Critical Issues Identified

### 4.1 Missing Value Handling
**Problem:** Integration uses `how='left'` merge, which creates NaN for ZIPs without team data.

**Current Behavior:**
```python
df_master = df_master.merge(df_jobs[['geoid', 'total_jobs']], on='geoid', how='left')
```

**Impact:** 
- ZIPs without William/Khanh data get NaN values
- Training script fills NaN with median (line 68)
- This is done AFTER merge, not during integration

**Risk:** ⚠️ Median imputation may not be appropriate for all features

### 4.2 No Standardization During Integration
**Problem:** Features are on different scales:
- Percentages: 0-100
- Absolute counts: 0-100,000+
- Ratios: 0-10+

**Current Behavior:** Standardization happens in training script using `StandardScaler`

**Impact:** ✅ This is actually correct - standardization should happen after train/test split

### 4.3 Keyword-Based Column Selection
**Problem:** Industry/occupation columns identified by keywords:
```python
tech_keywords = ['Professional', 'Scientific', 'Technical', 'Information', 'Finance', 'Management']
tech_cols = [col for col in industry_cols if any(kw in col for kw in tech_keywords)]
```

**Risk:** ⚠️ May miss columns or misclassify if naming conventions differ across cities

### 4.4 Percentage Calculations Assume Complete Data
**Problem:** Percentages calculated as:
```python
pct_hs_only = hs_cols.sum() / total_pop_edu * 100
```

**Risk:** ⚠️ If some education categories are missing, percentages won't sum to 100%

---

## 5. Data Quality Checks Needed

### 5.1 Check Percentage Sums
Do education percentages sum to ~100% for each ZIP?
```python
total_pct = pct_less_than_hs + pct_hs_only + pct_some_college + pct_bachelors_plus
# Should be close to 100%
```

### 5.2 Check Missing Values
How many ZIPs have missing team data?
```python
df_master['total_jobs'].isna().sum()
df_master['pct_hs_only'].isna().sum()
```

### 5.3 Check for Outliers
Are there extreme values that need capping?
```python
df_master['jobs_per_capita'].describe()
# Jobs per capita > 5 would be suspicious
```

### 5.4 Check Feature Distributions
Are features normally distributed or skewed?
```python
df_master['pct_hs_only'].hist()
# Skewed distributions may need log transformation
```

---

## 6. Recommendations

### 6.1 Immediate Actions
1. ✅ **Keep percentage-based features** - they're scale-invariant
2. ⚠️ **Review absolute count features** - consider normalizing by population/area
3. ⚠️ **Validate keyword matching** - manually check if industry/occupation columns are correctly classified
4. ⚠️ **Check percentage sums** - ensure education/occupation percentages sum to ~100%

### 6.2 Potential Improvements
1. **Add data validation** - check for impossible values (negative percentages, >100%, etc.)
2. **Document column mappings** - create explicit mapping of raw columns to aggregated features
3. **Handle missing categories** - if a city doesn't have a column, explicitly set to 0 vs. NaN
4. **Add feature correlation checks** - identify redundant features before training

### 6.3 For Production Deployment
1. **Create feature extraction pipeline** - document exactly how to get these features for new ZIPs
2. **Test on Jacksonville** - verify we can actually get this data for Jacksonville ZIPs
3. **Fallback strategy** - what if some features are unavailable for new predictions?

---

## 7. Conclusion

**Overall Assessment:** The preprocessing is reasonable but has gaps.

**Strengths:**
- ✅ Uses percentages (scale-invariant)
- ✅ Standardization happens at correct stage (after split)
- ✅ Creates interpretable engineered features

**Weaknesses:**
- ⚠️ No validation of percentage sums
- ⚠️ Keyword-based column selection is fragile
- ⚠️ Missing value handling is implicit (median imputation)
- ⚠️ Some absolute counts not normalized

**Critical Question:** Can we get this data for Jacksonville ZIPs we want to predict?

---

**Next Steps:**
1. Run data quality checks (Section 5)
2. Verify we can extract these features for Jacksonville
3. If not, build simpler model with only universally available features
