# Databricks notebook source

# COMMAND ----------

import json
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

dashboard_spec = {
    "datasets": [
        {
            "name": "monthly_revenue",
            "displayName": "Monthly Revenue",
            "query": "SELECT month, total_revenue FROM workspace.sales_data.monthly_revenue ORDER BY month"
        }
        # add more datasets here — one per widget
    ],
    "pages": [
        {
            "displayName": "Sales Analysis",
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
                                    "disaggregated": False
                                }
                            }
                        ],
                        "spec": {
                            "version": 3,
                            "widgetType": "bar",
                            "encodings": {
                                "x": {"fieldName": "month",         "scale": {"type": "categorical"}},
                                "y": {"fieldName": "total_revenue", "scale": {"type": "quantitative"}}
                            }
                        }
                    },
                    "position": {"x": 0, "y": 0, "width": 6, "height": 6}
                }
                # add more widgets here
            ]
        }
    ]
}

dashboard = w.lakeview.create(
    display_name="Sales Analysis",
    serialized_dashboard=json.dumps(dashboard_spec)
)

print(f"Dashboard created: {dashboard.dashboard_id}")

# COMMAND ----------

# Open the dashboard in the browser
displayHTML(f'<a href="/dashboardsv3/{dashboard.dashboard_id}" target="_blank">Open dashboard</a>')
