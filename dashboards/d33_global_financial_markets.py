"""
Dashboard Module: D33 - Global Financial Market Volatility & Major Exchange Trends
Domain: Capital Markets & Commodities (Archetype: macro_policy)
Authentic Source: Verified Primary Dataset (data/analytical/d33_global_financial_markets.csv)
Visuals: 5 KPI Cards + 12 Specialized Plotly Visualizations + 1 Data Grid = 18 Visuals
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APP_DIR = os.path.join(PROJECT_ROOT, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

try:
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
        create_parallel_coordinates, create_pyramid_chart,
        create_growth_velocity_bar, create_pareto_chart
    )
except (ImportError, ModuleNotFoundError):
    from components.html_utils import render_html
    from components.info_modal import render_info_button
    from components.kpi_card import render_kpi
    from components.charts import (
        base_layout, COLOR_PALETTE, create_geo_scatter, create_donut_chart,
        create_histogram, create_violin_chart, create_sunburst, create_funnel_chart,
        create_horizontal_bar, create_correlation_heatmap, create_density_heatmap,
        create_radar_chart, create_waterfall_chart, create_treemap, create_box_chart,
        create_line_chart, create_bar_chart, create_area_chart, create_scatter_chart,
        create_gauge_chart, create_bubble_chart, create_sankey_diagram,
        create_parallel_coordinates, create_pyramid_chart,
        create_growth_velocity_bar, create_pareto_chart
    )

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/analytical/d33_global_financial_markets.csv")
WHY_MATTERS = """Cross-asset historical co-movement between equity benchmarks (S&P 500, Nifty 50), safe-haven physical gold, and energy commodities (Brent crude) tracks macroeconomic regime shifts, inflation expectations, and systemic risk."""
DATA_NOTE = """Market pricing archives compiled from Robert Shiller Yale Financial Market Data, World Gold Council, US Energy Information Administration (EIA), and National Stock Exchange of India (NSE)."""

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
<span class="domain-pill domain-capital markets & commodities">Capital Markets & Commodities</span>
<span class="kpi-chip" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan); background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.3);">D33</span>
<span class="live-dot" style="margin-left:4px;"></span>
<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">OFFICIAL DATASET</span>
</div>
<h1 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; margin:0 0 6px 0; background:linear-gradient(135deg, #ffffff 40%, #94a3b8 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
Global Financial Market Volatility & Major Exchange Trends
</h1>
<div style="font-size:0.875rem; color:var(--text-secondary); line-height:1.4;">
Production analytical pipeline &bull; Verified source: <code style="font-size:0.78rem; color:var(--accent-cyan); background:#080808; border:1px solid #1a1a1a; padding:2px 6px; border-radius:4px;">data/analytical/d33_global_financial_markets.csv</code>
</div>""")
    with c_info:
        st.write("")
        render_info_button("D33")

    # Interactive Filters & Slicers
    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🎛️ Filters & Slicers</span>
