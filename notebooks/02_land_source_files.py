# Databricks notebook source
# MAGIC %md
# MAGIC # Blue Harbor Investment Research Agent
# MAGIC ## Step 3 — Controlled Data Landing
# MAGIC
# MAGIC This notebook copies the synthetic source data from the Databricks Git folder
# MAGIC into governed Unity Catalog Volumes.
# MAGIC
# MAGIC **Copied**
# MAGIC - `data/documents/` → research raw-documents Volume
# MAGIC - `data/seed/` → portfolio seed-data Volume
# MAGIC - `data/semi_structured/` → portfolio semi-structured Volume
# MAGIC
# MAGIC **Intentionally NOT copied**
# MAGIC - `evals/GROUND_TRUTH_DO_NOT_INDEX.md`
# MAGIC - `security_test_documents/`
# MAGIC
# MAGIC The notebook preserves the source folder hierarchy and validates the landing counts.

# COMMAND ----------

from pathlib import Path
import os
import shutil
from collections import Counter

CATALOG = "workspace"
RESEARCH_SCHEMA = "blue_harbor_research"
PORTFOLIO_SCHEMA = "blue_harbor_portfolio"

RAW_DOCUMENTS_PATH = Path(
    f"/Volumes/{CATALOG}/{RESEARCH_SCHEMA}/raw_documents"
)
SEED_DATA_PATH = Path(
    f"/Volumes/{CATALOG}/{PORTFOLIO_SCHEMA}/seed_data"
)
SEMI_STRUCTURED_PATH = Path(
    f"/Volumes/{CATALOG}/{PORTFOLIO_SCHEMA}/semi_structured"
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Resolve the Git repository root
# MAGIC
# MAGIC In current Databricks runtimes, the working directory for a notebook is
# MAGIC normally the directory containing the notebook. Because this notebook lives
# MAGIC in `notebooks/`, the repository root is its parent directory.

# COMMAND ----------

NOTEBOOK_DIR = Path(os.getcwd()).resolve()
REPO_ROOT = NOTEBOOK_DIR.parent

print(f"Notebook directory : {NOTEBOOK_DIR}")
print(f"Repository root    : {REPO_ROOT}")

expected_repo_folders = [
    REPO_ROOT / "data" / "documents",
    REPO_ROOT / "data" / "seed",
    REPO_ROOT / "data" / "semi_structured",
]

missing = [str(path) for path in expected_repo_folders if not path.exists()]

if missing:
    raise FileNotFoundError(
        "Expected Git-repository folders were not found:\n"
        + "\n".join(missing)
        + "\n\nIf this notebook is not under <repo>/notebooks/, "
          "set REPO_ROOT manually to the repository root."
    )

print("✅ Git repository data folders found.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Inspect the source dataset before copying

# COMMAND ----------

DOCUMENT_SOURCE = REPO_ROOT / "data" / "documents"
SEED_SOURCE = REPO_ROOT / "data" / "seed"
SEMI_STRUCTURED_SOURCE = REPO_ROOT / "data" / "semi_structured"

document_files = [p for p in DOCUMENT_SOURCE.rglob("*") if p.is_file()]
seed_files = [p for p in SEED_SOURCE.rglob("*") if p.is_file()]
semi_structured_files = [p for p in SEMI_STRUCTURED_SOURCE.rglob("*") if p.is_file()]

print(f"Research documents found : {len(document_files)}")
print(f"Seed files found         : {len(seed_files)}")
print(f"Semi-structured files    : {len(semi_structured_files)}")

extension_counts = Counter(
    path.suffix.lower() if path.suffix else "<no extension>"
    for path in document_files
)

print("\nResearch document formats:")
for extension, count in sorted(extension_counts.items()):
    print(f"  {extension:8} {count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Copy helper
# MAGIC
# MAGIC Standard Python file APIs are used so the source workspace files and
# MAGIC destination Unity Catalog Volume paths are handled as normal file-system paths.

# COMMAND ----------

def copy_tree(source: Path, destination: Path) -> list[Path]:
    """
    Copy all files below `source` to `destination`, preserving relative paths.
    Existing files with the same path are replaced.
    """
    copied_files = []

    destination.mkdir(parents=True, exist_ok=True)

    for source_file in source.rglob("*"):
        if not source_file.is_file():
            continue

        relative_path = source_file.relative_to(source)
        destination_file = destination / relative_path

        destination_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, destination_file)

        copied_files.append(destination_file)

    return copied_files

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Land the research documents

# COMMAND ----------

copied_documents = copy_tree(
    DOCUMENT_SOURCE,
    RAW_DOCUMENTS_PATH
)

print(f"✅ Copied {len(copied_documents)} research documents.")
print(f"Destination: {RAW_DOCUMENTS_PATH}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Land the structured seed files

# COMMAND ----------

copied_seed_files = copy_tree(
    SEED_SOURCE,
    SEED_DATA_PATH
)

print(f"✅ Copied {len(copied_seed_files)} seed files.")
print(f"Destination: {SEED_DATA_PATH}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Land the semi-structured Excel files

# COMMAND ----------

copied_semi_structured_files = copy_tree(
    SEMI_STRUCTURED_SOURCE,
    SEMI_STRUCTURED_PATH
)

print(f"✅ Copied {len(copied_semi_structured_files)} semi-structured files.")
print(f"Destination: {SEMI_STRUCTURED_PATH}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Validate landed research corpus

# COMMAND ----------

landed_documents = [
    p for p in RAW_DOCUMENTS_PATH.rglob("*")
    if p.is_file()
]

landed_extension_counts = Counter(
    path.suffix.lower() if path.suffix else "<no extension>"
    for path in landed_documents
)

print(f"Landed research documents: {len(landed_documents)}")

for extension, count in sorted(landed_extension_counts.items()):
    print(f"  {extension:8} {count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. Validate portfolio source files

# COMMAND ----------

landed_seed_files = [
    p for p in SEED_DATA_PATH.rglob("*")
    if p.is_file()
]

landed_semi_structured_files = [
    p for p in SEMI_STRUCTURED_PATH.rglob("*")
    if p.is_file()
]

print("Seed files:")
for path in sorted(landed_seed_files):
    print(f"  - {path.name}")

print("\nSemi-structured files:")
for path in sorted(landed_semi_structured_files):
    print(f"  - {path.name}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 9. Safety validation
# MAGIC
# MAGIC Evaluation ground truth and security-test documents must remain outside the
# MAGIC normal research corpus.

# COMMAND ----------

forbidden_names = {
    "GROUND_TRUTH_DO_NOT_INDEX.md",
    "DO_NOT_INDEX_UNTIL_SECURITY_PHASE_prompt_injection_test.txt",
}

accidentally_landed = [
    str(path)
    for path in RAW_DOCUMENTS_PATH.rglob("*")
    if path.is_file() and path.name in forbidden_names
]

if accidentally_landed:
    raise RuntimeError(
        "❌ Safety check failed. Restricted evaluation/security files were "
        "found in the research Volume:\n"
        + "\n".join(accidentally_landed)
    )

print("✅ Ground-truth and security-test files are NOT in the research corpus.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 10. Optional manifest sanity check
# MAGIC
# MAGIC We only inspect the document manifest here. We do not create Delta tables yet.

# COMMAND ----------

manifest_path = SEED_DATA_PATH / "document_manifest.csv"

if manifest_path.exists():
    manifest_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(manifest_path))
    )

    print(f"Manifest rows: {manifest_df.count()}")
    display(
        manifest_df.select(
            "ticker",
            "document_type",
            "source_type",
            "file_name"
        ).orderBy(
            "ticker",
            "document_type"
        )
    )
else:
    print("⚠️ document_manifest.csv was not found.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 11. Final landing summary

# COMMAND ----------

print("\n" + "=" * 78)
print("BLUE HARBOR CONTROLLED DATA LANDING COMPLETE")
print("=" * 78)

print(f"Research documents landed : {len(landed_documents)}")
print(f"Structured seed files     : {len(landed_seed_files)}")
print(f"Semi-structured files     : {len(landed_semi_structured_files)}")

print("\nRuntime locations:")
print(f"Research : {RAW_DOCUMENTS_PATH}")
print(f"Seed     : {SEED_DATA_PATH}")
print(f"Excel    : {SEMI_STRUCTURED_PATH}")

print("""
No Delta tables were created.
No documents were parsed.
No chunks or embeddings were created.
No AI Search index was created.
No agent or Genie resource was created.

Next step: profile the landed files and create the structured Delta foundation.
""")
