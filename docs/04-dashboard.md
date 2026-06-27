# Step 4 — Build the Dashboard

## Do this

1. In the left sidebar, click **Dashboards** → **Create dashboard**.

2. Name it `Sales Analysis`.

3. For each metric below, add a widget:
   - Click **Add** → **Visualization**
   - Write the SQL query
   - Choose the chart type
   - Click **Save**

---

### Widget 1 — Monthly Revenue (bar chart)

```sql
SELECT month, total_revenue
FROM workspace.sales_data.monthly_revenue
ORDER BY month
```

Chart type: **Bar**. X axis: `month`, Y axis: `total_revenue`.

---

### Widget 2 — Revenue by Category (pie chart)

```sql
SELECT category, total_revenue
FROM workspace.sales_data.revenue_by_category
```

Chart type: **Pie**. Label: `category`, Value: `total_revenue`.

---

### Widget 3 — Top 10 Products (table)

```sql
SELECT product_name, category, total_revenue
FROM workspace.sales_data.top_products
ORDER BY total_revenue DESC
LIMIT 10
```

Chart type: **Table**.

---

### Widget 4 — Units Sold by Month (line chart)

```sql
SELECT month, units_sold
FROM workspace.sales_data.units_sold_by_month
ORDER BY month
```

Chart type: **Line**. X axis: `month`, Y axis: `units_sold`.

---

## You are done with Step 4 when

- All 4 widgets are visible on the dashboard with data in them

## Next

You are done. You have built a full data pipeline: fake data → Delta tables → dashboard.
