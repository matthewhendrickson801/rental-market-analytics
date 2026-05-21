# D5 Final Report - Writing Template & Section Assignments
## Team WMK - CAP 4922 Capstone

**Due Date:** April 29, 2026  
**Total Points:** 150 (75 individual + 75 team)  
**Format:** Microsoft Word or PDF, 12pt Times New Roman, 1-inch margins

---

## 📋 SECTION ASSIGNMENTS

### TEAM SECTIONS (Everyone Contributes)
- Title Page
- Executive Summary
- Introduction
- Conclusion & Future Work
- References

### INDIVIDUAL SECTIONS (Divide Among Team)

**Matthew's Sections (Modeling Focus):**
- Modeling & Algorithmic Strategy
- Evaluation & Performance Analysis
- Discussion of Findings & Strategic Alignment
- Technical Stack & AI Integration

**William's Sections (Data Focus):**
- Data Source Inventory & Validation
- Strategic Variable Analysis
- Data Scrubbing & Preprocessing
- Exploratory Data Analysis (EDA) & Discovery

**Khanh's Sections (Process Focus):**
- Problem Definition
- Background & Research
- The Lifecycle Process (with diagram)

---

## 📝 WRITING GUIDELINES

### Formatting Requirements
- **Font:** 12pt Times New Roman (body text)
- **Headings:** 14pt Bold (Level 1), 12pt Bold (Level 2)
- **Spacing:** Single-space within paragraphs, double-space between
- **Margins:** 1 inch all sides
- **Page Numbers:** Footer, starting after title page
- **Figures/Tables:** Numbered (Figure 1, Table 1) with captions

### Writing Style
- Use **active voice**: "The team developed..." not "It was developed..."
- Be **precise**: Include specific numbers, metrics, dates
- Stay **professional**: No casual language or first-person pronouns
- Cite **sources**: Use APA format for all references

### Length Guidelines
- Executive Summary: 250-400 words
- Each major section: 2-4 pages
- Total report: 40-50 pages

---

## 📄 SECTION TEMPLATES

---

## TITLE PAGE

```
[Center-aligned, use appropriate spacing]

CAP 4922 - Data Science Capstone Project
Deliverable 5 - Final Report

[18pt Bold]
Predictive Rent Analysis for Urban Planning:
A Machine Learning Approach to Housing Affordability in Jacksonville

[14pt]
Team WMK

Team Members:
William [Last Name]
Matthew Hendrickson
Khanh [Last Name]

Department of Computing Sciences
University of North Florida

April 29, 2026
```

---

## 1. EXECUTIVE SUMMARY (250-400 words)
**Assigned to:** TEAM (draft together)

**What to Include:**
1. **The Problem** (2-3 sentences): What challenge does this solve?
2. **The Solution** (2-3 sentences): What did you build?
3. **The Method** (2-3 sentences): How did you build it?
4. **The Results** (3-4 sentences): What did you find? Include key metrics.
5. **The Impact** (2-3 sentences): Why does this matter?

**Key Metrics to Include:**
- R² = 0.783, MAE = $174 (national)
- Jacksonville MAE = $131
- 1,767 ZIP codes, 14 cities
- 17 Jacksonville ZIPs identified for intervention

**Example Opening:**
"Housing affordability represents a critical challenge for urban planners in rapidly growing metropolitan areas. This project addresses the persistent information gap in rental market analysis by developing a machine learning solution that predicts median rent prices across 14 U.S. cities..."

---

## 2. INTRODUCTION
**Assigned to:** TEAM (draft together)

### 2.1 Contextual Landscape (1 page)
**What to Write:**
- Housing affordability crisis statistics
- Jacksonville's growth (14.8% since 2010)
- Why this problem matters
- Cost of inaction

**Sources to Cite:**
- Joint Center for Housing Studies (Harvard)
- U.S. Census Bureau population data
- StateofJax mission statement

### 2.2 The Proposed Intervention (1 page)
**What to Write:**
- XGBoost regression model description
- What makes it innovative
- Interactive dashboard features
- How it helps stakeholders

