# Blue Harbor Investment Research Agent — POC Starter Data

All companies, funds, earnings information, and holdings are fictional and synthetic.

## What is included

- `sample_documents/` — 15 Q2 2026 research documents:
  - 5 earnings reports
  - 5 earnings-call transcripts
  - 5 analyst notes
- `catalog_data/companies.csv`
- `catalog_data/funds.csv`
- `catalog_data/holdings.csv`
- `catalog_data/documents_manifest.csv`
- `evals/evaluation_questions.jsonl`
- `evals/GROUND_TRUTH_DO_NOT_INDEX.md`
- `setup/01_create_catalog.sql`
- `notebooks/02_load_sample_data.py`

## Primary POC question

> Which companies lowered their outlook in Q2 2026, and how much do we own of them across all Blue Harbor funds?

The dataset is intentionally designed so the answer cannot be obtained from a single source:
1. Read/search the earnings documents to determine which companies lowered guidance.
2. Query structured holdings to determine Blue Harbor's exposure.
3. Combine both results in the agent response with citations.

## Upload layout

Run `setup/01_create_catalog.sql`.

Upload `sample_documents/*.md` to:

`/Volumes/blue_harbor/research/raw_documents/`

Upload the four CSV files under `catalog_data/` to:

`/Volumes/blue_harbor/portfolio/seed_data/`

Then run `notebooks/02_load_sample_data.py`.

## Expected structured tables

- `blue_harbor.portfolio.companies`
- `blue_harbor.portfolio.funds`
- `blue_harbor.portfolio.holdings`
- `blue_harbor.research.document_manifest`

Do NOT upload `evals/GROUND_TRUTH_DO_NOT_INDEX.md` into the research Volume or AI Search index.
