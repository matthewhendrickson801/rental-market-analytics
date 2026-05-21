# Strategies to Improve R² (Currently 0.733)

## Current Status
- XGBoost R²: 0.733 (Validation)
- RMSE: $268
- Median Error: 1.1%

## Strategy 1: Add Interaction Features (RECOMMENDED - Easy Win)

**What:** Create features that capture relationships between variables
**Why:** Rent isn't just about income OR transit - it's about income × region, transit × density, etc.

**Examples:**
```python
# Income × Region interactions
df['income_x_highcost'] = df['Median Household Income'] * df['region_HighCost']
df['income_x_midwest'] = df['Median Household Income'] * df['region_Midwest']

# Transit × Urban Type
df['transit_x_urban'] = df['Transit'] * df['urban_Urban']

# Population × Density
df['pop_density'] = df['Population'] / df['Housing Units']

# Income × Poverty (inequality measure)
df['income_inequality'] = df['Median Income'] / (df['poverty_rate_pct'] + 1)
```

**Expected Improvement:** R² → 0.78-0.82 (+5-9 points)

---

## Strategy 2: Add Polynomial Features for Key Variables

**What:** Add squared/cubed terms for non-linear relationships
**Why:** Income's effect on rent isn't linear - $100k→$150k has different impact than $50k→$100k

**Examples:**
```python
# Income polynomials
df['income_squared'] = df['Median Household Income'] ** 2
df['income_log'] = np.log(df['Median Household Income'] + 1)

# Population polynomials
df['pop_log'] = np.log(df['Population'] + 1)
df['pop_sqrt'] = np.sqrt(df['Population'])

# Transit polynomials
df['transit_log'] = np.log(df['Transit'] + 1)
```

**Expected Improvement:** R² → 0.76-0.80 (+3-7 points)

---

## Strategy 3: Add Ratio Features (RECOMMENDED - Easy Win)

**What:** Create meaningful ratios that capture economic relationships
**Why:** Ratios often have stronger predictive power than raw values

**Examples:**
```python
# Affordability ratios
df['income_to_rent_ratio'] = df['Median Income'] / (df['Rent'] + 1)
df['rent_burden'] = (df['Rent'] * 12) / df['Median Income']

# Housing market ratios
df['vacancy_ratio'] = df['Rental Vacancy'] / (df['Homeowner Vacancy'] + 0.01)
df['renter_to_owner_burden'] = df['Renter Excessive Costs'] / (df['Owner Excessive Costs'] + 1)

# Demographic ratios
df['affluence_to_poverty'] = df['Income 200%+'] / (df['Income <125%'] + 1)
df['new_to_old_housing'] = df['Built 2010+'] / (df['Built <1960'] + 1)

# Transit accessibility
df['transit_per_capita'] = df['Transit'] / df['Population']
df['cars_per_capita'] = df['No Vehicles'] / df['Population']
```

**Expected Improvement:** R² → 0.77-0.81 (+4-8 points)

---

## Strategy 4: Hyperparameter Tuning (RECOMMENDED - Medium Effort)

**What:** Optimize XGBoost parameters using GridSearch or RandomSearch
**Why:** Default parameters aren't optimal for your specific data

**Current Parameters:**
```python
n_estimators=200
max_depth=6
learning_rate=0.1
subsample=0.8
colsample_bytree=0.8
```

**Tuning Grid:**
```python
param_grid = {
    'n_estimators': [300, 500, 1000],
    'max_depth': [4, 6, 8, 10],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9],
    'min_child_weight': [1, 3, 5],
    'gamma': [0, 0.1, 0.2]
}
```

**Expected Improvement:** R² → 0.75-0.78 (+2-5 points)

---

## Strategy 5: Ensemble Multiple Models (Advanced)

**What:** Combine predictions from multiple models
**Why:** Different models capture different patterns

**Approach:**
```python
# Train multiple models
xgb_pred = xgb_model.predict(X)
rf_pred = rf_model.predict(X)
lgbm_pred = lgbm_model.predict(X)

# Weighted average
final_pred = 0.5 * xgb_pred + 0.3 * rf_pred + 0.2 * lgbm_pred
```

**Expected Improvement:** R² → 0.76-0.80 (+3-7 points)

---

## Strategy 6: Add External Data (High Effort, High Reward)

**What:** Incorporate additional data sources
**Why:** Your current features don't capture everything that affects rent

**Potential Data Sources:**
1. **Crime rates** (FBI UCR data)
2. **School quality** (GreatSchools API)
3. **Walkability scores** (Walk Score API)
4. **Distance to downtown** (Google Maps API)
5. **Employment centers** (BLS data)
6. **Amenities** (Yelp/Google Places - restaurants, parks, etc.)
7. **Weather/Climate** (NOAA data)
8. **Property tax rates** (County assessor data)

**Expected Improvement:** R² → 0.80-0.85 (+7-12 points)

---

## Strategy 7: Remove Outliers More Aggressively

**What:** Filter out ZIPs with extreme characteristics
**Why:** Outliers reduce R² even if predictions are reasonable

