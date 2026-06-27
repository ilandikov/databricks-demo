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

dashboard_spec = {
    "datasets": [
        {
            "name": "monthly_revenue",
            "displayName": "Monthly Revenue",
            "queryLines": [
                "SELECT month, total_revenue\n",
                "FROM workspace.sales_data.monthly_revenue\n",
                "ORDER BY month"
            ]
        },
        {
            "name": "top_products_by_month",
            "displayName": "Top Products By Month",
            "queryLines": [
                "SELECT month, product_name, category, total_revenue\n",
                "FROM workspace.sales_data.top_products_by_month\n",
                "QUALIFY ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_revenue DESC) <= 3\n",
                "ORDER BY month ASC, total_revenue DESC\n"
            ]
        }
        # add more datasets here — one per widget
    ],
    "pages": [
        {
            "name": "sales_page",
            "displayName": "Sales Analysis",
            "pageType": "PAGE_TYPE_CANVAS",
            "layoutVersion": "GRID_V1",
            "layout": [
                {
                    "widget": {
                        "name": "monthly_revenue_chart",
                        "queries": [
                            {
                                "name": "main_query",
                                "query": {
                                    "datasetName": "monthly_revenue",
                                    "fields": [
                                        {"name": "month",         "expression": "`month`"},
                                        {"name": "total_revenue", "expression": "`total_revenue`"}
                                    ],
                                    "disaggregated": True
                                }
                            }
                        ],
                        "spec": {
                            "version": 3,
                            "frame": {"title": "Monthly Revenue", "showTitle": True},
                            "widgetType": "bar",
                            "encodings": {
                                "x": {"fieldName": "month",         "scale": {"type": "categorical"}},
                                "y": {"fieldName": "total_revenue", "scale": {"type": "quantitative"}}
                            },
                            "data": {"queryName": "main_query"}
                        }
                    },
                    "position": {"x": 0, "y": 0, "width": 6, "height": 6}
                },
                {
                    "widget": {
                        "name": "top_products_by_month_chart",
                        "queries": [
                            {
                                "name": "main_query",
                                "query": {
                                    "datasetName": "top_products_by_month",
                                    "fields": [
                                        {"name": "month",         "expression": "`month`"},
                                        {"name": "product_name",  "expression": "`product_name`"},
                                        {"name": "category",      "expression": "`category`"},
                                        {"name": "total_revenue", "expression": "`total_revenue`"}
                                    ],
                                    "disaggregated": True
                                }
                            }
                        ],
                        "spec": {
                            "version": 3,
                            "frame": {"title": "Top Products By Month", "showTitle": True},
                            "widgetType": "table",
                            "encodings": {
                                "columns": [
                                    {"fieldName": "month",        "displayName": "Month"},
                                    {"fieldName": "product_name", "displayName": "Product"},
                                    {"fieldName": "category",     "displayName": "Category"},
                                    {"fieldName": "total_revenue","displayName": "Revenue"}
                                ]
                            },
                            "data": {"queryName": "main_query"}
                        }
                    },
                    "position": {"x": 0, "y": 6, "width": 12, "height": 6}
                }
                # add more widgets here — increment y by 6 for each new row
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
