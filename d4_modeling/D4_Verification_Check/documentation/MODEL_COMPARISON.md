# Model Comparison: Original vs City-Normalized

## Model 1: Original XGBoost (Absolute Rent Prediction)

**What it does:**
Predicts the actual rent price in dollars for each ZIP code.

**Performance:**
- R² Score: 0.757
- RMSE: $241
- Predicts rent directly: "ZIP 32207 should rent for $1,200/month"

**Pros:**
- Super easy to understand - everyone gets "this ZIP costs $1,200"
- Stakeholders love it - no math needed
- Direct comparison across cities
- Residuals show actual dollar savings

**Cons:**
- Might be "cheating" by learning regional patterns
- Could just memorize "Jacksonville = $1,400, San Francisco = $3,500"
- High R² might be fake - just learning city averages
- Harder to find TRUE market inefficiencies

**Top Features:**
1. Median household income
2. Housing age
3. Vacancy rates
4. Population density

---

## Model 2: City-Normalized XGBoost (Deviation Prediction)

**What it does:**
Predicts how much ABOVE or BELOW the city median each ZIP should be.

**Performance:**
- R² Score: 0.8615
- RMSE: $127
- Predicts deviation: "ZIP 32207 should be $275 below Jacksonville's median"

**Pros:**
- Removes regional bias - can't cheat with "Jacksonville = cheap"
- Better at finding REAL affordable housing opportunities
- Focuses on within-city market dynamics
- Lower overfitting risk

**Cons:**
- Harder to explain to non-technical people
- Need extra step: deviation + city median = actual rent
- Can't directly compare across cities
- More complex for stakeholders

**Top Features:**
1. Bachelor's degree % (12.5% importance)
2. Median household income (8.1%)
3. High school only % (6.0%)
4. Remote work premium (5.5%)

---

## Side-by-Side

| What You Care About | Original Model | City-Normalized Model |
|---------------------|----------------|----------------------|
| **Easy to explain?** | YES - "This ZIP costs $1,200" | MEDIUM - "This ZIP is $275 below average" |
| **Stakeholders get it?** | YES - everyone understands dollars | NEEDS EXPLANATION - what's a deviation? |
| **Finds real deals?** | MAYBE - might just be regional effects | YES - true market inefficiencies |
| **Avoids shortcuts?** | NO - learns "Jacksonville = cheap" | YES - removed regional bias |
| **R² Score** | 0.757 (lower) | 0.8615 (higher) |
| **Error** | $241 RMSE | $127 RMSE |
| **Overfitting risk** | MEDIUM | LOW |

---

## The Real Question

**What does StateofJax actually need?**

### Option A: Use Original Model
**Choose this if:** Simplicity matters most. You need to walk into a room and say "ZIP 32207 should rent for $1,200 but it's actually $925 - that's a $275 opportunity."

**Risk:** The model might just be learning "Jacksonville is cheaper than San Francisco" instead of understanding local housing economics.

### Option B: Use City-Normalized Model  
**Choose this if:** Finding REAL affordable housing matters most. You want to identify ZIPs that are genuinely underpriced relative to their local market, not just cheap because they're in Jacksonville.

**Risk:** Harder to explain. You have to say "This ZIP is $275 below Jacksonville's median of $1,400, so it should rent for $1,125."

### Option C: Hybrid Approach (NEW)
**Choose this if:** You want both simplicity AND accuracy.

**How it works:**
- Train a model to predict absolute rent (like Original)
- BUT remove all regional/city features (like City-Normalized)
- Forces model to learn housing economics, not geography
- Get easy interpretation + avoid shortcuts

**This might be the sweet spot.**

---

## My Recommendation

Go with **Option C - Hybrid Approach**.

**Why?**
1. StateofJax stakeholders need simple explanations (absolute rent)
2. But you also need REAL affordable housing opportunities (no regional shortcuts)
3. Hybrid gives you both

**What to do:**
1. Retrain XGBoost to predict absolute rent
2. Remove region_HighCost, region_Midwest, region_South features
3. Keep all the good stuff (education, income, jobs, housing age)
4. Should get R² around 0.80-0.85 with meaningful residuals

**Result:** 
"ZIP 32207 should rent for $1,200 based on its education levels, income, and housing stock - but it's actually $925. That's a $275 opportunity."

Simple to explain + finds real deals = Win.

---

## What do you think?

A) Stick with Original (simplicity over everything)
B) Stick with City-Normalized (accuracy over everything)  
C) Try Hybrid (best of both worlds)