**Approach:**
```python
# Remove extreme outliers (beyond 3 standard deviations)
z_scores = np.abs((df['Rent'] - df['Rent'].mean()) / df['Rent'].std())
df_filtered = df[z_scores < 3]

# Or remove luxury/resort areas
df_filtered = df[df['Rent'] < df['Rent'].quantile(0.95)]
```

**Expected Improvement:** R² → 0.76-0.80 (+3-7 points)
**Trade-off:** Smaller dataset, less generalizable

---

## Strategy 8: Feature Engineering for Geographic Isolation

**What:** Better capture the impact of isolation
**Why:** Your analysis showed geographic isolation is a major rent suppressor

**Examples:**
```python
# Isolation score
df['isolation_score'] = (
    (df['Transit'] == 0).astype(int) * 2 +
    (df['Population'] < 2000).astype(int) * 2 +
    (df['urban_Rural']).astype(int) * 1
)

# Distance proxy (using population density)
df['density_score'] = df['Population'] / df['Housing Units']
df['isolation_penalty'] = np.where(
    (df['Transit'] == 0) & (df['density_score'] < 2),
    0.7,  # 30% rent reduction for isolated areas
    1.0
)
```

**Expected Improvement:** R² → 0.75-0.78 (+2-5 points)

---

## Recommended Implementation Order

### Phase 1: Quick Wins (1-2 hours)
1. **Add ratio features** (Strategy 3) - Easy, high impact
2. **Add key interaction features** (Strategy 1) - Income × Region, Transit × Urban
3. **Add polynomial features** (Strategy 2) - Log transforms for income, population

**Expected R²:** 0.78-0.82

### Phase 2: Optimization (2-4 hours)
4. **Hyperparameter tuning** (Strategy 4) - Use GridSearchCV
5. **Ensemble models** (Strategy 5) - Combine XGBoost + Random Forest + LightGBM

**Expected R²:** 0.80-0.84

### Phase 3: Advanced (1-2 days)
6. **Add external data** (Strategy 6) - Crime, schools, walkability
7. **Geographic isolation features** (Strategy 8) - Better capture isolation effects

**Expected R²:** 0.82-0.87

---

## Code Template for Phase 1 (Quick Wins)

```python
def add_engineered_features(df):
    """Add interaction, ratio, and polynomial features"""
    
    # Ratio features
    df['income_to_rent_ratio'] = df['Median Household Income (2020-2024)'] / (df['Median Home Rent (2020-2024)'] + 1)
    df['rent_burden_pct'] = (df['Median Home Rent (2020-2024)'] * 12) / df['Median Household Income (2020-2024)'] * 100
    df['affluence_to_poverty'] = df['Income 200% and Over the Poverty Level (2020-2024)'] / (df['Income 49% and Below Poverty Level (2020-2024)'] + 1)
    df['transit_per_capita'] = df['Commute Transportation by Public Transit (2020-2024)'] / df['Total Population (2020-2024)']
    df['pop_density'] = df['Total Population (2020-2024)'] / df['Total Housing Units (2020-2024)']
    
    # Interaction features
    df['income_x_highcost'] = df['Median Household Income (2020-2024)'] * df['region_HighCost']
    df['income_x_midwest'] = df['Median Household Income (2020-2024)'] * df['region_Midwest']
    df['transit_x_urban'] = df['Commute Transportation by Public Transit (2020-2024)'] * df['urban_Urban']
    df['poverty_x_urban'] = df['poverty_rate_pct'] * df['urban_Urban']
    
    # Polynomial features
    df['income_log'] = np.log(df['Median Household Income (2020-2024)'] + 1)
    df['income_squared'] = df['Median Household Income (2020-2024)'] ** 2
    df['pop_log'] = np.log(df['Total Population (2020-2024)'] + 1)
    df['transit_log'] = np.log(df['Commute Transportation by Public Transit (2020-2024)'] + 1)
    
    return df
```

---

## Expected Final Results

**Current:** R² = 0.733, RMSE = $268
**After Phase 1:** R² = 0.80-0.82, RMSE = $220-$240
**After Phase 2:** R² = 0.82-0.84, RMSE = $200-$220
**After Phase 3:** R² = 0.85-0.87, RMSE = $180-$200

---

## Important Notes

1. **Don't overfit!** Always validate on test set, not just validation set
2. **Feature selection:** More features ≠ better. Use feature importance to remove weak features
3. **Cross-validation:** Use k-fold CV to ensure improvements are real, not lucky splits
4. **Interpretability trade-off:** More complex features = harder to explain to stakeholders
5. **Diminishing returns:** Going from 0.73 → 0.80 is easier than 0.80 → 0.85

---

## Which Strategy Should You Start With?

**If you want quick improvement (1-2 hours):**
→ Start with Strategy 3 (Ratios) + Strategy 1 (Interactions)

**If you want maximum improvement (1-2 days):**
→ Do Phase 1 + Phase 2 + add crime/school data

**If you want to understand what's missing:**
→ Analyze residuals to see which ZIPs have largest errors, then add features to address those patterns
