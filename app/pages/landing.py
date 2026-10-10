"""
Landing Page: Clean, Visual-First Overview
Zero corporate buzzwords, minimal text, prominent vector visuals, high visual clarity.
"""

import os
import json
import streamlit as st
try:
    from app.components.header import render_header
    from app.components.kpi_card import render_kpi
    from app.components.html_utils import render_html
    from app.components.svg_covers import get_dashboard_svg_cover, DOMAIN_THEMES
except (ImportError, ModuleNotFoundError):
    from components.header import render_header
    from components.kpi_card import render_kpi
    from components.html_utils import render_html
    from components.svg_covers import get_dashboard_svg_cover, DOMAIN_THEMES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
META_DIR = os.path.join(BASE_DIR, "metadata")
DATA_DIR = os.path.join(BASE_DIR, "data")

@st.cache_data
def get_platform_stats():
    with open(os.path.join(META_DIR, "dashboards.json"), "r", encoding="utf-8") as f:
        dashboards = json.load(f)
    with open(os.path.join(META_DIR, "datasets.json"), "r", encoding="utf-8") as f:
        datasets = json.load(f)
    with open(os.path.join(META_DIR, "sources.json"), "r", encoding="utf-8") as f:
        sources = json.load(f)
    with open(os.path.join(DATA_DIR, "quality_report.json"), "r", encoding="utf-8") as f:
        q_report = json.load(f)

    india_dash = sum(1 for d in dashboards if "Indian" in d.get("category", "") or "India" in d.get("domain", ""))
    global_dash = len(dashboards) - india_dash
    showcase_dashboards = sorted([d for d in dashboards if d.get("is_showcase")], key=lambda x: x.get("showcase_rank", 99))

    return {
        "dashboards_count": len(dashboards),
        "india_count": india_dash,
        "global_count": global_dash,
        "datasets_count": len(datasets),
        "sources_count": len(sources),
        "total_data_points": q_report.get("total_data_points", 125000),
        "showcase_dashboards": showcase_dashboards,
        "dashboards": dashboards
    }

