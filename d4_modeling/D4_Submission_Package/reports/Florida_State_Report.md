# Florida Housing Market Analysis
## Statewide Rent Prediction Analysis

---

## Executive Summary

**Cities Analyzed**: Jacksonville, Miami, Tampa, Orlando
**Total ZIP Codes**: 454
**Total Population**: 27922459
**Average Median Rent**: $1780
**Model Accuracy (MAE)**: ±$100
**Rent Range**: $830 - $3342

### City Comparison

| City | ZIPs | Avg Rent | Avg Income | Education | Coastal | MAE |
|------|------|----------|------------|-----------|---------|-----|
| Jacksonville | 57 | $1505 | $81505 | 32.9% | 57 | $91 |
| Miami | 177 | $2005 | $85509 | 39.3% | 177 | $94 |
| Tampa | 130 | $1632 | $80606 | 35.0% | 130 | $110 |
| Orlando | 90 | $1726 | $82671 | 34.8% | 0 | $104 |

---

## All Florida ZIP Codes

Complete listing sorted by actual rent:

| City | ZIP | Actual Rent | Predicted | Difference | Type | Beach |
|------|-----|-------------|-----------|------------|------|-------|
| Miami | 33327 | $3342 | $3198 | +$144 | Suburban |  |
| Miami | 33076 | $3263 | $3061 | +$202 | Urban |  |
| Miami | 33131 | $3124 | $3017 | +$107 | Suburban | 🏖️ |
| Miami | 33449 | $3102 | $2913 | +$189 | Suburban |  |
| Miami | 33478 | $3033 | $2863 | +$170 | Suburban |  |
| Miami | 33146 | $2975 | $2569 | +$406 | Suburban | 🌊 |
| Miami | 33331 | $2832 | $2702 | +$130 | Suburban |  |
| Miami | 33178 | $2771 | $2672 | +$99 | Urban |  |
| Miami | 33185 | $2737 | $2622 | +$115 | Suburban |  |
| Miami | 33194 | $2728 | $2626 | +$102 | Rural |  |
| Miami | 33431 | $2712 | $2514 | +$198 | Suburban |  |
| Tampa | 33715 | $2680 | $2527 | +$153 | Rural |  |
| Jacksonville | 32095 | $2676 | $2601 | +$75 | Suburban |  |
| Miami | 33470 | $2669 | $2607 | +$62 | Urban |  |
| Miami | 33132 | $2650 | $2593 | +$57 | Suburban | 🌊 |
| Miami | 33330 | $2641 | $2690 | $-49 | Suburban |  |
| Miami | 33029 | $2635 | $2709 | $-74 | Urban |  |
| Orlando | 32820 | $2611 | $2466 | +$145 | Suburban |  |
| Miami | 33496 | $2609 | $2545 | +$64 | Suburban |  |
| Miami | 33487 | $2603 | $2434 | +$169 | Suburban |  |
| Miami | 33418 | $2578 | $2486 | +$92 | Urban |  |
| Miami | 33323 | $2569 | $2415 | +$154 | Suburban |  |
| Miami | 33301 | $2568 | $2567 | +$1 | Suburban |  |
| Miami | 33180 | $2563 | $2419 | +$144 | Urban | 🏖️ |
| Tampa | 33776 | $2544 | $2178 | +$366 | Suburban |  |
| Miami | 33433 | $2521 | $2382 | +$139 | Urban |  |
| Miami | 33028 | $2511 | $2503 | +$8 | Suburban |  |
| Miami | 33326 | $2506 | $2384 | +$122 | Urban |  |
| Miami | 33137 | $2489 | $2291 | +$198 | Urban | 🌊 |
| Miami | 33483 | $2456 | $2406 | +$50 | Suburban |  |
| Tampa | 33596 | $2452 | $2327 | +$125 | Suburban |  |
| Miami | 33472 | $2444 | $2316 | +$128 | Suburban |  |
| Miami | 33414 | $2434 | $2350 | +$84 | Urban |  |
| Miami | 33428 | $2432 | $2011 | +$421 | Urban |  |
| Miami | 33154 | $2432 | $2178 | +$254 | Suburban | 🏖️ |
| Jacksonville | 32092 | $2424 | $2336 | +$88 | Urban |  |
| Miami | 33182 | $2416 | $2344 | +$72 | Suburban |  |
| Tampa | 33545 | $2374 | $2215 | +$159 | Urban |  |
| Miami | 33432 | $2361 | $2370 | $-9 | Suburban |  |
| Orlando | 32814 | $2361 | $2370 | $-9 | Suburban |  |
| Miami | 33328 | $2341 | $2276 | +$65 | Suburban |  |
| Miami | 33458 | $2330 | $2338 | $-8 | Urban |  |
| Miami | 33412 | $2321 | $2388 | $-67 | Suburban |  |
| Miami | 33486 | $2318 | $2156 | +$162 | Suburban |  |
| Orlando | 34786 | $2318 | $2084 | +$234 | Urban |  |
| Orlando | 32832 | $2314 | $2195 | +$119 | Urban |  |
| Miami | 33067 | $2287 | $2341 | $-54 | Suburban |  |
| Miami | 33324 | $2286 | $2015 | +$271 | Urban |  |
| Miami | 33149 | $2283 | $2679 | $-396 | Suburban | 🏖️ |
| Miami | 33498 | $2283 | $2483 | $-200 | Suburban |  |
| Miami | 33473 | $2283 | $2328 | $-45 | Suburban |  |
| Miami | 33158 | $2283 | $2292 | $-9 | Rural |  |
| Miami | 33332 | $2283 | $2438 | $-155 | Suburban |  |
| Miami | 33071 | $2283 | $2347 | $-64 | Urban |  |
| Orlando | 34787 | $2276 | $2038 | +$238 | Urban |  |
| Tampa | 34638 | $2275 | $2086 | +$189 | Urban |  |
| Tampa | 33569 | $2273 | $2087 | +$186 | Suburban |  |
| Tampa | 33602 | $2270 | $2299 | $-29 | Suburban |  |
| Miami | 33018 | $2269 | $2161 | +$108 | Urban |  |
| Miami | 33073 | $2265 | $2229 | +$36 | Urban |  |
| Miami | 33196 | $2259 | $2126 | +$133 | Urban |  |
| Miami | 33410 | $2259 | $2087 | +$172 | Urban |  |
| Jacksonville | 32259 | $2257 | $2318 | $-61 | Urban |  |
| Tampa | 33572 | $2251 | $2174 | +$77 | Suburban |  |
| Miami | 33129 | $2250 | $2283 | $-33 | Suburban | 🏖️ |
| Tampa | 33543 | $2239 | $2300 | $-61 | Urban |  |
| Miami | 33186 | $2224 | $2203 | +$21 | Urban |  |
| Tampa | 33547 | $2218 | $2293 | $-75 | Urban |  |
| Tampa | 33626 | $2204 | $2245 | $-41 | Urban |  |
| Miami | 33426 | $2202 | $1803 | +$399 | Suburban |  |
| Miami | 33140 | $2194 | $2206 | $-12 | Suburban | 🏖️ |
| Orlando | 32766 | $2175 | $2130 | +$45 | Suburban |  |
| Miami | 33177 | $2174 | $1847 | +$327 | Urban |  |
| Tampa | 33579 | $2165 | $2185 | $-20 | Urban |  |
| Miami | 33187 | $2164 | $2257 | $-93 | Suburban |  |
| Miami | 33322 | $2151 | $2010 | +$141 | Urban |  |
| Miami | 33467 | $2146 | $2202 | $-56 | Urban |  |
| Miami | 33173 | $2139 | $1953 | +$186 | Urban |  |
| Miami | 33019 | $2117 | $1950 | +$167 | Suburban |  |
| Miami | 33025 | $2109 | $2017 | +$92 | Urban |  |
| Miami | 33317 | $2104 | $2064 | +$40 | Urban |  |
| Miami | 33314 | $2104 | $1983 | +$121 | Urban |  |
| Tampa | 33606 | $2100 | $2180 | $-80 | Suburban |  |
| Miami | 33316 | $2100 | $2146 | $-46 | Suburban |  |
| Miami | 33172 | $2088 | $1961 | +$127 | Urban |  |
| Miami | 33484 | $2087 | $1901 | +$186 | Suburban |  |
| Orlando | 33896 | $2078 | $1948 | +$130 | Suburban |  |
| Miami | 33413 | $2077 | $1922 | +$155 | Suburban |  |
| Miami | 33437 | $2070 | $2119 | $-49 | Urban |  |
| Miami | 33133 | $2068 | $2145 | $-77 | Urban | 🏖️ |
| Miami | 33160 | $2064 | $2065 | $-1 | Urban | 🏖️ |
| Orlando | 32746 | $2059 | $2018 | +$41 | Urban |  |
| Tampa | 33616 | $2054 | $1893 | +$161 | Suburban |  |
| Miami | 33068 | $2053 | $1869 | +$184 | Urban |  |
| Miami | 33351 | $2052 | $1983 | +$69 | Urban |  |
| Orlando | 34715 | $2050 | $1753 | +$297 | Suburban |  |
| Miami | 33445 | $2045 | $1948 | +$97 | Urban |  |
| Tampa | 34639 | $2040 | $2031 | +$9 | Urban |  |
| Miami | 33325 | $2031 | $2152 | $-121 | Urban |  |
| Miami | 33175 | $2022 | $1997 | +$25 | Urban |  |
| Orlando | 34772 | $2016 | $1870 | +$146 | Urban |  |
| Orlando | 32819 | $2012 | $1970 | +$42 | Urban |  |
| Orlando | 32837 | $2009 | $1965 | +$44 | Urban |  |
| Miami | 33309 | $2006 | $1948 | +$58 | Urban |  |
| Orlando | 32836 | $2003 | $1929 | +$74 | Suburban |  |
| Miami | 33411 | $2002 | $2076 | $-74 | Urban |  |
| Miami | 33435 | $1997 | $1864 | +$133 | Urban |  |
| Orlando | 32751 | $1995 | $1805 | +$190 | Suburban |  |
| Tampa | 34685 | $1990 | $1987 | +$3 | Suburban |  |
| Tampa | 33708 | $1987 | $1700 | +$287 | Suburban | 🏖️ |
| Miami | 33442 | $1984 | $1904 | +$80 | Urban |  |
| Orlando | 32779 | $1981 | $1875 | +$106 | Suburban |  |
| Tampa | 33544 | $1979 | $2082 | $-103 | Urban |  |
| Tampa | 33548 | $1975 | $2338 | $-363 | Suburban |  |
| Miami | 33062 | $1971 | $1755 | +$216 | Suburban |  |
| Miami | 33305 | $1971 | $2008 | $-37 | Suburban |  |
| Orlando | 32829 | $1970 | $1977 | $-7 | Suburban |  |
| Orlando | 32828 | $1966 | $1992 | $-26 | Urban |  |
| Miami | 33183 | $1965 | $1929 | +$36 | Urban |  |
| Orlando | 32712 | $1958 | $1800 | +$158 | Urban |  |
| Miami | 33035 | $1958 | $1874 | +$84 | Suburban |  |
| Miami | 33026 | $1958 | $1900 | +$58 | Urban |  |
| Miami | 33321 | $1952 | $1905 | +$47 | Urban |  |
| Miami | 33156 | $1951 | $2236 | $-285 | Urban | 🏖️ |
| Orlando | 34758 | $1951 | $1840 | +$111 | Urban |  |
| Miami | 33436 | $1950 | $1902 | +$48 | Urban |  |
| Tampa | 33785 | $1948 | $1986 | $-38 | Rural | 🏖️ |
| Miami | 33015 | $1936 | $1958 | $-22 | Urban |  |
| Jacksonville | 32003 | $1935 | $2040 | $-105 | Urban |  |
| Orlando | 34734 | $1930 | $1845 | +$85 | Rural |  |
| Miami | 33166 | $1929 | $1987 | $-58 | Suburban |  |
| Orlando | 34759 | $1929 | $1861 | +$68 | Urban |  |
| Jacksonville | 32258 | $1928 | $1940 | $-12 | Urban |  |
| Miami | 33109 | $1928 | $1965 | $-37 | Rural | 🏖️ |
| Miami | 33143 | $1928 | $2068 | $-140 | Urban |  |
| Tampa | 33607 | $1927 | $1787 | +$140 | Suburban |  |
| Jacksonville | 32082 | $1925 | $2041 | $-116 | Suburban |  |
| Orlando | 32803 | $1919 | $1866 | +$53 | Suburban |  |
| Orlando | 32821 | $1913 | $1932 | $-19 | Suburban |  |
| Miami | 33065 | $1913 | $1860 | +$53 | Urban |  |
| Miami | 33408 | $1912 | $1877 | +$35 | Suburban |  |
| Miami | 33184 | $1911 | $1908 | +$3 | Suburban |  |
| Miami | 33469 | $1908 | $2021 | $-113 | Suburban |  |
| Tampa | 33647 | $1904 | $2376 | $-472 | Urban |  |
| Tampa | 33711 | $1897 | $1746 | +$151 | Suburban | 🌊 |
| Orlando | 34797 | $1896 | $1736 | +$160 | Rural |  |
| Orlando | 32708 | $1896 | $1867 | +$29 | Urban |  |
| Orlando | 32732 | $1896 | $1545 | +$351 | Rural |  |
| Orlando | 34739 | $1896 | $1681 | +$215 | Rural |  |
| Miami | 33165 | $1895 | $1933 | $-38 | Urban |  |
| Orlando | 32824 | $1895 | $1780 | +$115 | Urban |  |
| Tampa | 33625 | $1894 | $1937 | $-43 | Urban |  |
| Jacksonville | 32097 | $1892 | $1809 | +$83 | Suburban |  |
| Tampa | 33629 | $1891 | $2085 | $-194 | Suburban |  |
| Tampa | 33759 | $1890 | $1744 | +$146 | Suburban |  |
| Miami | 33134 | $1890 | $2024 | $-134 | Urban | 🌊 |
| Orlando | 34711 | $1883 | $1514 | +$369 | Urban |  |
| Miami | 33016 | $1883 | $1871 | +$12 | Urban |  |
| Tampa | 33782 | $1879 | $1697 | +$182 | Suburban |  |
| Orlando | 34761 | $1879 | $1796 | +$83 | Urban |  |
| Miami | 33179 | $1875 | $1840 | +$35 | Urban |  |
| Orlando | 32765 | $1874 | $1809 | +$65 | Urban |  |
| Miami | 33190 | $1874 | $1884 | $-10 | Suburban |  |
| Miami | 33181 | $1870 | $1858 | +$12 | Suburban | 🏖️ |
| Miami | 33155 | $1870 | $1812 | +$58 | Urban | 🌊 |
| Miami | 33100 | $1869 | $1634 | +$235 | Urban |  |
| Tampa | 33634 | $1866 | $1740 | +$126 | Suburban |  |
| Tampa | 33609 | $1861 | $2133 | $-272 | Suburban |  |
| Miami | 33174 | $1860 | $1753 | +$107 | Urban |  |
| Orlando | 32825 | $1859 | $1857 | +$2 | Urban |  |
| Tampa | 34637 | $1857 | $1924 | $-67 | Suburban |  |
| Tampa | 34684 | $1854 | $1815 | +$39 | Suburban |  |
| Miami | 33308 | $1851 | $2048 | $-197 | Suburban |  |
| Miami | 33193 | $1851 | $1934 | $-83 | Urban |  |
| Tampa | 33786 | $1849 | $1928 | $-79 | Rural | 🏖️ |
| Miami | 33145 | $1849 | $1741 | +$108 | Urban | 🌊 |
| Miami | 33024 | $1848 | $1831 | +$17 | Urban |  |
| Orlando | 32835 | $1848 | $1718 | +$130 | Urban |  |
| Miami | 33063 | $1844 | $1846 | $-2 | Urban |  |
| Tampa | 33556 | $1841 | $2085 | $-244 | Urban |  |
| Orlando | 34746 | $1840 | $1790 | +$50 | Urban |  |
| Miami | 33304 | $1839 | $1933 | $-94 | Suburban |  |
| Tampa | 33703 | $1833 | $1843 | $-10 | Suburban | 🌊 |
| Miami | 33027 | $1832 | $1913 | $-81 | Urban |  |
| Miami | 33141 | $1831 | $1873 | $-42 | Urban | 🏖️ |
| Tampa | 33594 | $1830 | $1823 | +$7 | Urban |  |
| Tampa | 33578 | $1829 | $1845 | $-16 | Urban |  |
| Orlando | 34743 | $1827 | $1841 | $-14 | Urban |  |
| Orlando | 34747 | $1827 | $1784 | +$43 | Urban |  |
| Miami | 33014 | $1827 | $1859 | $-32 | Urban |  |
| Orlando | 34771 | $1822 | $1722 | +$100 | Urban |  |
| Miami | 33139 | $1822 | $1768 | +$54 | Urban | 🏖️ |
| Miami | 33144 | $1816 | $1733 | +$83 | Suburban |  |
| Tampa | 33778 | $1811 | $1649 | +$162 | Suburban |  |
| Miami | 33306 | $1810 | $2109 | $-299 | Rural |  |
| Tampa | 33635 | $1809 | $1855 | $-46 | Suburban |  |
| Tampa | 33716 | $1809 | $1836 | $-27 | Suburban |  |
| Tampa | 33761 | $1806 | $1746 | +$60 | Suburban |  |
| Miami | 33004 | $1801 | $1740 | +$61 | Suburban |  |
| Tampa | 33511 | $1801 | $1768 | +$33 | Urban |  |
| Jacksonville | 32227 | $1799 | $1843 | $-44 | Rural |  |
| Miami | 33069 | $1797 | $1766 | +$31 | Suburban |  |
| Tampa | 33764 | $1797 | $1701 | +$96 | Suburban |  |
| Jacksonville | 32222 | $1795 | $1888 | $-93 | Suburban |  |
| Miami | 33055 | $1793 | $1707 | +$86 | Urban |  |
| Tampa | 34655 | $1793 | $1854 | $-61 | Urban |  |
| Miami | 33406 | $1792 | $1714 | +$78 | Suburban |  |
| Miami | 33130 | $1792 | $1780 | +$12 | Urban | 🌊 |
| Tampa | 33762 | $1792 | $1881 | $-89 | Rural |  |
| Tampa | 34609 | $1791 | $1727 | +$64 | Urban |  |
| Miami | 33463 | $1791 | $1834 | $-43 | Urban |  |
| Miami | 33064 | $1789 | $1740 | +$49 | Urban |  |
| Jacksonville | 32080 | $1788 | $1768 | +$20 | Suburban |  |
| Jacksonville | 32250 | $1787 | $2069 | $-282 | Suburban | 🏖️ |
| Orlando | 32817 | $1783 | $1717 | +$66 | Urban |  |
| Tampa | 33624 | $1782 | $1830 | $-48 | Urban |  |
| Miami | 33315 | $1779 | $1806 | $-27 | Suburban |  |
| Miami | 33462 | $1779 | $1736 | +$43 | Urban |  |
| Tampa | 33611 | $1778 | $1783 | $-5 | Urban |  |
| Miami | 33401 | $1776 | $1769 | +$7 | Urban |  |
| Miami | 33021 | $1775 | $1835 | $-60 | Urban |  |
| Miami | 33176 | $1774 | $2005 | $-231 | Urban |  |
| Miami | 33126 | $1771 | $1769 | +$2 | Urban | 🌊 |
| Miami | 33033 | $1766 | $1790 | $-24 | Urban |  |
| Miami | 33056 | $1764 | $1643 | +$121 | Urban |  |
| Jacksonville | 32224 | $1764 | $1870 | $-106 | Urban | 🌊 |
| Jacksonville | 32081 | $1763 | $1876 | $-113 | Urban |  |
| Jacksonville | 32266 | $1763 | $2031 | $-268 | Rural | 🏖️ |
| Jacksonville | 32246 | $1761 | $1751 | +$10 | Urban |  |
| Orlando | 36740 | $1760 | $1540 | +$220 | Urban |  |
| Orlando | 32714 | $1755 | $1630 | +$125 | Urban |  |
| Orlando | 32804 | $1753 | $1706 | +$47 | Suburban |  |
| Jacksonville | 32033 | $1752 | $1687 | +$65 | Rural |  |
| Miami | 33023 | $1750 | $1772 | $-22 | Urban |  |
| Orlando | 34714 | $1750 | $1709 | +$41 | Suburban |  |
| Tampa | 34683 | $1748 | $1708 | +$40 | Urban |  |
| Orlando | 32757 | $1747 | $1606 | +$141 | Urban |  |
| Tampa | 33619 | $1746 | $1701 | +$45 | Urban |  |
| Miami | 33031 | $1745 | $1765 | $-20 | Rural |  |
| Jacksonville | 32065 | $1743 | $1725 | +$18 | Urban |  |
| Orlando | 32789 | $1742 | $1777 | $-35 | Suburban |  |
| Miami | 33334 | $1737 | $1717 | +$20 | Urban |  |
| Orlando | 34762 | $1734 | $1728 | +$6 | Rural |  |
| Orlando | 32702 | $1734 | $1439 | +$295 | Rural |  |
| Orlando | 32750 | $1734 | $1629 | +$105 | Suburban |  |
| Orlando | 32831 | $1734 | $1720 | +$14 | Rural |  |
| Tampa | 33706 | $1733 | $1862 | $-129 | Suburban | 🏖️ |
| Miami | 33409 | $1731 | $1698 | +$33 | Urban |  |
| Tampa | 33777 | $1729 | $1758 | $-29 | Suburban |  |
| Jacksonville | 32225 | $1729 | $1748 | $-19 | Urban | 🌊 |
| Miami | 33066 | $1724 | $1837 | $-113 | Suburban |  |
| Orlando | 32822 | $1719 | $1697 | +$22 | Urban |  |
| Miami | 33319 | $1719 | $1824 | $-105 | Urban |  |
| Orlando | 32701 | $1715 | $1464 | +$251 | Suburban |  |
| Tampa | 33701 | $1711 | $1727 | $-16 | Suburban | 🌊 |
| Orlando | 32792 | $1710 | $1641 | +$69 | Urban |  |
| Jacksonville | 32221 | $1708 | $1693 | +$15 | Urban |  |
| Orlando | 32771 | $1707 | $1575 | +$132 | Urban |  |
| Tampa | 34695 | $1707 | $1701 | +$6 | Suburban |  |
| Miami | 33162 | $1704 | $1696 | +$8 | Urban |  |
| Miami | 33312 | $1703 | $1707 | $-4 | Urban |  |
| Jacksonville | 32256 | $1698 | $1703 | $-5 | Urban |  |
| Miami | 33404 | $1698 | $1675 | +$23 | Urban |  |
| Miami | 33444 | $1696 | $1727 | $-31 | Suburban |  |
| Orlando | 32707 | $1693 | $1738 | $-45 | Urban |  |
| Orlando | 34737 | $1692 | $1433 | +$259 | Rural |  |
| Tampa | 34698 | $1691 | $1645 | +$46 | Urban |  |
| Miami | 33461 | $1685 | $1685 | $-0 | Urban |  |
| Miami | 33313 | $1683 | $1683 | +$0 | Urban |  |
| Tampa | 34654 | $1682 | $1488 | +$194 | Suburban |  |
| Jacksonville | 32233 | $1681 | $1707 | $-26 | Suburban | 🌊 |
| Tampa | 33773 | $1679 | $1624 | +$55 | Suburban |  |
| Miami | 33013 | $1679 | $1641 | +$38 | Urban |  |
| Orlando | 34736 | $1679 | $1616 | +$63 | Suburban |  |
| Orlando | 32703 | $1676 | $1548 | +$128 | Urban |  |
| Tampa | 33558 | $1672 | $2060 | $-388 | Urban |  |
| Miami | 33415 | $1667 | $1702 | $-35 | Urban |  |
| Miami | 33012 | $1665 | $1641 | +$24 | Urban |  |
| Tampa | 33549 | $1661 | $1677 | $-16 | Suburban |  |
| Orlando | 34741 | $1661 | $1551 | +$110 | Urban |  |
| Miami | 33032 | $1658 | $1779 | $-121 | Urban |  |
| Tampa | 33615 | $1656 | $1768 | $-112 | Urban |  |
| Miami | 33169 | $1655 | $1743 | $-88 | Urban |  |
| Miami | 33441 | $1655 | $1635 | +$20 | Urban |  |
| Miami | 33157 | $1653 | $1875 | $-222 | Urban |  |
| Miami | 33009 | $1649 | $1749 | $-100 | Urban |  |
| Tampa | 33637 | $1648 | $1747 | $-99 | Suburban |  |
| Miami | 33417 | $1647 | $1605 | +$42 | Urban |  |
| Orlando | 32810 | $1645 | $1591 | +$54 | Urban |  |
| Tampa | 33765 | $1641 | $1642 | $-1 | Suburban |  |
| Tampa | 33760 | $1631 | $1578 | +$53 | Suburban |  |
| Tampa | 34681 | $1630 | $2087 | $-458 | Rural |  |
| Tampa | 33620 | $1630 | $1766 | $-137 | Rural |  |
| Miami | 33168 | $1629 | $1627 | +$2 | Suburban |  |
| Tampa | 45300 | $1628 | $1585 | +$43 | Urban |  |
| Tampa | 33712 | $1623 | $1590 | +$33 | Suburban | 🌊 |
| Orlando | 32812 | $1622 | $1666 | $-44 | Urban |  |
| Miami | 33189 | $1622 | $1723 | $-101 | Suburban |  |
| Orlando | 34744 | $1617 | $1676 | $-59 | Urban |  |
| Orlando | 32709 | $1616 | $1528 | +$88 | Rural |  |
| Orlando | 32811 | $1614 | $1319 | +$295 | Urban |  |
| Miami | 33161 | $1611 | $1628 | $-17 | Urban |  |
| Miami | 33138 | $1611 | $1795 | $-184 | Suburban | 🌊 |
| Tampa | 33772 | $1608 | $1644 | $-36 | Suburban |  |
| Miami | 33407 | $1608 | $1539 | +$69 | Urban |  |
| Jacksonville | 32034 | $1605 | $1741 | $-136 | Urban |  |
| Tampa | 33707 | $1605 | $1633 | $-28 | Suburban | 🏖️ |
| Tampa | 33770 | $1604 | $1537 | +$67 | Suburban | 🏖️ |
| Jacksonville | 32086 | $1601 | $1654 | $-53 | Urban |  |
| Miami | 33403 | $1601 | $1486 | +$115 | Suburban |  |
| Orlando | 32735 | $1600 | $1533 | +$67 | Rural |  |
| Miami | 33434 | $1598 | $1780 | $-182 | Suburban |  |
| Orlando | 32818 | $1589 | $1684 | $-95 | Urban |  |
| Jacksonville | 32223 | $1587 | $1793 | $-206 | Suburban |  |
| Orlando | 32807 | $1585 | $1509 | +$76 | Urban |  |
| Orlando | 32730 | $1581 | $1538 | +$43 | Rural |  |
| Miami | 33170 | $1578 | $1593 | $-15 | Suburban |  |
| Orlando | 32773 | $1577 | $1407 | +$170 | Urban |  |
| Tampa | 33710 | $1577 | $1669 | $-92 | Urban | 🌊 |
| Tampa | 33618 | $1574 | $1774 | $-200 | Suburban |  |
| Jacksonville | 32084 | $1567 | $1463 | +$104 | Urban |  |
| Miami | 33405 | $1566 | $1785 | $-219 | Suburban |  |
| Orlando | 32826 | $1564 | $1612 | $-48 | Suburban |  |
| Tampa | 33559 | $1561 | $1737 | $-176 | Suburban |  |
| Orlando | 34769 | $1560 | $1396 | +$164 | Urban |  |
| Tampa | 34610 | $1558 | $1406 | +$152 | Suburban |  |
| Tampa | 33756 | $1557 | $1510 | +$47 | Urban |  |
| Orlando | 32806 | $1552 | $1675 | $-123 | Suburban |  |
| Tampa | 33774 | $1545 | $1641 | $-96 | Suburban |  |
| Jacksonville | 32043 | $1545 | $1488 | +$57 | Urban |  |
| Tampa | 33810 | $1539 | $1563 | $-24 | Urban |  |
| Miami | 33460 | $1538 | $1604 | $-66 | Urban |  |
| Miami | 33020 | $1536 | $1618 | $-82 | Urban |  |
| Miami | 33125 | $1535 | $1502 | +$33 | Urban | 🌊 |
| Orlando | 34753 | $1529 | $1447 | +$82 | Rural |  |
| Tampa | 33705 | $1526 | $1593 | $-67 | Suburban | 🌊 |
| Jacksonville | 32257 | $1518 | $1593 | $-75 | Urban |  |
| Jacksonville | 32087 | $1518 | $1352 | +$166 | Rural |  |
| Tampa | 33603 | $1518 | $1535 | $-17 | Suburban |  |
| Orlando | 32778 | $1514 | $1452 | +$62 | Suburban |  |
| Orlando | 32776 | $1514 | $1676 | $-162 | Suburban |  |
| Miami | 33136 | $1513 | $1564 | $-51 | Suburban | 🌊 |
| Jacksonville | 27260 | $1513 | $1590 | $-77 | Urban |  |
| Orlando | 32833 | $1507 | $1615 | $-108 | Suburban |  |
| Orlando | 34756 | $1505 | $1508 | $-3 | Rural |  |
| Orlando | 32839 | $1503 | $1427 | +$76 | Urban |  |
| Jacksonville | 32218 | $1503 | $1559 | $-56 | Urban |  |
| Tampa | 33584 | $1502 | $1545 | $-43 | Suburban |  |
| Tampa | 33763 | $1497 | $1484 | +$13 | Suburban |  |
| Tampa | 33713 | $1497 | $1514 | $-17 | Urban | 🌊 |
| Tampa | 33704 | $1495 | $2126 | $-631 | Suburban | 🌊 |
| Miami | 33147 | $1486 | $1403 | +$83 | Urban |  |
| Tampa | 34677 | $1485 | $1720 | $-235 | Suburban |  |
| Tampa | 33510 | $1483 | $1601 | $-118 | Urban |  |
| Tampa | 33709 | $1479 | $1435 | +$44 | Suburban | 🌊 |
| Miami | 33054 | $1474 | $1525 | $-51 | Urban |  |
| Orlando | 32809 | $1472 | $1404 | +$68 | Suburban |  |
| Jacksonville | 32073 | $1472 | $1611 | $-139 | Urban |  |
| Jacksonville | 32244 | $1470 | $1526 | $-56 | Urban |  |
| Tampa | 33702 | $1465 | $1607 | $-142 | Urban | 🌊 |
| Tampa | 33755 | $1462 | $1397 | +$65 | Suburban |  |
| Miami | 33311 | $1461 | $1566 | $-105 | Urban |  |
| Tampa | 33614 | $1458 | $1468 | $-10 | Urban |  |
| Tampa | 33598 | $1458 | $1739 | $-281 | Urban |  |
| Miami | 33127 | $1455 | $1324 | +$131 | Suburban | 🌊 |
| Tampa | 33565 | $1454 | $1457 | $-3 | Suburban |  |
| Orlando | 32808 | $1453 | $1442 | +$11 | Urban |  |
| Miami | 33128 | $1452 | $1298 | +$154 | Suburban | 🌊 |
| Tampa | 33534 | $1452 | $1532 | $-80 | Suburban |  |
| Miami | 33060 | $1452 | $1601 | $-149 | Urban |  |
| Orlando | 34788 | $1438 | $1351 | +$87 | Suburban |  |
| Tampa | 33771 | $1436 | $1420 | +$16 | Suburban | 🏖️ |
| Tampa | 33617 | $1431 | $1534 | $-103 | Urban |  |
| Tampa | 34688 | $1429 | $2129 | $-700 | Rural |  |
| Miami | 33167 | $1425 | $1431 | $-6 | Suburban |  |
| Miami | 33135 | $1422 | $1373 | +$49 | Urban | 🌊 |
| Tampa | 33604 | $1412 | $1333 | +$79 | Urban |  |
| Tampa | 33566 | $1398 | $1499 | $-101 | Suburban |  |
| Miami | 33010 | $1394 | $1371 | +$23 | Urban |  |
| Jacksonville | 32068 | $1391 | $1505 | $-114 | Urban |  |
| Tampa | 34668 | $1391 | $1587 | $-196 | Urban |  |
| Miami | 33030 | $1389 | $1383 | +$6 | Urban |  |
| Jacksonville | 32063 | $1385 | $1168 | +$217 | Suburban |  |
| Tampa | 33610 | $1384 | $1428 | $-44 | Urban |  |
| Miami | 33034 | $1380 | $1438 | $-58 | Suburban |  |
| Jacksonville | 32277 | $1378 | $1579 | $-201 | Urban |  |
| Tampa | 34607 | $1373 | $1434 | $-61 | Suburban |  |
| Tampa | 33714 | $1373 | $1290 | +$83 | Suburban | 🌊 |
| Orlando | 32720 | $1368 | $1275 | +$93 | Urban |  |
| Tampa | 34604 | $1365 | $1374 | $-9 | Suburban |  |
| Jacksonville | 32216 | $1364 | $1458 | $-94 | Urban |  |
| Tampa | 33612 | $1352 | $1419 | $-67 | Urban |  |
| Tampa | 33563 | $1351 | $1371 | $-20 | Suburban |  |
| Tampa | 33781 | $1343 | $1368 | $-25 | Suburban |  |
| Jacksonville | 32220 | $1330 | $1320 | +$10 | Suburban |  |
| Tampa | 34669 | $1330 | $1309 | +$21 | Suburban |  |
| Orlando | 34773 | $1325 | $1417 | $-92 | Rural |  |
| Tampa | 34602 | $1322 | $1279 | +$43 | Suburban |  |
| Tampa | 33567 | $1319 | $1358 | $-39 | Suburban |  |
| Tampa | 33613 | $1298 | $1473 | $-175 | Urban |  |
| Tampa | 34652 | $1296 | $1366 | $-70 | Suburban |  |
| Jacksonville | 32210 | $1293 | $1431 | $-138 | Urban |  |
| Jacksonville | 32219 | $1292 | $1244 | +$48 | Suburban |  |
| Tampa | 34689 | $1289 | $1485 | $-196 | Suburban |  |
| Orlando | 34731 | $1286 | $1228 | +$58 | Suburban |  |
| Tampa | 34608 | $1286 | $1347 | $-61 | Urban |  |
| Tampa | 34690 | $1285 | $1239 | +$46 | Suburban |  |
| Jacksonville | 32207 | $1266 | $1367 | $-101 | Urban |  |
| Jacksonville | 32205 | $1263 | $1359 | $-96 | Suburban |  |
| Jacksonville | 32217 | $1261 | $1631 | $-370 | Suburban |  |
| Tampa | 33570 | $1253 | $1363 | $-110 | Urban |  |
| Tampa | 34606 | $1250 | $1356 | $-106 | Suburban |  |
| Tampa | 34653 | $1248 | $1299 | $-51 | Urban |  |
| Tampa | 33541 | $1233 | $1339 | $-106 | Suburban |  |
| Tampa | 34691 | $1224 | $1379 | $-155 | Suburban |  |
| Jacksonville | 32208 | $1214 | $1266 | $-52 | Urban |  |
| Orlando | 32805 | $1204 | $1238 | $-34 | Suburban |  |
| Miami | 33150 | $1200 | $1333 | $-133 | Urban | 🌊 |
| Tampa | 34667 | $1194 | $1655 | $-461 | Urban |  |
| Jacksonville | 32040 | $1189 | $1120 | +$69 | Suburban |  |
| Jacksonville | 32254 | $1187 | $1262 | $-75 | Suburban |  |
| Jacksonville | 32211 | $1185 | $1270 | $-85 | Urban |  |
| Jacksonville | 32204 | $1167 | $1257 | $-90 | Suburban |  |
| Tampa | 34601 | $1153 | $1231 | $-78 | Suburban |  |
| Tampa | 33592 | $1150 | $1300 | $-150 | Suburban |  |
| Orlando | 34705 | $1147 | $1124 | +$23 | Rural |  |
| Tampa | 33542 | $1141 | $1099 | +$42 | Suburban |  |
| Tampa | 34613 | $1141 | $1177 | $-36 | Suburban |  |
| Orlando | 32726 | $1141 | $1167 | $-26 | Suburban |  |
| Tampa | 33605 | $1135 | $1204 | $-69 | Suburban |  |
| Orlando | 32798 | $1131 | $1162 | $-31 | Rural |  |
| Miami | 33476 | $1126 | $1165 | $-39 | Rural |  |
| Orlando | 32736 | $1125 | $1594 | $-469 | Suburban |  |
| Jacksonville | 32202 | $1124 | $1115 | +$9 | Rural |  |
| Jacksonville | 32011 | $1120 | $1193 | $-73 | Suburban |  |
| Jacksonville | 32145 | $1113 | $1090 | +$23 | Rural |  |
| Tampa | 33540 | $1107 | $1153 | $-46 | Suburban |  |
| Tampa | 33523 | $1101 | $1156 | $-55 | Suburban |  |
| Tampa | 33525 | $1099 | $1228 | $-129 | Suburban |  |
| Jacksonville | 32234 | $1096 | $1110 | $-14 | Suburban |  |
| Jacksonville | 32656 | $1089 | $1112 | $-23 | Suburban |  |
| Jacksonville | 32209 | $1062 | $1164 | $-102 | Urban |  |
| Orlando | 32102 | $1055 | $1068 | $-13 | Rural |  |
| Orlando | 32784 | $1020 | $895 | +$125 | Suburban |  |
| Tampa | 33576 | $998 | $1191 | $-193 | Rural |  |
| Tampa | 34614 | $978 | $1171 | $-193 | Suburban |  |
| Orlando | 32767 | $971 | $1089 | $-118 | Rural |  |
| Tampa | 33527 | $968 | $1159 | $-191 | Suburban |  |
| Jacksonville | 32009 | $919 | $951 | $-32 | Rural |  |
| Jacksonville | 32046 | $917 | $1009 | $-92 | Suburban |  |
| Miami | 33430 | $890 | $1112 | $-222 | Suburban |  |
| Tampa | 33597 | $886 | $913 | $-27 | Suburban |  |
| Jacksonville | 32206 | $860 | $1006 | $-146 | Suburban |  |
| Jacksonville | 32091 | $830 | $967 | $-137 | Suburban |  |

