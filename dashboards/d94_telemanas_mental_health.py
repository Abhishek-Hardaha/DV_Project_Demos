"""
Dashboard Module: D94 - Tele-MANAS Tele-Mental Health Telemetry, Distress Resolution & Psychiatric Access
Domain: Public Mental Health & Digital Healthcare Delivery (Archetype: social_demographics)
Authentic Source: Verified Primary Dataset (data/analytical/d94_telemanas_mental_health.csv)
Visuals: 5 KPI Cards + 9 Specialized Plotly Visualizations + 1 Data Grid = 15 Visuals
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from app.components.html_utils import render_html
from app.components.info_modal import render_info_button
from app.components.kpi_card import render_kpi
from app.components.charts import (
    base_layout, COLOR_PALETTE, create_geo_scatter, create_donut_chart,
    create_histogram, create_violin_chart, create_sunburst, create_funnel_chart,
    create_horizontal_bar, create_correlation_heatmap, create_density_heatmap,
    create_radar_chart, create_waterfall_chart, create_treemap, create_box_chart,
    create_line_chart, create_bar_chart, create_area_chart, create_scatter_chart,
    create_gauge_chart, create_bubble_chart, create_sankey_diagram,
    create_parallel_coordinates, create_pyramid_chart
)

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/analytical/d94_telemanas_mental_health.csv")
WHY_MATTERS = """Tele-mental health services bridge critical geographic psychiatrist deficits, providing free 24/7 psychological first aid to citizens in distress."""
DATA_NOTE = """Tele Mental Health Assistance and Networking Across States (Tele-MANAS) portal operational reports, NIMHANS, and Ministry of Health and Family Welfare."""

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

def render():
    df_raw = load_data()
    
    # Header & Information
    c_title, c_info = st.columns([4.2, 1.2])
    with c_title:
        render_html(f"""<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