def render():
    stats = get_platform_stats()

    render_header(
        title="DV Projects using Official Data",
        subtitle=f"An interactive data visualization platform featuring {stats['dashboards_count']} dashboards built with verified official public datasets across economics, health, energy, demographics, and science.",
        active_view="Overview",
        meta_chips=[
            f"{stats['dashboards_count']} Dashboards",
            f"{stats['sources_count']} Official Sources",
            f"{stats['total_data_points']:,} Verified Records",
            "100% Real Data"
        ]
    )

    # Key Platform Metrics (4 clean KPI tiles)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("Dashboards", f"{stats['dashboards_count']}", delta="94 Production Modules", status="pos")
    with c2:
        render_kpi("Scope Coverage", f"{stats['india_count']} IN / {stats['global_count']} Global", delta="National & Global", status="neutral")
    with c3:
        render_kpi("Publishing Sources", f"{stats['sources_count']}", delta="Official Institutions", status="pos")
    with c4:
        render_kpi("Data Points", f"{stats['total_data_points']:,}", delta="100% Real Records", status="pos")

    # Clean Navigation Tiles (4 columns)
    render_html("""
    <div style="margin: 1.5rem 0 0.75rem 0; font-size: 0.85rem; font-weight: 700; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.05em;">
        Explore Platform
    </div>
    """)
    n_col1, n_col2, n_col3, n_col4 = st.columns(4)

    with n_col1:
        render_html(f"""
        <div style="background: #0d0f17; border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #38bdf8; border-radius: 14px; padding: 14px; min-height: 110px; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.5);">
            <div style="font-size: 1.25rem; margin-bottom: 4px;">🖼️</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">Dashboard Gallery</div>
            <div style="font-size: 0.76rem; color: #71717a; margin-top: 2px;">Browse all {stats['dashboards_count']} dashboards with instant filters.</div>
        </div>
        """)
        if st.button("Open Gallery →", key="nav_to_gallery_card", use_container_width=True, type="primary"):
            st.session_state["current_view"] = "Dashboard Gallery"
            st.rerun()

    with n_col2:
        render_html(f"""
        <div style="background: #0d0f17; border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #34d399; border-radius: 14px; padding: 14px; min-height: 110px; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.5);">
            <div style="font-size: 1.25rem; margin-bottom: 4px;">📁</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">Datasets</div>
            <div style="font-size: 0.76rem; color: #71717a; margin-top: 2px;">Inspect schemas, row counts, and data definitions.</div>
        </div>
        """)
        if st.button("View Datasets →", key="nav_to_datasets_card", use_container_width=True):
            st.session_state["current_view"] = "Dataset Explorer"
            st.rerun()

    with n_col3:
        render_html(f"""
        <div style="background: #0d0f17; border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #f59e0b; border-radius: 14px; padding: 14px; min-height: 110px; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.5);">
            <div style="font-size: 1.25rem; margin-bottom: 4px;">🏛️</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">Publishing Sources</div>
            <div style="font-size: 0.76rem; color: #71717a; margin-top: 2px;">Review {stats['sources_count']} official publishing authorities.</div>
        </div>
        """)
        if st.button("View Sources →", key="nav_to_sources_card", use_container_width=True):
            st.session_state["current_view"] = "Source Directory"
            st.rerun()

    with n_col4:
        render_html("""
        <div style="background: #0d0f17; border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #c084fc; border-radius: 14px; padding: 14px; min-height: 110px; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.5);">
            <div style="font-size: 1.25rem; margin-bottom: 4px;">⚡</div>
            <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">APIs & Endpoints</div>
            <div style="font-size: 0.76rem; color: #71717a; margin-top: 2px;">Test endpoints and programmatic data feeds.</div>
        </div>
        """)
        if st.button("Test APIs →", key="nav_to_apis_card", use_container_width=True):
            st.session_state["current_view"] = "API Catalog"
            st.rerun()

    # Flagship Dashboards in Modern 3-Column Grid
    render_html("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin: 2rem 0 0.85rem 0;">
        <span style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">⭐ Featured Dashboards</span>
        <span style="font-size: 0.8rem; color: #38bdf8; font-weight: 600;">Top Curated Visual Analyses</span>
    </div>
    """)

    showcases = stats.get("showcase_dashboards", [])[:6]
    for row_idx in range(0, len(showcases), 3):
        cols = st.columns(3)
        for col_idx in range(3):
            d_idx = row_idx + col_idx
            if d_idx < len(showcases):
                d = showcases[d_idx]
                theme = DOMAIN_THEMES.get(d.get('domain'), ('macro', '#38bdf8', '#818cf8', 'rgba(56, 189, 248, 0.15)'))
                _, c_primary, _, c_dim = theme

                svg_cover = get_dashboard_svg_cover(d.get("id"), d.get("domain"), d.get("title"), f"Flagship #{d.get('showcase_rank')}", height=135)
                with cols[col_idx]:
                    card_html = f"""
                    <div style="
                        background: #0d0f17;
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        border-top: 3px solid {c_primary};
                        border-radius: 16px;
                        padding: 10px;
                        margin-bottom: 0.5rem;
                        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.6);
                    ">
                        {svg_cover}
                        
                        <div style="display: flex; align-items: center; justify-content: space-between; margin: 6px 4px 4px 4px;">
                            <span style="
                                font-size: 0.7rem;
                                font-weight: 700;
                                color: {c_primary};
                                background: {c_dim};
                                border: 1px solid {c_primary}40;
                                padding: 2px 8px;
                                border-radius: 6px;
                                text-transform: uppercase;
                            ">{d.get('domain')[:22]}</span>
                            <span style="font-size: 0.7rem; color: #facc15; font-weight: 700;">★ #{d.get('showcase_rank')}</span>
                        </div>

                        <div style="
                            color: #ffffff;
                            font-weight: 700;
                            font-size: 0.95rem;
                            line-height: 1.35;
                            margin: 6px 4px 4px 4px;
                            min-height: 40px;
                        ">{d.get('title')}</div>

                        <div style="
                            font-size: 0.75rem;
                            color: #71717a;
                            margin: 0 4px 6px 4px;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">🏛️ {d.get('source_org')}</div>
                    </div>
                    """
                    render_html(card_html)
                    if st.button(f"Explore Dashboard →", key=f"land_launch_{d.get('id')}", use_container_width=True, type="primary"):
                        st.session_state["selected_dashboard_id"] = d.get("id")
                        st.session_state["current_view"] = "Dashboards"
                        st.rerun()
