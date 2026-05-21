# CAP4922 - Deliverable 4: Model Selection and Solution Approaches

**Team:** WMK  
**Student:** Matthew Hendrickson  
**Date:** March 25, 2026  
**Due Date:** April 1, 2026

---

## Executive Summary

This report presents a comprehensive machine learning solution for predicting rental prices across 14 metropolitan areas in the United States. Using 1,766 ZIP codes and 31 demographic, economic, and housing features, we developed and compared four regression models to identify rental market discrepancies.

**Key Results:**
- **Best Model:** XGBoost Regressor (RMSE: $292, R²: 0.72)
- **Performance Improvement:** 68.7% reduction in error vs. baseline
- **Top Predictor:** Median Household Income (42% importance)
- **Biggest Discrepancy:** San Francisco ZIP 94514 ($1,680 overpriced)

---

## 1. Justification for Machine Learning Models

### 1.1 Problem Statement

The goal is to predict expected rental prices based on demographic and economic characteristics, then identify ZIP codes where actual rent significantly deviates from predictions. These discrepancies reveal:
- **Underpriced markets:** Good deals for renters
- **Overpriced markets:** Areas with affordability challenges
- **Market inefficiencies:** Opportunities for policy intervention

### 1.2 Why Regression?

We chose **regression** over classification because:
1. **Magnitude matters:** Need to quantify HOW MUCH rent differs from expected
2. **Continuous target:** Rent is a continuous variable ($485 - $3,473)
3. **Residual analysis:** Regression residuals directly show discrepancies
4. **Interpretability:** Dollar amounts are more actionable than categories

### 1.3 Model Selection Strategy

We implemented a **tiered comparison approach** to justify model complexity:

#### Tier 1: Linear Regression (Baseline)
- **Purpose:** Establish baseline performance
- **Assumption:** Linear relationships between features and rent
- **Complexity:** Lowest (31 coefficients)
- **Training Time:** 0.01 seconds
- **Result:** RMSE = $1,089, R² = -1.53 (FAILED)

**Why it failed:** Negative R² means the model performs worse than predicting the mean. Linear assumptions are violated due to:
- Non-linear relationships (e.g., income has diminishing returns)
- Feature interactions (e.g., transit × income)
- Geographic heterogeneity (different cities have different patterns)

#### Tier 2: Ridge Regression (Regularized Baseline)
- **Purpose:** Handle multicollinearity between features
- **Improvement:** L2 regularization prevents overfitting
- **Complexity:** Low (31 coefficients + regularization)
- **Training Time:** 0.01 seconds
- **Result:** RMSE = $933, R² = -0.86 (STILL FAILED)

**Why it failed:** Regularization helps with multicollinearity but cannot capture non-linear patterns. Still performs worse than mean prediction.

#### Tier 3: Random Forest (Non-Linear)
- **Purpose:** Capture non-linear relationships and interactions
- **Method:** Ensemble of 200 decision trees
- **Complexity:** Medium (200 trees × ~15 depth)
- **Training Time:** 0.19 seconds
- **Result:** RMSE = $322, R² = 0.66 (SUCCESS!)

**Why it works:** 
- Decision trees naturally handle non-linearity
- Ensemble averaging reduces overfitting
- Feature interactions captured automatically
- Robust to outliers

#### Tier 4: XGBoost (State-of-the-Art)
- **Purpose:** Maximize prediction accuracy
- **Method:** Gradient boosting with regularization
- **Complexity:** High (200 boosting rounds + hyperparameters)
- **Training Time:** 0.40 seconds
- **Result:** RMSE = $292, R² = 0.72 (BEST!)

**Why it's best:**
- Sequential learning corrects previous errors
- Built-in regularization prevents overfitting
- Optimized for speed and accuracy
- Industry standard for tabular data

### 1.4 Complexity vs. Interpretability Trade-Off

