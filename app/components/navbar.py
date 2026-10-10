"""
Clean Modern Top Navigation Bar
Minimal, buzzword-free, beautiful header navigation.
"""

import streamlit as st
from app.components.html_utils import render_html

NAV_ITEMS = [
    ("Landing Page", "Overview"),
    ("Dashboard Gallery", "Gallery"),
    ("Dashboards", "Dashboards"),
    ("Dataset Explorer", "Datasets"),
    ("Source Directory", "Sources"),
    ("API Catalog", "APIs")
]

def render_top_navbar(total_dashboards=94):
    cur_view = st.session_state.get("current_view", "Landing Page")

    # Clean, modern header
    render_html(f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.65rem 1.25rem;
        background: #09090b;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        margin-bottom: 1.25rem;
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="
                width: 34px;
                height: 34px;
                border-radius: 10px;
                background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
            ">📊</div>
            <div>
                <div style="font-family: var(--font-sans); font-size: 1.05rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em;">
                    DV Projects
                </div>
                <div style="font-size: 0.73rem; color: #71717a;">
                    <span style="color: #38bdf8; font-weight: 600;">{total_dashboards} Dashboards</span> &bull; Official Data
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: #34d399; background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.25); padding: 3px 8px; border-radius: 9999px;">
                ● Live
            </span>
        </div>
    </div>
    """)

    # 6 clean navigation buttons
    nav_cols = st.columns(len(NAV_ITEMS))
    for idx, (view_key, label) in enumerate(NAV_ITEMS):
        with nav_cols[idx]:
            is_active = (cur_view == view_key)
            btn_label = f"● {label}" if is_active else label
            btn_type = "primary" if is_active else "secondary"
            if st.button(btn_label, key=f"nav_tab_{view_key}", use_container_width=True, type=btn_type):
                if cur_view != view_key:
                    st.session_state["current_view"] = view_key
                    st.rerun()

    render_html("<div style='height: 1px; background: rgba(255,255,255,0.06); margin: 0.85rem 0 1.25rem 0;'></div>")
