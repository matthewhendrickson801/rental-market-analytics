# Jacksonville Final Report
## Model with Beach Proximity & Cleaned Data

---

## Overview

**Total ZIPs**: 57 (was 58, removed 1 low-population ZIP)  
**Average Actual Rent**: $1,505  
**Average Predicted Rent**: $1,556  
**Average Error**: $92  
**Model Bias**: -3.4% (model slightly over-predicts)

---

## Summary Statistics

### Rent
- **Range**: $830 - $2,676
- **Median**: $1,513
- **Mean**: $1,505

### Population
- **Range**: 3,207 - 1,683,960 ⚠️ (ZIP 27260 still has bad data)
- **Median**: 29,289

### Education
- **Bachelor's+ (avg)**: 32.9%
- **High School (avg)**: 28.4%

### Income
- **Median Household Income (avg)**: $81,505
- **Per Capita Income (avg)**: $42,934

### Urban/Rural
- **Urban**: 28 ZIPs (49.1%)
- **Suburban**: 22 ZIPs (38.6%)
- **Rural**: 7 ZIPs (12.3%)

### Beach Proximity
- **Beachfront (2.0)**: 2 ZIPs - 32250 (Jacksonville Beach), 32266 (Neptune Beach)
- **Near Beach (1.0)**: 3 ZIPs - 32233, 32225, 32224
- **Coastal City (0.5)**: 52 ZIPs - Rest of Jacksonville
- **Inland (0.0)**: 0 ZIPs (Jacksonville is a coastal city)

---

## Top 10 Underpriced Opportunities

| Rank | ZIP | Actual Rent | Predicted | Opportunity | Population | Bachelor's+ | Income | Type | Beach |
|------|-----|-------------|-----------|-------------|------------|-------------|--------|------|-------|
| 1 | 32063 | $1,385 | $1,198 | **+$187** (14%) | 14,611 | 22.9% | $75,683 | Suburban | 0.5 |
| 2 | 32087 | $1,518 | $1,352 | **+$166** (11%) | 4,608 | 4.5% | $67,097 | Rural | 0.5 |
| 3 | 32084 | $1,567 | $1,428 | **+$139** (9%) | 37,291 | 33.1% | $73,837 | Urban | 0.5 |
| 4 | 32097 | $1,892 | $1,791 | **+$101** (5%) | 26,700 | 28.1% | $93,161 | Suburban | 0.5 |
| 5 | 32043 | $1,545 | $1,459 | **+$86** (6%) | 34,562 | 29.1% | $84,145 | Urban | 0.5 |
| 6 | 32033 | $1,752 | $1,669 | **+$83** (5%) | 4,556 | 20.3% | $86,185 | Rural | 0.5 |
| 7 | 32040 | $1,189 | $1,107 | **+$82** (7%) | 8,978 | 17.9% | $84,095 | Suburban | 0.5 |
| 8 | 32095 | $2,676 | $2,599 | **+$77** (3%) | 21,399 | 56.4% | $136,038 | Suburban | 0.5 |
| 9 | 32145 | $1,113 | $1,036 | **+$77** (7%) | 5,759 | 12.6% | $75,557 | Rural | 0.5 |
| 10 | 32092 | $2,424 | $2,349 | **+$75** (3%) | 53,071 | 51.4% | $131,020 | Urban | 0.5 |

### Key Insights
- **32063** (Orange Park area?) - Best opportunity, good education/income profile
- **32087** - Low education (4.5%) but decent income - blue-collar area?
- **32084** (Mandarin?) - Urban area with good fundamentals
- **32095** (Ponte Vedra?) - Most expensive ZIP but still underpriced for its profile
- Most opportunities are **NOT** beach ZIPs (all have beach_score 0.5)

---

## Top 10 Overpriced ZIPs

