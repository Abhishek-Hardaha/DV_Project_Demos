"""
Unit Test: Dashboard Visual Density & Module Imports
Verifies that all 34 dashboards import, contain render(), and meet visual density requirements (>=10 visuals).
"""

import os
import sys
import glob
import importlib
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def test_dashboard_modules_count():
    dash_files = [f for f in glob.glob(os.path.join(PROJECT_ROOT, "dashboards", "*.py")) if not f.endswith("__init__.py")]
    assert len(dash_files) >= 94, f"Expected 94 dashboards, found {len(dash_files)}"

def test_dashboard_visual_density():
    dash_files = [f for f in glob.glob(os.path.join(PROJECT_ROOT, "dashboards", "*.py")) if not f.endswith("__init__.py")]
    for f in dash_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        kpis = content.count("render_kpi(")
        charts = content.count("st.plotly_chart(")
        tables = content.count("st.dataframe(")
        total_visuals = kpis + charts + tables
        assert total_visuals >= 10, f"Dashboard {f} has only {total_visuals} visuals (< 10 required)."

def test_dashboard_render_function():
    dash_files = sorted([f for f in glob.glob(os.path.join(PROJECT_ROOT, "dashboards", "*.py")) if not f.endswith("__init__.py")])
    for f in dash_files:
        mod_name = os.path.basename(f)[:-3]
        mod = importlib.import_module(f"dashboards.{mod_name}")
        assert hasattr(mod, "render"), f"Dashboard {mod_name} lacks render() function."
