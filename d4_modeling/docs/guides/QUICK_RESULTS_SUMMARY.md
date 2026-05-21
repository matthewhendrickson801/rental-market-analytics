# D4 Quick Results Summary

**Date:** March 25, 2026  
**Status:** ✅ COMPLETE

---

## 🏆 Best Model: XGBoost

- **Validation RMSE:** $292
- **Validation R²:** 0.72
- **Validation MAE:** $211
- **Training Time:** 0.40 seconds
- **Improvement:** 68.7% better than baseline

---

## 📊 Model Comparison

| Model | RMSE | R² | MAE |
|-------|------|-----|-----|
| Linear | $1,089 | -1.53 | $448 |
| Ridge | $933 | -0.86 | $434 |
| Random Forest | $322 | 0.66 | $244 |
| **XGBoost** | **$292** | **0.72** | **$211** |

---

## 🔑 Top 5 Features

1. Median Household Income (42%)
2. Renter Excessive Housing Costs (7%)
3. Per Capita Income (7%)
4. Public Transit Usage (7%)
5. Home Owner Excessive Housing Costs (4%)

---

## 💰 Biggest Rent Discrepancies

### Underpriced (Good Deals)
1. San Antonio 78248: -$669 (49% below)
2. Louisville 40023: -$628 (53% below)
3. Philadelphia 19031: -$610 (44% below)

### Overpriced (Expensive)
1. San Francisco 94514: +$1,680 (63% above)
2. Philadelphia 19041: +$1,184 (35% above)
3. Austin 78739: +$1,144 (33% above)

---

## 🌆 City Rankings

**Most Overpriced:** San Francisco (+$281 avg)  
**Most Underpriced:** Louisville (-$184 avg)  
**Most Accurate:** Orlando ($145 avg error)

---

## 📁 Key Files

**Report:** `reports/D4_Model_Solutions_Report.md`  
**Best Model:** `models/regression/xgboost.pkl`  
**Predictions:** `results/metrics/test_set_predictions.csv`  
**Visualizations:** `results/plots/`

---

## ⚡ Quick Run

```bash
cd d4_modeling
python3 scripts/preprocessing/prepare_data_original_features.py
python3 scripts/training/train_baseline_models.py
python3 scripts/training/train_advanced_models.py
python3 scripts/evaluation/analyze_residuals.py
```
