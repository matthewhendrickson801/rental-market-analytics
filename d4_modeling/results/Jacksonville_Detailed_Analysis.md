# Jacksonville Detailed Analysis

## Overview

**Total ZIPs Analyzed**: 58  
**Average Actual Rent**: $1,505  
**Average Predicted Rent**: $1,569  
**Average Prediction Error**: $115  
**Model Bias**: -4.3% (model slightly over-predicts)

---

## Summary Statistics

### Rent
- **Range**: $830 - $2,676
- **Median**: $1,516
- **Mean**: $1,505

### Population
- **Range**: 43 - 1,683,960 ⚠️ (outlier detected)
- **Median**: 29,218
- **Mean**: 81,505

### Education
- **Bachelor's+ (avg)**: 33.7%
- **High School (avg)**: 28.2%

### Income
- **Median Household Income (avg)**: $81,505
- **Per Capita Income (avg)**: $43,350

### Urban/Rural Breakdown
- **Urban**: 28 ZIPs (48.3%)
- **Suburban**: 22 ZIPs (37.9%)
- **Rural**: 8 ZIPs (13.8%)

---

## Top 10 Underpriced Opportunities

These ZIPs have **positive residuals** - the model predicts higher rent than actual, suggesting affordable housing opportunities.

| Rank | ZIP | Actual Rent | Predicted Rent | Opportunity | Population | Bachelor's+ | Median Income | Type |
|------|-----|-------------|----------------|-------------|------------|-------------|---------------|------|
| 1 | 32087 | $1,518 | $999 | **+$519** (34%) | 4,608 | 4.5% | $67,097 | Rural |
| 2 | 32097 | $1,892 | $1,729 | **+$163** (9%) | 26,700 | 28.1% | $93,161 | Suburban |
| 3 | 32063 | $1,385 | $1,241 | **+$144** (10%) | 14,611 | 22.9% | $75,683 | Suburban |
| 4 | 32095 | $2,676 | $2,545 | **+$131** (5%) | 21,399 | 56.4% | $136,038 | Suburban |
| 5 | 32033 | $1,752 | $1,633 | **+$119** (7%) | 4,556 | 20.3% | $86,185 | Rural |
| 6 | 32040 | $1,189 | $1,092 | **+$97** (8%) | 8,978 | 17.9% | $84,095 | Suburban |
| 7 | 32084 | $1,567 | $1,472 | **+$95** (6%) | 37,291 | 33.1% | $73,837 | Urban |
| 8 | 32092 | $2,424 | $2,347 | **+$77** (3%) | 53,071 | 51.4% | $131,020 | Urban |
| 9 | 32145 | $1,113 | $1,055 | **+$58** (5%) | 5,759 | 12.6% | $75,557 | Rural |
| 10 | 32246 | $1,761 | $1,735 | **+$26** (2%) | 62,562 | 39.6% | $80,963 | Urban |

