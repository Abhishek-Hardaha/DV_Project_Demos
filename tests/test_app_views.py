"""
Integration Test: End-to-End Streamlit App Views and Dashboard Execution
Uses streamlit.testing.v1.AppTest to execute the entire app across views and dashboards.
"""

import os
import sys
import pytest
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

MAIN_APP_PATH = os.path.join(PROJECT_ROOT, "app", "main.py")

def test_landing_page_renders_cleanly():
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Landing Page"
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Landing page threw exceptions: {[e.value for e in at.exception]}"

def test_dashboard_gallery_renders_cleanly():
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dashboard Gallery"
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Gallery view threw exceptions: {[e.value for e in at.exception]}"

def test_dataset_explorer_renders_cleanly():
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dataset Explorer"
    at.session_state["selected_dataset_slug"] = "d35_india_gst_collections"
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Dataset Explorer threw exceptions: {[e.value for e in at.exception]}"

def test_source_directory_renders_cleanly():
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Source Directory"
    at.session_state["selected_source_name"] = "Goods and Services Tax Network (GSTN) / MoF"
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Source Directory threw exceptions: {[e.value for e in at.exception]}"

def test_api_catalog_renders_cleanly():
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "API Catalog"
    at.run(timeout=30)
    assert len(at.exception) == 0, f"API Catalog threw exceptions: {[e.value for e in at.exception]}"

@pytest.mark.parametrize("dashboard_id", [
    "D01", "D06", "D11", "D16", "D28", "D34", "D35", "D40", "D46", "D54", "D55", "D58", "D61", "D65", "D74", "D75", "D80", "D85", "D90", "D94"
])
def test_sample_dashboards_render_via_app(dashboard_id):
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dashboards"
    at.session_state["selected_dashboard_id"] = dashboard_id
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Dashboard {dashboard_id} threw exceptions: {[e.value for e in at.exception]}"
