# D4 Modeling Project - Quick Start Guide

## ✅ Project Setup Complete!

Your D4 (Model Selection and Solution Approaches) project is ready to go!

---

## What's Been Created

### Directory Structure
```
d4_modeling/
├── data/                          ✅ Dataset ready (1,766 × 55 features)
├── models/                        📁 For trained models
│   ├── classification/
│   ├── regression/
│   └── clustering/
├── scripts/                       📁 For Python code
│   ├── preprocessing/
│   ├── training/
│   ├── evaluation/
│   └── visualization/
├── results/                       📁 For outputs
│   ├── metrics/
│   ├── plots/
│   └── model_artifacts/
├── reports/                       📁 For final D4 report
└── notebooks/                     📁 For Jupyter notebooks
```

### Files Ready
- ✅ `data/final_dataset_with_boom_index.csv` - Your modeling dataset
- ✅ `CAP4922-D4-ModelSolutions.txt` - Assignment requirements
- ✅ `README.md` - Complete project documentation
- ✅ `STARTING_WITH_D4.md` - Progress tracking log
- ✅ `QUICK_START.md` - This file

---

## Your Modeling Tasks

### Track 1: Classification (Mismatch Categories)
**Goal:** Predict if a ZIP code is High-Rent/Low-Income, Low-Rent/High-Income, or Balanced

**Models to Try:**
1. Logistic Regression (baseline)
2. Random Forest
3. XGBoost
4. SVM

**Challenge:** Class imbalance (10% minority classes)  
**Solution:** Use SMOTE or class weighting

### Track 2: Regression (Rent Waste Score)
**Goal:** Predict Comprehensive Rent Waste Score (0-100)

**Models to Try:**
1. Linear Regression (baseline)
2. Ridge/Lasso
3. Random Forest Regressor
4. Gradient Boosting

**Challenge:** Right-skewed distribution  
**Solution:** May need log transformation

### Track 3: Clustering (Market Segmentation)
**Goal:** Group similar rental markets for policy targeting

**Models to Try:**
1. K-Means
2. Hierarchical Clustering
3. DBSCAN

**Challenge:** Interpretability for city planners  
**Solution:** Clear cluster descriptions

---

## Next Steps

### Step 1: Install Prerequisites
```bash
pip install pandas numpy scikit-learn xgboost lightgbm matplotlib seaborn joblib
```

### Step 2: Explore the Data
```bash
cd d4_modeling
python -c "import pandas as pd; df = pd.read_csv('data/final_dataset_with_boom_index.csv'); print(df.shape); print(df.columns.tolist())"
```

### Step 3: Start Building
Create your first script in `scripts/preprocessing/`:
- Load the data
- Create train/validation/test splits
- Handle class imbalance
- Scale features

---

## D4 Requirements Checklist

Your final report must include:

- [ ] **Justification for Machine Learning Models**
  - Why you chose each model
  - Complexity vs. interpretability
  - Comparison with alternatives

- [ ] **Input Variables and Feature Selection**
  - List of features used
  - Feature engineering recap from D3
  - Feature selection techniques

- [ ] **Training and Validation Set Details**
  - Split ratios (e.g., 70/15/15)
  - Cross-validation strategy
  - How you handled class imbalance

- [ ] **Evaluation Metrics**
  - Confusion matrices
  - Precision, Recall, F1, ROC-AUC
  - RMSE, R² for regression
  - Silhouette score for clustering

- [ ] **Overall Strategy**
  - Best model selection
  - Planned dashboard/web app
  - How city planners will use it

---

## Key Insights from D3 EDA

Remember these findings when building models:

1. **93-95% correlation** between historic housing and transit
2. **176 ZIP codes (10%)** show income-rent mismatches
3. **San Francisco** has highest rent waste (80.8/100)
4. **Non-linear relationships** detected (favor tree-based models)
5. **Geographic patterns** exist (consider stratified sampling)

---

## Timeline

**Week 1 (March 11-17):** Data prep + baseline models  
**Week 2 (March 18-24):** Advanced models + tuning  
**Week 3 (March 25-31):** Evaluation + report writing  
**Week 4 (April 1):** Final submission

---

## Tips for Success

1. **Start Simple:** Build baseline models first (Logistic Regression, Linear Regression)
2. **Document Everything:** Every decision needs justification for the report
3. **Compare Fairly:** Use same train/test splits for all models
4. **Think About Users:** City planners need interpretable results
5. **Track Progress:** Update STARTING_WITH_D4.md as you go

---

## Need Help?

- **Requirements:** See `CAP4922-D4-ModelSolutions.txt`
- **Project Overview:** See `README.md`
- **Progress Log:** See `STARTING_WITH_D4.md`
- **D3 EDA Results:** See `../reports/` and `../data/final/`

---

**Ready to start modeling! 🚀**

*Due Date: April 1, 2026*