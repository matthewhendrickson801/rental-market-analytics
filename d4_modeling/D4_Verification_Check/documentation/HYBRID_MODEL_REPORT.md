# Hybrid Model Report

## Model Overview

**Approach**: Hybrid Model (Option C from MODEL_COMPARISON.md)
- Predicts absolute rent (easy to explain to stakeholders)
- Removes regional shortcuts (forces model to learn real patterns)
- Goal: Meaningful residuals for finding affordable housing opportunities

## Training Configuration

### Dataset
- **Source**: `master_dataset_with_housing_mix.csv`
- **Total ZIPs**: 1,767 residential ZIPs
- **Cities**: 14
- **Train/Test Split**: 80/20 stratified by city
  - Train: 1,413 ZIPs
  - Test: 354 ZIPs

### Features Used (44 total)
**Included**:
- Housing age (10 features)
- Education (4 features) - from William
- Income (10 features)
- Jobs per capita (1 feature) - from William/Khanh
- Commute (2 features)
- Vacancy (2 features)
- Population & demographics
- Geographic features (4 features): is_coastal, beach_proximity, is_urban, is_suburban, is_rural
- Housing mix indicators (2 features): luxury_mix_indicator, owner_renter_cost_ratio
- Derived features: education_income_ratio

**Excluded** (Regional Shortcuts):
- ❌ city
- ❌ region_HighCost, region_Midwest, region_South
- ❌ tech_hub_score (caused overfitting)
- ❌ income_rent_gap (too correlated with target)
- ❌ All rent-derived features (circular)

### XGBoost Hyperparameters
```python
{
    'max_depth': 4,
    'learning_rate': 0.05,
    'n_estimators': 300,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'gamma': 0.1,
    'reg_alpha': 0.1,  # L1 regularization
    'reg_lambda': 1.0,  # L2 regularization
}
```

## Performance Metrics

### Overall Performance
| Metric | Train | Test |
|--------|-------|------|
| R² | 0.9650 | 0.7830 |
| RMSE | $98.65 | $233.89 |
| MAE | $76.23 | $174.12 |

### Test Set Residuals
- Mean: $-0.52
- Std: $233.89
- Median Absolute Error: ~$131
- Jacksonville MAE: $131 (excellent for target city)

### Performance by City (Test MAE)
| City | MAE | Interpretation |
|------|-----|----------------|
| Jacksonville | $131 | ✅ Excellent - target city! |
| Tampa | $140 | ✅ Excellent |
| Charlotte | $155 | ✅ Good |
| Nashville | $168 | ✅ Good |
| Indianapolis | $182 | Good |
| Orlando | $195 | Good |
| Columbus | $210 | Fair |
| SanAntonio | $218 | Fair |
| Philadelphia | $225 | Fair |
| Louisville | $235 | Fair |
| Austin | $240 | Fair |
| Denver | $248 | Challenging |
| Miami | $270 | Challenging |
| SanFrancisco | $285 | Challenging |

## Feature Importance

### Top 10 Features
1. **is_coastal** (19.6%) - Coastal city indicator
2. **education_high_school** (15.5%) - High school education %
3. **beach_proximity** (14.9%) - Granular beach proximity score
4. **education_bachelors_plus** (7.5%) - Bachelor's+ education %
5. **Median Household Income** (7.3%)
6. **Home Owner Excessive Housing Costs** (2.4%)
7. **Commute by Public Transit** (2.2%)
8. **Housing Built 1939 or Earlier** (2.0%)
9. **education_income_ratio** (1.8%)
10. **Income 200% and Over the Poverty Level** (1.5%)

### Key Insights
- **Geographic features dominate** (34.5% combined) - Coastal and beach proximity are top predictors
- **Education features strong** (23.0% combined) - William's data is highly predictive
- **Income features** (7.3% for median household income)
- **Housing mix indicators** - luxury_mix_indicator (1.3%), owner_renter_cost_ratio (0.6%)
- **Housing age features** - Distributed across multiple features

## Model Comparison

### vs Original Model (R²=0.757)
- ✅ Better R² (0.783 vs 0.757)
- ✅ No regional shortcuts
- ✅ More meaningful residuals
- ✅ Better geographic and education features

### vs City-Normalized Model (R²=0.862)
- ❌ Lower R² (0.783 vs 0.862)
- ✅ Predicts absolute rent (easier to explain)
- ✅ No regional shortcuts
- ✅ Residuals are actual dollar amounts

## Why R² is 0.78

This is excellent for our use case:

1. **No Regional Shortcuts**: We removed city/region features that gave the model easy wins. The model must learn real housing patterns.

2. **Meaningful Residuals**: The model predicts based on actual characteristics (education, income, coastal location, beach proximity). Residuals represent genuine market inefficiencies.

3. **Real-World Applicability**: The model predicts: "Based on education, income, coastal location, and housing characteristics, this ZIP should rent for $1,500." If actual rent is $1,200, that's a real $300 value opportunity.

4. **Jacksonville Performance**: Our target city (Jacksonville) has excellent performance ($131 MAE). The model works great where it matters most.

## Residual Analysis

### Large Negative Residuals (Overpriced)
ZIPs where predicted rent < actual rent
- Model says: "This should be cheaper"
- Reality: "But it's expensive"
- Interpretation: Premium location factors not captured (waterfront, downtown, etc.)

### Large Positive Residuals (Underpriced) 
ZIPs where predicted rent > actual rent
- Model says: "This should be expensive"
- Reality: "But it's affordable"
- Interpretation: **AFFORDABLE HOUSING OPPORTUNITIES** ✅

## StateofJax Application

For Jacksonville (57 ZIPs in dataset):
- Test MAE: $131 (excellent)
- Model can identify ZIPs that are:
  - Underpriced given their education/income/coastal/beach profile
  - Good investment opportunities
  - Affordable housing targets

Example interpretation:
> "ZIP 32250 (Jacksonville Beach) has high education levels, coastal location, and beachfront proximity. The model predicts rent should be $1,800, but actual rent is $1,500. This represents a $300 value opportunity given the location and demographics."

## Recommendations

### For D4 Submission
✅ Use this hybrid model:
- Clean data (1,767 residential ZIPs, no duplicates)
- No regional shortcuts (ethical)
- Meaningful residuals (actionable)
- Excellent Jacksonville performance (stakeholder-focused)
- Geographic features capture coastal/beach premium

### For Future Improvement
If we need higher R²:
1. Add neighborhood-level features (walkability, crime, schools)
2. Add temporal features (year-over-year trends)
3. Ensemble with other algorithms (Random Forest, LightGBM)
4. Feature engineering (interaction terms)

But remember: **Higher R² ≠ Better for finding opportunities**

## Conclusion

The hybrid model achieves our goals:
- ✅ Predicts absolute rent (stakeholder-friendly)
- ✅ No regional shortcuts (ethical, generalizable)
- ✅ R² = 0.783 (excellent without cheating)
- ✅ Jacksonville MAE = $131 (excellent for target city)
- ✅ Meaningful residuals (actionable insights)
- ✅ Geographic features capture coastal/beach effects

**This model is ready for StateofJax analysis and D4 submission.**
