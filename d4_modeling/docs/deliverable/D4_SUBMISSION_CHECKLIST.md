# Deliverable 4 - Submission Checklist

## ✅ Completed Items

### Required Sections

- [x] **Team Information**
  - Team Name: Team WMK
  - Team Members: Matthew Hendrickson, William Hughes, Khanh Linh Lieu
  - Project Title: Affordable Housing Detection in Jacksonville Using Multi-City Rental Market Analysis
  - Stakeholder: StateofJax (Non-Profit Organization)

- [x] **Project Overview** (5 points)
  - Jacksonville-focused affordable housing detection
  - StateofJax partnership context
  - Multi-city training approach (14 cities → Jacksonville insights)
  - Specific Census Bureau data sources (ACS 5-Year, table numbers)

- [x] **Justification for Machine Learning Models** (10 points individual + 10 team)
  - XGBoost selected as primary model
  - Comparison with Linear, Ridge, Random Forest, Gradient Boosting
  - Occam's Razor justification (complexity vs. performance)
  - Model assumptions and data challenge handling
  - Training time vs. prediction latency trade-offs
  - Why simple models (Linear Regression) were insufficient
  - Detailed exclusion rationale (16 military + 12 retirement = 28 ZIPs)

- [x] **Input Variables and Feature Selection** (10 points individual + 10 team)
  - 38 features across 8 categories documented
  - Link to D3 EDA analysis
  - Feature engineering explained (poverty_rate_pct, urban classification, region)
  - Feature selection rationale (domain knowledge + importance analysis)
  - Transformation steps (standardization, imputation, encoding)
  - Specific Census table numbers for each feature

- [x] **Training and Validation Set Details** (10 points individual + 10 team)
  - 65/15/20 split (train/val/test)
  - Stratified sampling by city
  - Cross-validation discussion (why not used for final model)
  - Overfitting mitigation (enhanced sample weighting, regularization, data exclusions)
  - Training vs. validation performance comparison
  - Detailed sample weighting strategy (2-72x multiplicative weights)

- [x] **Evaluation Metrics for Performance Assessment** (10 points individual + 10 team)
  - Primary metric: R² = 0.757
  - Secondary metrics: RMSE ($241), MAE ($182), MAPE (10%)
  - Training vs. validation vs. test comparison
  - Model failure analysis (where it struggles)
  - Jacksonville-specific performance metrics

- [x] **Overall Strategy for the Data Science Solution** (10 points individual + 5 team)
  - Best model selection (XGBoost)
  - Planned data product (Streamlit dashboard for StateofJax)
  - System workflow (data → preprocessing → inference → dashboard)
  - Usability and interpretability considerations
  - Anticipated challenges and limitations
  - How solution solves StateofJax's problem
  - Model retraining strategy (quarterly)
  - Future enhancements (UNF Symposium deployment plan)

## 📊 Key Metrics Summary

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| R² | 0.9652 | 0.7571 | 0.7459 |
| RMSE | $100 | $241 | $273 |
| MAE | $75 | $182 | $205 |
| MAPE | - | 10.0% | 9.3% |

## 🏙️ Jacksonville-Specific Results

- **ZIP codes analyzed:** 54 (out of ~127 total in metro area)
- **Market efficiency:** 97.5% (actual rents only 2.5% above predicted)
- **Highly affordable opportunities:** 2 ZIPs (32068 Middleburg -21.1%, 32091 Starke -18.2%)
- **Affordable opportunities:** 7 ZIPs (5-15% below predicted)
- **Overpriced areas:** 8 ZIPs (concentrated in St. Augustine: 32080, 32092, 32095)
- **Key finding:** Jacksonville has efficient rental market, offers affordability vs. Nashville/Tampa/Orlando

## 📝 New Sections Added

- [x] **Glossary of Technical Terms** - 20+ definitions for non-technical stakeholders
- [x] **Why These 14 Cities?** - Explains StateofJax's city selection criteria
- [x] **Jacksonville Data Coverage** - Explains why 54 ZIPs vs. ~127 total (data availability, not exclusions)
- [x] **References and Data Sources** - Complete citations for Census data, XGBoost paper, Python libraries
- [x] **Appendix A: Comprehensive Jacksonville Analysis** - All 54 ZIPs with detailed predictions, organized by affordability category
- [x] **StateofJax Action Items** - 7 specific recommendations based on Jacksonville findings

## 📁 Supporting Files

- `D4_MODEL_SELECTION_REPORT.md` - Main deliverable document (comprehensive)
- `JACKSONVILLE_AFFORDABILITY_REPORT.md` - Jacksonville-specific analysis for StateofJax
- `models/regression/xgboost.pkl` - Final trained model
- `results/metrics/all_models_comparison.csv` - Model comparison
- `results/metrics/xgboost_feature_importance.csv` - Feature importance
- `dashboard/app.py` - Interactive dashboard
- `BEST_WORST_DEALS_SUMMARY.md` - Multi-city market analysis
- `data/removed_retirement_zips.csv` - 12 retirement communities excluded
- `data/removed_military_zips.csv` - 16 military bases excluded (documented in report)

## 🎯 Assessment Points Breakdown

| Section | Individual | Team | Total |
|---------|-----------|------|-------|
| Project Overview | - | 5 | 5 |
| ML Model Justification | 10 | 10 | 20 |
| Input Variables | 10 | 10 | 20 |
| Training/Validation | 10 | 10 | 20 |
| Evaluation Metrics | 10 | 10 | 20 |
| Overall Strategy | 10 | 5 | 15 |
| **TOTAL** | **50** | **50** | **100** |

## 📝 Submission Format

- [x] Microsoft Word or PDF format (convert from markdown)
- [x] Consistent font sizes and formatting
- [x] Clear headings and organization
- [x] Cohesive narrative (not Q&A format)
- [x] Precise, active language
- [x] Citations for external data sources (U.S. Census Bureau ACS)
- [x] Jacksonville-focused context for StateofJax stakeholder

## 🚀 Next Steps for D5

1. **UNF Symposium Preparation (December 2026)**
   - Deploy dashboard to Streamlit Cloud (public access)
   - Create Jacksonville-focused landing page
   - Prepare 15-minute presentation
   - Design poster/slides highlighting StateofJax partnership

2. **Dashboard Enhancements**
   - Add Jacksonville affordability map visualization
   - Implement SHAP explanations for individual predictions
   - Create "Find Affordable Housing" search tool
   - Mobile-responsive design

3. **StateofJax Deliverables**
   - User guide for StateofJax staff
   - Tenant education materials (fair market rent values)
   - Policy brief on 8 overpriced Jacksonville ZIPs
   - Quarterly update plan

4. **Technical Documentation**
   - API documentation for potential StateofJax website integration
   - Retraining pipeline automation
   - Data quality monitoring dashboard

## 📧 Submission

Convert `D4_MODEL_SELECTION_REPORT.md` to PDF or Word document and submit by April 1, 2026.

**Supplementary Materials:**
- Include `JACKSONVILLE_AFFORDABILITY_REPORT.md` as appendix
- Reference dashboard URL (will be live for symposium)
- Provide GitHub repository link (if applicable)

---

**Prepared by:** Team WMK (Matthew Hendrickson, William Hughes, Khanh Linh Lieu)  
**For:** StateofJax Non-Profit Organization  
**Presentation:** UNF Computer Science Symposium, December 2026
