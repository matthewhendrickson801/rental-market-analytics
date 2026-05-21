# D4 Modeling - Directory Structure

**Last Updated:** April 1, 2026  
**Status:** ✅ Organized and Ready for Final Submission

---

## 📁 Root Directory

```
d4_modeling/
├── CAP4922-D4-ModelSolutions.txt          # Assignment requirements
├── SUBMISSION_PACKAGE_CONTENTS.txt        # ZIP package contents list
├── DIRECTORY_STRUCTURE.md                 # This file
│
├── 📂 docs/                               # All documentation
├── 📂 data/                               # Datasets and predictions
├── 📂 models/                             # Trained models
├── 📂 scripts/                            # Python scripts
├── 📂 results/                            # Model metrics
├── 📂 visualizations/                     # Charts and graphs
├── 📂 dashboard/                          # Streamlit dashboard
├── 📂 notebooks/                          # Jupyter notebooks
└── 📂 reports/                            # Old reports folder
```

---

## 📄 Documentation (docs/)

### Deliverable Files (docs/deliverable/)
**Main submission documents for grading:**
- `D4_MODEL_SELECTION_REPORT.md` - **PRIMARY DELIVERABLE** (54KB, 1,060 lines)
- `D4_EXECUTIVE_SUMMARY.md` - 1-page overview for StateofJax
- `D4_SUBMISSION_CHECKLIST.md` - Requirements verification
- `D4_FINAL_SUBMISSION_GUIDE.md` - Complete submission instructions

### Reports (docs/reports/)
**Analysis reports for StateofJax:**
- `DUVAL_COUNTY_ONLY_REPORT.md` - **FINAL** - 31 core Duval County ZIPs only
- `DUVAL_COUNTY_JACKSONVILLE_REPORT.md` - Earlier version with 51 ZIPs
- `JACKSONVILLE_AFFORDABILITY_REPORT.md` - Jacksonville-specific analysis
- `BEST_WORST_DEALS_SUMMARY.md` - Multi-city best/worst deals
- `TOP_DEALS_ANALYSIS.md` - Top affordable opportunities

### Guides (docs/guides/)
**Quick reference and how-to documents:**
- `QUICK_REFERENCE_D4.md` - Key facts and elevator pitches
- `QUICK_START.md` - Getting started guide
- `QUICK_RESULTS_SUMMARY.md` - Results summary
- `STARTING_WITH_D4.md` - Initial setup guide
- `README.md` - Project overview

### Archive (docs/archive/)
**Historical/experimental documents:**
- `WHY_73_R2_IS_GOOD.md` - R² justification (old)
- `IMPROVEMENT_STRATEGIES.md` - Model improvement experiments
- `STRATIFIED_WEIGHTING_RESULTS.md` - Weighting experiments

---

## 📊 Data (data/)

### Main Datasets
- `final_dataset_no_military.csv` - Training data (1,738 ZIPs, 28 excluded)
- `removed_military_zips.csv` - 16 military base exclusions
- `removed_retirement_zips.csv` - 12 retirement community exclusions
- `removed_anomalous_zips.csv` - Additional analysis
- `removed_rural_zips.csv` - Rural ZIP reference

### Dashboard Data
- Located in `dashboard/data/dashboard_data.csv`
- Contains all predictions for 1,738 ZIPs including 54 Jacksonville

---

## 🤖 Models (models/)

### Trained Models
- `regression/xgboost.pkl` - **FINAL MODEL** (R²=0.757, RMSE=$241)
- `regression/random_forest.pkl` - Random Forest (R²=0.709)
- `regression/linear_regression.pkl` - Linear baseline (failed)
- `regression/ridge_regression.pkl` - Ridge baseline (failed)

---

## 📈 Results (results/)

### Metrics
- `metrics/all_models_comparison.csv` - Performance comparison
- `metrics/xgboost_feature_importance.csv` - Feature rankings
- `metrics/xgboost_metrics.json` - Detailed XGBoost metrics

### Predictions
- `predictions/xgboost_predictions.csv` - All ZIP predictions
- `predictions/xgboost_residuals.csv` - Prediction errors

---

## 📊 Visualizations (visualizations/)

### D4 Submission Visuals (visualizations/d4/)
**6 required visualizations:**
1. `01_model_comparison.png` - XGBoost vs. other models
2. `02_feature_importance.png` - Top 15 features
3. `03_train_val_test_performance.png` - Performance across splits
4. `04_jacksonville_affordability_distribution.png` - 5 categories
5. `05_jacksonville_top_opportunities.png` - Top 5 affordable vs. overpriced
6. `06_data_exclusions.png` - 28 excluded ZIPs summary