| Model | Interpretability | Accuracy | Training Time | Chosen? |
|-------|-----------------|----------|---------------|---------|
| Linear | ⭐⭐⭐⭐⭐ | ❌ | ⚡⚡⚡⚡⚡ | No |
| Ridge | ⭐⭐⭐⭐⭐ | ❌ | ⚡⚡⚡⚡⚡ | No |
| Random Forest | ⭐⭐⭐ | ✅ | ⚡⚡⚡⚡ | No |
| XGBoost | ⭐⭐ | ✅✅ | ⚡⚡⚡ | **Yes** |

**Decision:** We prioritize **accuracy over interpretability** because:
1. **Real-world application:** City planners need accurate predictions
2. **Presentation looming:** Need best results for stakeholders
3. **Feature importance available:** XGBoost provides interpretability via feature importance
4. **Training time acceptable:** 0.4 seconds is negligible

---

## 2. Input Variables and Feature Selection

### 2.1 Feature List (31 Original Features)

We use ONLY original features from raw data sources to prevent data leakage. All engineered features from D3 EDA were removed because they were calculated FROM the target variable (rent).

#### Housing Age Features (10)
- Housing Built 1939 or Earlier
- Housing Built 1940 to 1949
- Housing Built 1950 to 1959
- Housing Built 1960 to 1969
- Housing Built 1970 to 1979
- Housing Built 1980 to 1989
- Housing Built 1990 to 1999
- Housing Built 2000 to 2009
- Housing Built 2010 to 2019
- Housing Built 2020 or Later

#### Economic Features (6)
- Renter Excessive Housing Costs
- Home Owner Excessive Housing Costs
- Median Household Income
- Per Capita Income
- Unemployment Rate
- Labor Force Participation Rate

#### Housing Market Features (3)
- Rental Vacancy Rate
- Homeowner Vacancy Rate
- Total Housing Units

#### Population Features (2)
- Percent Change in Population (2010-2020)
- Total Population

#### Income Distribution Features (7)
- Income 49% and Below Poverty Level
- Income 50% to 99% the Poverty Level
- Income 100% to 124% the Poverty Level
- Income 125% to 149% the Poverty Level
- Income 150% to 184% the Poverty Level
- Income 185% to 199% the Poverty Level
- Income 200% and Over the Poverty Level

#### Transportation Features (3)
- Commute Mean Travel Time
- Commute Transportation by Public Transit
- No Vehicles Available

### 2.2 Feature Importance (XGBoost)

Top 10 features ranked by importance:

1. **Median Household Income (42%)** - Strongest predictor
2. **Renter Excessive Housing Costs (7%)** - Housing burden indicator
3. **Per Capita Income (7%)** - Individual wealth
4. **Public Transit Usage (7%)** - Urban density proxy
5. **Home Owner Excessive Housing Costs (4%)** - Market pressure
6. **Income 200%+ Poverty Level (3%)** - Affluence indicator
7. **Housing Built pre-1940 (3%)** - Historic neighborhoods
8. **Income <49% Poverty Level (2%)** - Poverty indicator
9. **Population Change (2%)** - Growth indicator
10. **Unemployment Rate (2%)** - Economic health

**Key Insight:** Income-related features dominate (60% combined importance), confirming that economic factors are the primary drivers of rent.

### 2.3 Feature Engineering Decisions

**Why we removed engineered features:**
- D3 EDA created 18 engineered features (mismatch indexes, rent waste metrics)
- These were calculated USING the target variable (rent)
- Including them caused **data leakage** (perfect predictions: RMSE=$0)
- Solution: Use only original features from raw data sources

**Missing Value Handling:**
- 54 missing values in 6 income-related features
- Imputed with median (preserves distribution)
- Alternative considered: Drop features (rejected - too much information loss)

### 2.4 Feature Scaling

