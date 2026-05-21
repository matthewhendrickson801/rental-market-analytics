# Matthew's Presentation Script
## Team WMK Final Presentation
**Time: 8-10 minutes (Introduction + Housing Affordability)**

---

## INTRODUCTION - TEAM PROJECT OVERVIEW (2 minutes)

**[SLIDE 1: Title Slide]**

Good morning everyone. I'm Matthew Hendrickson, and I'm here with my teammates William Hughes and Khanh Linh Lieu to present our capstone project: **Predictive Rent Analysis for Urban Planning: A Machine Learning Approach to Housing Affordability in Jacksonville**.

**[SLIDE 2: The Housing Affordability Crisis]**

The United States faces an unprecedented housing affordability crisis. According to Harvard's Joint Center for Housing Studies, 21.6 million renter households - that's 49% of all renters - are cost-burdened, spending more than 30% of their income on housing.

This crisis hits especially hard in mid-sized cities experiencing rapid growth. Jacksonville exemplifies this challenge: as the largest city by area in the contiguous United States and the 13th most populous, Jacksonville has grown 14.8% since 2010. Yet comprehensive rental market analysis tools remain limited.

**[SLIDE 3: The Problem - StateofJax]**

Our stakeholder is StateofJax, a Jacksonville-based urban planning and policy advocacy organization serving the city's 1 million residents. They face a critical information gap: **they lack systematic, data-driven methods to identify neighborhoods where rental prices deviate significantly from expected market values.**

Currently, StateofJax relies on anecdotal reports and reactive responses to community complaints. This creates three major problems:

1. **Resource Misallocation** - Limited intervention resources may go to areas with less severe needs
2. **Policy Blind Spots** - Policymakers lack quantitative evidence to justify affordable housing initiatives  
3. **Market Opacity** - Residents can't determine if local rents reflect legitimate market conditions or potential exploitation

**[SLIDE 4: Our Solution - Machine Learning for Market Intelligence]**

We developed a machine learning-powered predictive rent analysis system that transforms raw demographic and housing data into actionable market intelligence.

Our XGBoost regression model was trained on 1,767 ZIP codes across 14 U.S. cities, predicting median rent prices based on 12 key urban characteristics - things like population density, educational attainment, income levels, and housing age.

The innovation is this: by establishing "expected" rent baselines for any ZIP code profile, we can systematically identify market anomalies. When actual rent is much higher than predicted, that's a red flag for potential overpricing. When it's lower, that might indicate an affordability opportunity.

**[SLIDE 5: Our Three-Dimensional Approach]**

We tackled this problem from three complementary angles, analyzing **54 Jacksonville ZIP codes** across all dimensions:

**Khanh's Dimension: Spatial Mismatch**  
Khanh analyzed the jobs-housing balance - are people living near where they work? He examined:
- Job density ratios
- Transit access percentages
- Commute time patterns
- Transportation mode choices

His spatial mismatch index identifies neighborhoods where residents face long commutes that reduce their effective income and quality of life.

**William's Dimension: Skills Gap**  
William focused on workforce readiness by analyzing:
- Educational attainment levels
- Skills prediction errors
- High school completion gaps
- Sector-specific skill mismatches

His work identifies ZIP codes where residents lack the skills needed for available jobs - a critical barrier to economic mobility.

**My Dimension: Housing Affordability**  
I built a machine learning model that predicts what rent *should be* based on local characteristics. By comparing predictions to actual rents, I identified:
- 17 Jacksonville ZIP codes with >20% rent discrepancies
- 280,000 residents affected
- Specific overpriced areas like ZIP 32217 ($370 above prediction)

**[SLIDE 6: Our Integrated Dashboard]**

We didn't just build three separate analyses - we integrated all three dimensions into an interactive choropleth map dashboard. Each ZIP code gets a composite score (0-100) combining all three dimensions.

This shows policymakers the full picture: A ZIP code might have affordable housing but terrible job access. Or great job access but a severe skills gap. Our dashboard reveals where these problems overlap, enabling targeted interventions.

