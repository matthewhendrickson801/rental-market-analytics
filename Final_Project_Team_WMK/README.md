# Final Project Package - Team WMK
## CAP 4922 Data Science Capstone

**Team Members:**
- Khanh Linh Lieu (Spatial Mismatch)
- Matthew Hendrickson (Housing Affordability)
- William Hughes (Skills Mismatch)

**Date:** April 27, 2026

---

## 📦 Package Contents

### 1. D5 Final Report Materials

**MATTHEW_D5_SECTIONS_Housing_Affordability.md**
- Complete Housing Affordability sections for D5 report
- Includes: Key Variables, Data Cleaning, EDA, Modeling, Evaluation, Discussion
- Ready to copy/paste into team's final D5 document
- Includes talking points for each section

**D5_WRITING_TEMPLATE_Team_WMK.md**
- Complete writing guide for all team members
- Section assignments (Matthew, William, Khanh)
- Talking points for every section
- Formatting requirements
- Point allocation breakdown

**generate_d5_figures.py**
- Python script to generate all 6 required figures
- Run: `python3 generate_d5_figures.py`
- Creates: D5_Figures/ directory with all images
- Figures included:
  1. Actual vs. Predicted Scatter Plot
  2. Residual Plot
  3. Residual Distribution Histogram
  4. Feature Importance Bar Chart
  5. Rent by City Box Plot
  6. Urban vs. Suburban Violin Plot

### 2. D6 Product Delivery Materials

**D6_PRODUCT_DELIVERY_README.md**
- Comprehensive README for D6 submission
- 500+ lines of documentation
- Complete setup instructions
- User tutorial
- Cloud deployment guide

**D6_SUBMISSION_CHECKLIST.md**
- Step-by-step submission guide
- ZIP file creation instructions
- Pre-submission verification
- Canvas submission template

**D6_Team_WMK_Final_Product.zip** (in parent directory)
- Complete D6 submission package
- Ready to upload to Canvas
- 1.3 MB, all components included

### 3. Summary Documents

**D5_D6_SUBMISSION_SUMMARY.md**
- Master checklist for both deliverables
- Point allocation (250 total points)
- Completion status
- Timeline and next steps

---

## 🚀 Quick Start

### For Matthew (Housing Affordability Sections)

1. **Review your sections:**
   ```bash
   open MATTHEW_D5_SECTIONS_Housing_Affordability.md
   ```

2. **Generate figures:**
   ```bash
   python3 generate_d5_figures.py
   ```
   This creates `D5_Figures/` with all 6 figures

3. **Copy sections into team's D5 report:**
   - Open your team's Google Doc or Word file
   - Copy/paste each section from MATTHEW_D5_SECTIONS_Housing_Affordability.md
   - Insert figures at appropriate locations

4. **Use talking points:**
   - Each section has bullet-point talking points
   - Use these to explain your work to the team
   - Reference these during presentation

### For the Team

1. **D5 Report Writing:**
   - Open `D5_WRITING_TEMPLATE_Team_WMK.md`
   - Follow section assignments
   - Use talking points provided
   - Matthew's sections are complete and ready

2. **D6 Submission:**
   - D6 is 100% complete
   - ZIP file is ready: `D6_Team_WMK_Final_Product.zip`
   - Just upload to Canvas before April 29

---

## 📊 Matthew's D5 Sections - Summary

### Section B: Key Variables (Housing Affordability)
**Length:** 2 pages  
**Key Points:**
- 12 features: Actual_Rent (target), Population, Bachelor's %, Income, Home Value, etc.
- Urban_Classification is dominant (47% importance)
- All features from ACS data
- Log transformations for skewed variables

### Section B: Data Cleaning & Preprocessing
**Length:** 2 pages  
**Key Points:**
- Removed 231 ZIPs with missing rent data
- Excluded military bases and retirement communities
- Log-transformed income and home value
- Created urban_classification from density
- Final dataset: 1,767 ZIPs, zero missing values

### Section B: EDA (Exploratory Data Analysis)
**Length:** 2 pages  
**Key Points:**
- Rent is right-skewed (median $1,200, mean $1,350)
- Urban rents $400 higher than suburban
- Bachelor's % strongest predictor (r=0.65)
- Jacksonville median: $1,100 (below national average)
- Housing age matters less than expected

### Section B: Modeling & Algorithmic Strategy
**Length:** 3 pages  
**Key Points:**
- Tested 4 models: Linear, Random Forest, XGBoost, Ensemble
- XGBoost won: R²=0.783, MAE=$174
- 80/20 split, 5-fold CV, grid search
- Feature importance: Urban (47%), Bachelor's (18%), Income (15%)
- Training time: 30 seconds

