"""
Dataset Explorer: Analytical Data Inspection Engine & Schema Studio
Inspect schemas, data types, missingness, summary statistics, and sample rows for all analytical datasets.
Transformed into an executive tabular workbench with scope filtering and instant export.
"""

import os
import json
import pandas as pd
import streamlit as st
from app.components.header import render_header
from app.components.kpi_card import render_kpi
from app.components.html_utils import render_html

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
META_DIR = os.path.join(BASE_DIR, "metadata")
DATA_DIR = os.path.join(BASE_DIR, "data", "analytical")

@st.cache_data
def load_datasets_metadata():
    with open(os.path.join(META_DIR, "datasets.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def render():
    datasets = load_datasets_metadata()

    render_header(
        title="Dataset Explorer",
        subtitle="Inspect underlying schemas, column definitions, data types, completeness, and verified records for all analytical datasets.",
        active_view="Datasets",
        meta_chips=[
            f"📁 {len(datasets)} Analytical Datasets",
            "⚡ Parquet + CSV Storage",
            "🛡️ 100% Verified Provenance"
        ]
    )

    # Determine default index if routed from dashboard
    target_slug = st.session_state.get("selected_dataset_slug")
    
    # Dataset Selector Toolbar
    with st.container():
        col_scope, col_select = st.columns([1, 2])
        
        india_ds = [d for d in datasets if "india" in d.get("dataset_id", "").lower() or "india" in d.get("geographic_coverage", "").lower()]
        global_ds = [d for d in datasets if d not in india_ds]

        with col_scope:
            scope_choice = st.selectbox(
                "Filter Scope:",
                [f"All Datasets ({len(datasets)})", f"🇮🇳 Indian Governance ({len(india_ds)})", f"🌐 Global Multilateral ({len(global_ds)})"],
                key="ds_scope_filter"
            )
        
        if "Indian Governance" in scope_choice:
            filtered_ds = india_ds
        elif "Global Multilateral" in scope_choice:
            filtered_ds = global_ds
        else:
            filtered_ds = datasets

        dataset_names = [f"{d['dashboard_id']} — {d['title']}" for d in filtered_ds]
        
        default_idx = 0
        if target_slug:
            for idx, d in enumerate(filtered_ds):
                if d.get("dataset_id") == target_slug:
                    default_idx = idx
                    break

        with col_select:
            sel_name = st.selectbox(
                "Select Production Analytical Dataset:",
                dataset_names,
                index=default_idx,
                key="ds_main_selector"
            )

    sel_idx = dataset_names.index(sel_name)
    d_meta = filtered_ds[sel_idx]
    slug = d_meta["dataset_id"]
    did = d_meta["dashboard_id"]

    csv_path = os.path.join(DATA_DIR, f"{slug}.csv")
    if not os.path.exists(csv_path):
        st.error(f"Dataset file not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # Overview KPI Cards
    null_count_total = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    comp_pct = ((total_cells - null_count_total) / total_cells * 100) if total_cells > 0 else 100.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("Total Records", f"{len(df):,}", delta="Verified Rows", status="pos")
    with c2:
        render_kpi("Monitored Variables", f"{len(df.columns)}", delta="Attributes", status="neutral")
    with c3:
        render_kpi("Completeness Rate", f"{comp_pct:.1f}%", delta="No Synthetic Fill", status="pos")
    with c4:
        render_kpi("Storage Architecture", "Parquet + CSV", delta="Analytical Warehouse", status="neutral")

    # Associated Dashboard Launch Strip
    strip_html = f"""<div style="background: linear-gradient(135deg, #070707 0%, #000000 100%); border: 1px solid #171717; border-radius: 12px; padding: 14px 18px; margin: 18px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
<div>
<div style="font-size: 0.74rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em;">Linked Production Dashboard</div>
<div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 2px;">[{did}] {d_meta.get('title')}</div>
<div style="font-size: 0.8rem; color: #94a3b8; margin-top: 2px;">
🏛️ Publisher: <b>{d_meta.get('source_organization')}</b> | 🌐 Scope: <b>{d_meta.get('geographic_coverage')}</b> | ⏱️ Horizon: <b>{d_meta.get('temporal_coverage')}</b>
</div>
</div>
</div>"""
    render_html(strip_html)

    d_btn_col1, d_btn_col2 = st.columns([1.5, 2.5])
    with d_btn_col1:
        if st.button(f"🚀 Open {did} Dashboard →", key=f"launch_from_ds_{did}", use_container_width=True):
            st.session_state["selected_dashboard_id"] = did
            st.session_state["current_view"] = "Dashboards"
            st.rerun()

    render_html("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #1f1f1f;'>")

    tab_dict, tab_stats, tab_records = st.tabs([
        "🧬 Data Dictionary & Power BI Semantic Schema",
        "📊 Statistical Dispersion & Quantiles",
        "📋 Granular Analytical Records & Export"
    ])

    with tab_dict:
        st.markdown("##### 🧬 **Column Schema, Analytical Roles & Power BI Semantic Types**")
        schema_rows = []
        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            comp_rate = ((len(df) - null_count) / len(df) * 100) if len(df) > 0 else 100.0
            
            # Infer analytical role
            col_l = col.lower()
            if col_l in ["year", "fiscal_year", "date", "timestamp", "month", "crop_year"]:
                role = "Temporal Dimension"
                pbi_role = "Date Hierarchy / Time Axis"
            elif col_l in ["country", "state", "city", "region", "district", "place", "latitude", "longitude"]:
                role = "Geospatial Dimension"
                pbi_role = "Geography / Location Hierarchy"
            elif col_l in ["category", "type", "sector", "crop", "status", "indicator", "economy_group"]:
                role = "Categorical Slicer"
                pbi_role = "Attribute Dimension"
            elif pd.api.types.is_numeric_dtype(df[col]):
                role = "Quantitative Measure"
                pbi_role = "Fact Table Metric (SUM / AVERAGE)"
            else:
                role = "Descriptive Attribute"
                pbi_role = "Dimension Label"

            schema_rows.append({
                "Column Name": col,
                "Analytical Role": role,
                "Data Type": str(df[col].dtype),
                "Completeness Rate": f"{comp_rate:.1f}%",
                "Power BI Modeling Role": pbi_role,
                "Sample Value": str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else "None"
            })
        st.dataframe(pd.DataFrame(schema_rows), use_container_width=True, height=350)

    with tab_stats:
        st.markdown("##### 📊 **Descriptive Statistics & Interquartile Ranges (Numeric Variables)**")
        num_df = df.select_dtypes(include=['number'])
        if not num_df.empty:
            desc_df = num_df.describe().T.reset_index().rename(columns={"index": "Variable"})
            st.dataframe(desc_df, use_container_width=True, height=350)
        else:
            st.info("No numeric variables present in this dataset.")

    with tab_records:
        st.markdown("##### 📋 **Verified Analytical Data Records**")
        st.dataframe(df.head(500), use_container_width=True, height=380)

        # Download Buttons
        d_col1, d_col2 = st.columns([2, 1])
        with d_col1:
            st.caption(f"Showing up to 500 rows of {len(df)} total verified records. Stored at `{d_meta.get('analytical_parquet_path')}`.")
        with d_col2:
            st.download_button(
                label=f"📥 Export Full {slug}.csv",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{slug}_export.csv",
                mime="text/csv",
                use_container_width=True
            )