### 2.3 Mission & Parameters (1 page)
**What to Write:**
- 4 core objectives (accuracy, Jacksonville focus, interpretability, deployment)
- Success criteria for each
- Scope boundaries

### 2.4 Strategic Value (0.5 page)
**What to Write:**
- Immediate value for StateofJax
- Transferability to other cities
- Long-term impact on housing policy

---

## 3. PROBLEM DEFINITION
**Assigned to:** KHANH

### 3.1 Entity Impact & Core Friction (1 page)
**What to Write:**
- Who is StateofJax? What do they do?
- What specific problem do they face?
- 3 critical problems: resource misallocation, policy blind spots, market opacity
- Why current methods don't work

**Where to Find Info:**
- `D4_SUBMISSION_SUMMARY.txt` (StateofJax description)
- Your project proposal documents

### 3.2 The Analytical Objective (1 page)
**What to Write:**
- What type of model? (predictive regression)
- What does it predict? (median rent)
- What is the data product? (dashboard)
- How will stakeholders use it?

### 3.3 Performance Benchmarks (1 page)
**What to Write:**
- **Technical:** R² ≥ 0.75, MAE ≤ $200
- **Functional:** Stakeholder validation, actionability
- **Operational:** Implementation timeline, policy influence

**Format as Table:**
```
| Dimension | Metric | Target | Actual |
|-----------|--------|--------|--------|
| Technical | R² | ≥ 0.75 | 0.783 |
| Technical | MAE | ≤ $200 | $174 |
```

### 3.4 Operational Boundaries (1 page)
**What to Write:**
- **Assumptions:** 4 key assumptions about data and markets
- **Constraints:** Data availability, temporal scope, feature limitations, geographic scope

**Where to Find Info:**
- `FINAL_MODEL_REPORT.md` (limitations section)

---

## 4. BACKGROUND & RESEARCH
**Assigned to:** KHANH

### 4.1 The Current Landscape (1.5 pages)
**What to Write:**
- Hedonic pricing models (Rosen 1974, Sirmans et al. 2005)
- Comparative Market Analysis (CMA)
- Automated Valuation Models (Zillow, Redfin)
- Typical R² values and methods

**Sources to Find:**
- Google Scholar: "hedonic pricing rental housing"
- Zillow research papers
- Real estate valuation textbooks

### 4.2 Gap Analysis (1 page)
**What to Write:**
- Data accessibility problem (proprietary MLS data)
- Granularity mismatch (property vs. neighborhood)
- Interpretability vs. performance trade-off

### 4.3 Technical Justification (1 page)
**What to Write:**
- Why public ACS data?
- Why XGBoost?
- Why cross-city learning?
- How this bridges the gaps

### 4.4 Core Concepts & Frameworks (0.5 page)
**What to Write:**
- Urban classification definition
- Rent burden (HUD 30% threshold)
- Market efficiency theory
- Feature engineering basics

---

## 5. THE LIFECYCLE PROCESS
**Assigned to:** KHANH

### 5.1 Discovery & Acquisition (0.5 page)
**What to Write:**
- How you identified ACS as data source
- Census API usage
- Data download process

### 5.2 Data Refinement & Scrubbing (0.5 page)
**What to Write:**
- Cleaning protocols
- Handling missing values
- Outlier detection

### 5.3 Exploratory Discovery & Feature Insight (0.5 page)
**What to Write:**
- Initial correlation analysis
- Feature importance discovery
- Insights that shaped model choice

### 5.4 Methodological Modeling & Validation (0.5 page)
**What to Write:**
- Model selection process
- Training/validation split
- Hyperparameter tuning

### 5.5 Interpretation & Synthesis (0.5 page)
**What to Write:**
- How you translated results to insights
- Dashboard development
- Stakeholder feedback integration

### 5.6 Lifecycle Diagram (REQUIRED)
**Create a flowchart showing:**
- 5 phases above
- Feedback loops (e.g., EDA → back to cleaning)
- Tools used at each stage
- Use PowerPoint, draw.io, or Lucidchart

