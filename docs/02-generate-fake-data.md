# Step 2 — Generate Fake Sales Data

## Do this

1. In the left sidebar, click **New** → **Notebook**. Name it `generate-sales-data`, set language to **Python**, click **Create**.

2. Paste this into the first cell and run it:

```python
import random
import csv
from datetime import date, timedelta
from io import StringIO

random.seed(42)

PRODUCTS = [
    ("P001", "Laptop",        "Electronics", 999.99),
    ("P002", "Headphones",    "Electronics", 79.99),
    ("P003", "Keyboard",      "Electronics", 49.99),
    ("P004", "Monitor",       "Electronics", 299.99),
    ("P005", "USB Hub",       "Electronics", 29.99),
    ("P006", "T-Shirt",       "Clothing",    19.99),
    ("P007", "Jeans",         "Clothing",    59.99),
    ("P008", "Jacket",        "Clothing",    89.99),
    ("P009", "Sneakers",      "Clothing",    74.99),
    ("P010", "Hat",           "Clothing",    24.99),
    ("P011", "Coffee Beans",  "Food",        14.99),
    ("P012", "Protein Bar",   "Food",         3.99),
    ("P013", "Olive Oil",     "Food",        12.99),
    ("P014", "Tea Set",       "Food",        22.99),
    ("P015", "Granola",       "Food",         8.99),
    ("P016", "Python Book",   "Books",       39.99),
    ("P017", "Sci-Fi Novel",  "Books",       14.99),
    ("P018", "Desk Lamp",     "Home",        34.99),
    ("P019", "Candle",        "Home",         9.99),
    ("P020", "Picture Frame", "Home",        17.99),
]

start_date = date(2024, 1, 1)
end_date   = date(2024, 3, 31)
days_range = (end_date - start_date).days

rows = []
for _ in range(1000):
    product_id, product_name, category, unit_price = random.choice(PRODUCTS)
    sale_date = start_date + timedelta(days=random.randint(0, days_range))
    quantity  = random.randint(1, 10)
    revenue   = round(quantity * unit_price, 2)
    rows.append([sale_date, product_id, product_name, category, quantity, unit_price, revenue])

# Preview first 5 rows
for row in rows[:5]:
    print(row)
```

   You should see 5 rows printed. Each row is one sale.

3. Add a new cell below (click **+** at the bottom of the cell). Paste this and run it:

```python
output = StringIO()
writer = csv.writer(output)
writer.writerow(["date", "product_id", "product_name", "category", "quantity", "unit_price", "revenue"])
writer.writerows(rows)

dbutils.fs.put("/FileStore/sales.csv", output.getvalue(), overwrite=True)
print("Saved to /FileStore/sales.csv")
```

   You should see `Saved to /FileStore/sales.csv`.

4. Verify the file exists — add a new cell and run:

```python
display(dbutils.fs.ls("/FileStore/"))
```

   You should see `sales.csv` in the list.

## You are done with Step 2 when

- The preview printed 5 rows with dates, product names, and revenue values
- `sales.csv` appears in `/FileStore/`

## Next

Step 3 — load `sales.csv` into a Delta table using PySpark.
