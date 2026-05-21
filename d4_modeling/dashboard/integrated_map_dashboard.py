#!/usr/bin/env python3
"""
Jacksonville Integrated Dashboard
Combines Housing, Spatial Mismatch, and Skills Gap data
Shows composite city planning score on interactive map
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import json

print("=" * 80)
print("STEP 1: LOADING AND MERGING DATA")
print("=" * 80)

# Load all three datasets
housing = pd.read_excel('../4:20/Matthew_Housing_Tableau_Clean.xls')
spatial = pd.read_excel('../4:20/Khanh_SpatialMismatch_Tableau_Clean.xls')
skills = pd.read_excel('../4:20/William_Skills_Tableau_Clean.xls')

print(f"\nHousing data: {len(housing)} ZIPs")
print(f"Spatial data: {len(spatial)} ZIPs")
print(f"Skills data: {len(skills)} ZIPs")

# Merge all three on ZIP_Code (inner join - only ZIPs in all 3)
merged = housing.merge(spatial, on='ZIP_Code', how='inner')
merged = merged.merge(skills, on='ZIP_Code', how='inner')

print(f"\nMerged data: {len(merged)} ZIPs (present in all 3 datasets)")

# Check for missing ZIPs
housing_zips = set(housing['ZIP_Code'])
spatial_zips = set(spatial['ZIP_Code'])
skills_zips = set(skills['ZIP_Code'])

missing_from_spatial = housing_zips - spatial_zips
missing_from_skills = housing_zips - skills_zips
missing_from_housing = (spatial_zips | skills_zips) - housing_zips

if missing_from_spatial:
    print(f"\n⚠️  ZIPs in housing but NOT in spatial: {sorted(missing_from_spatial)}")
if missing_from_skills:
    print(f"⚠️  ZIPs in housing but NOT in skills: {sorted(missing_from_skills)}")
if missing_from_housing:
    print(f"⚠️  ZIPs in spatial/skills but NOT in housing: {sorted(missing_from_housing)}")

print("\n" + "=" * 80)
print("STEP 2: CALCULATING NORMALIZED COMPOSITE SCORE")
print("=" * 80)

# HOUSING SCORE: Focus on affordability
# Over-predicted (predicted > actual, negative diff) = overpriced = BAD
# Under-predicted (predicted < actual, positive diff) = underpriced = GOOD
# We want to penalize over-predicted, reward under-predicted

# Use Rent_Difference directly (predicted - actual)
# Negative = overpriced (bad), Positive = underpriced (good)
# Invert and normalize so higher score = more affordable
merged['housing_score'] = 100 - (merged['Rent_Difference'].rank(pct=True) * 100)

# For spatial and skills, lower is still better
merged['spatial_score'] = 100 - (merged['Spatial_Mismatch_Index'].rank(pct=True) * 100)
merged['skills_score'] = 100 - (abs(merged['Skills_Prediction_Error']).rank(pct=True) * 100)

# Composite score = average of three normalized scores
merged['composite_score'] = (
    merged['housing_score'] + 
    merged['spatial_score'] + 
    merged['skills_score']
) / 3

print("\nNormalized Scores (0-100, higher = better):")
print(f"  Housing score (affordability): {merged['housing_score'].min():.1f} - {merged['housing_score'].max():.1f}")
print(f"    (Higher = more underpriced/affordable)")
print(f"  Spatial score: {merged['spatial_score'].min():.1f} - {merged['spatial_score'].max():.1f}")
print(f"    (Higher = better job access)")
print(f"  Skills score: {merged['skills_score'].min():.1f} - {merged['skills_score'].max():.1f}")
print(f"    (Higher = better skills match)")
print(f"  Composite score: {merged['composite_score'].min():.1f} - {merged['composite_score'].max():.1f}")

# Assign color labels for reference (but will use gradient on map)
def assign_color_label(score):
    if score >= 66.67:
        return 'green'
    elif score >= 33.33:
        return 'yellow'
    else:
        return 'red'

merged['color_label'] = merged['composite_score'].apply(assign_color_label)

print("\n" + "=" * 80)
print("STEP 3: COMPOSITE SCORE DISTRIBUTION")
print("=" * 80)

# Show distribution
print(f"\nComposite Score Statistics:")
print(f"  Mean: {merged['composite_score'].mean():.1f}")
print(f"  Median: {merged['composite_score'].median():.1f}")
print(f"  Std Dev: {merged['composite_score'].std():.1f}")

color_counts = merged['color_label'].value_counts()
print(f"\nColor Distribution (for reference):")
print(f"  🟢 Green (score ≥ 66.7): {color_counts.get('green', 0)} ZIPs")
print(f"  🟡 Yellow (score 33.3-66.7): {color_counts.get('yellow', 0)} ZIPs")
print(f"  🔴 Red (score < 33.3): {color_counts.get('red', 0)} ZIPs")

# Show top and bottom ZIPs
print(f"\n🏆 TOP 5 ZIPs (Highest Composite Score):")
top5 = merged.nlargest(5, 'composite_score')[['ZIP_Code', 'composite_score', 'housing_score', 'spatial_score', 'skills_score']]
for _, row in top5.iterrows():
    print(f"  {row['ZIP_Code']}: {row['composite_score']:.1f} (H:{row['housing_score']:.0f} S:{row['spatial_score']:.0f} K:{row['skills_score']:.0f})")

print(f"\n⚠️  BOTTOM 5 ZIPs (Lowest Composite Score):")
bottom5 = merged.nsmallest(5, 'composite_score')[['ZIP_Code', 'composite_score', 'housing_score', 'spatial_score', 'skills_score']]
for _, row in bottom5.iterrows():
    print(f"  {row['ZIP_Code']}: {row['composite_score']:.1f} (H:{row['housing_score']:.0f} S:{row['spatial_score']:.0f} K:{row['skills_score']:.0f})")

# Save merged data
output_path = 'dashboard/integrated_data.csv'
merged.to_csv(output_path, index=False)
print(f"\n✅ Saved integrated data: {output_path}")

print("\n" + "=" * 80)
print("STEP 4: DETAILED BREAKDOWN")
print("=" * 80)

print("\nRaw Metric Statistics:")
print(f"  Rent difference: min=${merged['Rent_Difference'].min():.0f}, max=${merged['Rent_Difference'].max():.0f}, median=${merged['Rent_Difference'].median():.0f}")
print(f"    (Negative = overpriced, Positive = underpriced)")
print(f"  Spatial mismatch: min={merged['Spatial_Mismatch_Index'].min():.1f}, max={merged['Spatial_Mismatch_Index'].max():.1f}, median={merged['Spatial_Mismatch_Index'].median():.1f}")
print(f"  Skills abs error: min={abs(merged['Skills_Prediction_Error']).min():.4f}, max={abs(merged['Skills_Prediction_Error']).max():.4f}, median={abs(merged['Skills_Prediction_Error']).median():.4f}")

# Show most affordable (underpriced) vs most overpriced
print(f"\n💰 Most UNDERPRICED (Affordable):")
underpriced = merged.nlargest(3, 'Rent_Difference')[['ZIP_Code', 'Rent_Difference', 'Actual_Rent', 'Predicted_Rent']]
for _, row in underpriced.iterrows():
    print(f"  {int(row['ZIP_Code'])}: ${int(row['Rent_Difference'])} under (actual ${int(row['Actual_Rent'])}, should be ${int(row['Predicted_Rent'])})")

print(f"\n💸 Most OVERPRICED (Expensive):")
overpriced = merged.nsmallest(3, 'Rent_Difference')[['ZIP_Code', 'Rent_Difference', 'Actual_Rent', 'Predicted_Rent']]
for _, row in overpriced.iterrows():
    print(f"  {int(row['ZIP_Code'])}: ${int(row['Rent_Difference'])} over (actual ${int(row['Actual_Rent'])}, should be ${int(row['Predicted_Rent'])})")

print("\n" + "=" * 80)
print("READY FOR MAP VISUALIZATION")
print("=" * 80)
print("\nNext steps:")
print("1. Download Jacksonville ZIP boundary shapefile")
print("2. Build interactive choropleth map")
print("3. Add hover/click interactions")