### Other Visuals
- `eda/` - Exploratory data analysis charts
- `model_performance/` - Additional model charts

---

## 🖥️ Dashboard (dashboard/)

### Streamlit App
- `app.py` - Main dashboard application
- `prepare_dashboard_data.py` - Data preparation script
- `data/dashboard_data.csv` - Dashboard dataset

**Run Dashboard:**
```bash
cd d4_modeling/dashboard
streamlit run app.py
```

---

## 🐍 Scripts (scripts/)

### Preprocessing
- `preprocessing/prepare_data.py` - Main data preparation
- `preprocessing/add_geographic_features.py` - Geographic features
- `preprocessing/prepare_data_original_features.py` - Original features

### Training
- `training/train_baseline_models.py` - Linear/Ridge models
- `training/train_advanced_models.py` - Random Forest/XGBoost
- `training/tune_xgboost.py` - Hyperparameter tuning
- `training/test_model_improvements.py` - Model experiments

### Evaluation
- `evaluation/analyze_residuals.py` - Residual analysis
- `evaluation/evaluate_models.py` - Model evaluation

### Visualization
- `visualization/create_d4_visuals.py` - D4 submission visuals
- `visualization/create_eda_visuals.py` - EDA charts

### Analysis
- `analysis/find_anomalous_clusters.py` - Anomaly detection
- `analysis/analyze_jacksonville.py` - Jacksonville analysis

---

## 📓 Notebooks (notebooks/)

### Jupyter Notebooks
- `01_eda.ipynb` - Exploratory data analysis
- `02_feature_engineering.ipynb` - Feature creation
- `03_model_training.ipynb` - Model training experiments
- `04_model_evaluation.ipynb` - Model evaluation

---

## 🎯 Key Files for Submission

### Must Submit
1. **D4_MODEL_SELECTION_REPORT.md** (convert to PDF/Word)
   - Location: `docs/deliverable/D4_MODEL_SELECTION_REPORT.md`
   - Size: 54KB, 1,060 lines, 40 sections

2. **6 Visualizations** (embed or attach)
   - Location: `visualizations/d4/*.png`

3. **Executive Summary** (optional appendix)
   - Location: `docs/deliverable/D4_EXECUTIVE_SUMMARY.md`

### For StateofJax
- **DUVAL_COUNTY_ONLY_REPORT.md** - 31 core Duval County ZIPs
  - Location: `docs/reports/DUVAL_COUNTY_ONLY_REPORT.md`

---

## 🚀 Quick Commands

### Run Model Training
```bash
python d4_modeling/scripts/training/train_advanced_models.py
```

### Generate Visualizations
```bash
python d4_modeling/scripts/visualization/create_d4_visuals.py
```

### Start Dashboard
```bash
cd d4_modeling/dashboard && streamlit run app.py
```

### Prepare Data
```bash
python d4_modeling/scripts/preprocessing/prepare_data.py
```

---

## 📦 Submission Package

**ZIP File:** `D4_Submission_Package_TeamWMK.zip` (1.4 MB)
- Located in workspace root
- Contains all deliverable files, visualizations, data, and models
- Ready for submission

**Contents:**
- Main report and supporting documents
- 6 visualizations
- Data files (predictions, exclusions)
- Trained model
- README and guides

---

## 🎓 Project Summary

**Team:** WMK (Matthew Hendrickson, William Hughes, Khanh Linh Lieu)  
**Stakeholder:** StateofJax (Non-Profit Organization)  
**Model:** XGBoost (R²=0.757, RMSE=$241)  
**Dataset:** 1,738 ZIP codes across 14 cities  
**Jacksonville Focus:** 54 ZIPs analyzed (31 core Duval County)  
**Deployment:** UNF Computer Science Symposium, December 2026

---

## ✅ Status Checklist

- [x] Directory structure organized
- [x] All documentation in `docs/`
- [x] Main deliverable ready (`D4_MODEL_SELECTION_REPORT.md`)
- [x] 6 visualizations created
- [x] Duval County report for StateofJax
- [x] Submission package created (ZIP)
- [x] Dashboard functional
- [x] Model trained and saved
- [x] Data cleaned and documented

**Status:** ✅ READY FOR FINAL SUBMISSION

---

**Last Updated:** April 1, 2026  
**Next Steps:** Convert main report to PDF/Word and submit by deadline