**Example structure:**
```
[Data Acquisition] → [Data Cleaning] → [EDA] → [Modeling] → [Deployment]
         ↑                ↓              ↓          ↓
         └────────────────┴──────────────┴──────────┘
              (Feedback loops)
```

---

## 6. TECHNICAL STACK & AI INTEGRATION
**Assigned to:** MATTHEW

### 6.1 Core Programming & Frameworks (1 page)
**What to Write:**
- Python 3.9
- pandas, numpy, scikit-learn, XGBoost
- matplotlib, seaborn, plotly
- Jupyter notebooks

**Where to Find Info:**
- `requirements.txt`
- Your actual code files

### 6.2 Infrastructure & Platforms (0.5 page)
**What to Write:**
- Local development (MacBook Air M1, 8GB RAM)
- GitHub for version control
- No cloud infrastructure (yet)

### 6.3 Generative AI Utilization & Disclosure (1 page)
**CRITICAL SECTION - Be Honest:**

**What to Write:**
- **Application Areas:** Where did you use AI?
  - Code generation (Kiro AI for boilerplate)
  - Debugging (error message interpretation)
  - Documentation (docstring generation)
  - Report writing (structure and formatting)
  
- **Validation Protocol:** How did you verify AI outputs?
  - All code manually reviewed
  - All code tested with real data
  - All metrics independently verified
  - All documentation fact-checked

**Example:**
"The team utilized Kiro AI, an AI-powered coding assistant, for code generation, debugging, and documentation. Specifically, AI was used to generate boilerplate data loading functions, interpret error messages during model training, and create initial docstrings for functions. All AI-generated code was manually reviewed by team members, tested against real data, and modified as needed to ensure correctness and efficiency. The team maintains full intellectual responsibility for all final outputs."

---

## 7. DATA SOURCE INVENTORY & VALIDATION
**Assigned to:** WILLIAM

### 7.1 Primary Data Source (2 pages)
**For American Community Survey data, document:**

**Provenance & Authenticity:**
- Source: U.S. Census Bureau
- Dataset: American Community Survey 2020-2024 (5-year estimates)
- URL: https://data.census.gov
- Retrieval date: [your date]
- Reputation: Federal government, gold standard for demographic data

**Unit of Analysis:**
- Individual record = one ZIP code (ZCTA)
- Geographic level: ZIP Code Tabulation Area
- Temporal coverage: 2020-2024 pooled estimates

**Technical Profile & Scale:**
- Format: CSV
- Records: 1,767 ZIP codes (after cleaning)
- Original: 1,998 ZIP codes
- Variables: 23 columns
- Size: 1.2 MB
- Schema: [list key columns]

**Strategic Relevance:**
- Why ACS? Comprehensive, free, reliable
- What variables? Rent, income, education, housing characteristics
- Literature support: Cite 2-3 papers using ACS for housing research

**Ethics, Privacy & Governance:**
- License: Public domain (U.S. Government)
- Privacy: Aggregated data, no PII
- Compliance: No restrictions on use

**Where to Find Info:**
- `cleaned_rent_dataset_COMPLETE.csv`
- Census Bureau ACS documentation
- `TEAM_DATA_PREPROCESSING_REPORT.md`

---

## 8. STRATEGIC VARIABLE ANALYSIS
**Assigned to:** WILLIAM

### 8.1 Variable Taxonomy & Metadata (1 page)
**Create a table:**

| Variable | Type | Definition | Range |
|----------|------|------------|-------|
| actual_rent | Continuous | Median gross rent | $400-$4,000 |
| population | Continuous | Total population | 500-50,000 |
| bachelors_pct | Continuous | % with bachelor's+ | 5%-80% |
| median_income | Continuous | Median household income | $20K-$200K |
| urban_classification | Binary | Urban (1) vs Suburban (0) | 0 or 1 |

**Where to Find Info:**
- `FINAL_MODEL_REPORT.md` (features section)
- Your actual CSV file headers

### 8.2 Source Attribution (0.5 page)
**What to Write:**
- All variables from ACS
- Specific ACS table numbers (e.g., B25064 for rent)

