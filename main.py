"""
Data Visualization Intelligence Suite - Root Entrypoint Proxy
Ensures seamless launch from root via `streamlit run main.py` or `streamlit run app/main.py`.
"""

import os
import sys
import runpy

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APP_DIR = os.path.join(PROJECT_ROOT, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Execute the application entrypoint
if __name__ == "__main__":
    runpy.run_path(os.path.join(APP_DIR, "main.py"), run_name="__main__")
