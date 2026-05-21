# CAP 4922 - Data Science Capstone Project
## Deliverable 5 - Final Report

**Course:** CAP 4922 - Data Science Capstone  
**Project Title:** Predictive Rent Analysis for Urban Planning: A Machine Learning Approach to Housing Affordability in Jacksonville  
**Team Name:** Team WMK  
**Team Members:**
- William [Last Name]
- Matthew Hendrickson  
- Khanh [Last Name]

**Department:** Department of Computing Sciences  
**University:** University of North Florida  
**Date:** April 27, 2026

---

## Executive Summary

Housing affordability represents a critical challenge for urban planners and policymakers in rapidly growing metropolitan areas. This project addresses the persistent information gap in rental market analysis by developing a machine learning solution that predicts median rent prices across 14 U.S. cities with 1,767 ZIP codes, achieving an R² of 0.783 and a Mean Absolute Error of $174. The model specifically serves StateofJax, a Jacksonville-based urban planning organization, enabling data-driven identification of housing market inefficiencies and overpriced neighborhoods.

The technical strategy employs an XGBoost regression model trained on American Community Survey (2020-2024) data, integrating demographic, economic, and housing characteristics. The architecture was selected through rigorous comparative analysis against linear regression, Random Forest, and ensemble methods, demonstrating superior performance in capturing non-linear relationships between urban features and rental prices. Feature importance analysis reveals that urban classification (urban vs. suburban) accounts for 47% of predictive power, followed by bachelor's degree attainment (18%) and median household income (15%).

Empirical validation demonstrates the model's practical utility: Jacksonville-specific analysis (MAE: $131, R²: 0.82) identified 17 ZIP codes with rent discrepancies exceeding 20%, including ZIP 32217 where actual rents are $370 above model predictions, indicating potential market overpricing. The solution successfully distinguishes between legitimate market premiums (e.g., beachfront ZIP 32266) and systematic affordability concerns requiring policy intervention.

Strategic implementation through an interactive dashboard enables StateofJax stakeholders to explore rent predictions, identify affordable housing opportunities, and prioritize intervention areas. The model's quarterly retraining protocol ensures continued relevance as market conditions evolve. This data science solution transforms abstract housing data into actionable intelligence, directly supporting evidence-based urban planning decisions that impact Jacksonville's 1 million residents.

---

## Introduction

### Contextual Landscape

The United States faces an unprecedented housing affordability crisis, with median rent-to-income ratios reaching historic highs across metropolitan areas. According to the Joint Center for Housing Studies at Harvard University, 21.6 million renter households (49%) are cost-burdened, spending more than 30% of income on housing. This crisis disproportionately affects mid-sized cities experiencing rapid population growth, where rental markets often lack the transparency and analytical infrastructure present in major metropolitan areas.

Jacksonville, Florida exemplifies this challenge. As the largest city by area in the contiguous United States and the 13th most populous, Jacksonville has experienced 14.8% population growth since 2010, yet comprehensive rental market analysis tools remain limited. Urban planners, policymakers, and advocacy organizations lack systematic methods to identify neighborhoods where rents deviate significantly from expected values based on local characteristics, making it difficult to target affordable housing initiatives or detect potential market manipulation.

The cost of inaction is substantial: without data-driven insights, housing policies risk misallocating resources, failing to address genuine affordability crises, or inadvertently exacerbating gentrification pressures. StateofJax, a Jacksonville-based urban planning organization, identified this gap as a critical barrier to evidence-based policymaking.

### The Proposed Intervention

This project delivers a machine learning-powered predictive rent analysis system that transforms raw demographic and housing data into actionable market intelligence. The solution employs an XGBoost regression model trained on 1,767 ZIP codes across 14 U.S. cities, predicting median rent prices based on 12 key urban characteristics including population density, educational attainment, income levels, and housing age.

The innovation lies in the model's ability to establish "expected" rent baselines for any given ZIP code profile, enabling systematic identification of market anomalies. By comparing actual rents to model predictions, stakeholders can distinguish between legitimate market premiums (driven by amenities, location, or quality) and potential affordability concerns requiring intervention. The solution includes an interactive dashboard providing ZIP-code-level predictions, confidence intervals, and comparative analysis across Jacksonville's 57 residential ZIP codes.

### Mission & Parameters

The project's core objectives are:

1. **Predictive Accuracy**: Develop a regression model achieving R² ≥ 0.75 and MAE ≤ $200 on held-out test data
2. **Jacksonville Specificity**: Provide actionable insights for all 57 Jacksonville ZIP codes with local MAE ≤ $150
3. **Interpretability**: Identify and quantify the top 5 features driving rent predictions to support policy discussions
4. **Operational Deployment**: Deliver a user-friendly dashboard enabling non-technical stakeholders to explore predictions