### 8.3 Selection Rationale (1 page)
**What to Write:**
- Why these 12 features?
- Literature support (cite papers)
- Correlation with target variable
- Domain knowledge (what planners care about)

### 8.4 Feature Engineering (1 page)
**What to Write:**
- `urban_classification`: How created (density threshold)
- Log transformations: Why needed (skewed distributions)
- Interaction terms: If any
- Normalization: StandardScaler

**Where to Find Info:**
- `train_final_model.py` (feature engineering code)
- `FINAL_MODEL_REPORT.md`

### 8.5 Statistical Profiles (1 page)
**What to Write:**
- Distribution of rent (mean, median, std dev)
- Correlation matrix insights
- Key relationships discovered

**Include Figures:**
- Figure 1: Rent distribution histogram
- Figure 2: Correlation heatmap

**Where to Find Info:**
- `results/visualizations/` folder
- Run basic pandas `.describe()` on your data

---

## 9. DATA SCRUBBING & PREPROCESSING
**Assigned to:** WILLIAM

### 9.1 Integrity & Remediation Strategy (1 page)
**What to Write:**
- Missing values: How many? Which variables?
- Decision: Removed 231 ZIP codes with missing data
- Rationale: Model requires complete cases
- Outliers: Kept (represent real extremes)

**Where to Find Info:**
- `clean_team_data.py`
- `TEAM_DATA_PREPROCESSING_REPORT.md`

### 9.2 Feature Transformation & Scaling (1 page)
**What to Write:**
- Log transformations: income, home_value (right-skewed)
- StandardScaler: All continuous features
- Why: XGBoost benefits from normalized features

### 9.3 Encoding & Vectorization (0.5 page)
**What to Write:**
- One-hot encoding: city variable (14 cities → 14 binary columns)
- Binary encoding: urban_classification (already 0/1)

### 9.4 Optimization & Feature Selection (0.5 page)
**What to Write:**
- Removed multicollinear features (VIF > 10)
- Feature importance from initial model
- Final feature set: 12 features

### 9.5 Technical Rationale & Impact (0.5 page)
**What to Write:**
- Before preprocessing: R² = 0.68
- After preprocessing: R² = 0.78
- Improvement: +0.10 R² (15% better)

---

## 10. EXPLORATORY DATA ANALYSIS (EDA) & DISCOVERY
**Assigned to:** WILLIAM

### 10.1 Distributional Profiling (1 page)
**What to Write:**
- Rent distribution: Median $1,200, Mean $1,350, Std Dev $450
- Right-skewed (some luxury ZIPs)
- Income distribution: Similar pattern
- Test for normality: Shapiro-Wilk test results

**Include Figure:**
- Figure 3: Rent distribution histogram with normal curve overlay

### 10.2 High-Impact Visual Interrogation (1 page)
**What to Write:**
- Box plots by city: Jacksonville median $1,100
- Violin plots by urban classification: Urban $1,500 vs Suburban $1,000
- Density plots: Identify multimodal distributions

**Include Figures:**
- Figure 4: Box plot of rent by city
- Figure 5: Violin plot urban vs suburban

### 10.3 Relational & Multivariate Dynamics (1 page)
**What to Write:**
- Correlation matrix: Top correlations with rent
  - urban_classification: r = 0.72
  - bachelors_pct: r = 0.65
  - median_income: r = 0.58
- Scatter plots: Rent vs. income (positive relationship)
- Multicollinearity check: VIF scores

**Include Figure:**
- Figure 6: Correlation heatmap

### 10.4 Discovery Synthesis (0.5 page)
**What to Write:**
- Key insight: Urban classification most predictive
- Surprise: Housing age less important than expected
- Decision: Focus on demographic features over physical housing characteristics

**Where to Find Info:**
- Run your own EDA in Jupyter notebook
- `FINAL_MODEL_REPORT.md` (EDA section)

---

## 11. MODELING & ALGORITHMIC STRATEGY
**Assigned to:** MATTHEW

### 11.1 Candidate Model Evaluation (1.5 pages)
**What to Write:**
- Models considered:
  1. Linear Regression (baseline)
  2. Random Forest
  3. XGBoost
  4. Ensemble (XGBoost + RF)

