# Databricks Learning Plan — Product Sales Dashboard

## Goal

Build a working data pipeline: fake CSV data → Delta tables → monthly sales dashboard.

**Dashboard metrics:** total revenue per month, top-selling products, revenue by category, units sold.

**Stack:** Databricks Free tier — Python (PySpark) + SQL Warehouse + Lakeview dashboards. No Delta Live Tables (not available on this tier).

---

## Databricks Object Map

Before touching code, you need to know what the objects are. Think of it like learning what a "Lambda", "S3 bucket", or "RDS instance" is before building on AWS.

| Object | What it is |
|---|---|
| **Workspace** | Your Databricks environment — like a project folder that contains everything below |
| **Notebook** | A file where you write code in blocks (cells) and run them one at a time, seeing output inline. Like a browser DevTools console you can save and chain. Not related to data storage — it's where you write code that *operates on* data. |
| **Cluster** | A virtual machine (or group of them) that runs your notebook code |
| **SQL Warehouse** | A compute engine optimized for SQL queries — separate from clusters |
| **Catalog / Schema / Table** | An **address** for where data lives: `catalog.schema.table`. Like a URL. The catalog is the top-level namespace, schema is a group of tables, table is the actual data. Same concept as `database.schema.table` in PostgreSQL. |
| **Parquet** | A file format for storing tabular data — binary and columnar, unlike CSV which is plain text rows. Faster to query, smaller on disk. You never open it by hand; Spark reads and writes it automatically. |
| **Delta Table** | A table backed by Parquet files **plus a transaction log**. The address (`catalog.schema.table`) tells you *where* a table lives; Delta tells you *how* it's stored. Delta adds: update/delete rows, see previous versions (time travel), safe concurrent writes. Default table format in Databricks. |
| **Apache Spark** | A distributed computation engine — a program that splits a big task across multiple machines and runs the pieces in parallel, then combines the results. Normal Python runs on one machine; if your data is 100GB you are limited by that machine's RAM. Spark splits the data into chunks, sends each chunk to a different machine in the cluster, processes them simultaneously, and merges the output. For small datasets the difference is invisible, but the API is the same whether you have 1000 rows or 1 billion. Runs on your cluster. You never interact with it directly. |
| **PySpark** | The Python library that lets you talk to Spark from Python. When you write PySpark code in a notebook, it translates your Python into Spark operations and executes them on the cluster. `spark` (the entry point) and `DataFrame` are both part of PySpark. |
| **Cell** | A single runnable block of code inside a notebook. Cells share the same Python session — a variable declared in cell 1 is accessible in cell 2. The split is not about scope isolation; it is about execution control: you run cells one at a time, inspect the output, and decide whether to continue. Think of it as a REPL where you hit Enter after each logical chunk. |
| **DataFrame** | An in-memory table of data with named columns and typed rows — the main object you work with in PySpark. Think of it as an array of objects in JavaScript, but distributed across a cluster. It is lazy: no computation happens when you define transformations — Spark waits until you call an action (`display()`, `.write`, `.count()`) and then executes everything at once. A DataFrame is temporary — it lives in memory during a notebook session. To persist it, you write it to a Delta table. |
| **DBFS** | Databricks File System — where you upload raw files (CSV, JSON) before loading them into tables |
| **Lakeview Dashboard** | Databricks' built-in BI dashboard — reads from SQL Warehouse, no external tool needed |

### Notebook vs. Catalog/Schema/Table — not the same category

- Notebook = **code** (where you write logic, transformations, queries)
- Catalog/Schema/Table = **data storage** (where results live)

A notebook creates tables, queries tables, deletes tables. It is not a table. Same distinction as a Node.js script vs. a PostgreSQL database.

### Catalog/Schema/Table vs. Delta Table — not the same question

- `catalog.schema.table` answers: **where is this table?** (the address)
- Delta answers: **how is this table stored?** (the format)

A table at `workspace.sales.products` is backed by *some* storage format. In Databricks, that format is almost always Delta — which adds row-level updates, deletes, and version history on top of plain Parquet.

---

## Steps

### Step 1 — Understand the workspace
Doc: `01-workspace-orientation.md`
- Navigate the Databricks UI
- Understand what you have on the free tier

### Step 2 — Generate fake data
Doc: `02-generate-fake-data.md`
- Write a Python script to generate `sales.csv`
- Schema: `date, product_id, product_name, category, quantity, unit_price`
- ~1000 rows, 3 months of data, 5 categories, 20 products

### ~~Step 3 — Upload CSV and create a Delta table~~ (merged into Step 2)
DBFS was disabled on the free tier, so we skipped the intermediate CSV file and wrote directly to a Delta table from the generation notebook. Result: `workspace.sales_data.raw_sales`.

### Step 3 — Transform data with PySpark
Doc: `04-transform.md`
- Create aggregated tables using PySpark:
  - Monthly revenue
  - Revenue by category
  - Top products
  - Units sold per month
- Understand: why we write results back as Delta tables (not keep them in memory)

### Step 5 — Build the dashboard
Doc: `05-dashboard.md`
- Connect Lakeview dashboard to SQL Warehouse
- Write 4 SQL queries (one per metric)
- Build charts and tiles

---

## What you will learn

- How Databricks organizes data (catalog/schema/table — the three-level namespace)
- What a Delta table is and why it matters (vs. a plain CSV or Parquet file)
- How PySpark works (it's like pandas but distributed — you already know JS array methods, same idea)
- How SQL Warehouse differs from a notebook cluster
- How a BI dashboard connects to a data warehouse

---

## What this project does NOT cover (intentionally)

- Delta Live Tables (declarative pipelines) — requires a paid/trial workspace
- Streaming data
- Unity Catalog (access control)
- Job scheduling / automation