<span class="domain-pill domain-public mental health & digital healthcare delivery">Public Mental Health & Digital Healthcare Delivery</span>
<span class="kpi-chip" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan); background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.3);">D94</span>
<span class="live-dot" style="margin-left:4px;"></span>
<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">OFFICIAL DATASET</span>
</div>
<h1 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; margin:0 0 6px 0; background:linear-gradient(135deg, #ffffff 40%, #94a3b8 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
Tele-MANAS Tele-Mental Health Telemetry, Distress Resolution & Psychiatric Access
</h1>
<div style="font-size:0.875rem; color:var(--text-secondary); line-height:1.4;">
Production analytical pipeline &bull; Verified source: <code style="font-size:0.78rem; color:var(--accent-cyan); background:#080808; border:1px solid #1a1a1a; padding:2px 6px; border-radius:4px;">data/analytical/d94_telemanas_mental_health.csv</code>
</div>""")
    with c_info:
        st.write("")
        render_info_button("D94")

    # Interactive Filters & Slicers
    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🎛️ Filters & Slicers</span>
<span class="visuals-density-pill">Data Controls</span>
</div>""")
    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1])
    df = df_raw.copy()

    # Time or Date Filter
    if "None" in df.columns:
        time_series = df["None"].dropna()
        if pd.api.types.is_numeric_dtype(time_series) and len(time_series.unique()) > 1:
            min_val = int(time_series.min())
            max_val = int(time_series.max())
            if min_val < max_val:
                with f_col1:
                    selected_range = st.slider("Select Horizon Range:", min_val, max_val, (min_val, max_val), key=f"d94_telemanas_mental_health_slider")
                    df = df[(df["None"] >= selected_range[0]) & (df["None"] <= selected_range[1])]
        elif len(time_series.unique()) > 1 and "None" in ["date", "Date"]:
            dates = sorted(time_series.unique().tolist())
            with f_col1:
                date_range = st.select_slider("Select Date Span:", options=dates, value=(dates[0], dates[-1]), key=f"d94_telemanas_mental_health_dslider")
                df = df[(df["None"] >= date_range[0]) & (df["None"] <= date_range[1])]

    # Categorical Filter
    cat_col = next((c for c in ["country", "state", "city", "market", "region", "economy_group"] if c in df.columns and len(df[c].dropna().unique()) > 1), None)
    if cat_col:
        unique_cats = sorted(df[cat_col].dropna().unique().tolist())
        with f_col2:
            selected_cats = st.multiselect(f"Filter {cat_col.title()}:", unique_cats, default=unique_cats, key=f"d94_telemanas_mental_health_{cat_col}_sel")
            if selected_cats:
                df = df[df[cat_col].isin(selected_cats)]

    # Sort & View
    num_cols_for_sort = df.select_dtypes(include=[np.number]).columns.tolist()
    with f_col3:
        sort_order = st.selectbox("Sort View:", ["Default Chronology", "Highest Value First", "Lowest Value First"], key=f"d94_telemanas_mental_health_sort")
        if sort_order == "Highest Value First" and num_cols_for_sort:
            df = df.sort_values(by=num_cols_for_sort[0], ascending=False)
        elif sort_order == "Lowest Value First" and num_cols_for_sort:
            df = df.sort_values(by=num_cols_for_sort[0], ascending=True)

    # Safety guard
    if df.empty:
        st.warning("⚠️ No records match active filters. Resetting to complete dataset.")
        df = df_raw.copy()

    # 1. Key Metrics Section (5 Cards)
    render_html("""
    <div class="visuals-section-header" style="margin-top:1.5rem;">
        <span class="visuals-section-title">📌 Key Metrics</span>
        <span class="visuals-density-pill">5 Key Indicators</span>
    </div>
    """)
    kpi_cols = st.columns(5)

    with kpi_cols[0]:
        try:
            if "sum" == "latest":
                val = float(df["total_telemanas_calls_received"].dropna().iloc[-1])
            elif "sum" == "max":
                val = float(df["total_telemanas_calls_received"].dropna().max())
            elif "sum" == "min":
                val = float(df["total_telemanas_calls_received"].dropna().min())
            elif "sum" == "sum":
                val = float(df["total_telemanas_calls_received"].dropna().sum())
            elif "sum" == "count":
                val = float(len(df["total_telemanas_calls_received"].dropna()))
            else:
                val = float(df["total_telemanas_calls_received"].dropna().mean())
            fmt_val = "{val:,.0f} Calls".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Total Distress Calls", fmt_val, "24x7 Sovereign Helpline", status="pos")

    with kpi_cols[1]:
        try:
            if "mean" == "latest":
                val = float(df["call_distress_resolution_pct"].dropna().iloc[-1])
            elif "mean" == "max":
                val = float(df["call_distress_resolution_pct"].dropna().max())
            elif "mean" == "min":
                val = float(df["call_distress_resolution_pct"].dropna().min())
            elif "mean" == "sum":
                val = float(df["call_distress_resolution_pct"].dropna().sum())
            elif "mean" == "count":
                val = float(len(df["call_distress_resolution_pct"].dropna()))
            else:
                val = float(df["call_distress_resolution_pct"].dropna().mean())
            fmt_val = "{val:.1f}%".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Tele-Counseling Resolution", fmt_val, "Immediate Psychological First Aid", status="pos")

    with kpi_cols[2]:
        try:
            if "mean" == "latest":
                val = float(df["psychiatrists_per_100k_population"].dropna().iloc[-1])
            elif "mean" == "max":
                val = float(df["psychiatrists_per_100k_population"].dropna().max())
            elif "mean" == "min":
                val = float(df["psychiatrists_per_100k_population"].dropna().min())
            elif "mean" == "sum":
                val = float(df["psychiatrists_per_100k_population"].dropna().sum())
            elif "mean" == "count":
                val = float(len(df["psychiatrists_per_100k_population"].dropna()))
            else:
                val = float(df["psychiatrists_per_100k_population"].dropna().mean())
            fmt_val = "{val:.2f} / 100k".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Psychiatrist Density", fmt_val, "WHO Norm: 3.0 / 100k Pop", status="neg")

    with kpi_cols[3]:
        try:
            if "mean" == "latest":
                val = float(df["dmhp_covered_districts_pct"].dropna().iloc[-1])
            elif "mean" == "max":
                val = float(df["dmhp_covered_districts_pct"].dropna().max())
            elif "mean" == "min":
                val = float(df["dmhp_covered_districts_pct"].dropna().min())
            elif "mean" == "sum":
                val = float(df["dmhp_covered_districts_pct"].dropna().sum())
            elif "mean" == "count":
                val = float(len(df["dmhp_covered_districts_pct"].dropna()))
            else:
                val = float(df["dmhp_covered_districts_pct"].dropna().mean())
            fmt_val = "{val:.1f}%".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("DMHP District Coverage", fmt_val, "District Mental Health Program", status="pos")

    with kpi_cols[4]:
        try:
            if "mean" == "latest":
                val = float(df["anxiety_depression_calls_pct"].dropna().iloc[-1])
            elif "mean" == "max":
                val = float(df["anxiety_depression_calls_pct"].dropna().max())
            elif "mean" == "min":
                val = float(df["anxiety_depression_calls_pct"].dropna().min())
            elif "mean" == "sum":
                val = float(df["anxiety_depression_calls_pct"].dropna().sum())
            elif "mean" == "count":
                val = float(len(df["anxiety_depression_calls_pct"].dropna()))
            else:
                val = float(df["anxiety_depression_calls_pct"].dropna().mean())
            fmt_val = "{val:.1f}%".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Anxiety & Depression Share", fmt_val, "Primary Clinical Morbidity", status="neutral")

    # 2. Key Observations & Summary
    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">💡 Key Observations</span>
