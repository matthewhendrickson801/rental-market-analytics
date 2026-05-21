# Best & Worst Rental Deals Analysis

## Dashboard Link
🌐 **http://localhost:8501**

## Model Performance
- **R² Score**: 0.757 (XGBoost with 38 features)
- **Median Absolute Error**: 5.2%
- **Mean Absolute Error**: 7.7%
- **Dataset**: 1,738 ZIP codes
- **Removed**: 16 military bases + 12 retirement communities = 28 total

---

## MIDWEST REGION (342 ZIP codes)

### 🟢 Top 3 Best Deals (Underpriced)

1. **40067 (Louisville, KY)** - BEST DEAL IN MIDWEST
   - Actual Rent: $687
   - Predicted Rent: $1,113
   - **Underpriced by $426 (38.3%)**
   - Median Income: $97,684
   - Poverty Rate: 8.7%
   - **Why**: High-income suburban area with surprisingly low rents

2. **40013 (Louisville, KY)**
   - Actual Rent: $722
   - Predicted Rent: $1,148
   - **Underpriced by $426 (37.1%)**
   - Median Income: $100,226
   - Poverty Rate: 11.3%
   - **Why**: Affluent suburb with moderate rents, excellent value

3. **47115 (Louisville, KY)**
   - Actual Rent: $632
   - Predicted Rent: $988
   - **Underpriced by $356 (36.1%)**
   - Median Income: $88,229
   - Poverty Rate: 7.9%
   - **Why**: Strong income-to-rent ratio

### 🔴 Top 3 Worst Deals (Overpriced)

1. **43136 (Columbus, OH)** - WORST DEAL IN MIDWEST
   - Actual Rent: $1,985
   - Predicted Rent: $1,412
   - **Overpriced by $573 (40.6%)**
   - Median Income: $114,375
   - Poverty Rate: 9.5%
   - **Why**: Premium pricing in suburban Columbus

2. **43146 (Columbus, OH)**
   - Actual Rent: $1,178
   - Predicted Rent: $879
   - **Overpriced by $299 (33.9%)**
   - Median Income: $81,191
   - Poverty Rate: 7.1%
   - **Why**: Rents exceed fundamentals

3. **47468 (Indianapolis, IN)**
   - Actual Rent: $1,652
   - Predicted Rent: $1,267
   - **Overpriced by $385 (30.4%)**
   - Median Income: $92,880
   - Poverty Rate: 11.3%
   - **Why**: Supply constraints or location premium

---

## SOUTH REGION (574 ZIP codes)

### 🟢 Top 3 Best Deals (Underpriced)

1. **29743 (Charlotte, NC)** - BEST DEAL IN SOUTH
   - Actual Rent: $862
   - Predicted Rent: $1,356
   - **Underpriced by $494 (36.4%)**
   - Median Income: $86,064
   - Poverty Rate: 4.5%
   - **Why**: Strong income base with competitive rental pricing

2. **37085 (Nashville, TN)**
   - Actual Rent: $978
   - Predicted Rent: $1,508
   - **Underpriced by $530 (35.1%)**
   - Median Income: $119,405
   - Poverty Rate: 3.1%
   - **Why**: High-income area with below-market rents

3. **37048 (Nashville, TN)**
   - Actual Rent: $1,148
   - Predicted Rent: $1,718
   - **Underpriced by $570 (33.2%)**
   - Median Income: $100,446
   - Poverty Rate: 6.8%
   - **Why**: Affluent Nashville suburb with great value

### 🔴 Top 3 Worst Deals (Overpriced)

1. **78861 (San Antonio, TX)** - WORST DEAL IN SOUTH
   - Actual Rent: $1,391
   - Predicted Rent: $926
   - **Overpriced by $465 (50.2%)**
   - Median Income: $64,917
   - Poverty Rate: 17.8%
   - **Why**: Rents far exceed income levels