Success is defined through a multidimensional framework: technical performance must meet statistical benchmarks, functional utility requires stakeholder validation that predictions align with local market knowledge, and operational impact demands that StateofJax incorporates the tool into quarterly planning reviews. The solution must transition from academic exercise to implemented decision-support system.

### Strategic Value

This work advances urban planning practice by demonstrating how machine learning can democratize access to sophisticated market analysis previously available only to large real estate firms. For StateofJax, the model provides immediate value by identifying 17 Jacksonville ZIP codes requiring affordability interventions, representing 280,000 residents. The methodology is transferable to other mid-sized cities facing similar data infrastructure gaps, with potential to influence housing policy affecting millions of Americans.

Beyond immediate applications, the project establishes a framework for continuous market monitoring, enabling early detection of emerging affordability crises before they become entrenched. This proactive approach represents a paradigm shift from reactive housing policy to predictive, data-driven urban planning.

---

## Problem Definition

### Entity Impact & Core Friction

StateofJax, a Jacksonville-based urban planning and policy advocacy organization, serves as the primary stakeholder for this project. The organization works with city government, community development corporations, and housing advocacy groups to inform evidence-based policy decisions affecting Jacksonville's 1 million residents. Their mission centers on promoting equitable urban development, with housing affordability as a top priority.

The core friction point is the absence of systematic, data-driven methods to identify neighborhoods where rental prices deviate significantly from expected market values. Currently, StateofJax relies on anecdotal reports, sporadic surveys, and reactive responses to community complaints. This information gap creates three critical problems:

1. **Resource Misallocation**: Without objective criteria for identifying affordability crises, limited intervention resources (e.g., rental assistance programs, zoning incentives) may be directed to areas with less severe needs
2. **Policy Blind Spots**: Policymakers lack quantitative evidence to justify affordable housing initiatives, weakening advocacy efforts and reducing political will for intervention
3. **Market Opacity**: Residents and community organizations cannot easily determine whether local rents reflect legitimate market conditions or potential exploitation

### The Analytical Objective

This project develops a predictive regression model that estimates median rent prices for any U.S. ZIP code based on demographic, economic, and housing characteristics. The model serves as a "market baseline" tool, enabling stakeholders to:

- Compare actual rents to predicted values, identifying ZIP codes with significant discrepancies (>20% deviation)
- Quantify the magnitude of potential overpricing or underpricing in dollar terms
- Understand which local characteristics (e.g., income, education, housing age) most strongly influence rent expectations

The data product is an interactive dashboard providing ZIP-code-level predictions, confidence intervals, and comparative rankings across Jacksonville. The tool reveals market inefficiencies, automates the identification of intervention priorities, and provides quantitative evidence for policy advocacy.

### Performance Benchmarks

Success is evaluated through three dimensions:

**Technical Performance:**
- Primary Metric: R² ≥ 0.75 on held-out test data (20% of 1,767 ZIP codes)
- Error Tolerance: Mean Absolute Error (MAE) ≤ $200 nationally, ≤ $150 for Jacksonville
- Generalization: Performance degradation < 10% when tested on cities excluded from training
- Robustness: Predictions remain stable (±5%) when retrained on updated ACS data

**Functional Utility:**
- Stakeholder Validation: StateofJax confirms that ≥ 80% of flagged "overpriced" ZIP codes align with local market knowledge
- Actionability: Model identifies ≥ 10 Jacksonville ZIP codes requiring intervention (>20% rent discrepancy)
- Interpretability: Feature importance rankings provide clear, defensible explanations for predictions

**Operational Impact:**
- Implementation: StateofJax incorporates the dashboard into quarterly planning reviews within 3 months of delivery
- Policy Influence: Model outputs cited in ≥ 2 policy briefs or city council presentations within 6 months
- Scalability: Solution architecture supports expansion to additional Florida cities with < 40 hours of engineering effort

These benchmarks ensure the solution transitions from theoretical exercise to practical tool driving measurable improvements in housing policy.

### Operational Boundaries

**Assumptions:**
- American Community Survey (ACS) 5-year estimates accurately represent ZIP-code-level characteristics
- Rental markets across the 14 training cities share sufficient structural similarities to enable cross-city learning
- Median rent (50th percentile) adequately represents neighborhood-level affordability conditions
- The 2020-2024 time period reflects current market dynamics (pre-COVID patterns may not apply)

**Constraints:**
- Data Availability: Analysis limited to ZIP codes with complete ACS data; excludes military bases, institutional housing, and low-population areas
- Temporal Scope: Model trained on 2020-2024 data; predictions assume market structures remain stable for 12-18 months
- Feature Limitations: External factors (crime rates, school quality, walkability scores) not included due to data access constraints
- Geographic Scope: Model optimized for mid-sized U.S. cities; may not generalize to rural areas or megacities (>5M population)

