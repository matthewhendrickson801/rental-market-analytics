# D6 - Final Product Delivery
## Predictive Rent Analysis for Urban Planning

**Team Name:** Team WMK  
**Team Members:** William, Matthew Hendrickson, Khanh  
**Project Title:** Predictive Rent Analysis for Urban Planning: A Machine Learning Approach to Housing Affordability in Jacksonville  
**Course:** CAP 4922 - Data Science Capstone  
**Date:** April 27, 2026

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Technical Dependencies](#technical-dependencies)
4. [Quick Start Guide](#quick-start-guide)
5. [Data Assets](#data-assets)
6. [Source Code Documentation](#source-code-documentation)
7. [Dashboard & Visualizations](#dashboard--visualizations)
8. [Operational Instructions](#operational-instructions)
9. [User Tutorial](#user-tutorial)
10. [Cloud Infrastructure](#cloud-infrastructure)

---

## 🎯 Project Overview

This project delivers a machine learning solution for predicting rental prices across U.S. ZIP codes, specifically optimized for Jacksonville, Florida urban planning applications. The system enables StateofJax and other stakeholders to:

- Predict median rent for any ZIP code based on demographic and housing characteristics
- Identify neighborhoods with significant rent discrepancies (>20% deviation from predictions)
- Explore interactive visualizations of housing affordability across Jacksonville
- Generate policy-ready reports highlighting intervention priorities

**Key Performance Metrics:**
- **National Model**: R² = 0.783, MAE = $174 (1,767 ZIP codes across 14 cities)
- **Jacksonville Model**: R² = 0.82, MAE = $131 (57 ZIP codes)
- **Training Data**: American Community Survey 2020-2024 (5-year estimates)
- **Model Architecture**: XGBoost Regression with 12 engineered features

---

## 📁 Directory Structure

```
d4_modeling/
├── data/
│   ├── raw/                          # Original ACS data files
│   │   ├── cleaned_rent_dataset_COMPLETE.csv
│   │   └── final_dataset_with_mismatch_indexes.csv
│   ├── processed/                    # Cleaned, model-ready datasets
│   │   ├── model_training_data.csv
│   │   └── jacksonville_predictions.csv
│   └── team_data/                    # Integrated multi-dimensional data
│       └── integrated_data.csv       # Housing + Spatial + Skills data
│
├── models/
│   ├── final_xgboost_model.pkl      # Trained XGBoost model
│   ├── city_normalized_model.pkl    # City-specific normalized model
│   └── model_metadata.json          # Hyperparameters and training config
│
├── scripts/
│   ├── preprocessing/
│   │   ├── clean_team_data.py       # Data cleaning pipeline
│   │   └── integrate_team_data.py   # Multi-source data integration
│   ├── training/
│   │   ├── train_final_model.py     # Main model training script
│   │   └── train_city_normalized_model.py
│   ├── analysis/
│   │   ├── final_model_comparison.py
│   │   └── find_affordable_mismatches.py
│   └── reports/
│       └── generate_stateofjax_report.py
│
├── dashboard/
│   ├── jacksonville_choropleth_map.py  # Interactive map dashboard
│   ├── duval_dashboard.py              # Streamlit dashboard
│   └── integrated_data.csv             # Dashboard data source
│
├── results/
│   ├── Jacksonville_Final_Report.md
│   ├── Jacksonville_Housing_Predictions_Tableau.csv
│   └── visualizations/
│       ├── feature_importance.png
│       ├── actual_vs_predicted.png
│       └── residuals_distribution.png
│
├── docs/
│   ├── deliverable/
│   │   ├── D4_MODEL_SELECTION_REPORT.md
│   │   └── D4_EXECUTIVE_SUMMARY.md
│   ├── reports/
│   │   └── FINAL_MODEL_REPORT.md
│   └── guides/
│       └── QUICK_START.md
│
├── requirements.txt                  # Python dependencies
├── environment.yml                   # Conda environment specification
└── README.md                         # This file
```

---

## 🔧 Technical Dependencies

### Core Requirements

**Python Version:** 3.9+

**Essential Libraries:**
```
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==1.7.6
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.15.0
dash==2.11.1
streamlit==1.24.0
```

### Installation Methods

**Option 1: pip (Recommended)**
```bash
pip install -r requirements.txt
```

**Option 2: conda**
```bash
conda env create -f environment.yml
conda activate rent-prediction
```

**Option 3: Manual Installation**
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn plotly dash streamlit
```

### System Requirements

- **RAM**: Minimum 8GB (16GB recommended for full dataset processing)
- **Storage**: 2GB free space for data and models
- **OS**: macOS, Linux, or Windows 10+
- **Internet**: Required for initial data download and dashboard deployment

---

## 🚀 Quick Start Guide

### 1. Environment Setup (5 minutes)

```bash
# Clone or navigate to project directory
cd d4_modeling

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Data Assets (2 minutes)

```bash
# Check that required data files exist
ls data/raw/cleaned_rent_dataset_COMPLETE.csv
ls data/processed/model_training_data.csv
ls models/final_xgboost_model.pkl
```

### 3. Run Model Predictions (3 minutes)

```bash
# Generate Jacksonville predictions
python3 scripts/analysis/final_model_comparison.py

# Output: results/Jacksonville_predictions.csv
```

### 4. Launch Interactive Dashboard (2 minutes)

```bash
# Start the choropleth map dashboard
python3 dashboard/jacksonville_choropleth_map.py

# Open browser to: http://127.0.0.1:8050
```

**Total Setup Time:** ~12 minutes from zero to running dashboard

---

## 📊 Data Assets

### Primary Dataset: `cleaned_rent_dataset_COMPLETE.csv`

**Source:** U.S. Census Bureau American Community Survey (2020-2024 5-year estimates)  
**Coverage:** 1,767 ZIP codes across 14 U.S. cities  
**Size:** 1.2 MB (1,767 rows × 23 columns)  
**License:** Public domain (U.S. Government data)

**Key Variables:**
- `geoid`: 5-digit ZIP code identifier
- `actual_rent`: Median gross rent (ACS Table B25064)
- `population`: Total population (ACS Table B01003)
- `bachelors_pct`: % adults with bachelor's degree or higher
- `median_income`: Median household income
- `median_home_value`: Median owner-occupied home value
- `median_year_built`: Median year structure built
- `urban_classification`: Binary (Urban/Suburban based on density)

**Data Quality:**
- Missing Values: 0% (all incomplete ZIP codes excluded during preprocessing)
- Outliers: Retained (represent legitimate market extremes)
- Validation: Cross-referenced with Zillow Rent Index for 50 sample ZIP codes (correlation: 0.89)

### Integrated Dataset: `integrated_data.csv`

**Purpose:** Multi-dimensional urban planning analysis combining housing, spatial mismatch, and skills gap data  
**Coverage:** 54 Jacksonville ZIP codes with complete data across all three dimensions  
**Size:** 156 KB (54 rows × 29 columns)

**Data Sources:**
1. **Housing Predictions** (Matthew): Rent model predictions and discrepancies
2. **Spatial Mismatch** (Khanh): Job access, transit availability, commute patterns
3. **Skills Gap** (William): Workforce education alignment with job requirements

**Composite Scoring:**
- Housing Score: Affordability based on rent predictions (0-100 scale)
- Spatial Score: Job accessibility and transit quality (0-100 scale)
- Skills Score: Education-job match quality (0-100 scale)
- Composite Score: Equal-weighted average of three dimensions

### Data Retrieval

All datasets are included in the repository. For updated ACS data:

```bash
# Download latest ACS 5-year estimates (requires Census API key)
python3 scripts/data_acquisition/fetch_acs_data.py --api-key YOUR_KEY --year 2024
```

---

## 💻 Source Code Documentation

### Core Scripts

#### 1. Model Training: `scripts/training/train_final_model.py`

**Purpose:** Train XGBoost regression model on full dataset

**Usage:**
```bash
python3 scripts/training/train_final_model.py
```

**Outputs:**
- `models/final_xgboost_model.pkl`: Serialized trained model
- `models/model_metadata.json`: Hyperparameters and performance metrics
- `results/training_log.txt`: Detailed training progress

**Key Functions:**
- `load_and_prepare_data()`: Loads CSV, handles missing values, creates train/test split
- `engineer_features()`: Creates interaction terms, log transformations, urban classification
- `train_xgboost_model()`: Trains model with optimized hyperparameters
- `evaluate_model()`: Calculates R², MAE, RMSE on test set
- `save_model()`: Serializes model using pickle

**Hyperparameters:**
```python
{
    'n_estimators': 500,
    'max_depth': 6,
    'learning_rate': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 3,
    'gamma': 0.1
}
```

#### 2. Data Integration: `scripts/preprocessing/integrate_team_data.py`

**Purpose:** Merge housing, spatial, and skills datasets for multi-dimensional analysis

**Usage:**
```bash
python3 scripts/preprocessing/integrate_team_data.py
```

**Outputs:**
- `dashboard/integrated_data.csv`: Merged dataset with composite scores
- `results/integration_report.txt`: Data quality summary

**Key Functions:**
- `load_team_datasets()`: Reads three Excel files from `4:20/` folder
- `standardize_zip_codes()`: Ensures consistent 5-digit string format
- `calculate_scores()`: Normalizes metrics to 0-100 scale, computes composite
- `merge_datasets()`: Inner join on ZIP_Code, handles missing values

#### 3. Dashboard Generation: `dashboard/jacksonville_choropleth_map.py`

**Purpose:** Interactive map visualization of Jacksonville ZIP code analysis

**Usage:**
```bash
python3 dashboard/jacksonville_choropleth_map.py
# Open browser to http://127.0.0.1:8050
```

**Features:**
- Choropleth map with continuous color gradient (red → yellow → green)
- Hover tooltips showing all metrics for each ZIP code
- Sortable/filterable data table with all 54 ZIP codes
- Responsive design for presentation and screenshots

**Technology Stack:**
- Plotly for choropleth mapping
- Dash for web application framework
- GeoJSON for ZIP code boundaries

---

## 🗺️ Dashboard & Visualizations

### Interactive Choropleth Map

**URL:** http://127.0.0.1:8050 (when running locally)

**Features:**
1. **Geographic Visualization**: ZIP codes colored by composite score
   - Green (66.7-100): Strong performance across all metrics
   - Yellow (33.3-66.7): Moderate performance
   - Red (0-33.3): Priority areas needing intervention

2. **Hover Details**: Mouse over any ZIP to see:
   - Composite score and breakdown (housing, spatial, skills)
   - Population and demographic data
   - Actual vs. predicted rent
   - Job access and transit metrics

3. **Data Table**: Complete sortable table below map
   - Filter by score ranges
   - Sort by any column
   - Export to CSV for further analysis

### Static Visualizations

Located in `results/visualizations/`:

1. **feature_importance.png**: Bar chart showing top 12 features driving predictions
2. **actual_vs_predicted.png**: Scatter plot with R² and regression line
3. **residuals_distribution.png**: Histogram of prediction errors

---

## 📖 Operational Instructions

### Complete Workflow (From Scratch)

#### Step 1: Environment Setup
```bash
cd d4_modeling
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 2: Data Preparation
```bash
# Clean and integrate team data
python3 scripts/preprocessing/clean_team_data.py
python3 scripts/preprocessing/integrate_team_data.py
```

#### Step 3: Model Training
```bash
# Train final model (takes ~5 minutes)
python3 scripts/training/train_final_model.py

# Verify model performance
python3 scripts/analysis/final_model_comparison.py
```

#### Step 4: Generate Predictions
```bash
# Create Jacksonville predictions
python3 scripts/analysis/find_affordable_mismatches.py

# Generate StateofJax report
python3 scripts/reports/generate_stateofjax_report.py
```

#### Step 5: Launch Dashboard
```bash
# Start interactive map
python3 dashboard/jacksonville_choropleth_map.py

# In separate terminal, start Streamlit dashboard
streamlit run dashboard/duval_dashboard.py
```

### Updating with New Data

```bash
# 1. Place new ACS data in data/raw/
# 2. Run preprocessing
python3 scripts/preprocessing/clean_team_data.py --input data/raw/new_acs_data.csv

# 3. Retrain model
python3 scripts/training/train_final_model.py --retrain

# 4. Regenerate predictions
python3 scripts/analysis/final_model_comparison.py
```

---

## 👥 User Tutorial

### For Non-Technical Users

#### Viewing Jacksonville Housing Analysis

1. **Open the Dashboard**
   - Ask your technical contact to start the dashboard
   - Open web browser to http://127.0.0.1:8050

2. **Understanding the Map**
   - **Green areas**: Affordable housing with good job access and skills match
   - **Yellow areas**: Moderate performance, some concerns
   - **Red areas**: Priority intervention needed (overpriced or poor planning)

3. **Exploring Specific ZIP Codes**
   - Hover your mouse over any colored area
   - A popup shows detailed information:
     - Composite Score: Overall rating (0-100)
     - Housing Score: Affordability rating
     - Actual Rent vs. Predicted Rent
     - Population and demographics

4. **Finding Specific Information**
   - Scroll down to the data table
   - Click column headers to sort (e.g., sort by Composite Score)
   - Use the search box to find specific ZIP codes

5. **Interpreting Results**
   - **Over-predicted rent** (Predicted > Actual): Area may be overpriced
   - **Under-predicted rent** (Actual > Predicted): Area may be undervalued or have hidden amenities
   - **Large discrepancies** (>$200): Warrant further investigation

#### Generating Reports

1. **Export Data**
   - In the dashboard, click "Export to CSV" button
   - Open in Excel or Google Sheets

2. **Create Policy Briefs**
   - Filter table to show only red ZIP codes (score < 33.3)
   - These are priority intervention areas
   - Copy data for inclusion in reports

3. **Quarterly Updates**
   - Ask technical contact to retrain model with latest ACS data
   - Compare new predictions to previous quarter
   - Identify emerging trends

---

## ☁️ Cloud Infrastructure

### Current Deployment: Local

The current solution runs locally on user machines. No cloud infrastructure is required for basic operation.

### Planned Cloud Deployment (Future Enhancement)

**Platform:** Streamlit Cloud (free tier)

**Architecture:**
```
User Browser
    ↓
Streamlit Cloud (streamlit.io)
    ↓
GitHub Repository (auto-sync)
    ↓
Data: CSV files in repo
Model: Pickle file in repo
```

**Deployment Steps:**
1. Push code to GitHub repository
2. Connect Streamlit Cloud to GitHub
3. Configure app settings (Python 3.9, requirements.txt)
4. Deploy (automatic from main branch)

**URL:** https://teamwmk-jacksonville-housing.streamlit.app (example)

**Benefits:**
- No local setup required for end users
- Automatic updates when code changes
- Accessible from any device with internet
- Free hosting for public projects

### Alternative Cloud Options

**AWS Deployment** (if scaling needed):
- **EC2 Instance**: t2.medium ($0.05/hour)
- **S3 Bucket**: Store data and models
- **Elastic Beanstalk**: Automated deployment and scaling
- **Estimated Cost**: $30-50/month for 24/7 availability

**Google Cloud Platform**:
- **Cloud Run**: Serverless container deployment
- **Cloud Storage**: Data and model hosting
- **Estimated Cost**: $20-40/month (pay-per-use)

---

## 📞 Support & Contact

**Technical Issues:**
- Matthew Hendrickson: [email]
- GitHub Issues: [repository URL]

**Data Questions:**
- Refer to `docs/reports/FINAL_MODEL_REPORT.md`
- ACS Documentation: https://www.census.gov/programs-surveys/acs

**Stakeholder Inquiries:**
- StateofJax: [contact information]

---

## 📄 License & Attribution

**Code:** MIT License (open source)  
**Data:** Public domain (U.S. Census Bureau)  
**Models:** Available for non-commercial use

**Citation:**
```
Team WMK (2026). Predictive Rent Analysis for Urban Planning: 
A Machine Learning Approach to Housing Affordability in Jacksonville.
University of North Florida, CAP 4922 Capstone Project.
```

---

## 🎉 Acknowledgments

- **StateofJax** for problem definition and domain expertise
- **U.S. Census Bureau** for comprehensive ACS data
- **UNF Department of Computing Sciences** for project guidance
- **Team Members**: William, Matthew, Khanh for collaborative development

---

**Last Updated:** April 27, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
