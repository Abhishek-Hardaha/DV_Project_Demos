"""
Unit Test: Metadata Registries & Power BI Models
Verifies metadata consistency across dashboards, datasets, and sources.
"""

import os
import json
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_DIR = os.path.join(PROJECT_ROOT, "metadata")

def test_dashboards_metadata():
    with open(os.path.join(META_DIR, "dashboards.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 94
    for d in data:
        assert "id" in d and "title" in d and "domain" in d and "source_org" in d
        assert len(d.get("kpis", [])) >= 3

def test_sources_metadata():
    with open(os.path.join(META_DIR, "sources.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 20
    for s in data:
        assert "name" in s and "url" in s and "tier" in s

def test_powerbi_models_metadata():
    with open(os.path.join(META_DIR, "powerbi", "powerbi_models.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 94
    for did, model in data.items():
        assert "fact_table" in model and "dax_measures" in model
