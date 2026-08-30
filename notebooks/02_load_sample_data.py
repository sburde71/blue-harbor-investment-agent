# Databricks notebook source
# Blue Harbor Investment Research Agent
# Step 2B — Load synthetic sample data into Unity Catalog

CATALOG = "blue_harbor"
RESEARCH_SCHEMA = "research"
PORTFOLIO_SCHEMA = "portfolio"

SEED_VOLUME = f"/Volumes/{CATALOG}/{PORTFOLIO_SCHEMA}/seed_data"
DOC_VOLUME = f"/Volumes/{CATALOG}/{RESEARCH_SCHEMA}/raw_documents"

# COMMAND ----------

# Companies
companies_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{SEED_VOLUME}/companies.csv")
)

(
    companies_df.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable(f"{CATALOG}.{PORTFOLIO_SCHEMA}.companies")
)

# COMMAND ----------

# Funds
funds_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{SEED_VOLUME}/funds.csv")
)

(
    funds_df.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable(f"{CATALOG}.{PORTFOLIO_SCHEMA}.funds")
)

# COMMAND ----------

# Holdings
holdings_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{SEED_VOLUME}/holdings.csv")
)

(
    holdings_df.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable(f"{CATALOG}.{PORTFOLIO_SCHEMA}.holdings")
)

# COMMAND ----------

# Document manifest
manifest_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{SEED_VOLUME}/documents_manifest.csv")
)

(
    manifest_df.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable(f"{CATALOG}.{RESEARCH_SCHEMA}.document_manifest")
)

# COMMAND ----------

# Validation
display(
    spark.sql(f"""
        SELECT
            h.ticker,
            c.company_name,
            ROUND(SUM(h.market_value_usd) / 1000000, 1) AS total_market_value_m
        FROM {CATALOG}.{PORTFOLIO_SCHEMA}.holdings h
        JOIN {CATALOG}.{PORTFOLIO_SCHEMA}.companies c
          ON h.ticker = c.ticker
        GROUP BY h.ticker, c.company_name
        ORDER BY total_market_value_m DESC
    """)
)

# COMMAND ----------

# Check that the 15 source documents exist in the Volume.
display(dbutils.fs.ls(DOC_VOLUME))
