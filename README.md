# Data Analysis Internship — Task 1: Foundational Setup & EDA

**Author:** KUMARI ARPANA SINHA  
**GitHub:** [@kumariarpanasinha](https://github.com/kumariarpanasinha)  
**Timeline:** 6 Days (Foundational Setup & Exploratory Data Analysis)

---

## Repository Structure

```text
Data-Analysis-Internship-/
├── data/
│   ├── superstore_raw.csv        # Raw Superstore Sales dataset (10,800 rows)
│   ├── superstore_cleaned.csv    # Cleaned dataset (9,993 rows)
│   └── superstore.db             # SQLite database (table: orders)
├── notebooks/
│   └── 01_eda_superstore.ipynb   # Executed EDA notebook (charts + SQLAlchemy checks)
├── scripts/
│   ├── verify_env.py             # Verifies Python & required libraries
│   ├── data_cleaning.py          # Cleans raw CSV & writes CSV + SQLite DB
│   └── generate_dashboard.py     # Builds interactive Plotly HTML dashboard
├── reports/
│   ├── eda_summary_report.md     # Executive summary of EDA findings
│   ├── category_performance.png
│   ├── region_segment_profit.png
│   ├── monthly_sales_trend.png
│   └── discount_vs_profit.png
├── dashboards/
│   └── sales_dashboard.html      # Interactive 4-panel Plotly dashboard
├── requirements.txt
└── README.md
```

---

## Environment Setup

1. Create and activate a Python virtual environment (Python 3.13):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install required libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `sqlalchemy`, `jupyter`):
   ```bash
   pip install -r requirements.txt
   ```
3. Verify installation:
   ```bash
   python scripts/verify_env.py
   ```

---

## How to Run

1. **Clean Data & Build SQLite Database:**
   ```bash
   python scripts/data_cleaning.py
   ```
2. **Generate Interactive Dashboard:**
   ```bash
   python scripts/generate_dashboard.py
   ```
   Open `dashboards/sales_dashboard.html` in any browser to explore the interactive charts.
3. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook notebooks/01_eda_superstore.ipynb
   ```

---

## Key Insights Snapshot

- **Total Sales:** \$2,296,919.49 | **Total Profit:** \$286,409.08 (**12.47%** margin)
- **Top Category:** Technology (\$836,154.03 sales, \$145,454.95 profit)
- **Loss Drivers:** `Tables` (-\$17,725.48), `Bookcases` (-\$3,472.56), and discounts above 20%
- Full details are documented in [reports/eda_summary_report.md](reports/eda_summary_report.md).