2. **29714 (Charlotte, NC)**
   - Actual Rent: $1,335
   - Predicted Rent: $920
   - **Overpriced by $415 (45.1%)**
   - Median Income: $70,475
   - Poverty Rate: 16.2%
   - **Why**: Possible gentrification pressure

3. **33711 (Tampa, FL)**
   - Actual Rent: $1,897
   - Predicted Rent: $1,355
   - **Overpriced by $542 (40.0%)**
   - Median Income: $66,540
   - Poverty Rate: 21.9%
   - **Why**: Coastal premium, high demand

---

## HIGH COST REGION (822 ZIP codes)

### 🟢 Top 3 Best Deals (Underpriced)

1. **21915 (Philadelphia, PA)** - BEST DEAL OVERALL
   - Actual Rent: $825
   - Predicted Rent: $1,656
   - **Underpriced by $831 (50.2%)**
   - Median Income: $95,875
   - Poverty Rate: 13.1%
   - **Why**: Best value in entire dataset, strong income with low rents

2. **76527 (Austin, TX)**
   - Actual Rent: $658
   - Predicted Rent: $1,284
   - **Underpriced by $626 (48.8%)**
   - Median Income: $81,574
   - Poverty Rate: 22.4%
   - **Why**: Austin exurb with very affordable rents

3. **21912 (Philadelphia, PA)**
   - Actual Rent: $817
   - Predicted Rent: $1,508
   - **Underpriced by $691 (45.8%)**
   - Median Income: $69,868
   - Poverty Rate: 9.1%
   - **Why**: Moderate-income area with surprisingly low rents

### 🔴 Top 3 Worst Deals (Overpriced)

1. **94514 (San Francisco, CA)** - WORST DEAL OVERALL
   - Actual Rent: $2,652
   - Predicted Rent: $1,412
   - **Overpriced by $1,240 (87.8%)**
   - Median Income: $76,511
   - Poverty Rate: 18.9%
   - **Why**: Extreme Bay Area premium, rents nearly double fundamentals

2. **94939 (San Francisco, CA)**
   - Actual Rent: $3,278
   - Predicted Rent: $2,160
   - **Overpriced by $1,118 (51.7%)**
   - Median Income: $203,988
   - Poverty Rate: 8.3%
   - **Why**: Ultra-premium Marin County location

3. **80603 (Denver, CO)**
   - Actual Rent: $2,578
   - Predicted Rent: $1,711
   - **Overpriced by $867 (50.6%)**
   - Median Income: $118,297
   - Poverty Rate: 7.6%
   - **Why**: Denver metro premium pricing

---

## Key Insights

### Data Quality Improvements
- **Removed 12 retirement communities** with abnormally low labor force participation (<40%)
- Retirement communities distort rental markets due to age-restricted housing and different demand patterns
- Model R² improved from 0.739 to 0.757 after removal

### Regional Patterns

**Midwest**: Louisville dominates best deals (3 of top 3). Columbus shows overpricing in suburban areas. Louisville appears to have more affordable rental market relative to incomes.

**South**: Best deals in Charlotte and Nashville suburbs. Worst deals in San Antonio and Tampa. Florida markets show coastal premiums.

**High Cost**: Best deals in Philadelphia suburbs and Austin exurbs. Worst deals in San Francisco Bay Area. Bay Area shows most extreme overpricing (87.8% worst deal).

### Common Characteristics

**Best Deals (Underpriced)**:
- High median incomes ($70k-$150k)
- Low poverty rates (3-13%)
- Suburban locations
- Strong income-to-rent ratios
- Competitive rental markets

**Worst Deals (Overpriced)**:
- Mixed income levels
- Often higher poverty rates
- Coastal/tourist areas (Florida)
- Bay Area premium (San Francisco)
- Supply constraints or gentrification pressure

### Model Accuracy
- Model performs well with median error of only 5.2%
- 50% of predictions within ±5.2% of actual rent
- R² of 0.757 indicates model explains 75.7% of rent variation
- Extreme outliers (>40% discrepancy) represent genuine market inefficiencies or location-specific factors not captured by the 38 features