### Key Insights
- **32087** shows the largest opportunity but has very low education (4.5% bachelor's) - may indicate data quality issue or unique area
- **32095** is the most expensive ZIP but still underpriced relative to its high education (56.4%) and income ($136K)
- Most opportunities are in **Suburban** and **Rural** areas

---

## Top 10 Overpriced ZIPs

These ZIPs have **negative residuals** - the model predicts lower rent than actual, suggesting location premiums not captured by features.

| Rank | ZIP | Actual Rent | Predicted Rent | Premium | Population | Bachelor's+ | Median Income | Type |
|------|-----|-------------|----------------|---------|------------|-------------|---------------|------|
| 1 | 32072 | $1,518 | $2,150 | **-$632** (42%) | 43 ⚠️ | 81.4% | $0 ⚠️ | Rural |
| 2 | 32222 | $1,795 | $2,155 | **-$360** (20%) | 18,258 | 27.9% | $85,649 | Suburban |
| 3 | 32266 | $1,763 | $2,012 | **-$249** (14%) | 7,168 | 60.9% | $119,294 | Rural |
| 4 | 32217 | $1,261 | $1,506 | **-$245** (19%) | 20,221 | 41.3% | $73,832 | Suburban |
| 5 | 32205 | $1,263 | $1,481 | **-$218** (17%) | 29,148 | 37.9% | $64,789 | Suburban |
| 6 | 32224 | $1,764 | $1,973 | **-$209** (12%) | 42,092 | 56.9% | $88,259 | Urban |
| 7 | 32223 | $1,587 | $1,788 | **-$201** (13%) | 26,160 | 45.0% | $95,347 | Suburban |
| 8 | 32034 | $1,605 | $1,802 | **-$197** (12%) | 41,029 | 53.0% | $98,583 | Urban |
| 9 | 32206 | $860 | $1,040 | **-$180** (21%) | 17,105 | 22.6% | $39,242 | Suburban |
| 10 | 32081 | $1,763 | $1,936 | **-$173** (10%) | 29,784 | 72.0% | $131,624 | Urban |

### Key Insights
- **32072** is a major outlier (43 people, $0 income) - likely bad data ⚠️
- **32081** has extremely high education (72% bachelor's+) but lower rent than expected
- Several high-education ZIPs are "cheaper" than fundamentals suggest

---

## Data Quality Issues ⚠️

### Critical Issues
1. **ZIP 32072**: Population of 43, $0 median income, but 81.4% bachelor's degrees
   - Likely a data collection error or special-use ZIP
   
2. **ZIP 27260**: Population of 1,683,960 in a single ZIP
   - This is clearly incorrect - may be a data merge error
   
3. **ZIP 32087**: Only 4.5% bachelor's degrees but $67K income
   - Unusual combination - may indicate blue-collar/trade-heavy area

### Recommendations
- Remove or investigate ZIPs with extreme outliers (32072, 27260)
- Validate education data for 32087
- Consider excluding ZIPs with population < 1,000 as potentially non-residential

---

## All Jacksonville ZIPs (Sorted by Opportunity)

| ZIP | Actual Rent | Predicted Rent | Opportunity | Population | Bachelor's+ | Median Income | Type |
|-----|-------------|----------------|-------------|------------|-------------|---------------|------|
| 32087 | $1,518 | $999 | +$519 | 4,608 | 4.5% | $67,097 | Rural |
| 32097 | $1,892 | $1,729 | +$163 | 26,700 | 28.1% | $93,161 | Suburban |
| 32063 | $1,385 | $1,241 | +$144 | 14,611 | 22.9% | $75,683 | Suburban |
| 32095 | $2,676 | $2,545 | +$131 | 21,399 | 56.4% | $136,038 | Suburban |
| 32033 | $1,752 | $1,633 | +$119 | 4,556 | 20.3% | $86,185 | Rural |
| 32040 | $1,189 | $1,092 | +$97 | 8,978 | 17.9% | $84,095 | Suburban |
| 32084 | $1,567 | $1,472 | +$95 | 37,291 | 33.1% | $73,837 | Urban |
| 32092 | $2,424 | $2,347 | +$77 | 53,071 | 51.4% | $131,020 | Urban |
| 32145 | $1,113 | $1,055 | +$58 | 5,759 | 12.6% | $75,557 | Rural |
| 32246 | $1,761 | $1,735 | +$26 | 62,562 | 39.6% | $80,963 | Urban |
| 32221 | $1,708 | $1,689 | +$19 | 32,833 | 24.4% | $82,969 | Urban |
| 32065 | $1,743 | $1,734 | +$9 | 41,578 | 24.8% | $97,455 | Urban |
| 32259 | $2,257 | $2,248 | +$9 | 75,016 | 55.4% | $150,736 | Urban |
| 32043 | $1,545 | $1,544 | +$1 | 34,562 | 29.1% | $84,145 | Urban |
| 32080 | $1,788 | $1,788 | $0 | 20,894 | 53.6% | $92,531 | Suburban |
| 32219 | $1,292 | $1,300 | -$8 | 14,302 | 21.5% | $72,184 | Suburban |
| 32218 | $1,503 | $1,513 | -$10 | 72,905 | 26.0% | $69,638 | Urban |
| 32202 | $1,124 | $1,135 | -$11 | 6,023 | 17.9% | $34,825 | Rural |
| 32220 | $1,330 | $1,357 | -$27 | 12,298 | 19.6% | $81,792 | Suburban |
| 32210 | $1,293 | $1,325 | -$32 | 65,729 | 22.9% | $61,050 | Urban |
| 32208 | $1,214 | $1,246 | -$32 | 32,699 | 15.6% | $41,324 | Urban |
| 32227 | $1,799 | $1,837 | -$38 | 3,207 | 19.7% | $85,833 | Rural |
| 32009 | $919 | $963 | -$44 | 4,045 | 17.5% | $72,792 | Rural |
| 32233 | $1,681 | $1,727 | -$46 | 24,633 | 44.4% | $89,185 | Suburban |
| 32256 | $1,698 | $1,745 | -$47 | 58,192 | 52.8% | $73,570 | Urban |
| 32254 | $1,187 | $1,238 | -$51 | 13,927 | 11.7% | $34,953 | Suburban |
| 32277 | $1,378 | $1,431 | -$53 | 36,338 | 25.9% | $61,554 | Urban |
| 32258 | $1,928 | $1,986 | -$58 | 40,408 | 47.0% | $102,204 | Urban |
| 32234 | $1,096 | $1,155 | -$59 | 9,678 | 20.0% | $87,331 | Suburban |
| 32211 | $1,185 | $1,247 | -$62 | 36,762 | 21.6% | $57,021 | Urban |
| 32225 | $1,729 | $1,798 | -$69 | 55,905 | 44.5% | $90,559 | Urban |
| 32209 | $1,062 | $1,133 | -$71 | 34,657 | 12.5% | $30,514 | Urban |
| 32011 | $1,120 | $1,196 | -$76 | 15,421 | 15.2% | $76,677 | Suburban |
| 32086 | $1,601 | $1,679 | -$78 | 34,855 | 35.5% | $76,512 | Urban |
| 32244 | $1,470 | $1,554 | -$84 | 63,592 | 25.5% | $62,204 | Urban |
| 32046 | $917 | $1,003 | -$86 | 10,593 | 12.4% | $71,563 | Suburban |
| 32207 | $1,266 | $1,354 | -$88 | 36,998 | 39.2% | $65,234 | Urban |
| 32068 | $1,391 | $1,485 | -$94 | 58,983 | 22.7% | $84,431 | Urban |
| 32204 | $1,167 | $1,269 | -$102 | 9,151 | 42.4% | $65,063 | Suburban |
| 32656 | $1,089 | $1,203 | -$114 | 15,836 | 22.4% | $74,213 | Suburban |
| 32216 | $1,364 | $1,481 | -$117 | 42,298 | 33.4% | $61,821 | Urban |
| 32257 | $1,518 | $1,640 | -$122 | 42,904 | 36.6% | $75,780 | Urban |
| 32082 | $1,925 | $2,050 | -$125 | 29,289 | 70.5% | $124,558 | Suburban |
| 27260 | $1,513 | $1,641 | -$128 | 1,683,960 ⚠️ | 36.5% | $79,643 | Urban |
| 32003 | $1,935 | $2,076 | -$141 | 29,766 | 49.6% | $116,611 | Urban |
| 32250 | $1,787 | $1,930 | -$143 | 29,072 | 54.6% | $117,724 | Suburban |
| 32073 | $1,472 | $1,633 | -$161 | 43,561 | 26.7% | $76,455 | Urban |
| 32091 | $830 | $992 | -$162 | 14,719 | 18.0% | $62,852 | Suburban |
| 32081 | $1,763 | $1,936 | -$173 | 29,784 | 72.0% | $131,624 | Urban |
| 32206 | $860 | $1,040 | -$180 | 17,105 | 22.6% | $39,242 | Suburban |
| 32034 | $1,605 | $1,802 | -$197 | 41,029 | 53.0% | $98,583 | Urban |
| 32223 | $1,587 | $1,788 | -$201 | 26,160 | 45.0% | $95,347 | Suburban |
| 32224 | $1,764 | $1,973 | -$209 | 42,092 | 56.9% | $88,259 | Urban |
| 32205 | $1,263 | $1,481 | -$218 | 29,148 | 37.9% | $64,789 | Suburban |
| 32217 | $1,261 | $1,506 | -$245 | 20,221 | 41.3% | $73,832 | Suburban |
| 32266 | $1,763 | $2,012 | -$249 | 7,168 | 60.9% | $119,294 | Rural |
| 32222 | $1,795 | $2,155 | -$360 | 18,258 | 27.9% | $85,649 | Suburban |
| 32072 | $1,518 | $2,150 | -$632 | 43 ⚠️ | 81.4% | $0 ⚠️ | Rural |

---

## Questions for Local Validation

As a Jacksonville resident, please review:

1. **Do these rent values look accurate for 2020-2024?**
   - Beaches (32250): $1,787
   - San Marco (32207): $1,266
   - Riverside (32205): $1,263
   - Ponte Vedra (32082): $1,925

2. **Are these ZIPs correctly classified?**
   - Urban vs Suburban vs Rural designations

3. **Known neighborhoods - any surprises?**
   - Which ZIPs are the "good deals" you'd recommend?
   - Which ZIPs are overpriced for what you get?

4. **Data quality issues:**
   - ZIP 32072 (43 people, $0 income) - what is this?
   - ZIP 27260 (1.68M people) - clearly wrong
   - ZIP 32087 (4.5% bachelor's) - does this match reality?

---

## Model Performance for Jacksonville

- **Mean Absolute Error**: $115
- **Bias**: -7.8% (model over-predicts by ~$108 on average)
- **Best predictions**: ZIPs with typical education/income profiles
- **Worst predictions**: Outlier ZIPs with data quality issues

The model performs reasonably well for Jacksonville, with most predictions within $100-200 of actual rent.