- **Method:** StandardScaler (z-score normalization)
- **Reason:** XGBoost is tree-based (doesn't require scaling), but included for consistency
- **Implementation:** Fitted on training data only (prevents leakage)

---

## 3. Training and Validation Set Details

### 3.1 Data Split Strategy

**Total Dataset:** 1,766 ZIP codes across 14 cities

**Split Ratios:**
- **Training:** 1,147 samples (65%)
- **Validation:** 265 samples (15%)
- **Test:** 354 samples (20%)

**Stratification:** Splits are stratified by city to ensure geographic balance in each set.

### 3.2 Handling Class Imbalance (Outliers)

**Problem:** Rent distribution is right-skewed with outliers
- Low rent (<$960): 177 ZIP codes (10%)
- Normal rent ($960-$2,287): 1,412 ZIP codes (80%)
- High rent (>$2,287): 177 ZIP codes (10%)

**Solution:** Weighted regression (NOT SMOTE)
- **3x weight** for outliers (top/bottom 10%)
- **1x weight** for normal ZIP codes
- **Reason:** City planners trust real data over synthetic data

**Why not SMOTE?**
- SMOTE creates synthetic samples (interpolation)
- Regression doesn't have "minority class" problem like classification
- Weighted regression achieves same goal with authentic data

### 3.3 Cross-Validation

**Method:** Single train/validation/test split (holdout method)
- **Reason:** Dataset is large enough (1,766 samples)
- **Alternative considered:** K-fold cross-validation (rejected - unnecessary complexity)

### 3.4 Overfitting Mitigation

**Techniques Applied:**

1. **Train/Validation/Test Split**
   - Validation set used for hyperparameter tuning
   - Test set held out until final evaluation

2. **Regularization (XGBoost)**
   - L1 regularization (alpha=0.1)
   - L2 regularization (lambda=1.0)
   - Gamma (min loss reduction=0.1)

3. **Tree Constraints**
   - Max depth = 6 (prevents deep trees)
   - Min child weight = 3 (requires minimum samples)

4. **Subsampling**
   - Row sampling = 80% (prevents overfitting to specific samples)
   - Column sampling = 80% (prevents overfitting to specific features)

**Evidence of Success:**
- Training RMSE: $17 (very low - some overfitting)
- Validation RMSE: $292 (acceptable generalization)
- Gap: $275 (reasonable for complex model)

---

## 4. Evaluation Metrics for Performance Assessment

### 4.1 Primary Metric: RMSE (Root Mean Squared Error)

**Formula:** RMSE = √(Σ(actual - predicted)² / n)

**Why RMSE?**
- Measures average prediction error in dollars
- Penalizes large errors more than small errors
- Directly interpretable (same units as rent)
- Standard metric for regression problems

**Results:**

| Model | Training RMSE | Validation RMSE | Test RMSE |
|-------|---------------|-----------------|-----------|
| Linear | $413 | $1,089 | N/A |
| Ridge | $413 | $933 | N/A |
| Random Forest | $194 | $322 | N/A |
| **XGBoost** | **$17** | **$292** | **$292** |

**Interpretation:** XGBoost predictions are off by $292 on average (±$292 error).

### 4.2 Secondary Metric: R² (R-Squared)

**Formula:** R² = 1 - (SS_residual / SS_total)

**Why R²?**
- Measures proportion of variance explained
- Range: -∞ to 1 (1 = perfect, 0 = mean prediction, <0 = worse than mean)
- Indicates model fit quality

**Results:**

| Model | Training R² | Validation R² |
|-------|-------------|---------------|
| Linear | 0.63 | -1.53 |
| Ridge | 0.63 | -0.86 |
| Random Forest | 0.87 | 0.66 |
| **XGBoost** | **0.999** | **0.72** |

**Interpretation:** XGBoost explains 72% of rent variation (good fit).

### 4.3 Tertiary Metric: MAE (Mean Absolute Error)

**Formula:** MAE = Σ|actual - predicted| / n

**Why MAE?**
- Measures average absolute error
- Less sensitive to outliers than RMSE
- Easier to interpret (average error magnitude)

**Results:**

| Model | Validation MAE |
|-------|----------------|
| Linear | $448 |
| Ridge | $434 |
| Random Forest | $244 |
| **XGBoost** | **$211** |

**Interpretation:** XGBoost predictions are off by $211 on average (median error).

### 4.4 Training vs. Validation Comparison

**Purpose:** Detect overfitting

| Model | Train RMSE | Val RMSE | Gap | Overfitting? |
|-------|------------|----------|-----|--------------|
| Linear | $413 | $1,089 | $676 | No (underfitting) |
| Ridge | $413 | $933 | $520 | No (underfitting) |
| Random Forest | $194 | $322 | $128 | Slight |
| XGBoost | $17 | $292 | $275 | Moderate |

**Analysis:**
- Linear/Ridge: Underfit (poor on both train and validation)
- Random Forest: Slight overfit (acceptable gap)
- XGBoost: Moderate overfit (training RMSE very low, but validation still good)

**Conclusion:** XGBoost's overfitting is acceptable because validation performance is still excellent.

### 4.5 Residual Analysis

**Purpose:** Identify systematic errors and biggest discrepancies

**Residual Distribution:**
- Mean: $0 (unbiased predictions)
- Std Dev: $292 (matches RMSE)
- Skewness: Slight right skew (underestimates high rents)

**Residual Plot:**
- No clear patterns (good - indicates model captures relationships)
- Variance increases slightly at high rents (heteroscedasticity)

---

## 5. Overall Strategy for the Data Science Solution

### 5.1 Best Model Selection

**Winner:** XGBoost Regressor

**Justification:**
1. **Lowest RMSE:** $292 (68.7% better than Ridge)
2. **Highest R²:** 0.72 (explains 72% of variance)
3. **Lowest MAE:** $211 (best average error)
4. **Acceptable training time:** 0.4 seconds
5. **Feature importance available:** Interpretable via importance scores

### 5.2 Model Performance Summary

**Strengths:**
- Accurately predicts rent for most ZIP codes (72% variance explained)
- Identifies income as primary driver (42% importance)
- Handles non-linear relationships and interactions
- Robust to outliers (weighted regression)

**Limitations:**
- Moderate overfitting (training RMSE = $17 vs. validation = $292)
- Underestimates very high rents (San Francisco, Austin)
- Requires all 31 features (cannot handle missing data)

**Confidence Level:** High (R² = 0.72, RMSE = $292)

### 5.3 Key Findings: Rent Discrepancies

#### Top 5 Underpriced Markets (Good Deals)
1. **San Antonio ZIP 78248:** $669 savings (49% below expected)
2. **Louisville ZIP 40023:** $628 savings (53% below expected)
3. **Philadelphia ZIP 19031:** $610 savings (44% below expected)
4. **Louisville ZIP 47114:** $598 savings (71% below expected)
5. **San Antonio ZIP 78222:** $596 savings (49% below expected)

#### Top 5 Overpriced Markets (Expensive)
1. **San Francisco ZIP 94514:** $1,680 premium (63% above expected)
2. **Philadelphia ZIP 19041:** $1,184 premium (35% above expected)
3. **Austin ZIP 78739:** $1,144 premium (33% above expected)
4. **San Francisco ZIP 94130:** $1,083 premium (45% above expected)
5. **Philadelphia ZIP 19025:** $1,031 premium (34% above expected)

#### City-Level Patterns
- **Most Overpriced:** San Francisco (+$281 avg)
- **Most Underpriced:** Louisville (-$184 avg)
- **Most Accurate:** Orlando ($145 avg error)

### 5.4 Planned Data Product: Interactive Dashboard

**Concept:** Web-based dashboard for city planners and policymakers

**Features:**
1. **ZIP Code Lookup:** Enter ZIP code → See predicted vs. actual rent
2. **City Comparison:** Compare rent discrepancies across cities
3. **Feature Explorer:** Adjust income/transit/housing → See rent prediction
4. **Heatmap:** Geographic visualization of over/underpriced areas
5. **Policy Simulator:** Test "what-if" scenarios (e.g., increase transit)

**Technology Stack:**
- **Backend:** Python (Flask/FastAPI)
- **Model Serving:** Pickle (XGBoost model)
- **Frontend:** React + Plotly (interactive charts)
- **Deployment:** AWS/Heroku (cloud hosting)

**User Workflow:**
1. City planner selects city
2. Dashboard shows map of ZIP codes colored by discrepancy
3. Click ZIP code → See detailed breakdown
4. Adjust features → See predicted rent change
5. Export report for policy recommendations

### 5.5 Stakeholder Usability

**Target Users:**
- City planners (housing policy)
- Real estate investors (market opportunities)
- Renters (finding affordable areas)
- Researchers (housing affordability studies)

**Usability Considerations:**
- **Non-technical users:** Simple interface, no ML jargon
- **Actionable insights:** Dollar amounts, not R² scores
- **Visual:** Maps and charts, not tables
- **Fast:** Predictions in <1 second

### 5.6 Future Enhancements

**Short-Term (Next 3 Months):**
1. **Add more cities:** Expand from 14 to 50+ cities
2. **Time series:** Predict rent trends (not just current rent)
3. **Confidence intervals:** Show prediction uncertainty
4. **Mobile app:** iOS/Android for renters

**Long-Term (Next Year):**
1. **Deep learning:** Neural networks for better accuracy
2. **External data:** Crime rates, school quality, walkability
3. **Causal inference:** Identify WHY rent is high (not just predict)
4. **Recommendation system:** Suggest best ZIP codes for user preferences

---

## 6. Conclusion

This project successfully developed a machine learning solution for predicting rental prices and identifying market discrepancies. The XGBoost model achieves 72% variance explained (R² = 0.72) with an average error of $292, representing a 68.7% improvement over baseline models.

**Key Takeaways:**
1. **Income dominates:** Median household income is the strongest predictor (42%)
2. **Non-linearity matters:** Linear models fail; tree-based models succeed
3. **Geographic patterns:** San Francisco overpriced, Louisville underpriced
4. **Actionable insights:** Identified specific ZIP codes with biggest discrepancies

**Impact:**
- City planners can target underpriced areas for development
- Renters can find affordable neighborhoods
- Policymakers can address affordability challenges

**Next Steps:**
- Deploy interactive dashboard
- Expand to more cities
- Incorporate time series forecasting

---

## Appendix: Files and Code

### Scripts
- `scripts/preprocessing/prepare_data_original_features.py` - Data preparation
- `scripts/training/train_baseline_models.py` - Linear and Ridge models
- `scripts/training/train_advanced_models.py` - Random Forest and XGBoost
- `scripts/evaluation/analyze_residuals.py` - Residual analysis and visualizations

### Models
- `models/regression/linear_regression.pkl`
- `models/regression/ridge_regression.pkl`
- `models/regression/random_forest.pkl`
- `models/regression/xgboost.pkl`

### Results
- `results/metrics/all_models_comparison.csv`
- `results/metrics/test_set_predictions.csv`
- `results/metrics/city_level_residuals.csv`
- `results/plots/residual_analysis.png`
- `results/plots/feature_importance_comparison.png`
- `results/plots/model_comparison.png`

### How to Run
```bash
# 1. Prepare data
python3 scripts/preprocessing/prepare_data_original_features.py

# 2. Train baseline models
python3 scripts/training/train_baseline_models.py

# 3. Train advanced models
python3 scripts/training/train_advanced_models.py

# 4. Analyze residuals
python3 scripts/evaluation/analyze_residuals.py
```

---

**End of Report**
