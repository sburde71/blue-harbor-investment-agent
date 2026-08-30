# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Blue Harbor Investment Research Agent
# MAGIC ## Step 1 — Environment Validation
# MAGIC
# MAGIC This notebook is intentionally **read-only**.
# MAGIC It validates the Databricks foundation before we create catalogs,
# MAGIC schemas, volumes, tables, AI Search indexes, tools, or agents.

# COMMAND ----------

from datetime import datetime
import sys
import importlib

print("=" * 78)
print("BLUE HARBOR INVESTMENT RESEARCH AGENT — ENVIRONMENT CHECK")
print(f"Run time: {datetime.now()}")
print("=" * 78)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Identity and current namespace

# COMMAND ----------

identity_df = spark.sql(
    """
    SELECT
      current_user()    AS current_user,
      current_catalog() AS current_catalog,
      current_schema()  AS current_schema,
      current_date()    AS current_date
    """
)
display(identity_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Runtime

# COMMAND ----------

print(f"Python version : {sys.version.split()[0]}")
print(f"Spark version  : {spark.version}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Unity Catalog visibility

# COMMAND ----------

catalogs_df = spark.sql("SHOW CATALOGS")
display(catalogs_df)

catalog_names = [row[0] for row in catalogs_df.collect()]

print("\nVisible catalogs:")
for catalog_name in catalog_names:
    print(f"  - {catalog_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Visible schemas by catalog

# COMMAND ----------

for catalog_name in catalog_names:
    print("\n" + "-" * 78)
    print(f"Catalog: {catalog_name}")
    try:
        schemas_df = spark.sql(f"SHOW SCHEMAS IN `{catalog_name}`")
        for row in schemas_df.collect():
            print(f"  - {row[0]}")
    except Exception as exc:
        print(f"  Could not inspect schemas: {exc}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Unity Catalog Volume path visibility

# COMMAND ----------

try:
    volume_root = dbutils.fs.ls("/Volumes")
    print("✅ /Volumes is accessible.")
    print(f"Visible root entries: {len(volume_root)}")
except Exception as exc:
    print("⚠️ /Volumes root could not be listed.")
    print(f"Reason: {exc}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Core package availability
# MAGIC
# MAGIC Missing optional AI packages are **not a failure** at this stage.

# COMMAND ----------

packages_to_check = {
    "mlflow": "MLflow",
    "databricks.sdk": "Databricks SDK",
    "openai": "OpenAI SDK",
    "databricks.vector_search": "Databricks AI Search SDK",
}

package_results = {}

for module_name, display_name in packages_to_check.items():
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "version not exposed")
        package_results[display_name] = True
        print(f"✅ {display_name}: {version}")
    except Exception:
        package_results[display_name] = False
        print(f"ℹ️ {display_name}: not currently available")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Databricks Workspace SDK authentication

# COMMAND ----------

workspace_client_ok = False

try:
    from databricks.sdk import WorkspaceClient

    workspace_client = WorkspaceClient()
    me = workspace_client.current_user.me()
    workspace_client_ok = True

    print("✅ WorkspaceClient authentication succeeded.")
    print(f"Workspace identity: {getattr(me, 'user_name', 'available')}")
except Exception as exc:
    print("⚠️ WorkspaceClient authentication check did not succeed.")
    print(f"Reason: {exc}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Final summary

# COMMAND ----------

print("\n" + "=" * 78)
print("ENVIRONMENT VALIDATION SUMMARY")
print("=" * 78)

print("Spark execution        : ✅")
print(f"Unity Catalog visible  : {'✅' if catalog_names else '❌'}")
print(f"MLflow                 : {'✅' if package_results.get('MLflow') else 'ℹ️'}")
print(f"Databricks SDK         : {'✅' if package_results.get('Databricks SDK') else 'ℹ️'}")
print(f"WorkspaceClient auth   : {'✅' if workspace_client_ok else '⚠️'}")
print(f"OpenAI SDK             : {'✅' if package_results.get('OpenAI SDK') else 'ℹ️ later'}")
print(f"AI Search SDK          : {'✅' if package_results.get('Databricks AI Search SDK') else 'ℹ️ later'}")

print(
    "\nNo Blue Harbor catalogs, schemas, volumes, tables, indexes, "
    "tools, or agents were created by this notebook."
)