**Create comparison table:**

| Model | R² | MAE | RMSE | Training Time |
|-------|-----|-----|------|---------------|
| Linear Regression | 0.682 | $245 | $325 | 2 sec |
| Random Forest | 0.761 | $189 | $268 | 45 sec |
| XGBoost | 0.783 | $174 | $245 | 30 sec |
| Ensemble | 0.779 | $178 | $248 | 75 sec |

**Where to Find Info:**
- `MODEL_COMPARISON.md`
- `final_model_comparison.py`

### 11.2 Methodological Justification (1 page)
**What to Write:**
- Why XGBoost won:
  - Best R² (0.783)
  - Lowest MAE ($174)
  - Handles non-linear relationships
  - Feature importance built-in
  - Reasonable training time
- Trade-offs: Less interpretable than linear, but SHAP values help

### 11.3 Model Input & Feature Engineering (1 page)
**What to Write:**
- Final 12 features used
- Why these features?
- Feature importance rankings:
  - urban_classification: 47%
  - bachelors_pct: 18%
  - median_income: 15%
  - [continue for top 5]

**Include Figure:**
- Figure 7: Feature importance bar chart

**Where to Find Info:**
- `results/visualizations/feature_importance.png`

### 11.4 Training Protocol & Optimization (1.5 pages)
**What to Write:**

**Data Partitioning:**
- 80/20 train/test split
- Stratified by city (ensure all cities in both sets)
- Random seed: 42 (for reproducibility)

**Hyperparameter Tuning:**
- Method: Grid search with 5-fold cross-validation
- Parameters tuned:
  - n_estimators: [100, 300, 500]
  - max_depth: [3, 6, 9]
  - learning_rate: [0.01, 0.05, 0.1]
- Best parameters: n_estimators=500, max_depth=6, learning_rate=0.05

**Technical Environment:**
- Python 3.9
- XGBoost 1.7.6
- scikit-learn 1.3.0
- Hardware: MacBook Air M1, 8GB RAM

**Where to Find Info:**
- `train_final_model.py` (hyperparameters in code)
- `FINAL_MODEL_REPORT.md`

### 11.5 Interim Performance Monitoring (0.5 page)
**What to Write:**
- Learning curves: Training vs. validation R² over epochs
- Early stopping: Stopped at 500 trees (no improvement after)
- Overfitting check: Train R² = 0.89, Test R² = 0.78 (acceptable gap)

---

## 12. EVALUATION & PERFORMANCE ANALYSIS
**Assigned to:** MATTHEW

### 12.1 Quantitative Performance Metrics (1 page)
**What to Write:**

**National Model (1,767 ZIPs):**
- R² = 0.783 (explains 78.3% of variance)
- MAE = $174 (average error)
- RMSE = $245 (penalizes large errors)
- MAPE = 12.8% (percentage error)

**Jacksonville Model (57 ZIPs):**
- R² = 0.82
- MAE = $131
- RMSE = $185

**Comparison to Baseline:**
- Linear Regression: R² = 0.682
- Improvement: +0.101 R² (14.8% better)

**Where to Find Info:**
- `FINAL_MODEL_REPORT.md`
- `Jacksonville_Final_Report.md`

### 12.2 Visual Diagnostic Analysis (1 page)
**What to Write:**
- Actual vs. Predicted scatter plot: Points cluster around diagonal
- Residual plot: Random scatter (no patterns = good)
- Residual distribution: Approximately normal, slight right skew

**Include Figures:**
- Figure 8: Actual vs. Predicted scatter plot
- Figure 9: Residual plot
- Figure 10: Residual distribution histogram

**Where to Find Info:**
- `results/visualizations/actual_vs_predicted.png`
- `results/visualizations/residuals_distribution.png`

### 12.3 Interpretation (1 page)
**What to Write:**
- Model excels: Suburban areas (MAE $120)
- Model struggles: Luxury urban ZIPs (MAE $280)
- Why? Luxury market has unique factors not in data (views, prestige)
- Systematic errors: Underpredicts beachfront ZIPs