<span class="visuals-density-pill">Data Controls</span>
</div>""")
    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1])
    df = df_raw.copy()

    # Time or Date Filter
    if "Date" in df.columns:
        time_series = df["Date"].dropna()
        if pd.api.types.is_numeric_dtype(time_series) and len(time_series.unique()) > 1:
            min_val = int(time_series.min())
            max_val = int(time_series.max())
            if min_val < max_val:
                with f_col1:
                    selected_range = st.slider("Select Horizon Range:", min_val, max_val, (min_val, max_val), key=f"d33_global_financial_markets_slider")
                    df = df[(df["Date"] >= selected_range[0]) & (df["Date"] <= selected_range[1])]
        elif len(time_series.unique()) > 1 and "Date" in ["date", "Date"]:
            dates = sorted(time_series.unique().tolist())
            with f_col1:
                date_range = st.select_slider("Select Date Span:", options=dates, value=(dates[0], dates[-1]), key=f"d33_global_financial_markets_dslider")
                df = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

    # Categorical Filter
    cat_col = next((c for c in ["country", "state", "city", "market", "region", "economy_group"] if c in df.columns and len(df[c].dropna().unique()) > 1), None)
    if cat_col:
        unique_cats = sorted(df[cat_col].dropna().unique().tolist())
        with f_col2:
            selected_cats = st.multiselect(f"Filter {cat_col.title()}:", unique_cats, default=unique_cats, key=f"d33_global_financial_markets_{cat_col}_sel")
            if selected_cats:
                df = df[df[cat_col].isin(selected_cats)]

    # Sort & View
    num_cols_for_sort = df.select_dtypes(include=[np.number]).columns.tolist()
    with f_col3:
        sort_order = st.selectbox("Sort View:", ["Default Chronology", "Highest Value First", "Lowest Value First"], key=f"d33_global_financial_markets_sort")
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
            if "latest" == "latest":
                val = float(df["SP500"].dropna().iloc[-1])
            elif "latest" == "max":
                val = float(df["SP500"].dropna().max())
            elif "latest" == "min":
                val = float(df["SP500"].dropna().min())
            elif "latest" == "sum":
                val = float(df["SP500"].dropna().sum())
            elif "latest" == "count":
                val = float(len(df["SP500"].dropna()))
            else:
                val = float(df["SP500"].dropna().mean())
            fmt_val = "{val:,.1f}".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("S&P 500 Index Level", fmt_val, "US Equity Benchmark", status="pos")

    with kpi_cols[1]:
        try:
            if "latest" == "latest":
                val = float(df["PE10"].dropna().iloc[-1])
            elif "latest" == "max":
                val = float(df["PE10"].dropna().max())
            elif "latest" == "min":
                val = float(df["PE10"].dropna().min())
            elif "latest" == "sum":
                val = float(df["PE10"].dropna().sum())
            elif "latest" == "count":
                val = float(len(df["PE10"].dropna()))
            else:
                val = float(df["PE10"].dropna().mean())
            fmt_val = "{val:.1f}x".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Shiller CAPE 10 P/E", fmt_val, "Cyclically Adjusted P/E", status="neutral")

    with kpi_cols[2]:
        try:
            if "latest" == "latest":
                val = float(df["Gold_USD"].dropna().iloc[-1])
            elif "latest" == "max":
                val = float(df["Gold_USD"].dropna().max())
            elif "latest" == "min":
                val = float(df["Gold_USD"].dropna().min())
            elif "latest" == "sum":
                val = float(df["Gold_USD"].dropna().sum())
            elif "latest" == "count":
                val = float(len(df["Gold_USD"].dropna()))
            else:
                val = float(df["Gold_USD"].dropna().mean())
            fmt_val = "${val:,.0f}".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Gold Spot Price (USD/oz)", fmt_val, "Safe-Haven Asset", status="pos")

    with kpi_cols[3]:
        try:
            if "latest" == "latest":
                val = float(df["Brent_Oil_USD"].dropna().iloc[-1])
            elif "latest" == "max":
                val = float(df["Brent_Oil_USD"].dropna().max())
            elif "latest" == "min":
                val = float(df["Brent_Oil_USD"].dropna().min())
            elif "latest" == "sum":
                val = float(df["Brent_Oil_USD"].dropna().sum())
            elif "latest" == "count":
                val = float(len(df["Brent_Oil_USD"].dropna()))
            else:
                val = float(df["Brent_Oil_USD"].dropna().mean())
            fmt_val = "${val:.2f}".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Brent Crude Oil (USD/bbl)", fmt_val, "Global Energy Commodity", status="neutral")

    with kpi_cols[4]:
        try:
            if "latest" == "latest":
                val = float(df["Gold_to_SP500_Ratio"].dropna().iloc[-1])
            elif "latest" == "max":
                val = float(df["Gold_to_SP500_Ratio"].dropna().max())
            elif "latest" == "min":
                val = float(df["Gold_to_SP500_Ratio"].dropna().min())
            elif "latest" == "sum":
                val = float(df["Gold_to_SP500_Ratio"].dropna().sum())
            elif "latest" == "count":
                val = float(len(df["Gold_to_SP500_Ratio"].dropna()))
            else:
                val = float(df["Gold_to_SP500_Ratio"].dropna().mean())
            fmt_val = "{val:.2f}".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("Gold-to-S&P 500 Ratio", fmt_val, "Asset Allocation Ratio", status="neutral")

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

    # 3. Visual Analytics Suite (12 Specialized Visualizations in 4 Executive Tabs)
    render_html("""<div class="visuals-section-header" style="margin-top:1.75rem;">
