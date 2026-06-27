# 🛒 E-Commerce Sales Analysis

**Week 4 – Complete Data Analysis Project**  
*The Developers Arena | Data Analysis with Python*

---

## 📁 Project Structure

```
ecommerce_analysis/
├── data/
│   ├── sales_data.csv          ← raw dataset (100 rows × 5 cols)
│   └── generate_data.py        ← sample data generator (run if CSV missing)
├── visualizations/
│   ├── 1_revenue_by_category.png
│   ├── 2_monthly_revenue_trend.png
│   ├── 3_revenue_share_pie.png
│   └── 4_orders_vs_revenue.png
├── report/
│   └── analysis_report.txt
├── main.py                     ← main analysis script ✅
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone / download the project
```bash
cd ecommerce_analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Generate sample data
> Skip this if you already have `data/sales_data.csv` from the course platform.
```bash
python data/generate_data.py
```

### 4. Run the full analysis
```bash
python main.py
```

---

## 📊 What the Script Does

| Step | Action |
|------|--------|
| Load | Reads `data/sales_data.csv`, validates all 5 required columns |
| Clean | Drops duplicates, fixes data types, removes null / negative values |
| Analyse | Computes revenue, order counts, monthly trends, category breakdowns |
| Visualise | Generates 4 PNG charts in `visualizations/` |
| Report | Writes key insights + recommendations to `report/analysis_report.txt` |

---

## 📈 Charts Generated

1. **Revenue by Category** – bar chart showing which product category earns most  
2. **Monthly Revenue Trend** – line chart with area fill, highlights peak & low months  
3. **Revenue Share Pie** – donut chart of each category's percentage contribution  
4. **Orders vs Revenue** – horizontal grouped bar comparing volume to revenue per category  

---

## 🗂️ Dataset Columns

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier |
| `product_category` | string | Product category name |
| `sales_amount` | float | Revenue from the order (₹) |
| `quantity` | int | Number of units sold |
| `order_date` | date | Date the order was placed |

---

## 🧰 Tech Stack

- **Python 3.8+**
- **pandas** – data loading, cleaning, analysis
- **matplotlib** – chart generation
- **numpy** – numerical operations

---

## ✅ Quality Checklist

- [x] Project Overview documented
- [x] Setup instructions provided
- [x] Well-organised code with clear file hierarchy
- [x] Visual documentation (4 chart types)
- [x] Technical details: algorithms, data structures explained in code comments
- [x] Error handling and validation on every step
