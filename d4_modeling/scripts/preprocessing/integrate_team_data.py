"""
Integrate William and Khanh's data with existing dataset
Goal: Push R² from 0.757 to 0.86+
"""

import pandas as pd
import numpy as np
from pathlib import Path
import glob

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
TEAM_DIR = BASE_DIR / 'team_data'
OUTPUT_FILE = DATA_DIR / 'master_dataset_with_team_data.csv'

print("=" * 80)
print("INTEGRATING TEAM DATA - WILLIAM & KHANH")
print("=" * 80)

# Load existing dataset
print("\n1. Loading existing dataset...")
df_existing = pd.read_csv(DATA_DIR / 'final_dataset_no_military.csv')
df_existing['geoid'] = df_existing['geoid'].astype(str)  # Convert to string for merging
print(f"   Existing data: {len(df_existing)} rows, {len(df_existing.columns)} columns")
print(f"   Cities: {df_existing['city'].unique()}")

# Initialize master dataframe
df_master = df_existing.copy()

# ============================================================================
# WILLIAM'S DATA - Employment & Jobs
# ============================================================================

print("\n2. Integrating William's data...")

# 2.1 Number of Jobs
print("   2.1 Adding Number of Jobs...")
jobs_files = glob.glob(str(TEAM_DIR / 'william' / 'NumberofJobs' / '*_simple.csv'))
jobs_data = []

for file in jobs_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    jobs_data.append(df_temp[['geoid', 'city', 'Number of Jobs (2023)']])

df_jobs = pd.concat(jobs_data, ignore_index=True)
df_jobs['geoid'] = df_jobs['geoid'].astype(str)
df_jobs.rename(columns={'Number of Jobs (2023)': 'total_jobs'}, inplace=True)

# Merge
df_master = df_master.merge(df_jobs[['geoid', 'total_jobs']], on='geoid', how='left')
print(f"      Added: total_jobs ({df_master['total_jobs'].notna().sum()} non-null)")

# 2.2 Education & Blue Collar
print("   2.2 Adding Education & Employment data...")
edu_files = glob.glob(str(TEAM_DIR / 'william' / 'Edu-BlueCollar-Occup-Employment' / '*_simple.csv'))
edu_data = []

for file in edu_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    edu_data.append(df_temp)

df_edu = pd.concat(edu_data, ignore_index=True)
df_edu['geoid'] = df_edu['geoid'].astype(str)

# Select education columns
edu_cols = [col for col in df_edu.columns if 'Education' in col]
print(f"      Found {len(edu_cols)} education columns")

# Calculate education percentages
df_edu['total_pop_edu'] = df_edu[edu_cols].sum(axis=1)

# Find actual column names (they vary slightly)
less_hs_cols = [col for col in edu_cols if '9th' in col or 'Less than' in col]
hs_cols = [col for col in edu_cols if 'High School' in col and 'Degree' in col]
some_college_cols = [col for col in edu_cols if 'Some College' in col or 'Associate' in col]
bachelors_cols = [col for col in edu_cols if 'Bachelor' in col or 'Graduate' in col]

df_edu['pct_less_than_hs'] = df_edu[less_hs_cols].sum(axis=1) / df_edu['total_pop_edu'] * 100 if less_hs_cols else 0
df_edu['pct_hs_only'] = df_edu[hs_cols].sum(axis=1) / df_edu['total_pop_edu'] * 100 if hs_cols else 0
df_edu['pct_some_college'] = df_edu[some_college_cols].sum(axis=1) / df_edu['total_pop_edu'] * 100 if some_college_cols else 0
df_edu['pct_bachelors_plus'] = df_edu[bachelors_cols].sum(axis=1) / df_edu['total_pop_edu'] * 100 if bachelors_cols else 0

# Merge education data
edu_merge_cols = ['geoid', 'pct_less_than_hs', 'pct_hs_only', 'pct_some_college', 'pct_bachelors_plus']
df_master = df_master.merge(df_edu[edu_merge_cols], on='geoid', how='left')
print(f"      Added: {len(edu_merge_cols)-1} education percentage columns")

# 2.3 Jobs by Industry
print("   2.3 Adding Industry data...")
industry_files = glob.glob(str(TEAM_DIR / 'william' / 'JobsbyWoker&Industry' / '*_simple.csv'))
industry_data = []

for file in industry_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    industry_data.append(df_temp)

df_industry = pd.concat(industry_data, ignore_index=True)
df_industry['geoid'] = df_industry['geoid'].astype(str)

# Get industry columns
industry_cols = [col for col in df_industry.columns if 'Industry' in col or 'Occupation' in col]
print(f"      Found {len(industry_cols)} industry/occupation columns")

