"""
Data Visualization Intelligence Suite - Streamlit Cloud Entrypoint
Allows Streamlit Community Cloud to boot directly from repository root.
"""

import os
import sys

# Ensure repository root and app directory are present at the head of sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APP_DIR = os.path.join(PROJECT_ROOT, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import runpy

if __name__ == "__main__":
    runpy.run_path(os.path.join(APP_DIR, "main.py"), run_name="__main__")
