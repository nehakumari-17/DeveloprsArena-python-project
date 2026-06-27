"""
generate_data.py
Run this ONCE to create sales_data.csv inside the data/ folder.
Usage:  python data/generate_data.py
"""

import csv
import random
from datetime import date, timedelta

CATEGORIES = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports"]

PRICE_RANGES = {
    "Electronics":    (500,  8000),
    "Clothing":       (200,  2500),
    "Books":          (100,   800),
    "Home & Garden":  (300,  5000),
    "Sports":         (250,  4000),
}

random.seed(42)

START_DATE = date(2025, 1, 1)
END_DATE   = date(2025, 12, 31)
DAYS       = (END_DATE - START_DATE).days

rows = []
for i in range(1, 101):
    cat   = random.choice(CATEGORIES)
    lo, hi = PRICE_RANGES[cat]
    amt   = round(random.uniform(lo, hi), 2)
    qty   = random.randint(1, 5)
    d     = START_DATE + timedelta(days=random.randint(0, DAYS))
    rows.append({
        "order_id":         f"ORD{i:04d}",
        "product_category": cat,
        "sales_amount":     amt,
        "quantity":         qty,
        "order_date":       d.strftime("%Y-%m-%d"),
    })

out = "data/sales_data.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✓  Created {out}  ({len(rows)} rows)")
