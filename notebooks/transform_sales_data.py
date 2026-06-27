# Databricks notebook source

# COMMAND ----------

df = spark.table("workspace.sales_data.raw_sales")
display(df)

# COMMAND ----------

from pyspark.sql.functions import col, month, year, sum, count, round

df = df.withColumn("month", month(col("date").cast("date"))) \
       .withColumn("year",  year(col("date").cast("date")))

# COMMAND ----------

monthly_revenue = df.groupBy("year", "month") \
    .agg(round(sum("revenue"), 2).alias("total_revenue")) \
    .orderBy("year", "month")

monthly_revenue.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.monthly_revenue")
display(monthly_revenue)

# COMMAND ----------

revenue_by_category = df.groupBy("category") \
    .agg(round(sum("revenue"), 2).alias("total_revenue")) \
    .orderBy(col("total_revenue").desc())

revenue_by_category.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.revenue_by_category")
display(revenue_by_category)

# COMMAND ----------

top_products = df.groupBy("product_id", "product_name", "category") \
    .agg(round(sum("revenue"), 2).alias("total_revenue")) \
    .orderBy(col("total_revenue").desc())

top_products.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.top_products")
display(top_products)

# COMMAND ----------

top_products_by_month = df.groupBy("year", "month", "product_id", "product_name", "category") \
    .agg(round(sum("revenue"), 2).alias("total_revenue")) \
    .orderBy("year", "month", col("total_revenue").desc())

top_products_by_month.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.top_products_by_month")
display(top_products_by_month)

# COMMAND ----------

units_sold_by_month = df.groupBy("year", "month") \
    .agg(sum("quantity").alias("units_sold")) \
    .orderBy("year", "month")

units_sold_by_month.write.format("delta").mode("overwrite").saveAsTable("workspace.sales_data.units_sold_by_month")
display(units_sold_by_month)