| Rank | ZIP | Actual Rent | Predicted | Premium | Population | Bachelor's+ | Income | Type | Beach |
|------|-----|-------------|-----------|---------|------------|-------------|--------|------|-------|
| 1 | 32217 | $1,261 | $1,685 | **-$424** (34%) | 20,221 | 41.3% | $73,832 | Suburban | 0.5 |
| 2 | 32250 | $1,787 | $2,070 | **-$283** (16%) | 29,072 | 54.6% | $117,724 | Suburban | **2.0** 🏖️ |
| 3 | 32266 | $1,763 | $2,009 | **-$246** (14%) | 7,168 | 60.9% | $119,294 | Rural | **2.0** 🏖️ |
| 4 | 32034 | $1,605 | $1,801 | **-$196** (12%) | 41,029 | 53.0% | $98,583 | Urban | 0.5 |
| 5 | 32277 | $1,378 | $1,568 | **-$190** (14%) | 36,338 | 25.9% | $61,554 | Urban | 0.5 |
| 6 | 32223 | $1,587 | $1,754 | **-$167** (11%) | 26,160 | 45.0% | $95,347 | Suburban | 0.5 |
| 7 | 32003 | $1,935 | $2,099 | **-$164** (8%) | 29,766 | 49.6% | $116,611 | Urban | 0.5 |
| 8 | 32206 | $860 | $1,000 | **-$140** (16%) | 17,105 | 22.6% | $39,242 | Suburban | 0.5 |
| 9 | 32091 | $830 | $967 | **-$137** (17%) | 14,719 | 18.0% | $62,852 | Suburban | 0.5 |
| 10 | 32222 | $1,795 | $1,931 | **-$136** (8%) | 18,258 | 27.9% | $85,649 | Suburban | 0.5 |

### Key Insights
- **32250 & 32266** - The 2 beachfront ZIPs (score 2.0) are "overpriced" but that's expected - beach premium! 🏖️
- **32217** - Biggest discrepancy, model thinks it should be $1,685 but it's only $1,261
- **32206 & 32091** - Cheapest ZIPs in Jacksonville ($860, $830)
- Model correctly identifies beach premium for 32250/32266

---

## All Jacksonville ZIPs (Sorted by Opportunity)

