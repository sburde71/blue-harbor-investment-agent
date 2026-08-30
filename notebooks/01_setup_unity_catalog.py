# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Blue Harbor Investment Research Agent
# MAGIC ## Step 2 — Unity Catalog Foundation
# MAGIC
# MAGIC Creates the initial governed namespace for the POC inside the
# MAGIC Databricks Free Edition `workspace` catalog.

# COMMAND ----------

CATALOG = "workspace"

RESEARCH_SCHEMA = "blue_harbor_research"
PORTFOLIO_SCHEMA = "blue_harbor_portfolio"
AGENT_SCHEMA = "blue_harbor_agent"

RAW_DOCUMENTS_VOLUME = "raw_documents"
SEED_DATA_VOLUME = "seed_data"
SEMI_STRUCTURED_VOLUME = "semi_structured"

print("Target Unity Catalog namespace:")
print(f"  {CATALOG}.{RESEARCH_SCHEMA}")
print(f"  {CATALOG}.{PORTFOLIO_SCHEMA}")
print(f"  {CATALOG}.{AGENT_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Create project schemas

# COMMAND ----------

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS {CATALOG}.{RESEARCH_SCHEMA}
COMMENT 'Blue Harbor research documents, parsed content, chunks, and retrieval assets'
""")

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS {CATALOG}.{PORTFOLIO_SCHEMA}
COMMENT 'Blue Harbor synthetic portfolio, fund, market, and analyst-model data'
""")

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS {CATALOG}.{AGENT_SCHEMA}
COMMENT 'Blue Harbor agent tools, evaluation assets, and operational objects'
""")

print("✅ Schemas created or already present.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Create managed Volumes

# COMMAND ----------

spark.sql(f"""
CREATE VOLUME IF NOT EXISTS {CATALOG}.{RESEARCH_SCHEMA}.{RAW_DOCUMENTS_VOLUME}
COMMENT 'Raw synthetic earnings reports, transcripts, filings, analyst notes, HTML, and TXT documents'
""")

spark.sql(f"""
CREATE VOLUME IF NOT EXISTS {CATALOG}.{PORTFOLIO_SCHEMA}.{SEED_DATA_VOLUME}
COMMENT 'Structured seed files such as companies, funds, holdings, prices, and guidance history'
""")

spark.sql(f"""
CREATE VOLUME IF NOT EXISTS {CATALOG}.{PORTFOLIO_SCHEMA}.{SEMI_STRUCTURED_VOLUME}
COMMENT 'Synthetic Excel analyst models and portfolio workbooks'
""")

print("✅ Managed volumes created or already present.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Define runtime paths

# COMMAND ----------

RAW_DOCUMENTS_PATH = f"/Volumes/{CATALOG}/{RESEARCH_SCHEMA}/{RAW_DOCUMENTS_VOLUME}"
SEED_DATA_PATH = f"/Volumes/{CATALOG}/{PORTFOLIO_SCHEMA}/{SEED_DATA_VOLUME}"
SEMI_STRUCTURED_PATH = f"/Volumes/{CATALOG}/{PORTFOLIO_SCHEMA}/{SEMI_STRUCTURED_VOLUME}"

print(f"Raw documents   : {RAW_DOCUMENTS_PATH}")
print(f"Seed data       : {SEED_DATA_PATH}")
print(f"Semi-structured : {SEMI_STRUCTURED_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Validate schemas

# COMMAND ----------

display(spark.sql(f"SHOW SCHEMAS IN {CATALOG}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Validate volumes

# COMMAND ----------

display(spark.sql(f"SHOW VOLUMES IN {CATALOG}.{RESEARCH_SCHEMA}"))
display(spark.sql(f"SHOW VOLUMES IN {CATALOG}.{PORTFOLIO_SCHEMA}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Validate file-system paths

# COMMAND ----------

for path in [RAW_DOCUMENTS_PATH, SEED_DATA_PATH, SEMI_STRUCTURED_PATH]:
    try:
        files = dbutils.fs.ls(path)
        print(f"✅ Accessible: {path} ({len(files)} file(s))")
    except Exception as exc:
        print(f"❌ Could not access: {path}")
        print(exc)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Final checkpoint
# MAGIC
# MAGIC Expected layout:
# MAGIC
# MAGIC ```
# MAGIC workspace
# MAGIC ├── blue_harbor_research
# MAGIC │   └── raw_documents
# MAGIC ├── blue_harbor_portfolio
# MAGIC │   ├── seed_data
# MAGIC │   └── semi_structured
# MAGIC └── blue_harbor_agent
# MAGIC ```
# MAGIC
# MAGIC No Delta tables, AI Search indexes, Genie spaces, MCP servers,
# MAGIC or agents are created yet.

# COMMAND ----------

print("=" * 78)
print("BLUE HARBOR UNITY CATALOG FOUNDATION READY")
print("=" * 78)
print(f"Catalog          : {CATALOG}")
print(f"Research schema  : {CATALOG}.{RESEARCH_SCHEMA}")
print(f"Portfolio schema : {CATALOG}.{PORTFOLIO_SCHEMA}")
print(f"Agent schema     : {CATALOG}.{AGENT_SCHEMA}")
print()
print("Next step: upload the GitHub seed files into these managed Volumes.")