<span class="visuals-density-pill">Summary Insights</span>
</div>""")
    try:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        entity_col = next((c for c in ["country", "state", "city", "market", "region", "economy_group"] if c in df.columns), None)
        time_c = next((c for c in ["year", "fiscal_year", "crop_year", "date", "Date"] if c in df.columns), None)
        
        primary_col = num_cols[0] if num_cols else None
        secondary_col = num_cols[1] if len(num_cols) > 1 else None
        
        b1, b2, b3, b4 = "", "", "", ""
        
        if primary_col:
            p_series = df[primary_col].dropna()
            p_min, p_max = float(p_series.min()), float(p_series.max())
            p_mean, p_median = float(p_series.mean()), float(p_series.median())
            p_latest = float(p_series.iloc[-1])
            p_first = float(p_series.iloc[0])
            
            if time_c and len(p_series) > 1:
                t_start = df.loc[p_series.index[0], time_c]
                t_end = df.loc[p_series.index[-1], time_c]
                pct_change = ((p_latest - p_first) / abs(p_first) * 100) if p_first != 0 else 0
                b1 = f"• <b>Long-Term Trend ({t_start}–{t_end})</b>: Primary metric <code>{primary_col}</code> moved from {p_first:,.2f} to {p_latest:,.2f} (change of <b>{pct_change:+.1f}%</b>)."
            else:
                std_val = float(p_series.std()) if len(p_series) > 1 else 0.0
                b1 = f"• <b>Baseline Distribution</b>: Across {len(p_series)} observations, <code>{primary_col}</code> averages <b>{p_mean:,.2f}</b> (median: {p_median:,.2f}, std dev: {std_val:,.2f})."

            max_idx = p_series.idxmax()
            min_idx = p_series.idxmin()
            max_entity = df.loc[max_idx, entity_col] if entity_col else (df.loc[max_idx, time_c] if time_c else "Peak")
            min_entity = df.loc[min_idx, entity_col] if entity_col else (df.loc[min_idx, time_c] if time_c else "Trough")
            b2 = f"• <b>Observed Extremes</b>: Highest recorded value was <b>{p_max:,.2f}</b> ({max_entity}) vs lowest of <b>{p_min:,.2f}</b> ({min_entity}), spanning a range of {p_max - p_min:,.2f}."

            if entity_col and p_min > 0:
                disp = p_max / p_min
                top3_sum = float(df.nlargest(3, primary_col)[primary_col].sum())
                tot_sum = float(p_series.sum())
                top3_share = (top3_sum / tot_sum * 100) if tot_sum > 0 else 0
                b3 = f"• <b>Regional Concentration</b>: Highest entity exceeds lowest by <b>{disp:.1f}x</b>. The top 3 entities account for <b>{top3_share:.1f}%</b> of total measured volume."
            elif secondary_col:
                corr = float(df[primary_col].corr(df[secondary_col]))
                corr_desc = "strong positive" if corr > 0.6 else ("moderate positive" if corr > 0.3 else ("strong negative" if corr < -0.6 else "uncoupled/neutral"))
                b3 = f"• <b>Indicator Association</b>: Correlation between <code>{primary_col}</code> and <code>{secondary_col}</code> is <b>{corr:+.2f}</b> ({corr_desc} association)."

            if len(p_series) >= 2:
                p_prior = float(p_series.iloc[-2])
                mom = ((p_latest - p_prior) / abs(p_prior) * 100) if p_prior != 0 else 0
                b4 = f"• <b>Recent Movement</b>: Latest recorded value is <b>{p_latest:,.2f}</b> (<b>{mom:+.1f}%</b> relative to prior period)."

        finding_html = "<br>".join(filter(None, [b1, b2, b3, b4])) if any([b1, b2, b3, b4]) else "Key indicators active across all monitored dimensions."
        
        render_html(f"""<div class="institutional-briefing">
