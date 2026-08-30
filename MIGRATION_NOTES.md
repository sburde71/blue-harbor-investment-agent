# Repository Structure Migration Notes

This ZIP contains the recommended folder structure only.

## Keep from your existing repository

- Your current `README.md`
- Your Databricks-style target architecture image
- Any GitHub metadata you already created

## Copy the expanded dataset into these folders

From the expanded Blue Harbor dataset:

- `data/documents/*` → `data/documents/`
- `data/seed/*` → `data/seed/`
- `data/semi_structured/*` → `data/semi_structured/`
- `evals/*` → `evals/`
- `security_test_documents/*` → `security_test_documents/`
- `docs/DATASET_GUIDE.md` → `docs/DATASET_GUIDE.md`

## Important

Do not index:
- `evals/GROUND_TRUTH_DO_NOT_INDEX.md`
- anything under `security_test_documents/` until the security-testing phase.

The `.gitkeep` files exist so GitHub preserves empty directories. Remove a `.gitkeep`
once the directory contains real files.