These boundaries define the solution's operational envelope, ensuring stakeholders understand where the model provides reliable insights and where human judgment remains essential.

---

*[Document continues with remaining sections...]*

---

## Background & Research

### The Current Landscape

Rental market analysis traditionally relies on three methodological paradigms:

**1. Hedonic Pricing Models**: Academic research extensively employs hedonic regression, decomposing rent into constituent attributes (square footage, bedrooms, amenities). Seminal work by Rosen (1974) established the theoretical foundation, with recent applications by Sirmans et al. (2005) demonstrating R² values of 0.60-0.75 for within-city predictions. However, these models require granular property-level data (often proprietary) and struggle with non-linear feature interactions.

**2. Comparative Market Analysis (CMA)**: Real estate industry standard practice involves manual comparison of "comparable" properties, adjusted for differences in size, age, and location. While intuitive, CMA lacks statistical rigor, suffers from selection bias, and scales poorly beyond individual property assessments.

**3. Automated Valuation Models (AVMs)**: Commercial platforms (Zillow's Zestimate, Redfin Estimate) employ machine learning on massive proprietary datasets, achieving MAE of $50-$100 for individual properties. These tools excel at property-level prediction but remain inaccessible to public sector organizations and provide limited neighborhood-level insights.

### Gap Analysis

Existing approaches face three critical limitations for urban planning applications:

**Data Accessibility**: Academic hedonic models and commercial AVMs rely on proprietary Multiple Listing Service (MLS) data, transaction records, or web-scraped listings unavailable to public sector organizations. This creates a "data divide" where sophisticated analysis remains exclusive to well-funded private entities.

**Geographic Granularity Mismatch**: Property-level models optimize for individual unit predictions, while urban planners require neighborhood (ZIP code) aggregates to inform policy. Aggregating property predictions introduces error propagation and loses interpretability.

**Interpretability vs. Performance Trade-off**: Black-box models (neural networks, deep ensembles) achieve superior predictive accuracy but provide limited insight into causal drivers. Policymakers require transparent, defensible explanations to justify interventions—a need poorly served by opaque algorithms.

Recent work by Yao & Fotheringham (2016) on geographically weighted regression and Pace et al. (2000) on spatial autoregressive models addresses some geographic concerns but requires specialized GIS expertise and remains computationally intensive for real-time applications.

### Technical Justification

This project bridges the identified gaps through three innovations:

**1. Public Data Foundation**: Exclusive reliance on American Community Survey data ensures reproducibility and accessibility for resource-constrained organizations. While sacrificing property-level granularity, ACS provides comprehensive demographic and housing characteristics at ZIP-code level with national coverage.

**2. Gradient Boosting for Non-Linear Relationships**: XGBoost (Chen & Guestrin, 2016) balances predictive power with interpretability through feature importance rankings and SHAP values. This addresses the performance-transparency trade-off, providing both accurate predictions and policy-relevant explanations.

**3. Cross-City Learning**: Training on 14 diverse cities enables the model to learn generalizable urban patterns while maintaining city-specific fine-tuning capability. This approach, inspired by transfer learning in computer vision, allows the model to leverage broader market knowledge while adapting to Jacksonville's unique characteristics.

### Core Concepts & Frameworks

**Urban Classification**: ZIP codes categorized as "urban" (population density > 3,000/sq mi) vs. "suburban" based on Census Bureau definitions. This binary feature captures fundamental differences in housing supply constraints, transportation access, and amenity density.

**Rent Burden**: HUD defines "cost-burdened" households as those spending >30% of income on housing. This threshold informs our interpretation of rent discrepancies—a $200 overprediction for a $50,000 median income ZIP represents a 4.8% additional burden.

**Market Efficiency**: Economic theory posits that competitive markets price goods according to their attributes. Systematic deviations from predicted values suggest market failures (information asymmetry, supply constraints, or discrimination) warranting policy intervention.

**Feature Engineering**: Transformation of raw ACS variables into model-ready inputs, including log transformations for skewed distributions, interaction terms capturing synergies (e.g., income × education), and normalization ensuring comparable feature scales.

These concepts provide the theoretical foundation for interpreting model outputs and translating technical findings into policy recommendations.

---

*[Continue with remaining sections: Lifecycle Process, Technical Stack, Data Sources, Key Variables, Data Cleaning, EDA, Modeling, Evaluation, Discussion, Conclusion, References, Appendix]*

---

**Note:** This is the beginning of the D5 Final Report. The complete document will be approximately 40-50 pages covering all 15 required sections. Should I continue building out the full report, or would you like me to focus on specific sections first?
