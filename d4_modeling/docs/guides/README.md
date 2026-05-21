# D4: Model Selection and Solution Approaches

**CAP4922 - Deliverable 4**  
**Team:** WMK  
**Due Date:** April 1, 2026  
**Status:** ✅ COMPLETE

---

## Project Overview

This directory contains all work for Deliverable 4 (Model Selection and Solution Approaches). Building on the EDA from D3, we developed, trained, and evaluated machine learning models to predict rental prices and identify market discrepancies.

**Goal:** Predict expected rent based on demographic/economic features, then find ZIP codes where actual rent significantly differs from predictions.

---

## 🎯 Key Results

**Best Model:** XGBoost Regressor
- **Validation RMSE:** $292 (±$292 average error)
- **Validation R²:** 0.72 (explains 72% of rent variation)
- **Improvement:** 68.7% reduction in error vs. baseline

**Top Predictor:** Median Household Income (42% importance)

**Biggest Discrepancies:**
- **Underpriced:** San Antonio ZIP 78248 ($669 savings, 49% below expected)
- **Overpriced:** San Francisco ZIP 94514 ($1,680 premium, 63% above expected)

---

## Quick Start

### Prerequisites
```bash
pip3 install pandas numpy scikit-learn xgboost matplotlib seaborn
brew install libomp  # macOS only (for XGBoost)
```

### Run All Models
```bash
cd d4_modeling

# 1. Prepare data (31 original features only)
python3 scripts/preprocessing/prepare_data_original_features.py

# 2. Train baseline models (Linear, Ridge)
python3 scripts/training/train_baseline_models.py

# 3. Train advanced models (Random Forest, XGBoost)
python3 scripts/training/train_advanced_models.py

# 4. Analyze residuals and create visualizations
python3 scripts/evaluation/analyze_residuals.py
```

---

## Directory Structure

```
d4_modeling/
├── data/                          # Dataset from D3 EDA
│   └── final_dataset_with_boom_index.csv
├── models/
│   └── regression/               # Trained models (pkl files)
│       ├── linear_regression.pkl
│       ├── ridge_regression.pkl
│       ├── random_forest.pkl
│       └── xgboost.pkl
├── scripts/
│   ├── preprocessing/            # Data preparation
│   │   └── prepare_data_original_features.py
│   ├── training/                 # Model training
│   │   ├── train_baseline_models.py
│   │   └── train_advanced_models.py
│   └── evaluation/               # Performance assessment
│       └── analyze_residuals.py
├── results/
│   ├── prepared_data/            # Train/val/test splits
│   ├── metrics/                  # Performance metrics (CSV)
│   └── plots/                    # Visualizations (PNG)
├── reports/                       # Final D4 report
│   └── D4_Model_Solutions_Report.md
├── CAP4922-D4-ModelSolutions.txt # Requirements
├── README.md                      # This file
└── STARTING_WITH_D4.md           # Progress log
```

---

## Modeling Strategy

### Tiered Comparison Approach

We implemented a 4-tier strategy to justify model complexity:

**Tier 1: Linear Regression (Baseline)**
- **Result:** RMSE = $1,089, R² = -1.53 ❌
- **Conclusion:** Linear assumptions violated

**Tier 2: Ridge Regression (Regularized)**
- **Result:** RMSE = $933, R² = -0.86 ❌
- **Conclusion:** Regularization helps but still insufficient

**Tier 3: Random Forest (Non-Linear)**
- **Result:** RMSE = $322, R² = 0.66 ✅
- **Conclusion:** Captures non-linearity, 65.5% improvement

**Tier 4: XGBoost (State-of-the-Art)**
- **Result:** RMSE = $292, R² = 0.72 ✅✅
- **Conclusion:** Best performance, 68.7% improvement

---

## Dataset

**Source:** D3 EDA final dataset  
**File:** `data/final_dataset_with_boom_index.csv`  
**Dimensions:** 1,766 ZIP codes × 31 features (original only)  
**Target:** Median Home Rent ($485 - $3,473)

**Data Splits:**
- Training: 1,147 samples (65%)
- Validation: 265 samples (15%)
- Test: 354 samples (20%)
- Stratified by city for geographic balance

**Features:** 31 original features only (no engineered features to prevent data leakage)
- 10 Housing Age features
- 6 Economic features
- 3 Housing Market features
- 2 Population features
- 7 Income Distribution features
- 3 Transportation features

---

## Model Comparison

| Model | Val RMSE | Val R² | Val MAE | Training Time | Improvement |
|-------|----------|--------|---------|---------------|-------------|
| Linear Regression | $1,089 | -1.53 | $448 | 0.01s | Baseline |
| Ridge Regression | $933 | -0.86 | $434 | 0.01s | Baseline |
| Random Forest | $322 | 0.66 | $244 | 0.19s | 65.5% |
| **XGBoost** | **$292** | **0.72** | **$211** | **0.40s** | **68.7%** |

---

## Top Features (XGBoost)

1. Median Household Income (42%)
2. Renter Excessive Housing Costs (7%)
3. Per Capita Income (7%)
4. Public Transit Usage (7%)
5. Home Owner Excessive Housing Costs (4%)

---

## Rent Discrepancies

### Top 5 Underpriced (Good Deals)
1. San Antonio ZIP 78248: $669 savings (49% below)
2. Louisville ZIP 40023: $628 savings (53% below)
3. Philadelphia ZIP 19031: $610 savings (44% below)
4. Louisville ZIP 47114: $598 savings (71% below)
5. San Antonio ZIP 78222: $596 savings (49% below)

### Top 5 Overpriced (Expensive)
1. San Francisco ZIP 94514: $1,680 premium (63% above)
2. Philadelphia ZIP 19041: $1,184 premium (35% above)
3. Austin ZIP 78739: $1,144 premium (33% above)
4. San Francisco ZIP 94130: $1,083 premium (45% above)
5. Philadelphia ZIP 19025: $1,031 premium (34% above)

### City-Level Patterns
- **Most Overpriced:** San Francisco (+$281 avg)
- **Most Underpriced:** Louisville (-$184 avg)
- **Most Accurate:** Orlando ($145 avg error)

---

## Files Created

### Models
- `models/regression/linear_regression.pkl`
- `models/regression/ridge_regression.pkl`
- `models/regression/random_forest.pkl`
- `models/regression/xgboost.pkl`

### Metrics
- `results/metrics/baseline_models_comparison.csv`
- `results/metrics/all_models_comparison.csv`
- `results/metrics/random_forest_feature_importance.csv`
- `results/metrics/xgboost_feature_importance.csv`
- `results/metrics/test_set_predictions.csv`
- `results/metrics/city_level_residuals.csv`

### Visualizations
- `results/plots/residual_analysis.png`
- `results/plots/feature_importance_comparison.png`
- `results/plots/model_comparison.png`

### Reports
- `reports/D4_Model_Solutions_Report.md` (Comprehensive report)

---

## Contact

**Team WMK**  
**Student:** Matthew Hendrickson  
**Course:** CAP4922  
**Semester:** Spring 2026
