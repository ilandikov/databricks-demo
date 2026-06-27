# Step 3 — Transform Data with PySpark

## Do this

1. Commit and push `notebooks/transform_sales_data.py` to GitHub. Let the action sync it to Databricks.

2. In Databricks, open the `transform_sales_data` notebook. Connect to Serverless.

3. Run cell 1 — reads `workspace.sales_data.raw_sales` and displays it. Verify the data looks correct.

4. Run cell 2 — adds `year` and `month` columns to the DataFrame.

5. Run cells 3–7 one by one. Each cell creates one aggregated Delta table:
   - Cell 3 → `workspace.sales_data.monthly_revenue`
   - Cell 4 → `workspace.sales_data.revenue_by_category`
   - Cell 5 → `workspace.sales_data.top_products`
   - Cell 6 → `workspace.sales_data.top_products_by_month`
   - Cell 7 → `workspace.sales_data.units_sold_by_month`

6. Verify the tables exist — go to **Catalog** in the left sidebar → `workspace` → `sales_data`. You should see all five tables.

## You are done with Step 3 when

- All five tables appear under `workspace.sales_data` in the Catalog

## Next

Step 4 — build the dashboard.
