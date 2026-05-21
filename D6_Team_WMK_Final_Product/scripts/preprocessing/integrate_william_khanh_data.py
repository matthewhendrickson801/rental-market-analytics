"""
Properly integrate William's education and Khanh's jobs data
"""

import pandas as pd
import os
import glob

print("=" * 80)
print("INTEGRATING WILLIAM & KHANH'S DATA")
print("=" * 80)

# ============================================================================
# STEP 1: Load base clean dataset
# ============================================================================
print("\n[1/4] Loading base clean dataset...")
base = pd.read_csv('d4_modeling/data/master_dataset_clean_v2.csv')
print(f"   Base dataset: {len(base)} ZIPs")

# ============================================================================
# STEP 2: Process William's Education Data
# ============================================================================
print("\n[2/4] Processing William's education data...")

edu_path = 'd4_modeling/team_data/william/Edu-BlueCollar-Occup-Employment'
edu_files = glob.glob(f'{edu_path}/*_simple.csv')

print(f"   Found {len(edu_files)} education files")

edu_dfs = []
for file in edu_files:
    df = pd.read_csv(file)
    edu_dfs.append(df)

edu_data = pd.concat(edu_dfs, ignore_index=True)
print(f"   Combined education data: {len(edu_data)} ZIPs")

# Calculate education percentages
edu_cols = [
    'Education Less than 9th Grade (2020-2024)',
    'Education 9th to 12th Grade, No Diploma (2020-2024)',
    'Education High School Degree (2020-2024)',
    'Education Some College No Degree (2020-2024)',
    'Education Associate Degree (2020-2024)',
    "Education Bachelor's Degree (2020-2024)",
    'Education Graduate Degree (2020-2024)'
]

# Check which columns exist
available_edu_cols = [col for col in edu_cols if col in edu_data.columns]
print(f"   Found {len(available_edu_cols)} education columns")

if len(available_edu_cols) > 0:
    # Calculate total
    edu_data['total_education'] = edu_data[available_edu_cols].sum(axis=1)
    
    # Create percentage features
    edu_data['education_less_than_hs'] = (
        (edu_data['Education Less than 9th Grade (2020-2024)'] + 
         edu_data['Education 9th to 12th Grade, No Diploma (2020-2024)']) / 
        edu_data['total_education'] * 100
    )
    
    edu_data['education_high_school'] = (
        edu_data['Education High School Degree (2020-2024)'] / 
        edu_data['total_education'] * 100
    )
    
    edu_data['education_some_college'] = (
        (edu_data['Education Some College No Degree (2020-2024)'] + 
         edu_data['Education Associate Degree (2020-2024)']) / 
        edu_data['total_education'] * 100
    )
    
    edu_data['education_bachelors_plus'] = (
        (edu_data["Education Bachelor's Degree (2020-2024)"] + 
         edu_data['Education Graduate Degree (2020-2024)']) / 
        edu_data['total_education'] * 100
    )
    
    # Keep only geoid and new features
    edu_features = edu_data[[
        'geoid',
        'education_less_than_hs',
        'education_high_school',
        'education_some_college',
        'education_bachelors_plus'
    ]].copy()
    
    print(f"   Created 4 education percentage features")
else:
    print("   ⚠️  No education columns found")
    edu_features = None

# ============================================================================
# STEP 3: Process William's Jobs Data
# ============================================================================
print("\n[3/4] Processing William's jobs data...")

jobs_path = 'd4_modeling/team_data/william/NumberofJobs'
jobs_files = glob.glob(f'{jobs_path}/*_simple.csv')

print(f"   Found {len(jobs_files)} jobs files")

jobs_dfs = []
for file in jobs_files:
    df = pd.read_csv(file)
    jobs_dfs.append(df)

jobs_data = pd.concat(jobs_dfs, ignore_index=True)
print(f"   Combined jobs data: {len(jobs_data)} ZIPs")

# Calculate jobs per capita
if 'Number of Jobs (2023)' in jobs_data.columns:
    # Need population - get from base dataset
    jobs_data = jobs_data.merge(
        base[['geoid', 'Total Population (2020-2024)']],
        on='geoid',
        how='left'
    )
    
    jobs_data['jobs_per_capita'] = (
        jobs_data['Number of Jobs (2023)'] / 
        jobs_data['Total Population (2020-2024)']
    )
    
    jobs_features = jobs_data[['geoid', 'jobs_per_capita']].copy()
    print(f"   Created jobs_per_capita feature")
else:
    print("   ⚠️  'Number of Jobs (2023)' column not found")
    jobs_features = None

# ============================================================================
# STEP 4: Merge all features
# ============================================================================
print("\n[4/4] Merging all features...")

final_dataset = base.copy()

# Merge education features
if edu_features is not None:
    print(f"   Merging education features...")
    final_dataset = final_dataset.merge(edu_features, on='geoid', how='left', suffixes=('', '_new'))
    
    # Drop old columns if they exist
    for col in ['education_less_than_hs', 'education_high_school', 'education_some_college', 'education_bachelors_plus']:
        if f'{col}_new' in final_dataset.columns:
            if col in final_dataset.columns:
                final_dataset = final_dataset.drop(columns=[col])
            final_dataset = final_dataset.rename(columns={f'{col}_new': col})

# Merge jobs features
if jobs_features is not None:
    print(f"   Merging jobs features...")
    final_dataset = final_dataset.merge(jobs_features, on='geoid', how='left', suffixes=('', '_new'))
    
    # Use new jobs_per_capita if available
    if 'jobs_per_capita_new' in final_dataset.columns:
        final_dataset['jobs_per_capita'] = final_dataset['jobs_per_capita_new']
        final_dataset = final_dataset.drop(columns=['jobs_per_capita_new'])

# Create education_income_ratio if we have both
if 'education_bachelors_plus' in final_dataset.columns and 'Per Capita Income (2020-2024)' in final_dataset.columns:
    final_dataset['education_income_ratio'] = (
        final_dataset['education_bachelors_plus'] / 
        (final_dataset['Per Capita Income (2020-2024)'] / 1000)
    )
    print(f"   Created education_income_ratio feature")

print(f"\n   Final dataset: {len(final_dataset)} ZIPs")
print(f"   Total columns: {len(final_dataset.columns)}")

# Remove duplicates
duplicates_before = final_dataset.duplicated(subset=['geoid']).sum()
if duplicates_before > 0:
    print(f"\n   Removing {duplicates_before} duplicate geoids...")
    final_dataset = final_dataset.drop_duplicates(subset=['geoid'], keep='first')

# Validation
print(f"\n   Validation:")
print(f"      Duplicates: {final_dataset.duplicated(subset=['geoid']).sum()}")
print(f"      Unique geoids: {final_dataset['geoid'].nunique()}")

# Check missing values in new features
new_features = ['education_less_than_hs', 'education_high_school', 'education_some_college', 
                'education_bachelors_plus', 'jobs_per_capita', 'education_income_ratio']

for feat in new_features:
    if feat in final_dataset.columns:
        missing = final_dataset[feat].isnull().sum()
        pct = (missing / len(final_dataset)) * 100
        print(f"      {feat}: {missing} missing ({pct:.1f}%)")

# Save
output_path = 'd4_modeling/data/master_dataset_clean_final.csv'
final_dataset.to_csv(output_path, index=False)
print(f"\n✅ Saved: {output_path}")

print("\n" + "=" * 80)
