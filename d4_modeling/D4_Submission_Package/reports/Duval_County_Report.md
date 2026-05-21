# Duval County Housing Market Analysis
## Model-Based Rent Predictions for Duval County ZIP Codes

---

## Executive Summary

**Total ZIP Codes Analyzed**: 57
**Average Median Rent**: $1505
**Model Accuracy (MAE)**: ±$91
**Rent Range**: $830 - $2676
**Total Population**: 3358089

### County Characteristics

- **Urban ZIPs**: 28 (49.1%)
- **Suburban ZIPs**: 22 (38.6%)
- **Rural ZIPs**: 7 (12.3%)
- **Beach/Waterfront ZIPs**: 5
- **Average Household Income**: $81505
- **Average Education (Bachelor's+)**: 32.9%

---

## All Duval County ZIP Codes

Complete listing sorted by actual rent (highest to lowest):

| ZIP | Actual Rent | Predicted Rent | Difference | Population | Education | Income | Type | Beach |
|-----|-------------|----------------|------------|------------|-----------|--------|------|-------|
| 32095 | $2676 | $2601 | +$75 | 21399 | 56.4% | $136038 | Suburban |  |
| 32092 | $2424 | $2336 | +$88 | 53071 | 51.4% | $131020 | Urban |  |
| 32259 | $2257 | $2318 | $-61 | 75016 | 55.4% | $150736 | Urban |  |
| 32003 | $1935 | $2040 | $-105 | 29766 | 49.6% | $116611 | Urban |  |
| 32258 | $1928 | $1940 | $-12 | 40408 | 47.0% | $102204 | Urban |  |
| 32082 | $1925 | $2041 | $-116 | 29289 | 70.5% | $124558 | Suburban |  |
| 32097 | $1892 | $1809 | +$83 | 26700 | 28.1% | $93161 | Suburban |  |
| 32227 | $1799 | $1843 | $-44 | 3207 | 19.7% | $85833 | Rural |  |
| 32222 | $1795 | $1888 | $-93 | 18258 | 27.9% | $85649 | Suburban |  |
| 32080 | $1788 | $1768 | +$20 | 20894 | 53.6% | $92531 | Suburban |  |
| 32250 | $1787 | $2069 | $-282 | 29072 | 54.6% | $117724 | Suburban | 🏖️ |
| 32224 | $1764 | $1870 | $-106 | 42092 | 56.9% | $88259 | Urban | 🌊 |
| 32081 | $1763 | $1876 | $-113 | 29784 | 72.0% | $131624 | Urban |  |
| 32266 | $1763 | $2031 | $-268 | 7168 | 60.9% | $119294 | Rural | 🏖️ |
| 32246 | $1761 | $1751 | +$10 | 62562 | 39.6% | $80963 | Urban |  |
| 32033 | $1752 | $1687 | +$65 | 4556 | 20.3% | $86185 | Rural |  |
| 32065 | $1743 | $1725 | +$18 | 41578 | 24.8% | $97455 | Urban |  |
| 32225 | $1729 | $1748 | $-19 | 55905 | 44.5% | $90559 | Urban | 🌊 |
| 32221 | $1708 | $1693 | +$15 | 32833 | 24.4% | $82969 | Urban |  |
| 32256 | $1698 | $1703 | $-5 | 58192 | 52.8% | $73570 | Urban |  |
| 32233 | $1681 | $1707 | $-26 | 24633 | 44.4% | $89185 | Suburban | 🌊 |
| 32034 | $1605 | $1741 | $-136 | 41029 | 53.0% | $98583 | Urban |  |
| 32086 | $1601 | $1654 | $-53 | 34855 | 35.5% | $76512 | Urban |  |
| 32223 | $1587 | $1793 | $-206 | 26160 | 45.0% | $95347 | Suburban |  |
| 32084 | $1567 | $1463 | +$104 | 37291 | 33.1% | $73837 | Urban |  |
| 32043 | $1545 | $1488 | +$57 | 34562 | 29.1% | $84145 | Urban |  |
| 32257 | $1518 | $1593 | $-75 | 42904 | 36.6% | $75780 | Urban |  |
| 32087 | $1518 | $1352 | +$166 | 4608 | 4.5% | $67097 | Rural |  |
| 27260 | $1513 | $1590 | $-77 | 1683960 | 36.5% | $79643 | Urban |  |
| 32218 | $1503 | $1559 | $-56 | 72905 | 26.0% | $69638 | Urban |  |
| 32073 | $1472 | $1611 | $-139 | 43561 | 26.7% | $76455 | Urban |  |
| 32244 | $1470 | $1526 | $-56 | 63592 | 25.5% | $62204 | Urban |  |
| 32068 | $1391 | $1505 | $-114 | 58983 | 22.7% | $84431 | Urban |  |
| 32063 | $1385 | $1168 | +$217 | 14611 | 22.9% | $75683 | Suburban |  |
| 32277 | $1378 | $1579 | $-201 | 36338 | 25.9% | $61554 | Urban |  |
| 32216 | $1364 | $1458 | $-94 | 42298 | 33.4% | $61821 | Urban |  |
| 32220 | $1330 | $1320 | +$10 | 12298 | 19.6% | $81792 | Suburban |  |
| 32210 | $1293 | $1431 | $-138 | 65729 | 22.9% | $61050 | Urban |  |
| 32219 | $1292 | $1244 | +$48 | 14302 | 21.5% | $72184 | Suburban |  |
| 32207 | $1266 | $1367 | $-101 | 36998 | 39.2% | $65234 | Urban |  |
| 32205 | $1263 | $1359 | $-96 | 29148 | 37.9% | $64789 | Suburban |  |
| 32217 | $1261 | $1631 | $-370 | 20221 | 41.3% | $73832 | Suburban |  |
| 32208 | $1214 | $1266 | $-52 | 32699 | 15.6% | $41324 | Urban |  |
| 32040 | $1189 | $1120 | +$69 | 8978 | 17.9% | $84095 | Suburban |  |
| 32254 | $1187 | $1262 | $-75 | 13927 | 11.7% | $34953 | Suburban |  |
| 32211 | $1185 | $1270 | $-85 | 36762 | 21.6% | $57021 | Urban |  |
| 32204 | $1167 | $1257 | $-90 | 9151 | 42.4% | $65063 | Suburban |  |
| 32202 | $1124 | $1115 | +$9 | 6023 | 17.9% | $34825 | Rural |  |
| 32011 | $1120 | $1193 | $-73 | 15421 | 15.2% | $76677 | Suburban |  |
| 32145 | $1113 | $1090 | +$23 | 5759 | 12.6% | $75557 | Rural |  |
| 32234 | $1096 | $1110 | $-14 | 9678 | 20.0% | $87331 | Suburban |  |
| 32656 | $1089 | $1112 | $-23 | 15836 | 22.4% | $74213 | Suburban |  |
| 32209 | $1062 | $1164 | $-102 | 34657 | 12.5% | $30514 | Urban |  |
| 32009 | $919 | $951 | $-32 | 4045 | 17.5% | $72792 | Rural |  |
| 32046 | $917 | $1009 | $-92 | 10593 | 12.4% | $71563 | Suburban |  |
| 32206 | $860 | $1006 | $-146 | 17105 | 22.6% | $39242 | Suburban |  |
| 32091 | $830 | $967 | $-137 | 14719 | 18.0% | $62852 | Suburban |  |

---

## Top 10 Over-Predicted ZIP Codes

Model predicted higher rent than actual (negative residual):

### 1. ZIP 32217
- **Actual Rent**: $1261
- **Predicted Rent**: $1631
- **Difference**: $-370
- **Characteristics**: Suburban, 20221 population, 41.3% bachelor's+, $73832 income
- **Analysis**: Model predicted $1631 but actual is $1261. High education (41.3% bachelor's+) suggests higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 2. ZIP 32250
- **Actual Rent**: $1787
- **Predicted Rent**: $2069
- **Difference**: $-282
- **Characteristics**: Suburban, 29072 population, 54.6% bachelor's+, $117724 income
- **Analysis**: Model predicted $2069 but actual is $1787. High education (54.6% bachelor's+) suggests higher rent. High income ($117724) indicates affluent area. Beach proximity (score 2.0) adds premium. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 3. ZIP 32266
- **Actual Rent**: $1763
- **Predicted Rent**: $2031
- **Difference**: $-268
- **Characteristics**: Rural, 7168 population, 60.9% bachelor's+, $119294 income
- **Analysis**: Model predicted $2031 but actual is $1763. High education (60.9% bachelor's+) suggests higher rent. High income ($119294) indicates affluent area. Beach proximity (score 2.0) adds premium. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 4. ZIP 32223
- **Actual Rent**: $1587
- **Predicted Rent**: $1793
- **Difference**: $-206
- **Characteristics**: Suburban, 26160 population, 45.0% bachelor's+, $95347 income
- **Analysis**: Model predicted $1793 but actual is $1587. High education (45.0% bachelor's+) suggests higher rent. High income ($95347) indicates affluent area. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 5. ZIP 32277
- **Actual Rent**: $1378
- **Predicted Rent**: $1579
- **Difference**: $-201
- **Characteristics**: Urban, 36338 population, 25.9% bachelor's+, $61554 income
- **Analysis**: Model predicted $1579 but actual is $1378. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 6. ZIP 32206
- **Actual Rent**: $860
- **Predicted Rent**: $1006
- **Difference**: $-146
- **Characteristics**: Suburban, 17105 population, 22.6% bachelor's+, $39242 income
- **Analysis**: Model predicted $1006 but actual is $860. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 7. ZIP 32073
- **Actual Rent**: $1472
- **Predicted Rent**: $1611
- **Difference**: $-139
- **Characteristics**: Urban, 43561 population, 26.7% bachelor's+, $76455 income
- **Analysis**: Model predicted $1611 but actual is $1472. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 8. ZIP 32210
- **Actual Rent**: $1293
- **Predicted Rent**: $1431
- **Difference**: $-138
- **Characteristics**: Urban, 65729 population, 22.9% bachelor's+, $61050 income
- **Analysis**: Model predicted $1431 but actual is $1293. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 9. ZIP 32091
- **Actual Rent**: $830
- **Predicted Rent**: $967
- **Difference**: $-137
- **Characteristics**: Suburban, 14719 population, 18.0% bachelor's+, $62852 income
- **Analysis**: Model predicted $967 but actual is $830. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 10. ZIP 32034
- **Actual Rent**: $1605
- **Predicted Rent**: $1741
- **Difference**: $-136
- **Characteristics**: Urban, 41029 population, 53.0% bachelor's+, $98583 income
- **Analysis**: Model predicted $1741 but actual is $1605. High education (53.0% bachelor's+) suggests higher rent. High income ($98583) indicates affluent area. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

---

## Top 10 Under-Predicted ZIP Codes

Model predicted lower rent than actual (positive residual):

### 1. ZIP 32063
- **Actual Rent**: $1385
- **Predicted Rent**: $1168
- **Difference**: +$217
- **Characteristics**: Suburban, 14611 population, 22.9% bachelor's+, $75683 income
- **Analysis**: Model predicted $1168 but actual is $1385. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 2. ZIP 32087
- **Actual Rent**: $1518
- **Predicted Rent**: $1352
- **Difference**: +$166
- **Characteristics**: Rural, 4608 population, 4.5% bachelor's+, $67097 income
- **Analysis**: Model predicted $1352 but actual is $1518. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 3. ZIP 32084
- **Actual Rent**: $1567
- **Predicted Rent**: $1463
- **Difference**: +$104
- **Characteristics**: Urban, 37291 population, 33.1% bachelor's+, $73837 income
- **Analysis**: Model predicted $1463 but actual is $1567. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 4. ZIP 32092
- **Actual Rent**: $2424
- **Predicted Rent**: $2336
- **Difference**: +$88
- **Characteristics**: Urban, 53071 population, 51.4% bachelor's+, $131020 income
- **Analysis**: Model predicted $2336 but actual is $2424. Urban area with educated population drives demand. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 5. ZIP 32097
- **Actual Rent**: $1892
- **Predicted Rent**: $1809
- **Difference**: +$83
- **Characteristics**: Suburban, 26700 population, 28.1% bachelor's+, $93161 income
- **Analysis**: Model predicted $1809 but actual is $1892. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 6. ZIP 32095
- **Actual Rent**: $2676
- **Predicted Rent**: $2601
- **Difference**: +$75
- **Characteristics**: Suburban, 21399 population, 56.4% bachelor's+, $136038 income
- **Analysis**: Model predicted $2601 but actual is $2676. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 7. ZIP 32040
- **Actual Rent**: $1189
- **Predicted Rent**: $1120
- **Difference**: +$69
- **Characteristics**: Suburban, 8978 population, 17.9% bachelor's+, $84095 income
- **Analysis**: Model predicted $1120 but actual is $1189. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 8. ZIP 32033
- **Actual Rent**: $1752
- **Predicted Rent**: $1687
- **Difference**: +$65
- **Characteristics**: Rural, 4556 population, 20.3% bachelor's+, $86185 income
- **Analysis**: Model predicted $1687 but actual is $1752. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 9. ZIP 32043
- **Actual Rent**: $1545
- **Predicted Rent**: $1488
- **Difference**: +$57
- **Characteristics**: Urban, 34562 population, 29.1% bachelor's+, $84145 income
- **Analysis**: Model predicted $1488 but actual is $1545. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 10. ZIP 32219
- **Actual Rent**: $1292
- **Predicted Rent**: $1244
- **Difference**: +$48
- **Characteristics**: Suburban, 14302 population, 21.5% bachelor's+, $72184 income
- **Analysis**: Model predicted $1244 but actual is $1292. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.
