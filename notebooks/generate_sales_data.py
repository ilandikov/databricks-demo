# Databricks notebook source

# COMMAND ----------

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
for _ in range(10000):
    product_id, product_name, category, unit_price = random.choice(PRODUCTS)
    sale_date = start_date + timedelta(days=random.randint(0, days_range))
    quantity  = random.randint(1, 10)
    revenue   = round(quantity * unit_price, 2)
    rows.append([sale_date, product_id, product_name, category, quantity, unit_price, revenue])

for row in rows[:5]:
    print(row)

# COMMAND ----------

output = StringIO()
writer = csv.writer(output)
writer.writerow(["date", "product_id", "product_name", "category", "quantity", "unit_price", "revenue"])
writer.writerows(rows)

dbutils.fs.put("/FileStore/sales.csv", output.getvalue(), overwrite=True)
print("Saved to /FileStore/sales.csv")

# COMMAND ----------

display(dbutils.fs.ls("/FileStore/"))