---

## Top 10 Over-Predicted ZIP Codes (Statewide)

### 1. Tampa - ZIP 34688
- **Actual**: $1429 | **Predicted**: $2129 | **Difference**: $-700
- **Profile**: Rural, 51.0% bachelor's+, $112091 income
- **Analysis**: Model predicted $2129 but actual is $1429. High education (51.0% bachelor's+) suggests higher rent. High income ($112091) indicates affluent area. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 2. Tampa - ZIP 33704
- **Actual**: $1495 | **Predicted**: $2126 | **Difference**: $-631
- **Profile**: Suburban, 57.8% bachelor's+, $107889 income
- **Analysis**: Model predicted $2126 but actual is $1495. High education (57.8% bachelor's+) suggests higher rent. High income ($107889) indicates affluent area. Beach proximity (score 1.0) adds premium. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 3. Tampa - ZIP 33647
- **Actual**: $1904 | **Predicted**: $2376 | **Difference**: $-472
- **Profile**: Urban, 60.6% bachelor's+, $109285 income
- **Analysis**: Model predicted $2376 but actual is $1904. High education (60.6% bachelor's+) suggests higher rent. High income ($109285) indicates affluent area. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 4. Orlando - ZIP 32736
- **Actual**: $1125 | **Predicted**: $1594 | **Difference**: $-469
- **Profile**: Suburban, 22.0% bachelor's+, $96542 income
- **Analysis**: Model predicted $1594 but actual is $1125. High income ($96542) indicates affluent area. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 5. Tampa - ZIP 34667
- **Actual**: $1194 | **Predicted**: $1655 | **Difference**: $-461
- **Profile**: Urban, 17.7% bachelor's+, $51280 income
- **Analysis**: Model predicted $1655 but actual is $1194. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 6. Tampa - ZIP 34681
- **Actual**: $1630 | **Predicted**: $2087 | **Difference**: $-458
- **Profile**: Rural, 34.3% bachelor's+, $nan income
- **Analysis**: Model predicted $2087 but actual is $1630. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 7. Miami - ZIP 33149
- **Actual**: $2283 | **Predicted**: $2679 | **Difference**: $-396
- **Profile**: Suburban, 77.2% bachelor's+, $181505 income
- **Analysis**: Model predicted $2679 but actual is $2283. High education (77.2% bachelor's+) suggests higher rent. High income ($181505) indicates affluent area. Beach proximity (score 2.0) adds premium. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 8. Tampa - ZIP 33558
- **Actual**: $1672 | **Predicted**: $2060 | **Difference**: $-388
- **Profile**: Urban, 57.2% bachelor's+, $116090 income
- **Analysis**: Model predicted $2060 but actual is $1672. High education (57.2% bachelor's+) suggests higher rent. High income ($116090) indicates affluent area. Urban location typically commands higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 9. Jacksonville - ZIP 32217
- **Actual**: $1261 | **Predicted**: $1631 | **Difference**: $-370
- **Profile**: Suburban, 41.3% bachelor's+, $73832 income
- **Analysis**: Model predicted $1631 but actual is $1261. High education (41.3% bachelor's+) suggests higher rent. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

### 10. Tampa - ZIP 33548
- **Actual**: $1975 | **Predicted**: $2338 | **Difference**: $-363
- **Profile**: Suburban, 56.2% bachelor's+, $129857 income
- **Analysis**: Model predicted $2338 but actual is $1975. High education (56.2% bachelor's+) suggests higher rent. High income ($129857) indicates affluent area. Actual rent may be lower due to: older housing stock, mixed housing types, or local market conditions.

---

## Top 10 Under-Predicted ZIP Codes (Statewide)

### 1. Miami - ZIP 33428
- **Actual**: $2432 | **Predicted**: $2011 | **Difference**: +$421
- **Profile**: Urban, 38.9% bachelor's+, $88543 income
- **Analysis**: Model predicted $2011 but actual is $2432. Urban area with educated population drives demand. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 2. Miami - ZIP 33146
- **Actual**: $2975 | **Predicted**: $2569 | **Difference**: +$406
- **Profile**: Suburban, 78.5% bachelor's+, $131500 income
- **Analysis**: Model predicted $2569 but actual is $2975. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 3. Miami - ZIP 33426
- **Actual**: $2202 | **Predicted**: $1803 | **Difference**: +$399
- **Profile**: Suburban, 32.3% bachelor's+, $74223 income
- **Analysis**: Model predicted $1803 but actual is $2202. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 4. Orlando - ZIP 34711
- **Actual**: $1883 | **Predicted**: $1514 | **Difference**: +$369
- **Profile**: Urban, 37.1% bachelor's+, $90245 income
- **Analysis**: Model predicted $1514 but actual is $1883. Urban area with educated population drives demand. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 5. Tampa - ZIP 33776
- **Actual**: $2544 | **Predicted**: $2178 | **Difference**: +$366
- **Profile**: Suburban, 46.3% bachelor's+, $105337 income
- **Analysis**: Model predicted $2178 but actual is $2544. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 6. Orlando - ZIP 32732
- **Actual**: $1896 | **Predicted**: $1545 | **Difference**: +$351
- **Profile**: Rural, 46.3% bachelor's+, $119205 income
- **Analysis**: Model predicted $1545 but actual is $1896. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 7. Miami - ZIP 33177
- **Actual**: $2174 | **Predicted**: $1847 | **Difference**: +$327
- **Profile**: Urban, 23.2% bachelor's+, $82682 income
- **Analysis**: Model predicted $1847 but actual is $2174. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 8. Orlando - ZIP 34715
- **Actual**: $2050 | **Predicted**: $1753 | **Difference**: +$297
- **Profile**: Suburban, 31.6% bachelor's+, $105262 income
- **Analysis**: Model predicted $1753 but actual is $2050. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 9. Orlando - ZIP 32811
- **Actual**: $1614 | **Predicted**: $1319 | **Difference**: +$295
- **Profile**: Urban, 26.4% bachelor's+, $54082 income
- **Analysis**: Model predicted $1319 but actual is $1614. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

### 10. Orlando - ZIP 32702
- **Actual**: $1734 | **Predicted**: $1439 | **Difference**: +$295
- **Profile**: Rural, 18.1% bachelor's+, $50935 income
- **Analysis**: Model predicted $1439 but actual is $1734. Actual rent may be higher due to: recent development, desirable amenities, or strong local demand.

---

## Methodology

**Model**: XGBoost Regression

**Features Used**:
- Housing age distribution (10 categories)
- Education levels (4 categories)
- Income metrics (median household, per capita)
- Jobs per capita
- Commute patterns
- Coastal/beach proximity
- Urban/suburban/rural classification

**Performance Metrics**:
- R² Score: 0.783
- Overall MAE: $174
- Florida MAE: $100