"""
Source Explorer: Directory of Primary Source Organizations
Showcases all authoritative institutions, ministries, central banks, and multilateral bodies.
Transformed into an executive authority directory with instant search and deep dashboard linking.
"""

import os
import json
import streamlit as st
from app.components.header import render_header
from app.components.kpi_card import render_kpi
from app.components.states import render_empty_state
from app.components.html_utils import render_html

META_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "metadata")

@st.cache_data
def load_sources_and_dashboards():
    with open(os.path.join(META_DIR, "sources.json"), "r", encoding="utf-8") as f:
        sources = json.load(f)
    with open(os.path.join(META_DIR, "dashboards.json"), "r", encoding="utf-8") as f:
        dashboards = json.load(f)
    return sources, dashboards

def render():
    sources, dashboards = load_sources_and_dashboards()

    tier1_c = sum(1 for s in sources if "Tier 1" in s.get("tier", ""))
    tier2_c = sum(1 for s in sources if "Tier 2" in s.get("tier", ""))

    render_header(
        title="Official Data Sources",
        subtitle=f"Directory of all {len(sources)} authoritative external publishers, ministries, central banks, and international statistical organizations.",
        active_view="Sources",
        meta_chips=[
            f"🏛️ {len(sources)} Publishing Bodies",
            f"🛡️ {tier1_c} National Agencies",
            f"🌐 {tier2_c} Global Organizations",
            "🚫 0 Mock Providers"
        ]
    )

    # Overview KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi("Total Organizations", f"{len(sources)}", delta="Official Entities", status="pos")
    with c2:
        render_kpi("National Agencies", f"{tier1_c}", delta="Ministries & Central Banks", status="pos")
    with c3:
        render_kpi("Global Organizations", f"{tier2_c}", delta="UN, IMF, World Bank, IEA", status="neutral")
    with c4:
        render_kpi("Synthetic Providers", "0", delta="100% Real Data", status="pos")

    render_html("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #1f1f1f;'>")

    # Filter Toolbar
    with st.container():
        f_c1, f_c2 = st.columns([1.5, 1])
        with f_c1:
            search_src = st.text_input(
                "Search Sovereign Authority, Ministry or Mandate:",
                placeholder="e.g. Reserve Bank of India, MoSPI, World Bank, USGS, CEA, SEBI...",
                key="src_search"
            )
        with f_c2:
            countries = ["All Jurisdictions"] + sorted(list(set(s.get("country", "") for s in sources if s.get("country"))))
            sel_country = st.selectbox("Filter by Jurisdiction / Realm:", countries, key="src_country")
    
    filtered_src = sources
    if sel_country != "All Jurisdictions":
        filtered_src = [s for s in filtered_src if s.get("country") == sel_country]
    if search_src:
        q = search_src.lower()
        filtered_src = [s for s in filtered_src if q in s.get("name", "").lower() or q in s.get("official_status", "").lower() or q in s.get("country", "").lower()]

    st.caption(f"Displaying {len(filtered_src)} of {len(sources)} official publishing authorities:")

    # Preselected source highlighting from session state
    target_src = st.session_state.get("selected_source_name")

    if target_src:
        c_banner, c_clear = st.columns([4, 1])
        with c_banner:
            banner_html = f"""<div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px; padding: 10px 14px; font-size: 0.86rem; color: #7dd3fc; display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
<span style="font-size: 1.1rem;">🎯</span>
<span>Focused on Publishing Authority: <strong style="color: #ffffff;">{target_src}</strong></span>
</div>"""
            render_html(banner_html)
        with c_clear:
            if st.button("✖ Clear Focus", key="clear_src_focus", use_container_width=True):
                st.session_state.pop("selected_source_name", None)
                st.rerun()

    # Prioritize matched sources if focused
    if target_src:
        def match_priority(s):
            if s.get("name") in target_src or target_src in s.get("name"):
                return 0
            if any(w.lower() in target_src.lower() for w in s.get("name", "").replace("(", "").replace(")", "").split() if len(w) > 3):
                return 1
            return 2
        filtered_src = sorted(filtered_src, key=match_priority)

    if not filtered_src:
        render_empty_state(
            title="No Publishing Authorities Match Criteria",
            description=f"Your search for '{search_src}' in '{sel_country}' yielded zero matches. Clear your filters to browse all {len(sources)} authorities.",
            icon="🏛️"
        )
        return

    for s in filtered_src:
        is_highlighted = target_src and (s.get("name") in target_src or target_src in s.get("name") or any(w.lower() in target_src.lower() for w in s.get("name", "").replace("(", "").replace(")", "").split() if len(w) > 3))
        glow_style = "border-color: #38bdf8; box-shadow: 0 0 20px rgba(56, 189, 248, 0.25); background: linear-gradient(145deg, #070707 0%, #000000 100%);" if is_highlighted else ""
        
        # Find dashboards backed by this source
        linked_d = [d for d in dashboards if s.get("name", "") in d.get("source_org", "") or any(word in d.get("source_org", "") for word in s.get("name", "").split() if len(word) > 4)]
        
        tier_badge = '<span class="badge badge-tier1">Tier 1 Sovereign</span>' if "Tier 1" in s.get("tier", "") else '<span class="badge badge-global">Tier 2 Multilateral</span>'

        card_html = f"""<div class="gallery-card" style="{glow_style} margin-bottom: 0.5rem;">
<div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
{tier_badge}
<span class="badge badge-live">Verified Authority</span>
<span style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">{s.get('country')}</span>
</div>
<h3 style="margin: 4px 0 6px 0; color: #ffffff; font-size: 1.15rem; font-weight: 700;">{s.get('name')}</h3>
<div style="font-size: 0.84rem; color: #94a3b8; line-height: 1.5;">
<b>Official Mandate:</b> {s.get('official_status')}<br>
<b>Primary Portal:</b> <a href="{s.get('url')}" target="_blank" style="color: #38bdf8; text-decoration: underline;">{s.get('url')} ↗</a>
</div>
</div>
<div style="display: flex; gap: 12px;">
<div style="background: #050505; padding: 8px 14px; border-radius: 8px; border: 1px solid #171717; text-align: center;">
<div style="font-size: 1.2rem; font-weight: 700; color: #f8fafc; font-family: var(--font-mono);">{s.get('datasets_count', 1)}</div>
<div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Datasets</div>
</div>
<div style="background: #050505; padding: 8px 14px; border-radius: 8px; border: 1px solid #171717; text-align: center;">
<div style="font-size: 1.2rem; font-weight: 700; color: #38bdf8; font-family: var(--font-mono);">{s.get('dashboards_count', 1)}</div>
<div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Dashboards</div>
</div>
</div>
</div>
</div>"""
        render_html(card_html)

        if linked_d:
            render_html("<div style='font-size: 0.76rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin: 6px 0 6px 0;'>Backed Dashboards</div>")
            btn_cols = st.columns(min(len(linked_d), 3))
            for idx, ld in enumerate(linked_d[:3]):
                with btn_cols[idx % 3]:
                    if st.button(f"🚀 Open {ld['id']} ({ld['title'][:22]}...)", key=f"src_btn_{s.get('id', idx)}_{ld['id']}", use_container_width=True):
                        st.session_state["selected_dashboard_id"] = ld["id"]
                        st.session_state["current_view"] = "Dashboards"
                        st.rerun()

        render_html("<div style='height: 12px;'></div>")
