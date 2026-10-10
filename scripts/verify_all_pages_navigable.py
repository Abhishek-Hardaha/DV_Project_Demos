"""
Comprehensive Navigation & Page Health Verification Suite
Verifies that all 6 main platform views and all 94 registered dashboards
are fully functional, render with 0 exceptions, and have working navigation links.
"""

import os
import sys
import json
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from streamlit.testing.v1 import AppTest

MAIN_APP_PATH = os.path.join(PROJECT_ROOT, "app", "main.py")
DASHBOARDS_JSON = os.path.join(PROJECT_ROOT, "metadata", "dashboards.json")

def test_all():
    print("======================================================================")
    print("  VERIFYING ALL PAGES & NAVIGATION WORK FLAWLESSLY")
    print("======================================================================")

    with open(DASHBOARDS_JSON, "r", encoding="utf-8") as f:
        dashboards = json.load(f)

    # 1. Test All 6 Top-Level Platform Views
    views = [
        "Landing Page",
        "Dashboard Gallery",
        "Dataset Explorer",
        "Source Directory",
        "API Catalog",
        "Dashboards"
    ]

    print("\n--- 1. Testing Top-Level Platform Views ---")
    for v in views:
        at = AppTest.from_file(MAIN_APP_PATH)
        at.session_state["current_view"] = v
        at.run(timeout=30)
        assert len(at.exception) == 0, f"View '{v}' threw exception: {[e.message for e in at.exception]}"
        print(f"  [PASS] {v} renders cleanly.")

    # 2. Test Deep Navigation Actions
    print("\n--- 2. Testing Deep Navigation Actions ---")
    
    # 2a. Landing -> Gallery
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Landing Page"
    at.run(timeout=30)
    btn_gal = at.button(key="nav_to_gallery_card")
    btn_gal.click().run(timeout=30)
    assert at.session_state["current_view"] == "Dashboard Gallery"
    assert len(at.exception) == 0
    print("  [PASS] Landing -> Dashboard Gallery button navigation")

    # 2b. Landing -> Dataset Explorer
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Landing Page"
    at.run(timeout=30)
    btn_wh = at.button(key="nav_to_datasets_card")
    btn_wh.click().run(timeout=30)
    assert at.session_state["current_view"] == "Dataset Explorer"
    assert len(at.exception) == 0
    print("  [PASS] Landing -> Dataset Explorer button navigation")

    # 2c. Landing -> Source Directory
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Landing Page"
    at.run(timeout=30)
    btn_src = at.button(key="nav_to_sources_card")
    btn_src.click().run(timeout=30)
    assert at.session_state["current_view"] == "Source Directory"
    assert len(at.exception) == 0
    print("  [PASS] Landing -> Source Directory button navigation")

    # 2d. Landing -> API Catalog
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Landing Page"
    at.run(timeout=30)
    btn_api = at.button(key="nav_to_apis_card")
    btn_api.click().run(timeout=30)
    assert at.session_state["current_view"] == "API Catalog"
    assert len(at.exception) == 0
    print("  [PASS] Landing -> API Catalog button navigation")

    # 2e. Gallery -> Open Dashboard
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dashboard Gallery"
    at.run(timeout=30)
    btn_d01 = at.button(key="btn_D01")
    btn_d01.click().run(timeout=30)
    assert at.session_state["current_view"] == "Dashboards"
    assert at.session_state["selected_dashboard_id"] == "D01"
    assert len(at.exception) == 0
    print("  [PASS] Gallery -> Open D01 Dashboard button navigation")

    # 2f. Dataset Explorer -> Open Dashboard
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dataset Explorer"
    at.session_state["selected_dataset_slug"] = "d01_india_macro_gdp"
    at.run(timeout=30)
    btn_launch_ds = at.button(key="launch_from_ds_D01")
    btn_launch_ds.click().run(timeout=30)
    assert at.session_state["current_view"] == "Dashboards"
    assert at.session_state["selected_dashboard_id"] == "D01"
    assert len(at.exception) == 0
    print("  [PASS] Dataset Explorer -> Open D01 Dashboard button navigation")

    # 2g. Dashboard D01 -> Dataset Explorer
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dashboards"
    at.session_state["selected_dashboard_id"] = "D01"
    at.run(timeout=30)
    btn_to_ds = at.button(key="f_nav_ds_d01_india_macro_gdp")
    btn_to_ds.click().run(timeout=30)
    assert at.session_state["current_view"] == "Dataset Explorer"
    assert at.session_state["selected_dataset_slug"] == "d01_india_macro_gdp"
    assert len(at.exception) == 0
    print("  [PASS] Dashboard D01 -> Dataset Explorer deep navigation")

    # 2h. Dashboard D01 -> Source Directory
    at = AppTest.from_file(MAIN_APP_PATH)
    at.session_state["current_view"] = "Dashboards"
    at.session_state["selected_dashboard_id"] = "D01"
    at.run(timeout=30)
    btn_to_src = at.button(key="f_nav_src_d01_india_macro_gdp")
    btn_to_src.click().run(timeout=30)
    assert at.session_state["current_view"] == "Source Directory"
    assert len(at.exception) == 0
    print("  [PASS] Dashboard D01 -> Source Directory deep navigation")

    # 3. Test All 94 Dashboards Render Cleanly
    print(f"\n--- 3. Verifying All {len(dashboards)} Individual Dashboards Render Cleanly ---")
    failed_dashboards = []
    
    t_start = time.time()
    for idx, d in enumerate(dashboards):
        did = d["id"]
        at = AppTest.from_file(MAIN_APP_PATH)
        at.session_state["current_view"] = "Dashboards"
        at.session_state["selected_dashboard_id"] = did
        at.run(timeout=30)
        
        if at.exception:
            err_msg = [e.message for e in at.exception]
            print(f"  [FAIL] {did} ({d['slug']}) failed: {err_msg}")
            failed_dashboards.append((did, d['slug'], err_msg))
        else:
            if (idx + 1) % 20 == 0 or idx == len(dashboards) - 1:
                print(f"  [PASS] Tested {idx + 1} / {len(dashboards)} dashboards... ({did} verified)")

    total_time = round(time.time() - t_start, 2)
    print(f"\nCompleted dashboard render verification in {total_time}s.")

    if failed_dashboards:
        print(f"\n[ERROR] Found {len(failed_dashboards)} failed dashboards:")
        for did, slug, err in failed_dashboards:
            print(f"  - {did} ({slug}): {err}")
        sys.exit(1)
    else:
        print("\n======================================================================")
        print("  ALL 6 PLATFORM PAGES & ALL 94 DASHBOARDS ARE 100% OPERATIONAL & NAVIGABLE!")
        print("======================================================================")

if __name__ == "__main__":
    test_all()