**[SLIDE 7: Technical Performance]**

Our housing affordability model achieved:
- **R² of 0.783** nationally (78.3% of rent variance explained)
- **Mean Absolute Error of $174**
- **Jacksonville-specific: R² of 0.82, MAE of $131** - even better locally

Now let me walk you through how I built the housing affordability model - my part of this team effort.

---

---

## PART 1: HOUSING AFFORDABILITY - MY APPROACH (1.5 minutes)

**[SLIDE 5: Housing Affordability Challenge]**

For my dimension, the challenge was this: **How do you systematically identify which neighborhoods have affordability problems?** 

You can't just look at raw rent prices. A $1,500 apartment might be reasonable in one neighborhood but overpriced in another, depending on local income, education levels, and urban amenities.

**[SLIDE 6: My Machine Learning Solution]**

I built an XGBoost regression model that predicts what rent *should be* based on 12 local characteristics:
- Population density and urban classification
- Education levels (bachelor's degree percentage)
- Median household income
- Employment sector composition
- Housing characteristics

The model was trained on 1,767 ZIP codes across 14 major U.S. cities - not just Jacksonville. This cross-city learning helps the model understand what drives rent in different urban contexts.

Then I compared predictions to actual Jacksonville rents. When actual rent is much higher than predicted, that's a red flag for potential overpricing. When actual rent is lower than predicted, that might indicate an affordability opportunity or undervalued neighborhood.

---

---

## PART 2: KEY VARIABLES & DATA (1.5 minutes)

**[SLIDE 7: Data Source]**

All my data comes from the U.S. Census Bureau's American Community Survey - the 5-Year Estimates covering 2020-2024. This is the gold standard for demographic data: comprehensive, reliable, and publicly available. No proprietary real estate data needed.

**[SLIDE 8: The 12 Features - Show Table]**

I used 12 key features to predict rent. Let me highlight the three most important:

**1. Urban Classification - 47% of predictive power**  
This is the secret weapon. I created a binary indicator: is a ZIP code urban or suburban? Urban means population density over 3,000 people per square mile. 

Why does this matter so much? Because urban areas have fundamental supply constraints - you can't just build more land in downtown Jacksonville. Urban ZIPs in our dataset rent for $400 more on average than suburban ZIPs with similar income and education levels.

**2. Bachelor's Degree Percentage - 18% importance**  
Here's something interesting: education matters *more* than income for predicting rent. Educated renters are willing to pay premiums for walkability, cultural amenities, and urban lifestyle - even beyond what their income alone would suggest.

**3. Median Income - 15% importance**  
This is the obvious one - higher income areas can support higher rents. But notice it's only third. Location and education are stronger signals.

The remaining 20% of predictive power comes from employment sector shares, housing age, median home value, and population size.

---

## PART 3: DATA CLEANING & PREPROCESSING (1 minute)

**[SLIDE 6: Data Cleaning Pipeline]**

Before modeling, we had to clean the data carefully. We removed 231 ZIP codes with missing rent data - about 12% of the original dataset. We can't predict rent for areas where we don't have ground truth.

We also excluded some special cases: military bases like NAS Jacksonville, because military housing operates under non-market rules, and active retirement communities, because they have near-zero workforce participation.

**[SLIDE 7: Feature Engineering]**

We applied log transformations to right-skewed variables like income and home value. This reduces the influence of extreme outliers - think billionaire neighborhoods - and helps the model focus on typical patterns.

After cleaning, we had 1,767 ZIP codes with zero missing values, ready for modeling.

---

## PART 4: MODELING APPROACH (1.5 minutes)

**[SLIDE 8: Model Comparison Table]**

We tested four different models:

1. **Linear Regression** - Our baseline. Simple, interpretable, but assumes linear relationships. R² of 0.682, MAE of $245.

2. **Random Forest** - Better at capturing non-linear patterns. R² improved to 0.761, MAE down to $189.

3. **XGBoost** - Our winner. R² of 0.783, MAE of just $174. This means our average prediction error is $174.

4. **Ensemble** - We tried combining XGBoost and Random Forest, but it only marginally improved performance while doubling computation time.

**[SLIDE 9: Why XGBoost Won]**

We selected XGBoost as our production model for three reasons:

First, **best accuracy** - it explains 78.3% of rent variance across all 1,767 ZIP codes.

Second, **lowest error** - average prediction error of $174 is well within our target of under $200.

Third, **feature importance** - XGBoost gives us clear rankings of what matters most, which is crucial for communicating findings to policymakers.

**[SLIDE 10: Training Protocol]**

We used an 80/20 train-test split, stratified by city to ensure every city was represented in both sets. We tuned hyperparameters using 5-fold cross-validation. The model trained in just 30 seconds on a standard laptop - this is important because it means we can retrain quarterly as new Census data comes in.

---

## PART 5: RESULTS & PERFORMANCE (2 minutes)

**[SLIDE 11: Figure 1 - Actual vs Predicted Scatter Plot]**

Here's our model performance. Each dot is a ZIP code. The diagonal line represents perfect prediction. You can see most points cluster tightly around that line - that's good.

Our R² of 0.783 means we're explaining about 78% of rent variance. The remaining 22% is likely due to factors we don't have data for - things like crime rates, school quality, and walkability scores.

**[SLIDE 12: Figure 2 - Residual Plot]**

This plot shows our prediction errors. The key thing to look for is random scatter around zero - which is what we see. No systematic bias. The model isn't consistently over-predicting or under-predicting.

You'll notice slightly more variance at high rent values - that's the luxury market, where prestige and views drive prices beyond what observable characteristics predict.

**[SLIDE 13: Jacksonville-Specific Performance]**

Here's the exciting part: our model performs even *better* on Jacksonville than on the national dataset.

- **National**: R² = 0.783, MAE = $174
- **Jacksonville**: R² = 0.82, MAE = $131

Jacksonville's housing market is more predictable than the national average. The model excels in suburban areas with MAE of just $120, but struggles a bit in luxury urban ZIPs with MAE of $280.

**[SLIDE 14: Figure 4 - Feature Importance]**

This chart shows what drives rent predictions. Urban classification dominates at 47%. Education is second at 18%. Income is third at 15%.

The key insight: **Location and education matter more than income alone.** This has direct policy implications - affordability programs can't just target low-income areas. They need to consider educated but cost-burdened renters in high-amenity urban cores.

---

## PART 6: KEY FINDINGS & POLICY IMPLICATIONS (1.5 minutes)

**[SLIDE 15: Jacksonville ZIP Codes - Map with Flagged Areas]**

We identified **17 Jacksonville ZIP codes** where rent discrepancies exceed 20% - that's more than $200 difference between predicted and actual rent.

**Over-predicted ZIPs** (actual rent is lower than expected):
- **ZIP 32217**: Model predicts $1,631, actual is $1,261 - that's $370 under-predicted, or 29% below expectations
- **ZIP 32250**: $282 under-predicted
- **ZIP 32266**: $268 under-predicted

These might represent affordability opportunities for workforce housing development.

**Under-predicted ZIPs** (actual rent exceeds expectations):
- **ZIP 32063**: Actual rent is $217 higher than predicted
- **ZIP 32087**: $166 higher than predicted

These areas may be experiencing rapid gentrification or market overpricing.

**[SLIDE 16: Impact Numbers]**

These 17 flagged ZIP codes represent approximately **280,000 Jacksonville residents** - that's 28% of the city's population. This gives city planners a clear geographic target for interventions.

**[SLIDE 17: Strategic Recommendations]**

Based on our findings, we recommend:

1. **Target rental assistance programs** to the 17 flagged ZIP codes, prioritizing the 5 with highest discrepancies.

2. **Investigate over-predicted ZIPs** for workforce housing development opportunities. If rent is lower than expected, there may be underutilized land or favorable zoning.

3. **Monitor under-predicted ZIPs** for displacement risk. If actual rent keeps exceeding predictions, consider rent stabilization policies.

4. **Quarterly model retraining** using latest Census data to detect emerging crises early. The 30-second training time makes this operationally feasible.

5. **Integrate crime and school data** in the next iteration. This should improve our R² from 0.78 to 0.85+ based on literature benchmarks.

---

## CONCLUSION (30 seconds)

**[SLIDE 18: Summary]**

To wrap up: We built a machine learning model that explains 78% of rent variance across 1,767 ZIP codes. We identified 17 Jacksonville neighborhoods with significant rent discrepancies, affecting 280,000 residents. And we provided actionable recommendations for city planners.

The model is production-ready, retrainable quarterly, and provides clear geographic targets for housing affordability interventions.

Thank you. I'm happy to take questions.

---

---

---

## TIMING BREAKDOWN

- **Introduction (Team Overview)**: 2.5 minutes
  - Housing crisis context (30 sec)
  - StateofJax problem (45 sec)
  - Our solution overview (30 sec)
  - Three dimensions explained (45 sec)
- **Housing Affordability - My Part**: 6-7 minutes
  - Key Variables & Data (1.5 min)
  - Data Cleaning (1 min)
  - Modeling Approach (1.5 min)
  - Results & Performance (1.5 min)
  - Key Findings & Impact (1.5 min)
- **Conclusion**: 0.5 minutes

**Total: 9-10 minutes** (perfect for 8-10 minute target)

---

## PRESENTATION TIPS

### Pacing
- **Speak at 130-150 words per minute** (conversational pace)
- **Pause after key numbers** to let them sink in
- **Slow down for complex concepts** (like feature importance)

### Emphasis Points
- **47% importance** for urban classification (this is your headline finding)
- **280,000 residents** affected (this is your impact number)
- **$174 average error** (this proves accuracy)
- **17 ZIP codes** flagged (this is your actionable output)

### Body Language
- **Point to figures** when referencing them
- **Use hand gestures** for comparisons (urban vs suburban, predicted vs actual)
- **Make eye contact** with different audience members
- **Smile when delivering good news** (Jacksonville performs better than national average)

### Handling Questions
**Expected questions:**

**Q: Why did you exclude military bases?**
A: Military housing operates under non-market allocation rules. Including them would skew the model because rent isn't determined by market forces - it's set by military policy.

**Q: What about crime and school quality?**
A: Great question. Those are the two biggest missing factors. We don't have that data in the Census ACS tables, but we're planning to integrate Jacksonville Sheriff's Office crime data and Duval County school ratings in the next iteration. Literature suggests this could improve our R² from 0.78 to 0.85.

**Q: How often should the model be retrained?**
A: Quarterly, using the latest ACS 1-Year Estimates when available. The model trains in 30 seconds, so frequent updates are operationally feasible. This lets us detect emerging affordability crises before they become entrenched.

**Q: Can this model be applied to other cities?**
A: Absolutely. The model was trained on 14 cities, so it already generalizes well. For a new city, you'd just need to pull ACS data for that city's ZIP codes and run predictions. No retraining needed unless you want to optimize specifically for that city.

**Q: What's the confidence interval on your predictions?**
A: Our MAE of $174 means 50% of predictions are within ±$174 of actual rent. For a 95% confidence interval, you'd roughly double that to ±$350. So we're quite confident in identifying ZIPs with discrepancies over $200.

---

## SLIDE RECOMMENDATIONS

**Slide 1: Title**
- Team WMK Final Presentation
- Predictive Rent Analysis for Urban Planning in Jacksonville
- Team members: William Hughes, Matthew Hendrickson, Khanh Linh Lieu

**Slide 2: The Housing Affordability Crisis**
- "21.6 million renter households (49%) are cost-burdened"
- "Jacksonville: 14.8% population growth since 2010"
- Photo of Jacksonville skyline
- "Mid-sized cities lack analytical infrastructure"

**Slide 3: The Problem - StateofJax**
- StateofJax logo/description
- "1 million Jacksonville residents served"
- Three problems listed:
  - Resource Misallocation
  - Policy Blind Spots
  - Market Opacity

**Slide 4: Our Solution**
- XGBoost model diagram
- "1,767 ZIP codes across 14 cities"
- "12 urban characteristics analyzed"
- "Predict → Compare → Identify anomalies"

**Slide 5: Our Three-Dimensional Approach**
- Three columns with icons:
  - **Khanh - Spatial Mismatch**
    - Job Density Ratio
    - Transit Access %
    - Commute Patterns
  - **William - Skills Gap**
    - Educational Attainment
    - Skills Prediction Error
    - HS Completion Gaps
  - **Matthew - Housing Affordability**
    - Rent Predictions
    - Price Discrepancies
    - 17 ZIPs Flagged
- "54 Jacksonville ZIP codes analyzed"

**Slide 6: Integrated Dashboard**
- Screenshot of choropleth map showing all 3 dimensions
- "Composite Score: 0-100 scale"
- "Red → Yellow → Green gradient"
- "Shows where problems overlap"

**Slide 7: Technical Performance**
- Housing Affordability Model Results:
  - R² = 0.783 (National)
  - MAE = $174
  - R² = 0.82 (Jacksonville)
  - MAE = $131
- "Now let's dive into Matthew's housing model..."

**Slide 6: Machine Learning Solution**
- XGBoost model diagram
- "1,767 ZIP codes across 14 cities"
- "Predict → Compare → Identify discrepancies"

**Slide 7: Data Source**
- ACS logo
- "U.S. Census Bureau - American Community Survey"
- "2020-2024 data, 1,767 ZIP codes"

**Slide 8: Key Variables**
- Table with top 3 features highlighted:
  - Urban Classification: 47%
  - Bachelor's %: 18%
  - Median Income: 15%

**Slide 6: Data Cleaning**
- Before/After numbers (1,998 → 1,767 ZIPs)
- Icons for excluded categories

**Slide 7: Feature Engineering**
- Urban vs Suburban definition
- Density threshold: 3,000/sq mi

**Slide 8: Model Comparison**
- Table with 4 models
- Highlight XGBoost row

**Slide 9: Why XGBoost**
- Three reasons with icons
- R² = 0.783, MAE = $174

**Slide 10: Training Protocol**
- 80/20 split diagram
- 5-fold CV illustration

**Slide 11: Figure 1**
- Your actual vs predicted scatter plot
- Annotate R² = 0.783

**Slide 12: Figure 2**
- Your residual plot
- Annotate "random scatter = good"

**Slide 13: Jacksonville Performance**
- Side-by-side comparison
- National vs Jacksonville metrics

**Slide 14: Figure 4**
- Your feature importance bar chart
- Highlight top 3 features

**Slide 15: Jacksonville Map**
- Map of Jacksonville with flagged ZIPs
- Color-code: red = over-predicted, blue = under-predicted

**Slide 16: Impact Numbers**
- Big text: "280,000 residents"
- "17 ZIP codes"
- "28% of city population"

**Slide 17: Recommendations**
- 5 bullet points
- Icons for each recommendation

**Slide 18: Summary**
- Key achievements
- "Questions?"

---

## BACKUP SLIDES (if time permits or for Q&A)

**Backup 1: Figure 3 - Residual Distribution**
- Shows approximately normal distribution
- Mean ≈ $0, confirming no bias

**Backup 2: Figure 5 - Rent by City**
- Box plots showing Jacksonville vs other cities
- Jacksonville highlighted in green

**Backup 3: Figure 6 - Urban vs Suburban**
- Violin plots
- $400 urban premium clearly visible

**Backup 4: Detailed ZIP Code Table**
- All 17 flagged ZIPs with numbers
- Predicted, Actual, Difference, Population

**Backup 5: Model Limitations**
- Missing factors (crime, schools, walkability)
- Temporal lag (ACS 5-year estimates)
- Luxury market outliers

**Backup 6: Future Work**
- Integrate crime data
- Add school quality scores
- Quarterly retraining pipeline
- Expand to more cities

---

**Good luck with your presentation! You've got this! 🎉**
