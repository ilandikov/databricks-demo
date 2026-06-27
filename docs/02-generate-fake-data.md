# Step 2 — Generate Fake Sales Data

## Do this

1. The notebook is already in your repo at `notebooks/generate_sales_data.py`. Commit and push it to GitHub.

2. In Databricks, open **Workspace** → your username → the linked Git folder → `notebooks/` → `generate_sales_data`. Databricks renders the `.py` file as a notebook automatically.

3. Attach a cluster: click **Connect** in the top right and select the available cluster. If no cluster is running, Databricks will start one (takes ~2 minutes).

4. Run cell 1 (the data generation). You should see 5 rows printed — one per sale.

5. Run cell 2 (the file save). You should see `Saved to /FileStore/sales.csv`.

6. Run cell 3 (the verification). You should see `sales.csv` in the file list.

## You are done with Step 2 when

- 5 rows printed in cell 1
- `sales.csv` appears in `/FileStore/` in cell 3

## Next

Step 3 — load `sales.csv` into a Delta table using PySpark.