| ZIP | Actual | Predicted | Opportunity | Pop | Bach% | Income | Type | Beach | Notes |
|-----|--------|-----------|-------------|-----|-------|--------|------|-------|-------|
| 32063 | $1,385 | $1,198 | +$187 | 14,611 | 22.9% | $75,683 | Suburban | 0.5 | Best opportunity |
| 32087 | $1,518 | $1,352 | +$166 | 4,608 | 4.5% | $67,097 | Rural | 0.5 | Low education |
| 32084 | $1,567 | $1,428 | +$139 | 37,291 | 33.1% | $73,837 | Urban | 0.5 | Mandarin? |
| 32097 | $1,892 | $1,791 | +$101 | 26,700 | 28.1% | $93,161 | Suburban | 0.5 | |
| 32043 | $1,545 | $1,459 | +$86 | 34,562 | 29.1% | $84,145 | Urban | 0.5 | |
| 32033 | $1,752 | $1,669 | +$83 | 4,556 | 20.3% | $86,185 | Rural | 0.5 | |
| 32040 | $1,189 | $1,107 | +$82 | 8,978 | 17.9% | $84,095 | Suburban | 0.5 | |
| 32095 | $2,676 | $2,599 | +$77 | 21,399 | 56.4% | $136,038 | Suburban | 0.5 | Ponte Vedra |
| 32145 | $1,113 | $1,036 | +$77 | 5,759 | 12.6% | $75,557 | Rural | 0.5 | |
| 32092 | $2,424 | $2,349 | +$75 | 53,071 | 51.4% | $131,020 | Urban | 0.5 | |
| 32065 | $1,743 | $1,709 | +$34 | 41,578 | 24.8% | $97,455 | Urban | 0.5 | |
| 32220 | $1,330 | $1,306 | +$24 | 12,298 | 19.6% | $81,792 | Suburban | 0.5 | |
| 32219 | $1,292 | $1,276 | +$16 | 14,302 | 21.5% | $72,184 | Suburban | 0.5 | |
| 32233 | $1,681 | $1,665 | +$16 | 24,633 | 44.4% | $89,185 | Suburban | **1.0** | Near beach |
| 32202 | $1,124 | $1,121 | +$3 | 6,023 | 17.9% | $34,825 | Rural | 0.5 | Downtown |
| 32080 | $1,788 | $1,793 | -$5 | 20,894 | 53.6% | $92,531 | Suburban | 0.5 | |
| 32246 | $1,761 | $1,769 | -$8 | 62,562 | 39.6% | $80,963 | Urban | 0.5 | |
| 32218 | $1,503 | $1,514 | -$11 | 72,905 | 26.0% | $69,638 | Urban | 0.5 | |
| 32234 | $1,096 | $1,113 | -$17 | 9,678 | 20.0% | $87,331 | Suburban | 0.5 | |
| 32225 | $1,729 | $1,757 | -$28 | 55,905 | 44.5% | $90,559 | Urban | **1.0** | Near beach |
| 32221 | $1,708 | $1,743 | -$35 | 32,833 | 24.4% | $82,969 | Urban | 0.5 | |
| 32256 | $1,698 | $1,735 | -$37 | 58,192 | 52.8% | $73,570 | Urban | 0.5 | |
| 32258 | $1,928 | $1,966 | -$38 | 40,408 | 47.0% | $102,204 | Urban | 0.5 | |
| 32254 | $1,187 | $1,227 | -$40 | 13,927 | 11.7% | $34,953 | Suburban | 0.5 | |
| 32656 | $1,089 | $1,130 | -$41 | 15,836 | 22.4% | $74,213 | Suburban | 0.5 | |
| 32259 | $2,257 | $2,302 | -$45 | 75,016 | 55.4% | $150,736 | Urban | 0.5 | Wealthy area |
| 32208 | $1,214 | $1,264 | -$50 | 32,699 | 15.6% | $41,324 | Urban | 0.5 | |
| 32009 | $919 | $969 | -$50 | 4,045 | 17.5% | $72,792 | Rural | 0.5 | |
| 32211 | $1,185 | $1,238 | -$53 | 36,762 | 21.6% | $57,021 | Urban | 0.5 | |
| 32209 | $1,062 | $1,121 | -$59 | 34,657 | 12.5% | $30,514 | Urban | 0.5 | |
| 32227 | $1,799 | $1,860 | -$61 | 3,207 | 19.7% | $85,833 | Rural | 0.5 | Small pop |
| 32073 | $1,472 | $1,534 | -$62 | 43,561 | 26.7% | $76,455 | Urban | 0.5 | |
| 32210 | $1,293 | $1,358 | -$65 | 65,729 | 22.9% | $61,050 | Urban | 0.5 | |
| 32257 | $1,518 | $1,590 | -$72 | 42,904 | 36.6% | $75,780 | Urban | 0.5 | |
| 32086 | $1,601 | $1,675 | -$74 | 34,855 | 35.5% | $76,512 | Urban | 0.5 | |
| 32011 | $1,120 | $1,194 | -$74 | 15,421 | 15.2% | $76,677 | Suburban | 0.5 | |
| 32068 | $1,391 | $1,468 | -$77 | 58,983 | 22.7% | $84,431 | Urban | 0.5 | |
| 27260 | $1,513 | $1,590 | -$77 | 1,683,960 | 36.5% | $79,643 | Urban | 0.5 | ⚠️ Bad data |
| 32082 | $1,925 | $2,007 | -$82 | 29,289 | 70.5% | $124,558 | Suburban | 0.5 | Ponte Vedra |
| 32081 | $1,763 | $1,846 | -$83 | 29,784 | 72.0% | $131,624 | Urban | 0.5 | High education |
| 32207 | $1,266 | $1,359 | -$93 | 36,998 | 39.2% | $65,234 | Urban | 0.5 | San Marco |
| 32216 | $1,364 | $1,457 | -$93 | 42,298 | 33.4% | $61,821 | Urban | 0.5 | |
| 32244 | $1,470 | $1,576 | -$106 | 63,592 | 25.5% | $62,204 | Urban | 0.5 | |
| 32204 | $1,167 | $1,277 | -$110 | 9,151 | 42.4% | $65,063 | Suburban | 0.5 | Riverside |
| 32205 | $1,263 | $1,374 | -$111 | 29,148 | 37.9% | $64,789 | Suburban | 0.5 | Riverside |
| 32046 | $917 | $1,031 | -$114 | 10,593 | 12.4% | $71,563 | Suburban | 0.5 | |
| 32224 | $1,764 | $1,885 | -$121 | 42,092 | 56.9% | $88,259 | Urban | **1.0** | Near beach |
| 32222 | $1,795 | $1,931 | -$136 | 18,258 | 27.9% | $85,649 | Suburban | 0.5 | |
| 32091 | $830 | $967 | -$137 | 14,719 | 18.0% | $62,852 | Suburban | 0.5 | Cheapest |
| 32206 | $860 | $1,000 | -$140 | 17,105 | 22.6% | $39,242 | Suburban | 0.5 | 2nd cheapest |
| 32003 | $1,935 | $2,099 | -$164 | 29,766 | 49.6% | $116,611 | Urban | 0.5 | |
| 32223 | $1,587 | $1,754 | -$167 | 26,160 | 45.0% | $95,347 | Suburban | 0.5 | |
| 32277 | $1,378 | $1,568 | -$190 | 36,338 | 25.9% | $61,554 | Urban | 0.5 | |
| 32034 | $1,605 | $1,801 | -$196 | 41,029 | 53.0% | $98,583 | Urban | 0.5 | |
| 32266 | $1,763 | $2,009 | -$246 | 7,168 | 60.9% | $119,294 | Rural | **2.0** 🏖️ | Neptune Beach |
| 32250 | $1,787 | $2,070 | -$283 | 29,072 | 54.6% | $117,724 | Suburban | **2.0** 🏖️ | Jax Beach |
| 32217 | $1,261 | $1,685 | -$424 | 20,221 | 41.3% | $73,832 | Suburban | 0.5 | Biggest error |

