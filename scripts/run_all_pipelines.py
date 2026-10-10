"""
Master Execution Pipeline: End-to-End Ingestion, Transformation & Validation
Orchestrates:
1. Data Ingestion (pipelines/ingestion/)
2. Deterministic Transformation (pipelines/transformation/)
3. Quality & Authenticity Audit (pipelines/validation/)
4. Metadata & Power BI Models Generation (pipelines/generate_metadata.py)
5. Master Suite Audit Gate (scripts/audit_suite.py)
"""

import sys
import subprocess
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_step(desc, cmd):
    print("\n" + "=" * 60)
    print(f"  STEP: {desc}")
    print("=" * 60)
    res = subprocess.run([sys.executable] + cmd, cwd=PROJECT_ROOT)
    if res.returncode != 0:
        print(f"Error in step: {desc} (code {res.returncode})")
        return False
    return True

def main():
    print("============================================================")
    print("  LAUNCHING FULL DATA VISUALIZATION REPRODUCIBLE PIPELINE")
    print("============================================================")

    steps = [
        ("Ingest Indian Government Datasets", ["pipelines/ingestion/fetch_india_govt_data.py"]),
        ("Ingest Live & Dynamic APIs", ["pipelines/ingestion/fetch_live_apis.py"]),
        ("Ingest Global Multilateral Datasets", ["pipelines/ingestion/fetch_global_datasets.py"]),
        ("Execute Deterministic Transformations", ["pipelines/transformation/transform_all.py"]),
        ("Execute Data Quality Scorecard Audit", ["pipelines/validation/validate_all.py"]),
        ("Generate Metadata Registries & Power BI Models", ["pipelines/generate_metadata.py"]),
        ("Generate Machine-Readable Evidence Registry", ["pipelines/generate_evidence_registry.py"]),
        ("Run Master Automated Audit Gate", ["scripts/audit_suite.py"])
    ]

    for desc, cmd in steps:
        if not run_step(desc, cmd):
            print("\nPipeline stopped due to error.")
            sys.exit(1)

    print("\n============================================================")
    print("  ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
    print("  Launch platform: streamlit run app/main.py")
    print("============================================================")

if __name__ == "__main__":
    main()
