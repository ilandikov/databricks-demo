# Step 1 — Workspace Orientation

## Do this

1. Open your Databricks workspace in the browser.

2. In the left sidebar, click **Compute** → **SQL Warehouses**. If your warehouse shows "Stopped", click **Start** and wait for it to turn green.

3. In the left sidebar, click **SQL Editor**. In the query box, type:
   ```sql
   SELECT 1
   ```
   Click **Run**. You should see `1` in the results. This confirms your SQL Warehouse is working.

4. In the left sidebar, click **New** → **Notebook**. Set the default language to **Python**. Click **Create**. A blank notebook opens with one empty cell.

5. In the first cell, type:
   ```python
   print("hello")
   ```
   Click **Run cell** (the play button on the left of the cell). You should see `hello` printed below the cell.

6. Close the notebook. You don't need to save it.

## You are done with Step 1 when

- SQL Warehouse is running (green status)
- `SELECT 1` returned a result in SQL Editor
- `print("hello")` ran successfully in a notebook

## Git setup (done)

7. Created a local git repo in the project folder and pushed to `https://github.com/ilandikov/databricks-demo.git`.

8. Connected the GitHub repo to Databricks:
   - Workspace → username folder → kebab menu (⋮) → **Add** → **Git folder**
   - Repo URL: `https://github.com/ilandikov/databricks-demo.git`, branch: `main`

Any `.py` file pushed to `notebooks/` now appears as a runnable notebook in Databricks automatically.

## Next

Step 2 — generate the fake sales CSV with Python.