### 12.4 Validation of Success (0.5 page)
**What to Write:**
- Target: R² ≥ 0.75 → Achieved: 0.783 ✓
- Target: MAE ≤ $200 → Achieved: $174 ✓
- Target: Jacksonville MAE ≤ $150 → Achieved: $131 ✓
- Conclusion: All technical benchmarks exceeded

---

## 13. DISCUSSION OF FINDINGS & STRATEGIC ALIGNMENT
**Assigned to:** MATTHEW

### 13.1 Synthesis of Major Insights (1 page)
**What to Write:**
- **Insight 1:** Urban classification is dominant predictor (47% importance)
  - Urban ZIPs rent $400 higher on average
  - Reflects supply constraints in dense areas
  
- **Insight 2:** Education matters more than income
  - Bachelor's % (18% importance) > Income (15%)
  - Suggests amenity preferences of educated renters
  
- **Insight 3:** Housing age less important than expected
  - Only 8% importance
  - Contradicts conventional wisdom

### 13.2 Direct Problem Alignment (1 page)
**What to Write:**
- Original problem: Identify overpriced Jacksonville ZIPs
- Solution delivered: 17 ZIPs with >20% discrepancy
- Example: ZIP 32217 ($370 overpredicted)
- Impact: 280,000 residents in flagged ZIPs
- Stakeholder validation: StateofJax confirmed 14/17 align with local knowledge

### 13.3 Critical Evaluation & Error Analysis (1 page)
**What to Write:**
- **Limitation 1:** Missing external factors (crime, schools)
  - Explains remaining 22% of variance
  - Future enhancement opportunity
  
- **Limitation 2:** Luxury market outliers
  - Model underpredicts high-end ZIPs
  - Beachfront premium not captured
  
- **Limitation 3:** Temporal lag
  - ACS data is 5-year average
  - May miss recent market shifts

### 13.4 Evidence-Based Reasoning (0.5 page)
**What to Write:**
- All claims supported by data
- No anecdotal conclusions
- Transparent about limitations

### 13.5 Actionable Strategic Recommendations (1 page)
**What to Write:**
1. **Immediate:** Investigate 17 flagged Jacksonville ZIPs
2. **Short-term:** Implement quarterly model retraining
3. **Medium-term:** Add crime and school quality data
4. **Long-term:** Expand to all Florida cities
5. **Policy:** Use predictions to target rental assistance programs

---

## 14. CONCLUSION & FUTURE WORK
**Assigned to:** TEAM (draft together)

### 14.1 Synthesis of Solution (0.5 page)
**What to Write:**
- Recap: Built XGBoost model predicting rent for 1,767 ZIPs
- Innovation: Public data + ML + interactive dashboard
- Success: Exceeded all technical benchmarks

### 14.2 Reflection on Outcomes (0.5 page)
**What to Write:**
- Original goals vs. actual results
- R² target: 0.75 → Achieved: 0.783
- Jacksonville focus: Delivered 57 ZIP predictions
- Dashboard: Fully functional and deployed

### 14.3 Key Lessons Learned (0.5 page)
**What to Write:**
- **Technical:** Feature engineering critical (improved R² by 0.10)
- **Process:** Iterative model selection paid off
- **Collaboration:** Team coordination on data integration
- **Stakeholder:** Regular feedback improved usability

### 14.4 Critical Limitations (0.5 page)
**What to Write:**
- Data constraints: Missing crime, schools, walkability
- Temporal lag: 5-year ACS averages
- Geographic scope: Optimized for mid-sized cities
- Model complexity: XGBoost less interpretable than linear

### 14.5 Future Scope & Extensions (1 page)
**What to Write:**
1. **Data Enhancement:** Integrate crime data (FBI UCR), school ratings (GreatSchools API)
2. **Model Improvement:** SHAP values for interpretability, ensemble methods
3. **Geographic Expansion:** Extend to 50 largest U.S. cities
4. **Real-time Updates:** Automate quarterly retraining with latest ACS data
5. **Advanced Features:** Walkability scores, transit access, gentrification indicators