# Calculate key industry percentages
if 'Total Jobs (2020-2024)' in df_industry.columns:
    total_col = 'Total Jobs (2020-2024)'
elif 'Total Employed (2020-2024)' in df_industry.columns:
    total_col = 'Total Employed (2020-2024)'
else:
    # Sum all industry columns
    df_industry['total_industry_jobs'] = df_industry[industry_cols].sum(axis=1)
    total_col = 'total_industry_jobs'

# Tech/Professional industries
tech_keywords = ['Professional', 'Scientific', 'Technical', 'Information', 'Finance', 'Management']
tech_cols = [col for col in industry_cols if any(kw in col for kw in tech_keywords)]
if tech_cols:
    df_industry['pct_tech_jobs'] = df_industry[tech_cols].sum(axis=1) / df_industry[total_col] * 100
else:
    df_industry['pct_tech_jobs'] = 0

# Service industries
service_keywords = ['Retail', 'Food', 'Accommodation', 'Entertainment', 'Recreation', 'Services']
service_cols = [col for col in industry_cols if any(kw in col for kw in service_keywords)]
if service_cols:
    df_industry['pct_service_jobs'] = df_industry[service_cols].sum(axis=1) / df_industry[total_col] * 100
else:
    df_industry['pct_service_jobs'] = 0

# Manufacturing/Construction
manuf_keywords = ['Manufacturing', 'Construction', 'Production', 'Transportation', 'Utilities']
manuf_cols = [col for col in industry_cols if any(kw in col for kw in manuf_keywords)]
if manuf_cols:
    df_industry['pct_manufacturing_jobs'] = df_industry[manuf_cols].sum(axis=1) / df_industry[total_col] * 100
else:
    df_industry['pct_manufacturing_jobs'] = 0

# Merge industry data
industry_merge_cols = ['geoid', 'pct_tech_jobs', 'pct_service_jobs', 'pct_manufacturing_jobs']
df_master = df_master.merge(df_industry[industry_merge_cols], on='geoid', how='left')
print(f"      Added: {len(industry_merge_cols)-1} industry percentage columns")

# ============================================================================
# KHANH'S DATA - Occupation & Commute
# ============================================================================

print("\n3. Integrating Khanh's data...")

# 3.1 Workers by Occupation
print("   3.1 Adding Occupation mix...")
occup_files = glob.glob(str(TEAM_DIR / 'khanh' / 'WorkersbyOccupation' / '*_simple.csv'))
occup_data = []

for file in occup_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    occup_data.append(df_temp)

df_occup = pd.concat(occup_data, ignore_index=True)
df_occup['geoid'] = df_occup['geoid'].astype(str)

# Get occupation columns
occup_cols = [col for col in df_occup.columns if 'Occupations' in col or 'Occupation' in col]
print(f"      Found {len(occup_cols)} occupation columns")

# Calculate occupation percentages
df_occup['total_workers'] = df_occup[occup_cols].sum(axis=1)

# Management/Professional
mgmt_cols = [col for col in occup_cols if 'Management' in col or 'Business' in col or 'Science' in col or 'Arts' in col]
if mgmt_cols:
    df_occup['pct_mgmt_professional'] = df_occup[mgmt_cols].sum(axis=1) / df_occup['total_workers'] * 100
else:
    df_occup['pct_mgmt_professional'] = 0

# Service
service_occup_cols = [col for col in occup_cols if 'Service' in col]
if service_occup_cols:
    df_occup['pct_service_occup'] = df_occup[service_occup_cols].sum(axis=1) / df_occup['total_workers'] * 100
else:
    df_occup['pct_service_occup'] = 0

# Sales/Office
sales_cols = [col for col in occup_cols if 'Sales' in col or 'Office' in col]
if sales_cols:
    df_occup['pct_sales_office'] = df_occup[sales_cols].sum(axis=1) / df_occup['total_workers'] * 100
else:
    df_occup['pct_sales_office'] = 0

# Blue collar
blue_cols = [col for col in occup_cols if 'Natural Resources' in col or 'Construction' in col or 'Maintenance' in col or 'Production' in col or 'Transportation' in col]
if blue_cols:
    df_occup['pct_blue_collar'] = df_occup[blue_cols].sum(axis=1) / df_occup['total_workers'] * 100
else:
    df_occup['pct_blue_collar'] = 0

# Merge occupation data
occup_merge_cols = ['geoid', 'pct_mgmt_professional', 'pct_service_occup', 'pct_sales_office', 'pct_blue_collar']
df_master = df_master.merge(df_occup[occup_merge_cols], on='geoid', how='left')
print(f"      Added: {len(occup_merge_cols)-1} occupation percentage columns")