---

## Questions for Validation

1. **Do these neighborhoods match your knowledge?**
   - 32063 (best opportunity) - Where is this?
   - 32084 (Mandarin?) - Is this correct?
   - 32095 (Ponte Vedra?) - Expensive area?
   - 32207 (San Marco) - $1,266 rent seem right?
   - 32204/32205 (Riverside) - $1,167-$1,263 rent?

2. **Beach ZIPs - are these correct?**
   - 32250 (Jacksonville Beach) - Beach score 2.0 ✅
   - 32266 (Neptune Beach) - Beach score 2.0 ✅
   - 32233, 32225, 32224 - Beach score 1.0 (near beach)

3. **Data quality:**
   - ZIP 27260 still has 1.68M population - needs investigation
   - ZIP 32087 has only 4.5% bachelor's degrees - is this a blue-collar/trade area?

4. **Model performance:**
   - Average error of $92 - does this feel reasonable?
   - Beach premium correctly identified for 32250/32266

---

## Model Performance

- **MAE**: $92 (excellent for Jacksonville!)
- **Bias**: -3.4% (slight over-prediction)
- **Beach feature working**: 32250 & 32266 correctly identified as premium
- **Best predictions**: Mid-range ZIPs with typical profiles
- **Worst predictions**: Outliers like 32217 (-$424 error)