<span class="visuals-section-title">📊 Visual Analytics Suite</span>
<span class="visuals-density-pill">12 Specialized Visualizations &bull; 4 Executive Tabs</span>
</div>""")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Primary Trends & Trajectory",
        "📊 Structural Breakdown & Distribution",
        "🔬 Deep Drivers & Relationships",
        "🏆 Rankings & Benchmarks"
    ])

    with tab1:
        # Row 1: Hero Trajectory Split (2.3 : 1.0) with Target Benchmark Gauge
        t1_c1, t1_c2 = st.columns([2.3, 1.0])
        with t1_c1:
            # Chart 1: Hero Trajectory
            fig1 = create_line_chart(df, x="Date", y=['SP500', 'PE10'], title="S&P 500 Price Benchmark & Shiller Cyclically Adjusted PE10", x_title="Date", y_title="Level / Ratio", subtitle="Historical trajectory and long-term trend", height=380)
            st.plotly_chart(fig1, use_container_width=True)
        with t1_c2:
            # Chart 2: Target Benchmark Gauge
            val_gauge_2 = float(df['SP500'].dropna().iloc[-1]) if ('SP500' in df.columns and len(df['SP500'].dropna()) > 0) else 0.0
            fig2 = create_gauge_chart(val_gauge_2, min_val=605.7, max_val=9639.1, target=2408.9, title="S&P 500 Index Level Target Benchmark Gauge", subtitle="Current level against target benchmark", suffix="", height=380)
            st.plotly_chart(fig2, use_container_width=True)

        # Row 2: Period Growth Velocity Bar (Full Width)
        # Chart 3: Period Growth Velocity Bar
        fig3 = create_growth_velocity_bar(df, time_col="Date", metric_col="SP500", title="Sp500 Period Growth Velocity", subtitle="Period-over-period growth velocity and acceleration", height=380)
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        # Row 1: Structural Classification & Dispersion Spread (1 : 1)
        t2_c1, t2_c2 = st.columns(2)
        with t2_c1:
            # Chart 4: Structural Classification
            wf_df_4 = df.dropna(subset=['Date']).tail(8) if 'Date' in df.columns else df.tail(8)
            wf_x_4 = [str(v) for v in wf_df_4['Date']] if 'Date' in wf_df_4.columns else ['Start', 'Mid', 'End']
            wf_y_4 = wf_df_4['SP500'].diff().fillna(wf_df_4['SP500'].iloc[0]).tolist() if 'SP500' in wf_df_4.columns else [10, 5, -2]
            fig4 = create_waterfall_chart(wf_x_4, wf_y_4, title="S&P 500 Index Level Change Attribution", subtitle="Hierarchical classification and structural composition", height=380)
            st.plotly_chart(fig4, use_container_width=True)
        with t2_c2:
            # Chart 5: Dispersion Spread
            fig5 = create_box_chart(df, x=None, y="Consumer Price Index", title="Distribution & Outlier Analysis", x_title="Quartiles", y_title="Consumer Price Index", subtitle="Distribution spread, quartiles, and variance", height=380)
            st.plotly_chart(fig5, use_container_width=True)

        # Row 2: Multi-Factor Matrix & Proportional Contribution (1 : 1)
        t2_c3, t2_c4 = st.columns(2)
        with t2_c3:
            # Chart 6: Multi-Factor Matrix
            fig6 = create_bubble_chart(df, x="SP500", y="Consumer Price Index", size="Long Interest Rate", color="PE10", hover_name="Date", title="Sp500 vs Consumer Price Index Multidimensional Matrix", x_title="Sp500", y_title="Consumer Price Index", subtitle="Multi-factor comparison (bubble size represents scale)", height=380)
            st.plotly_chart(fig6, use_container_width=True)
        with t2_c4:
            # Chart 7: Proportional Contribution
            wf_labels_7 = [col.replace('_', ' ').title() for col in ['SP500', 'Consumer Price Index', 'Long Interest Rate', 'PE10'] if col in df.columns]
            wf_vals_7 = [float(df[col].dropna().iloc[-1]) if (col in df.columns and len(df[col].dropna()) > 0) else 0.0 for col in ['SP500', 'Consumer Price Index', 'Long Interest Rate', 'PE10'] if col in df.columns]
            fig7 = create_waterfall_chart(wf_labels_7, wf_vals_7, title="Key Indicator Scale Comparison", subtitle="Proportional contribution and component share", height=380)
            st.plotly_chart(fig7, use_container_width=True)

    with tab3:
        # Row 1: Diverging Correlation Matrix & Frontier Trade-Off Scatter (1 : 1)
        t3_c1, t3_c2 = st.columns(2)
        with t3_c1:
            # Chart 8: Pearson Correlation Matrix
            corr_cols_8 = [c for c in ['SP500', 'Consumer Price Index', 'Long Interest Rate', 'PE10', 'Gold_USD', 'Brent_Oil_USD'] if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
            fig8 = create_correlation_heatmap(df, cols=corr_cols_8 if corr_cols_8 else None, title="Cross-Indicator Correlation Matrix (6 Dimensions)", subtitle="Pairwise correlation coefficients across indicators", height=380)
            st.plotly_chart(fig8, use_container_width=True)
        with t3_c2:
            # Chart 9: Frontier Trade-Off Scatter
            fig9 = create_scatter_chart(df, x="Long Interest Rate", y="PE10", trendline="ols", title="Long Interest Rate vs Pe10 Regression Frontier", x_title="Long Interest Rate", y_title="Pe10", subtitle="Bivariate regression and empirical frontier", height=380)
            st.plotly_chart(fig9, use_container_width=True)

        # Row 2: Multi-Indicator Capabilities Profile (Full Width)
        # Chart 10: Multi-Indicator Capabilities Profile Radar
        radar_cols_10 = list(dict.fromkeys([c for c in ['SP500', 'Consumer Price Index', 'Long Interest Rate', 'PE10', 'Gold_USD', 'Brent_Oil_USD'] if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]))
        radar_vals_10 = [float(df[c].dropna().iloc[-1]) if c in df.columns and len(df[c].dropna()) > 0 else 0.0 for c in radar_cols_10]
        fig10 = create_radar_chart(radar_cols_10, radar_vals_10, title="Multi-Indicator Capabilities Footprint", subtitle="Multi-indicator capability footprint (independently normalized)", height=380, df=df)
        st.plotly_chart(fig10, use_container_width=True)

    with tab4:
        # Row 1: Performance Rankings & Concentration Analysis (1 : 1)
        t4_c1, t4_c2 = st.columns(2)
        with t4_c1:
            # Chart 11: Performance Rankings Horizontal Bar
            fig11 = create_horizontal_bar(df, x="SP500", y="Date", title="Progress Over Time (Sp500)", x_title="Sp500", y_title="Timeline", subtitle="Cross-sectional comparative rankings by volume", height=380)
            st.plotly_chart(fig11, use_container_width=True)
        with t4_c2:
            # Chart 12: Concentration & Pareto Analysis
            fig12 = create_pareto_chart(df, cat_col="Date", metric_col="SP500", title="Pareto Concentration & Cumulative Distribution", subtitle="Cumulative distribution and Pareto 80/20 concentration", height=380)
            st.plotly_chart(fig12, use_container_width=True)

    # 4. Interactive Data Table (Visual 18)
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
            file_name=f"d33_global_financial_markets_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🔗 Related Views</span>
<span class="visuals-density-pill">Quick Navigation</span>
</div>""")
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🔍 Explore Full Schema in Dataset Explorer", key=f"f_nav_ds_d33_global_financial_markets", use_container_width=True):
            st.session_state["current_view"] = "Dataset Explorer"
            st.session_state["selected_dataset_slug"] = "d33_global_financial_markets"
            st.rerun()
    with nav_col2:
        if st.button("🏛️ View Publishing Authority in Source Directory", key=f"f_nav_src_d33_global_financial_markets", use_container_width=True):
            st.session_state["current_view"] = "Source Directory"
            st.session_state["selected_source_name"] = "S&P Dow Jones / World Gold Council / US EIA / NSE India"
            st.rerun()
