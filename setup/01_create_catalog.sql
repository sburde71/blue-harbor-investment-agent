-- Blue Harbor Investment Research Agent — Unity Catalog setup
-- If your Free Edition workspace does not allow CREATE CATALOG,
-- replace `blue_harbor` below with an existing catalog you own.

CREATE CATALOG IF NOT EXISTS blue_harbor;

CREATE SCHEMA IF NOT EXISTS blue_harbor.research;
CREATE SCHEMA IF NOT EXISTS blue_harbor.portfolio;
CREATE SCHEMA IF NOT EXISTS blue_harbor.agent;

CREATE VOLUME IF NOT EXISTS blue_harbor.research.raw_documents;
CREATE VOLUME IF NOT EXISTS blue_harbor.portfolio.seed_data;

-- After running this:
-- 1) Upload all sample_documents/*.md to:
--    /Volumes/blue_harbor/research/raw_documents/
-- 2) Upload catalog_data/companies.csv, funds.csv, holdings.csv,
--    and documents_manifest.csv to:
--    /Volumes/blue_harbor/portfolio/seed_data/
