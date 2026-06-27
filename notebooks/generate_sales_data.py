# Databricks notebook source

# COMMAND ----------

import random
from datetime import date, timedelta

random.seed(42)

PRODUCTS = [
    # Electronics
    ("P001", "Smartwatch",        "Electronics",  149.99),
    ("P002", "Headphones",        "Electronics",   79.99),
    ("P003", "Keyboard",          "Electronics",   59.99),
    ("P004", "Webcam",            "Electronics",   89.99),
    ("P005", "USB Hub",           "Electronics",   34.99),
    ("P006", "Monitor Stand",     "Electronics",   49.99),
    # Sports
    ("P007", "Yoga Mat",          "Sports",        49.99),
    ("P008", "Dumbbell Set",      "Sports",        89.99),
    ("P009", "Running Shoes",     "Sports",        99.99),
    ("P010", "Water Bottle",      "Sports",        24.99),
    ("P011", "Resistance Bands",  "Sports",        19.99),
    ("P012", "Jump Rope",         "Sports",        14.99),
    # Clothing
    ("P013", "T-Shirt",           "Clothing",      29.99),
    ("P014", "Jacket",            "Clothing",      89.99),
    ("P015", "Jeans",             "Clothing",      59.99),
    ("P016", "Sneakers",          "Clothing",      74.99),
    ("P017", "Hoodie",            "Clothing",      49.99),
    ("P018", "Cap",               "Clothing",      19.99),
    # Food
    ("P019", "Coffee Beans",      "Food",          14.99),
    ("P020", "Protein Powder",    "Food",          49.99),
    ("P021", "Olive Oil",         "Food",          12.99),
    ("P022", "Granola",           "Food",           8.99),
    ("P023", "Tea Set",           "Food",          22.99),
    ("P024", "Dark Chocolate",    "Food",           9.99),
    # Books
    ("P025", "Python Book",       "Books",         39.99),
    ("P026", "Design Handbook",   "Books",         54.99),
    ("P027", "Sci-Fi Novel",      "Books",         14.99),
    ("P028", "History of Rome",   "Books",         19.99),
    ("P029", "Cook Book",         "Books",         29.99),
    ("P030", "Business Strategy", "Books",         34.99),
    # Home
    ("P031", "Desk Lamp",         "Home",          44.99),
    ("P032", "Throw Blanket",     "Home",          34.99),
    ("P033", "Candle Set",        "Home",          19.99),
    ("P034", "Picture Frame",     "Home",          14.99),
    ("P035", "Storage Box",       "Home",          24.99),
    ("P036", "Wall Clock",        "Home",          39.99),
    # Beauty
    ("P037", "Face Serum",        "Beauty",        59.99),
    ("P038", "Sunscreen SPF50",   "Beauty",        24.99),
    ("P039", "Moisturizer",       "Beauty",        34.99),
    ("P040", "Lip Balm",          "Beauty",         9.99),
    ("P041", "Eye Cream",         "Beauty",        44.99),
    ("P042", "Hair Mask",         "Beauty",        19.99),
    # Toys
    ("P043", "LEGO Set",          "Toys",          69.99),
    ("P044", "Board Game",        "Toys",          44.99),
    ("P045", "Puzzle 1000pc",     "Toys",          24.99),
    ("P046", "RC Car",            "Toys",          59.99),
    ("P047", "Drawing Kit",       "Toys",          19.99),
    ("P048", "Science Kit",       "Toys",          34.99),
    # Garden
    ("P049", "Garden Hose",       "Garden",        39.99),
    ("P050", "Plant Pots Set",    "Garden",        29.99),
    ("P051", "Pruning Shears",    "Garden",        24.99),
    ("P052", "Watering Can",      "Garden",        19.99),
    ("P053", "Seed Starter Kit",  "Garden",        14.99),
    ("P054", "Compost Bin",       "Garden",        49.99),
    # Automotive
    ("P055", "Car Phone Mount",   "Automotive",    24.99),
    ("P056", "Dash Cam",          "Automotive",    99.99),
    ("P057", "Car Vacuum",        "Automotive",    49.99),
    ("P058", "Seat Organizer",    "Automotive",    19.99),
    ("P059", "Jump Starter",      "Automotive",    89.99),
    ("P060", "Air Freshener",     "Automotive",     9.99),
]

start_date = date(2023, 1, 1)
end_date   = date(2024, 12, 31)
days_range = (end_date - start_date).days

rows = []
for _ in range(1000000):
    product_id, product_name, category, unit_price = random.choice(PRODUCTS)
    sale_date = start_date + timedelta(days=random.randint(0, days_range))
    quantity  = random.randint(1, 10)
    revenue   = round(quantity * unit_price, 2)
    rows.append((sale_date.isoformat(), product_id, product_name, category, quantity, unit_price, revenue))

for row in rows[:5]:
    print(row)

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

schema = StructType([
    StructField("date",         StringType(),  False),
    StructField("product_id",   StringType(),  False),
    StructField("product_name", StringType(),  False),
    StructField("category",     StringType(),  False),
    StructField("quantity",     IntegerType(), False),
    StructField("unit_price",   DoubleType(),  False),
    StructField("revenue",      DoubleType(),  False),
])

df = spark.createDataFrame(rows, schema)
display(df)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.sales_data")

df.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.raw_sales")

print("Done. Table: workspace.sales_data.raw_sales")