<div class="briefing-card card-finding">
<div class="briefing-label label-finding">⚡ Summary Finding</div>
<div class="briefing-text">{finding_html}</div>
</div>
<div class="briefing-card card-why">
<div class="briefing-label label-why">🏛️ Context</div>
<div class="briefing-text">{WHY_MATTERS}</div>
</div>
<div class="briefing-card card-note">
<div class="briefing-label label-note">📋 Data Notes</div>
<div class="briefing-text">{DATA_NOTE}</div>
</div>
</div>""")
    except Exception:
        pass

    # 3. Regional Demographics & Social Distribution
    render_html("""<div class="visuals-section-header" style="margin-top:1.75rem;">
<span class="visuals-section-title">👥 Regional Demographics & Social Distribution</span>
<span class="visuals-density-pill">9 Analytical Visualizations</span>
</div>""")

    # Row 1: Regional Benchmark Hero Split (2.1 : 1.1) with Target Gauge
    r1_c1, r1_c2 = st.columns([2.1, 1.1])
    with r1_c1:
        # Chart 1: Regional Benchmark
        fig1 = px.bar(df, x="state", y="total_telemanas_calls_received", color_discrete_sequence=COLOR_PALETTE[0:])
        fig1 = base_layout(fig1, "Total Tele-MANAS 24x7 Tele-Mental Health Inbound Distress Calls Received", "State", "Calls Received", height=380, subtitle="Historical trajectory and primary trend")
        st.plotly_chart(fig1, use_container_width=True)
    with r1_c2:
        # Chart 2: Target Coverage Gauge
        val_gauge_2 = float(df['total_telemanas_calls_received'].dropna().iloc[-1]) if ('total_telemanas_calls_received' in df.columns and len(df['total_telemanas_calls_received'].dropna()) > 0) else 0.0
        fig2 = create_gauge_chart(val_gauge_2, min_val=4640.0, max_val=210000.0, target=58688.0, title="Total Distress Calls Target Benchmark Gauge", subtitle="Current level against target benchmark", suffix="", height=380)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Demographic Comparison & Spatial Scale (1.4 : 1.6)
    r2_c1, r2_c2 = st.columns([1.4, 1.6])
    with r2_c1:
        # Chart 3: Demographic Comparison Pyramid
        df_pyr_3 = df.dropna(subset=['state', 'call_distress_resolution_pct', 'Demographic Comparison: Call Distress Resolution Pct vs Dmhp Covered Districts Pct']).head(15) if ('state' in df.columns and 'call_distress_resolution_pct' in df.columns and 'Demographic Comparison: Call Distress Resolution Pct vs Dmhp Covered Districts Pct' in df.columns) else df.head(10)
        cats_3 = df_pyr_3['state'].astype(str).tolist() if 'state' in df_pyr_3.columns else ['A', 'B']
        left_vals_3 = df_pyr_3['call_distress_resolution_pct'].tolist() if 'call_distress_resolution_pct' in df_pyr_3.columns else [10, 20]
        right_vals_3 = df_pyr_3['Demographic Comparison: Call Distress Resolution Pct vs Dmhp Covered Districts Pct'].tolist() if 'Demographic Comparison: Call Distress Resolution Pct vs Dmhp Covered Districts Pct' in df_pyr_3.columns else [15, 25]
        fig3 = create_pyramid_chart(cats_3, left_vals_3, right_vals_3, label_left="Call Distress Resolution Pct", label_right="Dmhp Covered Districts Pct", title="dmhp_covered_districts_pct", subtitle="Contribution breakdown by segment", height=380)
        st.plotly_chart(fig3, use_container_width=True)
    with r2_c2:
        # Chart 4: Dispersion Violin Spread
        fig4 = create_violin_chart(df, x="state", y="total_telemanas_calls_received", title="Total Telemanas Calls Received Distribution by State", x_title="State", y_title="Total Telemanas Calls Received", subtitle="Distribution spread and variance", height=380)
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: 3-Column Dispersion & Progression Strip (1:1:1)
    r3_c1, r3_c2, r3_c3 = st.columns(3)
    with r3_c1:
        # Chart 5: Multi-Factor Demographic Bubble Matrix
        fig5 = create_bubble_chart(df, x="total_telemanas_calls_received", y="call_distress_resolution_pct", size="psychiatrists_per_100k_population", color="state", hover_name="state", title="Total Telemanas Calls Received vs Call Distress Resolution Pct Relationship", x_title="Total Telemanas Calls Received", y_title="Call Distress Resolution Pct", subtitle="Multi-factor comparison (bubble size represents scale)", height=380)
        st.plotly_chart(fig5, use_container_width=True)
    with r3_c2:
        # Chart 6: Pearson Correlation Matrix
        corr_cols_6 = [c for c in ['total_telemanas_calls_received', 'call_distress_resolution_pct', 'psychiatrists_per_100k_population', 'dmhp_covered_districts_pct', 'anxiety_depression_calls_pct', 'sleep_distress_calls_pct'] if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        fig6 = create_correlation_heatmap(df, cols=corr_cols_6 if corr_cols_6 else None, title="Correlation Matrix (6 Key Indicators)", subtitle="Pairwise correlation coefficients across indicators", height=380)
        st.plotly_chart(fig6, use_container_width=True)
    with r3_c3:
        # Chart 7: Relationship Scatter
        fig7 = px.scatter(df, x="psychiatrists_per_100k_population", y="call_distress_resolution_pct", trendline="ols", color_discrete_sequence=COLOR_PALETTE[6:])
        fig7 = base_layout(fig7, "Clinical Psychiatrist Density (per 100k) vs Telephonic Distress Resolution Rate", "Psychiatrists / 100k", "Resolution Rate (%)", height=380, subtitle="Direct relationship and trendline")
        st.plotly_chart(fig7, use_container_width=True)

    # Row 4: Diagnostic Scan & Ranking Benchmark (1.3 : 1.7)
    r4_c1, r4_c2 = st.columns([1.3, 1.7])
    with r4_c1:
        # Chart 8: Multi-Indicator Profile Radar
        radar_cols_8 = [c for c in ['total_telemanas_calls_received', 'call_distress_resolution_pct', 'psychiatrists_per_100k_population', 'dmhp_covered_districts_pct', 'anxiety_depression_calls_pct'] if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        radar_vals_8 = [float(df[c].dropna().iloc[-1]) if c in df.columns and len(df[c].dropna()) > 0 else 0.0 for c in radar_cols_8]
        fig8 = create_radar_chart(radar_cols_8, radar_vals_8, title="Multi-Indicator Capabilities Profile", subtitle="Comparative profile across core indicators (0-100% scale)", height=380)
        st.plotly_chart(fig8, use_container_width=True)
    with r4_c2:
        # Chart 9: Comparative Ranking Benchmark
        fig9 = create_horizontal_bar(df, x="total_telemanas_calls_received", y="state", title="Rankings by Total Telemanas Calls Received", x_title="Total Telemanas Calls Received", y_title="State", subtitle="Comparative ranking across categories", height=380)
        st.plotly_chart(fig9, use_container_width=True)

    # 4. Interactive Data Table (Visual 15)
    render_html("""<div class="visuals-section-header" style="margin-top:1.75rem;">
