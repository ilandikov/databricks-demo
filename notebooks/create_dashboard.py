# Databricks notebook source

# COMMAND ----------

import json
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dashboards import Dashboard

w = WorkspaceClient()

# COMMAND ----------

for d in w.lakeview.list():
    w.lakeview.trash(dashboard_id=d.dashboard_id)
    print(f"Deleted: {d.display_name} ({d.dashboard_id})")

# COMMAND ----------

def bar_widget(name, title, dataset_name, fields, x_field, y_field, position):
    return {
        "widget": {
            "name": name,
            "queries": [
                {
                    "name": "main_query",
                    "query": {
                        "datasetName": dataset_name,
                        "fields": [{"name": f, "expression": f"`{f}`"} for f in fields],
                        "disaggregated": True
                    }
                }
            ],
            "spec": {
                "version": 3,
                "frame": {"title": title, "showTitle": True},
                "widgetType": "bar",
                "encodings": {
                    "x": {"fieldName": x_field, "scale": {"type": "categorical"}},
                    "y": {"fieldName": y_field, "scale": {"type": "quantitative"}}
                },
                "data": {"queryName": "main_query"}
            }
        },
        "position": position
    }

def table_widget(name, title, dataset_name, fields, position):
    return {
        "widget": {
            "name": name,
            "queries": [
                {
                    "name": "main_query",
                    "query": {
                        "datasetName": dataset_name,
                        "fields": [{"name": f, "expression": f"`{f}`"} for f in fields],
                        "disaggregated": True
                    }
                }
            ],
            "spec": {
                "version": 2,
                "frame": {"title": title, "showTitle": True},
                "widgetType": "table",
                "encodings": {
                    "columns": [{"fieldName": f} for f in fields]
                },
                "data": {"queryName": "main_query"}
            }
        },
        "position": position
    }

# COMMAND ----------

def dataset(name, display_name, query_lines):
    return {
        "name": name,
        "displayName": display_name,
        "queryLines": query_lines
    }

dashboard_spec = {
    "datasets": [
        dataset("monthly_revenue", "Monthly Revenue", [
            "SELECT month, total_revenue\n",
            "FROM workspace.sales_data.monthly_revenue\n",
            "ORDER BY month"
        ]),
        dataset("top_products_by_month", "Top Products By Month", [
            "SELECT month, product_name, category, total_revenue\n",
            "FROM workspace.sales_data.top_products_by_month\n",
            "QUALIFY ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_revenue DESC) <= 3\n",
            "ORDER BY month ASC, total_revenue DESC\n"
        ]),
        dataset("revenue_by_category", "Revenue By Category", [
            "SELECT category, total_revenue\n",
            "FROM workspace.sales_data.revenue_by_category\n",
            "ORDER BY total_revenue DESC"
        ]),
        dataset("top_products", "Top Products", [
            "SELECT product_name, category, total_revenue\n",
            "FROM workspace.sales_data.top_products\n",
            "ORDER BY total_revenue DESC\n",
            "LIMIT 10"
        ]),
        dataset("units_sold_by_month", "Units Sold By Month", [
            "SELECT month, units_sold\n",
            "FROM workspace.sales_data.units_sold_by_month\n",
            "ORDER BY month"
        ]),
        dataset("worst_products", "Worst Products", [
            "SELECT product_name, category, total_revenue\n",
            "FROM workspace.sales_data.worst_products\n",
            "ORDER BY total_revenue ASC\n",
            "LIMIT 10"
        ]),
        dataset("worst_products_by_month", "Worst Products By Month", [
            "SELECT month, product_name, category, total_revenue\n",
            "FROM workspace.sales_data.worst_products_by_month\n",
            "QUALIFY ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_revenue ASC) <= 3\n",
            "ORDER BY month ASC, total_revenue ASC\n"
        ]),
    ],
    "pages": [
        {
            "name": "sales_page",
            "displayName": "Sales Analysis",
            "pageType": "PAGE_TYPE_CANVAS",
            "layoutVersion": "GRID_V1",
            "layout": [
                bar_widget(
                    name="monthly_revenue_chart",
                    title="Monthly Revenue",
                    dataset_name="monthly_revenue",
                    fields=["month", "total_revenue"],
                    x_field="month",
                    y_field="total_revenue",
                    position={"x": 0, "y": 0, "width": 6, "height": 6}
                ),
                table_widget(
                    name="top_products_by_month_table",
                    title="Top Products By Month",
                    dataset_name="top_products_by_month",
                    fields=["month", "product_name", "category", "total_revenue"],
                    position={"x": 0, "y": 6, "width": 12, "height": 6}
                ),
                bar_widget(
                    name="revenue_by_category_chart",
                    title="Revenue By Category",
                    dataset_name="revenue_by_category",
                    fields=["category", "total_revenue"],
                    x_field="category",
                    y_field="total_revenue",
                    position={"x": 6, "y": 0, "width": 6, "height": 6}
                ),
                table_widget(
                    name="top_products_table",
                    title="Top 10 Products",
                    dataset_name="top_products",
                    fields=["product_name", "category", "total_revenue"],
                    position={"x": 0, "y": 12, "width": 6, "height": 6}
                ),
                bar_widget(
                    name="units_sold_by_month_chart",
                    title="Units Sold By Month",
                    dataset_name="units_sold_by_month",
                    fields=["month", "units_sold"],
                    x_field="month",
                    y_field="units_sold",
                    position={"x": 6, "y": 12, "width": 6, "height": 6}
                ),
                table_widget(
                    name="worst_products_table",
                    title="Worst 10 Products",
                    dataset_name="worst_products",
                    fields=["product_name", "category", "total_revenue"],
                    position={"x": 0, "y": 18, "width": 6, "height": 6}
                ),
                table_widget(
                    name="worst_products_by_month_table",
                    title="Worst 3 Products By Month",
                    dataset_name="worst_products_by_month",
                    fields=["month", "product_name", "category", "total_revenue"],
                    position={"x": 6, "y": 18, "width": 6, "height": 6}
                ),
            ]
        }
    ],
    "uiSettings": {
        "theme": {"widgetHeaderAlignment": "ALIGNMENT_UNSPECIFIED"},
        "applyModeEnabled": False
    }
}

dashboard = w.lakeview.create(dashboard=Dashboard(
    display_name="Sales Analysis",
    serialized_dashboard=json.dumps(dashboard_spec)
))

w.lakeview.publish(dashboard_id=dashboard.dashboard_id)
print(f"Dashboard created and published: {dashboard.dashboard_id}")

# COMMAND ----------

displayHTML(f'<a href="/dashboardsv3/{dashboard.dashboard_id}" target="_blank">Open dashboard</a>')
