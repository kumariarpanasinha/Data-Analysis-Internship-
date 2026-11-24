# Task 1: Exploratory Data Analysis (EDA) Summary Report

**Dataset:** Sample Superstore Sales  
**Date Range:** 2015-01-03 to 2018-12-30  
**Repository:** `Data-Analysis-Internship-`

---

## 1. Data Cleaning Summary

| Step | Count | Details |
|---|---:|---|
| Raw rows loaded | 10,800 | `data/superstore_raw.csv` |
| Non-order rows removed | 806 | Appended metadata/return rows missing `Order Date` and `Sales` |
| Duplicate rows removed | 1 | Identical order line item excluding `Row ID` |
| Missing values imputed | 11 | Missing `Postal Code` in Burlington, Vermont filled with `05401` |
| **Final cleaned rows** | **9,993** | Saved to `data/superstore_cleaned.csv` and `data/superstore.db` (`orders` table) |

---

## 2. Executive KPI Overview

- **Total Sales:** \$2,296,919.49
- **Total Profit:** \$286,409.08
- **Overall Profit Margin:** 12.47%
- **Unique Orders:** 5,009
- **Unique Customers:** 793
- **Average Shipping Time:** 3.96 days

---

## 3. Category & Sub-Category Performance

| Category | Total Sales (USD) | Total Profit (USD) |
|---|---:|---:|
| Technology | \$836,154.03 | \$145,454.95 |
| Office Supplies | \$719,047.03 | \$122,490.80 |
| Furniture | \$741,718.42 | \$18,463.33 |

- **Top Profitable Sub-Categories:**
  1. `Copiers` (\$55,617.82 profit on \$149,528.03 sales)
  2. `Phones` (\$44,515.73 profit on \$330,007.05 sales)
  3. `Accessories` (\$41,936.64 profit on \$167,380.32 sales)
- **Loss-Making Sub-Categories:**
  1. `Tables` (-\$17,725.48 profit on \$206,965.53 sales)
  2. `Bookcases` (-\$3,472.56 profit on \$114,880.00 sales)
  3. `Supplies` (-\$1,189.10 profit on \$46,673.54 sales)

---

## 4. Regional Performance

| Region | Total Sales (USD) | Total Profit (USD) |
|---|---:|---:|
| West | \$725,457.82 | \$108,418.45 |
| East | \$678,499.87 | \$91,534.84 |
| Central | \$501,239.89 | \$39,706.36 |
| South | \$391,721.90 | \$46,749.43 |

- **West** and **East** generate the largest share of both revenue and profit.
- **Central** generates more sales than **South** (\$501.2K vs \$391.7K) but delivers lower total profit (\$39.7K vs \$46.7K), indicating heavier discounting or lower-margin product mix.

---

## 5. Discount Impact Analysis

| Discount Band | Line Items | Mean Profit (USD) | Total Profit (USD) |
|---|---:|---:|---:|
| 0% | 4,798 | \$66.90 | \$320,987.60 |
| 1–20% | 3,803 | \$26.50 | \$100,785.47 |
| 21–40% | 459 | -\$78.01 | -\$35,805.41 |
| >40% | 933 | -\$106.71 | -\$99,558.59 |

- Orders with discounts **above 20%** consistently lose money on average, eroding **\$135,364.00** in combined profit across 1,392 line items.

---

## 6. Generated Visuals & Interactive Dashboard

- `reports/category_performance.png`
- `reports/region_segment_profit.png`
- `reports/monthly_sales_trend.png`
- `reports/discount_vs_profit.png`
- `dashboards/sales_dashboard.html` (interactive Plotly dashboard)

