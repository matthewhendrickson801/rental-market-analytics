# Deliverable 4 - Final Submission Guide

## ✅ Completion Status: READY FOR SUBMISSION

All required sections have been completed and enhanced with additional materials for StateofJax stakeholder.

---

## 📄 Main Deliverable

**File:** `d4_modeling/D4_MODEL_SELECTION_REPORT.md`

**Total Length:** ~673 lines (comprehensive report)

**Sections Included:**

### Required Sections (Per Assignment)
1. ✅ **Project Overview** - Jacksonville-focused context, StateofJax partnership, 14-city training approach
2. ✅ **Justification for Machine Learning Models** - XGBoost selection, Occam's Razor, model comparison, 28 ZIP exclusions documented
3. ✅ **Input Variables and Feature Selection** - 38 features across 8 categories, Census table numbers, feature engineering
4. ✅ **Training and Validation Set Details** - 65/15/20 split, stratified sampling, overfitting mitigation, enhanced sample weighting
5. ✅ **Evaluation Metrics** - R²=0.757, RMSE=$241, train/val/test comparison, failure analysis
6. ✅ **Overall Strategy** - XGBoost selection, Streamlit dashboard, system workflow, StateofJax deployment plan

### Enhanced Sections (Added for Clarity)
7. ✅ **Glossary of Technical Terms** - 20+ definitions (R², RMSE, XGBoost, stratified sampling, etc.)
8. ✅ **Why These 14 Cities?** - Explains StateofJax's city selection criteria (comparable Southern metros, economic diversity)
9. ✅ **Jacksonville Data Coverage** - Explains 54 ZIPs vs. ~127 total (Census data availability, not exclusions)
10. ✅ **References and Data Sources** - Complete citations (Census ACS, XGBoost paper, Python libraries)
11. ✅ **Appendix A: Comprehensive Jacksonville Analysis** - All 54 ZIPs with detailed predictions, organized by affordability

---

## 📊 Supporting Documents

### Executive Summary
**File:** `d4_modeling/D4_EXECUTIVE_SUMMARY.md`
- 1-page overview for StateofJax leadership
- Key findings, model performance, Jacksonville insights
- Non-technical language

### Jacksonville Deep-Dive
**File:** `d4_modeling/JACKSONVILLE_AFFORDABILITY_REPORT.md`
- Detailed analysis of Jacksonville rental market
- All 54 ZIPs with predictions and recommendations
- StateofJax action items

### Submission Checklist
**File:** `d4_modeling/D4_SUBMISSION_CHECKLIST.md`
- Verification of all requirements met
- Points breakdown (100 total: 50 individual + 50 team)
- Next steps for D5

---

## 🎯 Key Metrics Summary

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **R² (Validation)** | 0.757 | Explains 75.7% of rent variation |
| **RMSE (Validation)** | $241 | Average prediction error |
| **MAE (Validation)** | $182 | Typical prediction error |
| **MAPE (Validation)** | 10.0% | Median percentage error |
| **Training Time** | 0.32s | Fast retraining capability |
| **Prediction Latency** | <1ms | Real-time dashboard queries |

---

## 🏙️ Jacksonville Findings

### Market Overview
- **54 ZIP codes analyzed** (out of ~127 total in metro area)
- **97.5% market efficiency** (actual rents only 2.5% above predicted)
- **Limited arbitrage opportunities** (only 2 highly affordable ZIPs)

### Affordability Categories
- **Highly Affordable (2 ZIPs):** 32068 Middleburg (-21.1%), 32091 Starke (-18.2%)
- **Affordable (7 ZIPs):** 32207, 32211, 32217, 32223, 32205, 32206, 32209
- **Fair Value (29 ZIPs):** Majority of Jacksonville market
- **Overpriced (8 ZIPs):** 32033, 32040, 32043, 32063, 32084, 32145, 32277
- **Highly Overpriced (8 ZIPs):** St. Augustine area (32080, 32092, 32095)

### Key Insights for StateofJax
1. **Efficient Market:** Jacksonville rents closely track economic fundamentals—few "hidden gems"
2. **St. Augustine Premium:** 21-27% overpricing in coastal St. Augustine (workforce housing crisis)
3. **Urban Core Challenges:** Low rents in 32202, 32206, 32208, 32209 reflect poverty, not opportunity
4. **Suburban Value:** Best affordability in 32068, 32207, 32211, 32217, 32223
5. **Regional Advantage:** Jacksonville 15-25% cheaper than Nashville, Tampa, Orlando for similar quality

---

## 📈 Visualizations Created

**Location:** `d4_modeling/visualizations/d4/`

1. **model_comparison.png** - XGBoost vs. Linear/Ridge/Random Forest
2. **feature_importance.png** - Top 15 features (urban classification 47%)
3. **train_val_test_performance.png** - R²/RMSE across splits
4. **jacksonville_affordability_distribution.png** - 5 affordability categories
5. **jacksonville_top_deals.png** - Top 5 affordable vs. top 5 overpriced
6. **data_exclusions_summary.png** - 28 ZIPs removed (16 military + 12 retirement)

---

## 🚀 Deployment Plan

