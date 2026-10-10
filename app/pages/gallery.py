"""
Dashboard Gallery: Modern, Visual-First Card Catalog
Minimal text, prominent vector visuals, domain-specific colors, clean responsive grid.
"""

import os
import json
import streamlit as st
from app.components.header import render_header
from app.components.states import render_empty_state
from app.components.html_utils import render_html
from app.components.svg_covers import get_dashboard_svg_cover, DOMAIN_THEMES

META_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "metadata")

@st.cache_data
def load_dashboards():
    with open(os.path.join(META_DIR, "dashboards.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def render(on_select_dashboard):
    dashboards = load_dashboards()

    render_header(
        title="DV Projects using Official Data",
        subtitle=f"Explore {len(dashboards)} production dashboards powered by verified official data across national and global domains.",
        active_view="Gallery",
        meta_chips=[
            f"{len(dashboards)} Dashboards",
            "100% Real Data",
            "89 Official Sources",
            "Interactive Visual Suite"
        ]
    )

    # Clean Filter Bar
    s_col1, s_col2, s_col3 = st.columns([2, 1.2, 0.8])
    with s_col1:
        search_query = st.text_input(
            "Search:",
            placeholder="Search topics, indicators, countries, or sources...",
            key="gal_search",
            label_visibility="collapsed"
        )
    with s_col2:
        categories = ["All Categories"] + sorted(list(set(d.get("category") for d in dashboards if d.get("category"))))
        selected_cat = st.selectbox("Category:", categories, key="gal_cat", label_visibility="collapsed")
    with s_col3:
        has_active = bool(search_query) or (selected_cat != "All Categories")
        if st.button("↺ Reset", key="reset_filters_btn", use_container_width=True, disabled=not has_active):
            st.session_state["gal_search"] = ""
            st.session_state["gal_cat"] = "All Categories"
            st.rerun()

    # Filter application
    filtered = dashboards
    if search_query:
        q = search_query.lower()
        filtered = [
            d for d in filtered
            if q in d["title"].lower() or q in d["domain"].lower() or q in d["source_org"].lower() or any(q in k.lower() for k in d.get("kpis", []))
        ]
    if selected_cat != "All Categories":
        filtered = [d for d in filtered if d.get("category") == selected_cat]

    render_html(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin: 0.5rem 0 1rem 0; font-size: 0.82rem; color: #71717a;">
        <span>Showing <strong style="color: #ffffff;">{len(filtered)}</strong> of {len(dashboards)} dashboards</span>
        <span style="font-family: var(--font-mono); color: #38bdf8;">15 Visuals / Dashboard</span>
    </div>
    """)

    if not filtered:
        render_empty_state(
            title="No Dashboards Found",
            description=f"No dashboards match '{search_query}'. Try resetting your search filter.",
            icon="🔎"
        )
        return

    # Visual-First 3-Column Grid
    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered):
                d = filtered[i + j]
                theme = DOMAIN_THEMES.get(d.get('domain'), ('macro', '#38bdf8', '#818cf8', 'rgba(56, 189, 248, 0.15)'))
                _, c_primary, c_secondary, c_dim = theme

                kpi_list = d.get("kpis", [])
                kpi1 = kpi_list[0] if len(kpi_list) > 0 else "Official Data"

                svg_cover = get_dashboard_svg_cover(d.get("id"), d.get("domain"), d.get("title"), kpi1, height=135)

                with cols[j]:
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
                                letter-spacing: 0.03em;
                            ">{d.get('domain')[:22]}</span>
                            <span style="font-size: 0.7rem; color: #71717a; font-family: var(--font-mono);">{d.get('date_range', '')}</span>
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
                    if st.button(f"Explore Dashboard →", key=f"btn_{d.get('id')}", use_container_width=True, type="primary"):
                        on_select_dashboard(d.get("id"))