# 3.2 Work from Home / Commute patterns
print("   3.2 Adding work-from-home data...")
wfh_files = glob.glob(str(TEAM_DIR / 'khanh' / 'WorkersWhoCommuteorWork' / '*_simple.csv'))
wfh_data = []

for file in wfh_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    wfh_data.append(df_temp)

if wfh_data:
    df_wfh = pd.concat(wfh_data, ignore_index=True)
    df_wfh['geoid'] = df_wfh['geoid'].astype(str)
    
    # Find work from home column
    wfh_cols = [col for col in df_wfh.columns if 'Work' in col and 'Home' in col]
    commute_cols = [col for col in df_wfh.columns if 'Commute' in col or 'Drive' in col or 'Transit' in col]
    
    if wfh_cols and commute_cols:
        df_wfh['total_workers_wfh'] = df_wfh[wfh_cols + commute_cols].sum(axis=1)
        df_wfh['pct_work_from_home'] = df_wfh[wfh_cols].sum(axis=1) / df_wfh['total_workers_wfh'] * 100
        
        df_master = df_master.merge(df_wfh[['geoid', 'pct_work_from_home']], on='geoid', how='left')
        print(f"      Added: pct_work_from_home ({df_master['pct_work_from_home'].notna().sum()} non-null)")

# 3.3 Employment Status
print("   3.3 Adding employment status...")
emp_files = glob.glob(str(TEAM_DIR / 'khanh' / 'EmploymentStatus-TotalEmployed' / '*_simple.csv'))
emp_data = []

for file in emp_files:
    city_name = Path(file).stem.replace('_simple', '').replace(' ', '')
    df_temp = pd.read_csv(file)
    df_temp['city'] = city_name
    emp_data.append(df_temp)

if emp_data:
    df_emp = pd.concat(emp_data, ignore_index=True)
    df_emp['geoid'] = df_emp['geoid'].astype(str)
    
    # Get total employed
    emp_cols = [col for col in df_emp.columns if 'Employed' in col or 'Employment' in col]
    if emp_cols:
        df_emp['total_employed'] = df_emp[emp_cols].sum(axis=1)
        df_master = df_master.merge(df_emp[['geoid', 'total_employed']], on='geoid', how='left')
        print(f"      Added: total_employed ({df_master['total_employed'].notna().sum()} non-null)")

# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

print("\n4. Engineering new features...")

# 4.1 Jobs per capita
if 'total_jobs' in df_master.columns and 'Total Population (2020-2024)' in df_master.columns:
    df_master['jobs_per_capita'] = df_master['total_jobs'] / df_master['Total Population (2020-2024)']
    print("   4.1 Added: jobs_per_capita")

# 4.2 Education-Income alignment
if 'pct_bachelors_plus' in df_master.columns and 'Median Household Income (2020-2024)' in df_master.columns:
    df_master['education_income_ratio'] = df_master['pct_bachelors_plus'] / (df_master['Median Household Income (2020-2024)'] / 1000)
    print("   4.2 Added: education_income_ratio")

# 4.3 Tech job premium indicator
if 'pct_tech_jobs' in df_master.columns:
    df_master['high_tech_area'] = (df_master['pct_tech_jobs'] > df_master['pct_tech_jobs'].median()).astype(int)
    print("   4.3 Added: high_tech_area")

# 4.4 Professional occupation density
if 'pct_mgmt_professional' in df_master.columns and 'Total Population (2020-2024)' in df_master.columns:
    df_master['professional_density'] = (df_master['pct_mgmt_professional'] / 100) * df_master['Total Population (2020-2024)']
    print("   4.4 Added: professional_density")

# 4.5 Remote work advantage
if 'pct_work_from_home' in df_master.columns:
    df_master['high_remote_work'] = (df_master['pct_work_from_home'] > df_master['pct_work_from_home'].median()).astype(int)
    print("   4.5 Added: high_remote_work")

# ============================================================================
# SAVE MASTER DATASET
# ============================================================================

print("\n5. Saving master dataset...")
df_master.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved to: {OUTPUT_FILE}")
print(f"   Final shape: {df_master.shape}")
print(f"   Total columns: {len(df_master.columns)}")

# Summary of new features
new_cols = [col for col in df_master.columns if col not in df_existing.columns]
print(f"\n6. New features added: {len(new_cols)}")
for i, col in enumerate(new_cols, 1):
    non_null = df_master[col].notna().sum()
    print(f"   {i:2d}. {col:40s} ({non_null:4d} non-null, {non_null/len(df_master)*100:5.1f}%)")

print("\n" + "=" * 80)
print("INTEGRATION COMPLETE!")
print("=" * 80)
print(f"\nNext step: Run XGBoost on {OUTPUT_FILE}")
