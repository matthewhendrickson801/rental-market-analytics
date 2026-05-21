# D4 Submission Package - Team WMK
## Hybrid XGBoost Model for Rent Prediction

**Submission Date:** 2026-04-08 11:52:34
**Team Members:** William, Matthew, Khanh
**Stakeholder:** StateofJax (Jacksonville Affordable Housing)

---

## 📦 Package Contents

### Models (`/models/`)
- `xgboost_hybrid.pkl` - Trained XGBoost model (R²=0.783, MAE=$174)
- `hybrid_features.txt` - List of 44 features used in the model

### Data (`/data/`)
- `master_dataset_with_housing_mix.csv` - Final cleaned dataset (1,767 residential ZIPs)

### Reports (`/reports/`)
- `Duval_County_Report.md` - Analysis of 57 Duval County ZIPs
- `Jacksonville_Metro_Report.md` - Jacksonville Metro analysis
- `Florida_State_Report.md` - Florida-wide analysis (454 ZIPs)
- `all_predictions.csv` - Predictions for all 1,767 ZIPs
- `hybrid_feature_importance.csv` - Feature importance rankings

### Visualizations (`/visualizations/`)
- `hybrid_feature_importance.png` - Top 20 features by importance
- `hybrid_actual_vs_predicted.png` - Model accuracy visualization
- `hybrid_residuals_distribution.png` - Residual distribution analysis

### Documentation (`/documentation/`)
- `HYBRID_MODEL_REPORT.md` - Complete model methodology and results
- `DATA_CLEANING_SUMMARY.md` - Data preprocessing steps
- `MODEL_COMPARISON.md` - Comparison of different modeling approaches

### Scripts (`/scripts/`)
- `train_hybrid_model.py` - Model training script (reproducible)

### Dashboard (`/dashboard/`)
- `duval_dashboard_clean.py` - Interactive Dash dashboard for Duval County

---

## 🎯 Model Performance

**Test Set Performance:**
- R² Score: 0.783
- MAE: $174
- RMSE: $234

**Jacksonville Performance:**
- MAE: $131 (excellent for target city)
- 57 ZIPs analyzed

**Top Features:**
1. is_coastal (19.6%)
2. education_high_school (15.5%)
3. beach_proximity (14.9%)
4. education_bachelors_plus (7.5%)
5. Median Household Income (7.3%)

---

## 🚀 Quick Start

### Run the Dashboard
```bash
cd dashboard
python duval_dashboard_clean.py
# Open browser to http://127.0.0.1:8050
```

### Retrain the Model
```bash
cd scripts
python train_hybrid_model.py
```

### Requirements
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn dash plotly
```

---

## 📊 Dataset Details

**Final Dataset:** 1,767 residential ZIP codes
- 14 cities across the United States
- Target city: Jacksonville, FL (57 ZIPs)

**Data Cleaning:**
- Removed 381 duplicate geoids
- Removed 45 non-residential ZIPs (commercial/military/retirement)
- Removed 201 low-population ZIPs (< 1,000 people)
- Started from 2,013 clean ZIPs → Final 1,767 ZIPs

**Feature Categories (44 total):**
- Housing characteristics (age, vacancy, units)
- Education levels (4 features from William)
- Income and employment (jobs data from Khanh)
- Commute patterns
- Geographic features (coastal, beach proximity, urban/rural)
- Housing mix indicators (luxury mix, owner/renter ratios)

**Excluded Features:**
- City and region (to avoid shortcuts)
- Tech hub scores (caused overfitting)
- Income-rent gap (too correlated with target)
- All rent-derived features

---

## 📈 Regional Reports

### Duval County Report
- 57 ZIP codes analyzed
- Top 10 over-predicted ZIPs (model thinks should be more expensive)
- Top 10 under-predicted ZIPs (model thinks should be cheaper)
- Justifications for each prediction difference

### Jacksonville Metro Report
- Same as Duval County (dataset limitation)

### Florida State Report
- 454 ZIP codes across 4 cities
- Cities: Jacksonville, Miami, Tampa, Orlando
- Comprehensive state-wide analysis

---

## 🏠 Model Approach: Hybrid Strategy

**Why Hybrid?**
- Predicts absolute rent (easy to explain to stakeholders)
- Removes regional/city features (avoids shortcuts)
- Focuses on real housing characteristics
- Residuals are meaningful for finding affordable housing

**Not Used:**
- City-normalized approach (R²=0.86 but harder to explain)
- Original model with city features (R²=0.76 but uses shortcuts)

---

## 🎓 Key Insights

1. **Coastal proximity matters** - Top feature at 19.6% importance
2. **Education drives rent** - High school and bachelor's education are top 5 features
3. **Beach proximity is granular** - Beachfront ZIPs scored 2.0, near-beach 1.0, coastal city 0.5
4. **Housing mix matters** - Luxury mix indicator helps with mixed neighborhoods
5. **Jacksonville is affordable** - Model performs well with MAE of $131

---

## 📞 Contact

For questions about this submission, contact Team WMK.

**Stakeholder:** StateofJax
**Focus:** Jacksonville affordable housing opportunities
**Goal:** Identify ZIPs where rent is lower than expected based on characteristics

---

## 🔍 How to Use Reports

1. **All ZIPs Section** - See every ZIP sorted by actual rent
2. **Over-Predicted ZIPs** - Model thinks these should be more expensive (potential value)
3. **Under-Predicted ZIPs** - Model thinks these should be cheaper (may be overpriced)
4. **Justifications** - Understand why predictions differ from actual rent

---

**Generated:** 2026-04-08 11:52:34
**Model Version:** Hybrid XGBoost v1.0
**Dataset Version:** master_dataset_with_housing_mix.csv
