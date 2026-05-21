# Starting with D4 - Model Selection and Solution Approaches

## Project Setup - March 11, 2026

### Matthew's Request:
"d4 the txt doccument is the next step for the project shall we begining and can you creat a new project for this"

### Kiro's Response:

**✅ D4 Project Structure Created!**

Created organized directory structure for Deliverable 4 (Model Selection and Solution Approaches):

```
d4_modeling/
├── data/                          # Dataset from D3 EDA
├── models/
│   ├── classification/           # Mismatch category prediction
│   ├── regression/               # Rent waste score prediction
│   └── clustering/               # Market segmentation
├── notebooks/                     # Jupyter notebooks
├── scripts/
│   ├── preprocessing/            # Data preparation
│   ├── training/                 # Model training
│   ├── evaluation/               # Performance assessment
│   └── visualization/            # Results plots
├── results/
│   ├── metrics/                  # Performance metrics
│   ├── plots/                    # Visualizations
│   └── model_artifacts/          # Saved models
├── reports/                       # Final D4 report
├── CAP4922-D4-ModelSolutions.txt # Requirements
├── README.md                      # Project documentation
└── STARTING_WITH_D4.md           # This file
```

### D4 Requirements Overview

**Due Date:** April 1, 2026

**Required Sections:**
1. **Justification for Machine Learning Models**
   - Why specific models were chosen
   - Complexity vs. interpretability trade-offs
   - Comparison with alternatives
   - Training time vs. performance analysis

2. **Input Variables and Feature Selection**
   - Feature list and definitions (from D3 EDA)
   - Feature engineering recap
   - Feature selection techniques
   - Relevance justification

3. **Training and Validation Set Details**
   - Train/validation/test split strategy
   - Cross-validation approach
   - Handling class imbalance (SMOTE)
   - Overfitting mitigation

4. **Evaluation Metrics for Performance Assessment**
   - Confusion matrix analysis
   - Primary metric selection
   - Classification: Precision, Recall, F1, ROC-AUC
   - Regression: RMSE, R², MAE
   - Clustering: Silhouette score
   - Training vs. validation comparison

5. **Overall Strategy for the Data Science Solution**
   - Best model selection
   - Planned data product (dashboard/web app)
   - System workflow design
   - Stakeholder usability
   - Future enhancements

### Modeling Strategy

**Three Parallel Tracks:**

**Track 1: Classification (Mismatch Category Prediction)**
- **Target:** Income-Rent Mismatch Category (3 classes)
- **Challenge:** Class imbalance (10% minority classes)
- **Models:** Logistic Regression, Random Forest, XGBoost, SVM
- **Primary Metric:** Macro-averaged F1-score

**Track 2: Regression (Rent Waste Score Prediction)**
- **Target:** Comprehensive Rent Waste Score (0-100)
- **Challenge:** Right-skewed distribution
- **Models:** Linear Regression, Ridge/Lasso, Random Forest, Gradient Boosting
- **Primary Metric:** RMSE

**Track 3: Clustering (Market Segmentation)**
- **Target:** Unsupervised grouping of similar markets
- **Challenge:** Interpretability for city planners
- **Models:** K-Means, Hierarchical, DBSCAN
- **Primary Metric:** Silhouette score

### Dataset Ready

**Source:** D3 EDA final dataset  
**File:** `data/final_dataset_with_boom_index.csv`  
**Dimensions:** 1,766 ZIP codes × 55 features  
**Quality:** 100% complete cases

**Features Available:**
- 37 original features (demographics, housing, economic, transportation)
- 18 engineered features (mismatch indexes, rent waste metrics, boom indicators)

### Key Insights from D3 EDA Informing Model Selection

1. **Non-Linear Relationships** → Favor tree-based models
2. **Class Imbalance** → Need SMOTE or class weighting
3. **High Feature Correlations** → May need feature selection
4. **Geographic Patterns** → Consider stratified sampling
5. **Skewed Distributions** → May need transformations

### Next Steps

**Immediate Actions:**
1. Create data preprocessing script
2. Implement train/validation/test split
3. Build baseline models (Logistic Regression, Linear Regression, K-Means)
4. Establish evaluation framework
5. Document all decisions for D4 report

**Timeline:**
- Week 1: Data prep + baseline models
- Week 2: Advanced models + hyperparameter tuning
- Week 3: Evaluation + comparison + report writing
- Week 4: Final review + submission

---

## Progress Log

### Session 1 - March 11, 2026

**Completed:**
- ✅ Created D4 project structure
- ✅ Copied dataset from D3 EDA
- ✅ Created README.md with project overview
- ✅ Reviewed D4 requirements
- ✅ Defined modeling strategy

**Next Session Goals:**
- Create data preprocessing script
- Implement baseline models
- Set up evaluation framework

---

*This log will track all progress, decisions, and prompts for Deliverable 4.*


---

## Session 2 - March 11, 2026 (Continued)

### Matthew's Strategic Decisions:

**1. Regression Focus** ✅
- Predict expected rent → Find residuals → Identify biggest discrepancies
- More nuanced than classification - shows MAGNITUDE of problem

**2. Train on All 14 Cities** ✅
- Maximize training data
- Include Jacksonville in training set

**3. Weighted Regression Approach** ✅
- 3x weight for outliers (top/bottom 10%)
- Uses real data only (no synthetic SMOTE)
- City planners trust authentic data

**4. Model Comparison Strategy** ✅
- Tier 1: Linear Regression (baseline)
- Tier 2: Ridge Regression (handle correlations)
- Tier 3: Random Forest (handle non-linearity)
- Tier 4: XGBoost (best accuracy)

