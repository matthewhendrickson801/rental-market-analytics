# D4 Submission Summary - Team WMK

**Submission Date:** April 8, 2026  
**Package File:** `D4_Submission_Package_TeamWMK.zip` (0.77 MB)  
**Team Members:** William, Matthew, Khanh  
**Stakeholder:** StateofJax (Jacksonville Affordable Housing)

---

## ✅ Deliverables Included

### 1. Trained Model
- **File:** `models/xgboost_hybrid.pkl`
- **Performance:** R²=0.783, MAE=$174, Jacksonville MAE=$131
- **Features:** 44 features (housing, education, income, jobs, geographic)
- **Dataset:** 1,767 residential ZIP codes across 14 cities

### 2. Regional Reports (3 Reports)
- **Duval County Report** - 57 ZIPs analyzed
- **Jacksonville Metro Report** - Jacksonville metro analysis
- **Florida State Report** - 454 ZIPs across 4 Florida cities

Each report includes:
- All ZIPs sorted by actual rent
- Top 10 over-predicted ZIPs (model thinks should be more expensive)
- Top 10 under-predicted ZIPs (model thinks should be cheaper)
- Justifications explaining prediction differences

### 3. Complete Dataset
- **File:** `data/master_dataset_with_housing_mix.csv`
- **Size:** 1,767 residential ZIPs
- **Cleaning:** Removed duplicates, non-residential, low-population ZIPs

### 4. Predictions & Analysis
- **All predictions:** `reports/all_predictions.csv` (1,767 ZIPs)
- **Feature importance:** `reports/hybrid_feature_importance.csv`
- **Visualizations:** Feature importance chart

### 5. Documentation
- **Model Report:** Complete methodology and results
- **Data Cleaning Summary:** Preprocessing steps and decisions
- **Model Comparison:** Analysis of different approaches

### 6. Reproducible Code
- **Training script:** `scripts/train_hybrid_model.py`
- **Dashboard:** `dashboard/duval_dashboard_clean.py`

### 7. README
- Complete usage instructions
- Model performance metrics
- Quick start guide
- Contact information

---

## 🎯 Model Highlights

**Approach:** Hybrid XGBoost
- Predicts absolute rent (easy to explain to stakeholders)
- Removes regional/city features (avoids shortcuts)
- Focuses on real housing characteristics
- Meaningful residuals for finding affordable housing

**Top 5 Features:**
1. is_coastal (19.6%)
2. education_high_school (15.5%)
3. beach_proximity (14.9%)
4. education_bachelors_plus (7.5%)
5. Median Household Income (7.3%)

**Data Quality:**
- Started: 2,013 ZIPs
- Removed: 381 duplicates, 45 non-residential, 201 low-population
- Final: 1,767 residential ZIPs

---

## 📦 Package Contents

```
D4_Submission_Package_TeamWMK.zip (0.77 MB)
├── models/
│   ├── xgboost_hybrid.pkl
│   └── hybrid_features.txt
├── data/
│   └── master_dataset_with_housing_mix.csv
├── reports/
│   ├── Duval_County_Report.md
│   ├── Jacksonville_Metro_Report.md
│   ├── Florida_State_Report.md
│   ├── all_predictions.csv
│   └── hybrid_feature_importance.csv
├── visualizations/
│   └── hybrid_feature_importance.png
├── documentation/
│   ├── HYBRID_MODEL_REPORT.md
│   ├── DATA_CLEANING_SUMMARY.md
│   └── MODEL_COMPARISON.md
├── scripts/
│   └── train_hybrid_model.py
├── dashboard/
│   └── duval_dashboard_clean.py
└── README.md
```

---

## 🚀 Quick Start

### View Reports
```bash
unzip D4_Submission_Package_TeamWMK.zip
cd D4_Submission_Package
cat reports/Duval_County_Report.md
```

### Run Dashboard
```bash
cd dashboard
python3 duval_dashboard_clean.py
# Open browser to http://127.0.0.1:8050
```

### Retrain Model
```bash
cd scripts
python3 train_hybrid_model.py
```

---

## 📊 Key Results

**Jacksonville Performance:**
- 57 ZIP codes analyzed
- MAE: $131 (excellent accuracy for target city)
- Model identifies affordable housing opportunities

**State-wide Coverage:**
- Florida: 454 ZIPs across 4 cities
- All predictions available in `all_predictions.csv`

**Model Accuracy:**
- Test R²: 0.783 (realistic, not overfitting)
- Test MAE: $174
- Meaningful residuals for stakeholder analysis

---

## ✅ Submission Checklist

- [x] Trained model file (.pkl)
- [x] Feature list
- [x] Complete dataset (1,767 ZIPs)
- [x] Three regional reports (Duval, Metro, Florida)
- [x] All predictions CSV
- [x] Feature importance analysis
- [x] Visualizations
- [x] Complete documentation
- [x] Reproducible training script
- [x] Interactive dashboard
- [x] Comprehensive README
- [x] Package size: 0.77 MB (reasonable)

---

**Status:** ✅ READY FOR SUBMISSION

**Location:** `d4_modeling/D4_Submission_Package_TeamWMK.zip`
