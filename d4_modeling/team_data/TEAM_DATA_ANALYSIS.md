# Team Data Analysis - William & Khanh

**Purpose:** Explore additional variables from team members to potentially improve model R²  
**Current Model:** R² = 0.757, RMSE = $241  
**Goal:** Find variables that could push R² above 0.80

---

## William's Data - Employment & Jobs

### 1. Number of Jobs (2023)
**File:** `william/NumberofJobs/`
- **Variable:** Total number of jobs in ZIP code
- **Potential Value:** Job density could correlate with rent (more jobs = higher demand)
- **Coverage:** All 14 cities

### 2. Education & Blue Collar Employment
**File:** `william/Edu-BlueCollar-Occup-Employment/`
**Variables:**
- Education levels (9th-12th no diploma, <9th grade, HS degree, some college, etc.)
- Blue collar occupation counts
- Employment by education level
- **Potential Value:** Education mix could predict rent better than just median income
- **Coverage:** All 14 cities

### 3. Jobs by Worker & Industry
**File:** `william/JobsbyWoker&Industry/`
- **Variables:** Industry-specific employment data
- **Potential Value:** Tech jobs vs. service jobs could explain rent differences (Austin tech premium)
- **Coverage:** All 14 cities

---

## Khanh's Data - Occupation & Commute Details

### 1. Workers by Occupation
**File:** `khanh/WorkersbyOccupation/`
**Variables:**
- Management/Business/Science/Arts occupations by commute type
- Service occupations by commute type
- Sales/Office occupations by commute type
- Natural Resources/Construction/Maintenance by commute type
- Production/Transportation/Material Moving by commute type
- Military occupations by commute type
- **Potential Value:** Occupation mix could be stronger predictor than income alone
- **Coverage:** All 14 cities

### 2. Employment by Industry
**File:** `khanh/EmploymentbyIndustry/`
- **Variables:** Detailed industry breakdown
- **Potential Value:** Industry composition (tech vs. manufacturing vs. service)
- **Coverage:** All 14 cities

### 3. Commute Transportation
**File:** `khanh/CommuteTransportation/`
- **Variables:** Detailed commute methods beyond our current "public transit" variable
- **Potential Value:** More granular transit data
- **Coverage:** All 14 cities

### 4. Employment by Occupation (by Sex)
**Files:** `khanh/Employment by Occupation by Sex-Male/` and `Female/`
- **Variables:** Gender-specific occupation data
- **Potential Value:** Gender wage gap indicators
- **Coverage:** All 14 cities

### 5. Employment Status - Total Employed
**File:** `khanh/EmploymentStatus-TotalEmployed/`
- **Variables:** Total employment counts
- **Potential Value:** Employment density
- **Coverage:** All 14 cities

### 6. Jobs by Industry Type
**File:** `khanh/Jobs by Industry Type/`
- **Variables:** Industry-specific job counts
- **Potential Value:** Industry mix (tech-heavy vs. service-heavy)
- **Coverage:** All 14 cities

### 7. Workers by Industry and Commute Type
**Files:** `khanh/Workers by Industry and by Commute Type-Part1/` and `Part2/`
- **Variables:** Cross-tabulation of industry and commute method
- **Potential Value:** Industry-specific commute patterns
- **Coverage:** All 14 cities

### 8. Workers Who Commute or Work
**File:** `khanh/WorkersWhoCommuteorWork/`
- **Variables:** Work-from-home vs. commute patterns
- **Potential Value:** Remote work prevalence (COVID impact)
- **Coverage:** All 14 cities

---

## Promising Variables for Model Improvement

### High Priority (Likely to Improve R²)

1. **Number of Jobs** (William)
   - **Why:** Job density = demand for housing
   - **Expected Impact:** +2-3% R²
   - **Easy to integrate:** Single variable

2. **Industry Mix** (William + Khanh)
   - **Why:** Tech jobs pay more → higher rents (Austin, SF)
   - **Expected Impact:** +3-5% R²
   - **Variables:** % tech jobs, % service jobs, % manufacturing

3. **Education Levels** (William)
   - **Why:** Better predictor than income alone
   - **Expected Impact:** +2-4% R²
   - **Variables:** % bachelor's+, % HS only, % <HS

4. **Occupation Mix** (Khanh)
   - **Why:** Management/professional vs. service workers
   - **Expected Impact:** +2-3% R²
   - **Variables:** % management/business/science, % service

### Medium Priority

5. **Work-from-Home Rate** (Khanh)
   - **Why:** Remote work changes housing demand patterns
   - **Expected Impact:** +1-2% R²
   - **Relevant:** Post-COVID trend

6. **Detailed Commute Patterns** (Khanh)
   - **Why:** More granular than our current transit variable
   - **Expected Impact:** +1-2% R²

### Lower Priority

7. **Gender-Specific Employment** (Khanh)
   - **Why:** Wage gap indicators
   - **Expected Impact:** +0.5-1% R²
   - **Complexity:** High (many variables)

---

## Recommended Next Steps

### Quick Win (30 minutes)
1. **Add "Number of Jobs"** from William's data
   - Single variable, easy merge
   - Likely +2-3% R²

### Medium Effort (2 hours)
2. **Add Industry Mix** (% tech, % service, % manufacturing)
   - Calculate from William or Khanh's industry data
   - Likely +3-5% R²

3. **Add Education Levels** (% bachelor's+, % HS only)
   - From William's education data
   - Likely +2-4% R²

### Full Analysis (4+ hours)
4. **Comprehensive Feature Engineering**
   - Occupation mix
   - Work-from-home rate
   - Detailed commute patterns
   - Potential +5-10% R² total

---

## Data Quality Check Needed

Before integrating, verify:
1. **ZIP code coverage:** Do they have all 1,738 ZIPs?
2. **Missing values:** How complete is the data?
3. **Data year:** Is it 2020-2024 like our current data?
4. **Consistency:** Do ZIP codes match our dataset?

---

## Expected Model Performance

**Current:** R² = 0.757, RMSE = $241

**With Quick Win (Jobs):**
- R² = 0.78-0.79
- RMSE = $225-230

**With Medium Effort (Jobs + Industry + Education):**
- R² = 0.82-0.85
- RMSE = $200-215

**With Full Analysis:**
- R² = 0.85-0.88
- RMSE = $180-200

---

## Action Plan

1. **Merge Jacksonville data first** (test on 54 ZIPs)
2. **Check correlation with rent**
3. **If promising, merge all 14 cities**
4. **Retrain XGBoost with new features**
5. **Compare performance**

Let's start with the quick win!