### Data Preparation Completed ✅

**Script:** `scripts/preprocessing/prepare_data.py`

**Results:**
- Dataset: 1,766 ZIP codes × 56 features
- Target: Median Home Rent ($485 - $3,473)
- Outliers identified: 353 ZIP codes (20% total)
  - Low rent (<$960): 177 ZIP codes
  - High rent (>$2,287): 176 ZIP codes
- Sample weights: 3x for outliers, 1x for normal

**Data Splits:**
- Training: 1,147 samples (65%)
- Validation: 265 samples (15%)
- Test: 354 samples (20%)
- Stratified by city for geographic balance

**Feature Scaling:**
- StandardScaler fitted on training data only
- Prevents data leakage

**Issue Identified:**
- 54 missing values in 6 features (income-related)
- Need to handle before modeling

**Files Created:**
- `results/prepared_data/train_data.csv`
- `results/prepared_data/val_data.csv`
- `results/prepared_data/test_data.csv`
- `results/prepared_data/scaler.pkl`
- `results/prepared_data/feature_list.txt`

### Next Steps:
1. Handle missing values (imputation or drop features)
2. Build Tier 1: Linear Regression baseline
3. Build Tier 2: Ridge Regression
4. Build Tier 3: Random Forest
5. Build Tier 4: XGBoost
6. Compare all models
7. Analyze residuals for biggest discrepancies


### Data Leakage Issue Resolved ✅

**Problem Identified:** Initial models showed perfect performance (RMSE=$0, R²=1.0)
- Engineered features from D3 were calculated FROM the target variable (rent)
- Features like `Total_Monthly_Location_Cost`, `Time_Value_Rent_Waste`, `Commute_Rent_Mismatch` all included rent

**Solution:** Removed ALL 18 engineered features
- Using only 31 original features from raw data sources
- Clean data with no leakage

### Baseline Models Trained ✅

**Script:** `scripts/training/train_baseline_models.py`

**Results with Clean Data:**

| Model | Val RMSE | Val R² | Val MAE | Training Time |
|-------|----------|--------|---------|---------------|
| Linear Regression | $1,089 | -1.53 | $448 | 0.01s |
| Ridge Regression | $933 | -0.86 | $434 | 0.01s |

**Key Insights:**
- Negative R² means models perform worse than predicting the mean
- Significant overfitting (training RMSE ~$413, validation RMSE ~$933-$1,089)
- Linear models are INSUFFICIENT for this problem ✅
- This justifies moving to complex models (Random Forest, XGBoost)

**Top Features (Ridge Regression):**
1. Income 49% Below Poverty (+$794)
2. Public Transit Usage (+$772)
3. Housing Built pre-1940 (-$582)
4. Income 125-149% Poverty (-$444)
5. Housing Built 2010-2019 (-$339)

**Next:** Train Tier 3 (Random Forest) and Tier 4 (XGBoost) to capture non-linear relationships


### Advanced Models Trained ✅

**Script:** `scripts/training/train_advanced_models.py`

**Results:**

| Model | Val RMSE | Val R² | Val MAE | Improvement |
|-------|----------|--------|---------|-------------|
| Linear Regression | $1,089 | -1.53 | $448 | Baseline |
| Ridge Regression | $933 | -0.86 | $434 | Baseline |
| Random Forest | $322 | 0.66 | $244 | 65.5% better |
| XGBoost | $292 | 0.72 | $211 | 68.7% better |

**Key Insights:**
- XGBoost is the BEST model (lowest RMSE, highest R²)
- Advanced models capture non-linear relationships successfully
- 68.7% reduction in error compared to Ridge Regression
- Validation R² = 0.72 means model explains 72% of rent variation

**Top Features (XGBoost):**
1. Median Household Income (42%)
2. Renter Excessive Housing Costs (7%)
3. Per Capita Income (7%)
4. Public Transit Usage (7%)
5. Home Owner Excessive Housing Costs (4%)

### Residual Analysis Completed ✅

**Script:** `scripts/evaluation/analyze_residuals.py`

**Biggest Rent Discrepancies (Test Set):**

**🔴 UNDERPRICED (Good Deals):**
- San Antonio ZIP 78248: $669 savings (49% below expected)
- Louisville ZIP 40023: $628 savings (53% below expected)
- Philadelphia ZIP 19031: $610 savings (44% below expected)

**🔵 OVERPRICED (Expensive):**
- San Francisco ZIP 94514: $1,680 premium (63% above expected)
- Philadelphia ZIP 19041: $1,184 premium (35% above expected)
- Austin ZIP 78739: $1,144 premium (33% above expected)

**City-Level Patterns:**
- San Francisco: Most overpriced (+$281 avg)
- Louisville: Most underpriced (-$184 avg)
- Orlando: Most accurate predictions ($145 avg error)

**Files Created:**
- `models/regression/random_forest.pkl`
- `models/regression/xgboost.pkl`
- `results/metrics/all_models_comparison.csv`
- `results/metrics/random_forest_feature_importance.csv`
- `results/metrics/xgboost_feature_importance.csv`
- `results/metrics/test_set_predictions.csv`
- `results/metrics/city_level_residuals.csv`
- `results/plots/residual_analysis.png`
- `results/plots/feature_importance_comparison.png`
- `results/plots/model_comparison.png`

### Next Steps:
1. Write D4 Model Solutions Report
2. Document modeling decisions and justifications
3. Create final presentation materials