### Section B: Evaluation & Performance Analysis
**Length:** 3 pages  
**Key Points:**
- National: R²=0.783, MAE=$174 (exceeds targets)
- Jacksonville: R²=0.82, MAE=$131 (even better!)
- Model excels in suburban areas (MAE $120)
- Struggles with luxury ZIPs (MAE $280)
- 17 Jacksonville ZIPs with >20% discrepancy identified

### Section B: Discussion of Findings
**Length:** 3 pages  
**Key Points:**
- Urban classification dominates (47% importance)
- Education matters more than income (18% vs 15%)
- 17 overpriced ZIPs identified (280,000 residents)
- Missing crime, schools, walkability data
- 5 policy recommendations provided

**Total:** ~15 pages of content for Matthew's sections

---

## 📈 Figures Generated

All figures are created by running `generate_d5_figures.py`:

1. **Figure 1: Actual vs. Predicted Scatter**
   - Shows R²=0.783
   - Points colored by city
   - Perfect prediction diagonal line
   - ±$200 error bands

2. **Figure 2: Residual Plot**
   - Residuals vs. predicted rent
   - Random scatter (good!)
   - Colored by urban/suburban
   - Zero line reference

3. **Figure 3: Residual Distribution**
   - Histogram with normal curve
   - Mean ≈ $0, Std Dev ≈ $245
   - Approximately normal distribution
   - Slight right skew

4. **Figure 4: Feature Importance**
   - Bar chart of top 10 features
   - Urban Classification: 47%
   - Bachelor's %: 18%
   - Median Income: 15%

5. **Figure 5: Rent by City**
   - Box plots for all 14 cities
   - Jacksonville highlighted in green
   - Shows Jacksonville below national median

6. **Figure 6: Urban vs. Suburban**
   - Violin plots comparing distributions
   - Urban median: $1,500
   - Suburban median: $1,100
   - $400 premium for urban

---

## ✅ Completion Status

### D5 Final Report
- **Matthew's Sections:** ✅ 100% Complete (15 pages)
- **William's Sections:** ⏳ To be written
- **Khanh's Sections:** ⏳ To be written
- **Team Sections:** ⏳ To be written together
- **Figures:** ✅ Script ready, run to generate

**Estimated Time to Complete D5:** 6-8 hours for William and Khanh

### D6 Product Delivery
- **All Components:** ✅ 100% Complete
- **ZIP File:** ✅ Ready to submit
- **Documentation:** ✅ Comprehensive
- **Status:** Ready for Canvas upload

---

## 📝 Next Steps

### Immediate (Today - April 27)
1. ✅ Matthew: Review your sections
2. ✅ Matthew: Generate figures (`python3 generate_d5_figures.py`)
3. ⏳ Team: Meet to divide remaining D5 sections
4. ⏳ William: Write your sections (Data, Variables, Preprocessing, EDA)
5. ⏳ Khanh: Write your sections (Problem, Background, Lifecycle)

### Tomorrow (April 28)
1. ⏳ Team: Write team sections together (Executive Summary, Intro, Conclusion)
2. ⏳ Team: Compile all sections into single document
3. ⏳ Team: Insert all figures
4. ⏳ Team: Proofread and format
5. ⏳ Team: Convert to PDF

### Submission Day (April 29)
1. ⏳ Submit D5 Final Report PDF to Canvas
2. ⏳ Submit D6 ZIP file to Canvas
3. 🎉 Celebrate!

---

## 🎯 Point Breakdown

### D5 Final Report: 150 points
- Matthew's sections: ~40 points
- William's sections: ~40 points
- Khanh's sections: ~40 points
- Team sections: ~30 points

### D6 Product Delivery: 100 points
- All components complete: 100 points

**Total: 250 points**

---

## 📞 Questions?

If you have questions about:
- **Matthew's sections:** Review MATTHEW_D5_SECTIONS_Housing_Affordability.md
- **Figure generation:** Run `python3 generate_d5_figures.py --help`
- **D6 submission:** Check D6_SUBMISSION_CHECKLIST.md
- **Overall status:** Review D5_D6_SUBMISSION_SUMMARY.md

---

## 🎉 You've Got This!

Matthew's sections are complete and ready. The D6 package is done. You just need to finish the remaining D5 sections and you're ready to submit!

**Good luck, Team WMK!** 🚀

---

**Last Updated:** April 27, 2026  
**Package Version:** 1.0  
**Status:** Ready for Team Review