---

## 15. REFERENCES
**Assigned to:** TEAM (compile together)

**Format:** APA style

**Required Citations:**
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.

- Rosen, S. (1974). Hedonic prices and implicit markets: Product differentiation in pure competition. *Journal of Political Economy*, 82(1), 34-55.

- Sirmans, G. S., Macpherson, D. A., & Zietz, E. N. (2005). The composition of hedonic pricing models. *Journal of Real Estate Literature*, 13(1), 3-43.

- U.S. Census Bureau. (2024). *American Community Survey 5-year estimates*. Retrieved from https://data.census.gov

- Yao, J., & Fotheringham, A. S. (2016). Local forms of spatial relationships. *Geographical Analysis*, 48(2), 162-183.

**Add More:**
- Any papers you cited in Background section
- StateofJax website/reports
- Housing affordability statistics sources

---

## 16. TECHNICAL APPENDIX
**Assigned to:** MATTHEW

### A. Code Repository
**What to Include:**
- GitHub URL: https://github.com/[your-repo]
- Repository structure overview
- How to clone and run

### B. Extended Data Dictionary
**What to Include:**
- Full table of all 23 variables
- ACS table numbers
- Data types and ranges

### C. Supplementary Visualizations
**What to Include:**
- Additional charts not in main report
- Full correlation matrix
- City-by-city performance breakdown

### D. Model Hyperparameters
**What to Include:**
- Complete XGBoost configuration
- Grid search results table
- Cross-validation scores

### E. Hardware/Environment Specs
**What to Include:**
- MacBook Air M1, 8GB RAM
- Python 3.9.7
- Library versions (from requirements.txt)
- Training time: 30 seconds

---

## ✅ FINAL CHECKLIST

### Before Submission
- [ ] All 15 sections complete
- [ ] Executive summary 250-400 words
- [ ] All figures numbered and captioned
- [ ] All tables formatted consistently
- [ ] References in APA format
- [ ] Page numbers in footer
- [ ] Consistent 12pt Times New Roman
- [ ] 1-inch margins all sides
- [ ] Proofread for typos
- [ ] Converted to PDF

### Quality Checks
- [ ] No first-person pronouns (I, we, our)
- [ ] Active voice throughout
- [ ] Specific numbers and metrics
- [ ] All claims supported by data
- [ ] Professional tone
- [ ] Clear section transitions

---

## 📊 POINT ALLOCATION

| Section | Points | Assigned To |
|---------|--------|-------------|
| Executive Summary | 10 | Team |
| Introduction | 10 | Team |
| Background & Research | 10 | Khanh |
| Problem Definition | 10 | Khanh |
| Lifecycle Process | 10 | Khanh |
| Technical Stack | 10 | Matthew |
| Data Sources | 10 | William |
| Variable Analysis | 10 | William |
| Data Preprocessing | 10 | William |
| EDA | 10 | William |
| Modeling Strategy | 10 | Matthew |
| Evaluation | 10 | Matthew |
| Discussion | 10 | Matthew |
| Conclusion | 10 | Team |
| Overall Quality | 10 | Team |
| **TOTAL** | **150** | |

---

## 🚀 WRITING TIPS

### For Matthew (Modeling Sections)
- Pull heavily from `FINAL_MODEL_REPORT.md`
- Include all your model comparison tables
- Use your existing visualizations
- Explain WHY XGBoost won, not just that it did

### For William (Data Sections)
- Pull from `TEAM_DATA_PREPROCESSING_REPORT.md`
- Run `.describe()` on your data for statistics
- Create simple visualizations in Python
- Explain WHAT you did and WHY

### For Khanh (Process Sections)
- Focus on the JOURNEY, not just the destination
- Create the lifecycle diagram (most important!)
- Cite academic papers for background
- Explain how insights led to decisions

### For Everyone
- **Start with your assigned sections**
- **Use existing reports as source material**
- **Don't start from scratch - we have 90% of content already!**
- **Meet to write team sections together**
- **Review each other's sections before final submission**

---

**Good luck! You've got this! 🎉**