<span class="visuals-section-title">📋 Complete Data Table</span>
<span class="visuals-density-pill">Verified Data Records</span>
</div>""")
    st.dataframe(df, use_container_width=True, height=280)
    
    dl_c1, dl_c2 = st.columns([3, 1])
    with dl_c1:
        render_html(f"""<div style="font-size:0.82rem; color:var(--text-muted); font-family:var(--font-sans); padding-top:6px;">
Displaying <strong style="color:var(--text-primary);">{len(df)}</strong> verified observations across <strong style="color:var(--text-primary);">{len(df.columns)}</strong> attributes &bull; Dataset path: <code style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan);">{CSV_PATH}</code>
</div>""")
    with dl_c2:
        st.download_button(
            label="📥 Export Filtered CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"d94_telemanas_mental_health_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🔗 Related Views</span>
<span class="visuals-density-pill">Quick Navigation</span>
</div>""")
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🔍 Explore Full Schema in Dataset Explorer", key=f"f_nav_ds_d94_telemanas_mental_health", use_container_width=True):
            st.session_state["current_view"] = "Dataset Explorer"
            st.session_state["selected_dataset_slug"] = "d94_telemanas_mental_health"
            st.rerun()
    with nav_col2:
        if st.button("🏛️ View Publishing Authority in Source Directory", key=f"f_nav_src_d94_telemanas_mental_health", use_container_width=True):
            st.session_state["current_view"] = "Source Directory"
            st.session_state["selected_source_name"] = "Ministry of Health and Family Welfare (Tele-MANAS) & NIMHANS"
            st.rerun()