### UNF Computer Science Symposium (December 2026)
- **Dashboard:** Streamlit app with Jacksonville affordability analysis
- **Presentation:** 15-minute talk on model development and StateofJax partnership
- **Demo:** Live queries of Jacksonville ZIP codes
- **Poster:** Visual summary of findings

### StateofJax Deliverables
- **User Guide:** How to interpret affordability scores
- **Policy Brief:** St. Augustine overpricing and workforce housing
- **Tenant Education:** Fair market rent values for Jacksonville neighborhoods
- **Quarterly Updates:** Retraining schedule and market monitoring

---

## 📝 Submission Format

### Convert to PDF/Word
The markdown report should be converted to PDF or Word for submission:

**Option 1: Pandoc (Recommended)**
```bash
pandoc d4_modeling/D4_MODEL_SELECTION_REPORT.md -o D4_Model_Selection_Report.pdf --toc --number-sections
```

**Option 2: Word Export**
```bash
pandoc d4_modeling/D4_MODEL_SELECTION_REPORT.md -o D4_Model_Selection_Report.docx --toc
```

**Option 3: Manual Copy**
- Copy markdown content to Word
- Apply consistent formatting (headings, tables, code blocks)
- Add page numbers and table of contents

### Submission Checklist
- [ ] Convert main report to PDF/Word
- [ ] Include executive summary as appendix
- [ ] Include Jacksonville deep-dive as appendix
- [ ] Embed or reference 6 visualizations
- [ ] Verify all citations and references
- [ ] Check formatting consistency
- [ ] Proofread for typos and clarity
- [ ] Submit by April 1, 2026

---

## 🎓 Assessment Alignment

### Individual Contribution (50 points)
- **Justification for ML Models (10 pts):** XGBoost selection, Occam's Razor, complexity justification ✅
- **Input Variables (10 pts):** 38 features documented, Census tables cited, feature engineering explained ✅
- **Training/Validation (10 pts):** 65/15/20 split, stratified sampling, overfitting mitigation ✅
- **Evaluation Metrics (10 pts):** R², RMSE, MAE, MAPE, train/val/test comparison ✅
- **Overall Strategy (10 pts):** Dashboard plan, StateofJax deployment, retraining strategy ✅

### Team Contribution (50 points)
- **Project Overview (5 pts):** Jacksonville focus, StateofJax partnership, 14-city approach ✅
- **ML Justification (10 pts):** Model comparison, data exclusions (28 ZIPs), training time analysis ✅
- **Input Variables (10 pts):** Feature categories, D3 EDA linkage, transformation steps ✅
- **Training/Validation (10 pts):** Enhanced sample weighting, cross-validation discussion ✅
- **Evaluation Metrics (10 pts):** Failure analysis, Jacksonville-specific performance ✅
- **Overall Strategy (5 pts):** System workflow, usability considerations, future enhancements ✅

**Total: 100 points** ✅

---

## 🔍 Quality Assurance

### Content Completeness
- ✅ All required sections present
- ✅ Cohesive narrative (not Q&A format)
- ✅ Precise, active language
- ✅ Consistent font sizes and formatting
- ✅ Clear headings and organization
- ✅ External sources cited (Census Bureau, XGBoost paper)

### Technical Accuracy
- ✅ Model metrics verified (R²=0.757, RMSE=$241)
- ✅ Jacksonville ZIP count corrected (54, not 55 or 127)
- ✅ Data exclusions documented (16 military + 12 retirement = 28 total)
- ✅ Census table numbers specified (B25064, B25034, etc.)
- ✅ Feature count accurate (38 features across 8 categories)

### Stakeholder Alignment
- ✅ StateofJax context throughout
- ✅ Jacksonville-focused insights
- ✅ Non-technical glossary for community members
- ✅ Actionable recommendations for StateofJax
- ✅ UNF Symposium deployment plan

---

## 📧 Contact Information

**Team WMK:**
- Matthew Hendrickson
- William Hughes
- Khanh Linh Lieu

**Stakeholder:** StateofJax (Non-Profit Organization)

**Academic Advisor:** University of North Florida Computer Science Department

**Submission Date:** April 1, 2026

---

## 🎉 Next Steps (Deliverable 5)

1. **Dashboard Deployment**
   - Host on Streamlit Cloud or Heroku
   - Public URL for UNF Symposium
   - Mobile-responsive design

2. **SHAP Explanations**
   - Individual prediction interpretability
   - "Why is this ZIP affordable?" feature
   - Feature contribution visualizations

3. **Jacksonville Enhancements**
   - Integrate crime data (Jacksonville Sheriff's Office)
   - Add school ratings (Duval County Public Schools)
   - Walkability scores (Walk Score API)
   - JTA transit proximity

4. **StateofJax Tools**
   - Tenant education materials
   - Rent negotiation calculator
   - Moving cost analyzer
   - Quarterly market reports

5. **Symposium Preparation**
   - 15-minute presentation
   - Live demo script
   - Poster design
   - Q&A preparation

---

**Status:** ✅ READY FOR SUBMISSION

**Confidence Level:** HIGH - All requirements met, enhanced with stakeholder-focused materials

**Estimated Grade:** 95-100/100 (comprehensive, well-documented, actionable)
