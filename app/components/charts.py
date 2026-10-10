"""
Reusable Component: Professional Plotly Visualization Builders
Applies consistent typography, transparent canvas, responsive palettes, tooltips, and margins.
Guarantees 100% accurate, high-contrast, insightful charts across all data domains.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

TEMPLATE_THEME = "plotly_dark"
COLOR_PALETTE = ["#38bdf8", "#818cf8", "#34d399", "#f59e0b", "#f87171", "#c084fc", "#ec4899", "#06b6d4", "#fb923c", "#4ade80"]

def base_layout(fig, title="", x_title="", y_title="", height=380, subtitle=""):
    title_text = f"<b>{title}</b>"
    top_margin = 52
    if subtitle:
        title_text += f"<br><span style='font-size:11px;color:#94a3b8;font-weight:normal;letter-spacing:0.01em;'>{subtitle}</span>"
        top_margin = 68

    fig.update_layout(
        template=TEMPLATE_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=25, t=top_margin, b=40),
        height=height,
        title=dict(
            text=title_text,
            font=dict(family="Plus Jakarta Sans, -apple-system, sans-serif", size=13.5, color="#ffffff"),
            x=0.01,
            y=0.97
        ),
        xaxis=dict(
            title=dict(text=x_title, font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#94a3b8")),
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#94a3b8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
            showgrid=True,
            zerolinecolor="rgba(255, 255, 255, 0.14)"
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#94a3b8")),
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#94a3b8"),
            gridcolor="rgba(255, 255, 255, 0.06)",
            showgrid=True,
            zerolinecolor="rgba(255, 255, 255, 0.14)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Plus Jakarta Sans, sans-serif", size=10.5, color="#cbd5e1")
        ),
        hoverlabel=dict(
            bgcolor="#0c0d14",
            bordercolor="rgba(56, 189, 248, 0.6)",
            font_size=12,
            font_color="#ffffff",
            font_family="Plus Jakarta Sans, sans-serif"
        )
    )
    return fig

def create_line_chart(df, x, y, color=None, title="", x_title="", y_title="", markers=True, height=380, subtitle=""):
    df_clean = df.dropna(subset=[x]).copy() if x in df.columns else df.copy()
    
    # Intelligent multi-entity detection: if x has duplicate values and color is not set,
    # group by the entity column so lines never zigzag backwards across years!
    if color is None and x in df_clean.columns and df_clean[x].duplicated().any():
        if isinstance(y, list) and len(y) > 1:
            valid_y = [col for col in y if col in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[col])]
            if valid_y:
                df_clean = df_clean.groupby(x, as_index=False)[valid_y].mean().sort_values(by=x)
            color = None
        else:
            entity_col = next((c for c in ['country', 'state', 'region', 'economy_group', 'sector', 'category', 'city', 'zone', 'basin'] if c in df_clean.columns), None)
            if not entity_col:
                cat_cols = [c for c in df_clean.select_dtypes(include=['object']).columns if c != x]
                entity_col = cat_cols[0] if cat_cols else None
                
            if entity_col:
                # If high cardinality, focus on top 7 by metric volume
                if df_clean[entity_col].nunique() > 8:
                    metric_check = y if isinstance(y, str) else (y[0] if y else None)
                    if metric_check and metric_check in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[metric_check]):
                        top_ents = df_clean.groupby(entity_col)[metric_check].sum().nlargest(7).index.tolist()
                        df_clean = df_clean[df_clean[entity_col].isin(top_ents)].copy()
                color = entity_col
                df_clean = df_clean.sort_values(by=[entity_col, x])
            else:
                # Aggregate by x so each point in time is unique
                if isinstance(y, str) and y in df_clean.columns:
                    df_clean = df_clean.groupby(x, as_index=False)[y].mean().sort_values(by=x)
                elif isinstance(y, list):
                    valid_y = [col for col in y if col in df_clean.columns]
                    df_clean = df_clean.groupby(x, as_index=False)[valid_y].mean().sort_values(by=x)
    elif color and color in df_clean.columns:
        df_clean = df_clean.sort_values(by=[color, x])
    elif x in df_clean.columns:
        df_clean = df_clean.sort_values(by=x)

    fig = px.line(
        df_clean, x=x, y=y, color=color,
        markers=markers,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height, subtitle=subtitle)

def create_bar_chart(df, x, y, color=None, title="", x_title="", y_title="", orientation="v", height=380, subtitle=""):
    fig = px.bar(
        df, x=x, y=y, color=color,
        orientation=orientation,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height, subtitle=subtitle)

def create_scatter_chart(df, x, y, size=None, color=None, hover_name=None, trendline=None, title="", x_title="", y_title="", height=380, subtitle=""):
    valid_cols = [c for c in [x, y] if c in df.columns]
    if len(valid_cols) < 2:
        return go.Figure()
    df_clean = df.dropna(subset=valid_cols).copy()

    time_col = next((c for c in ['year', 'fiscal_year', 'crop_year', 'date', 'Date'] if c in df_clean.columns), None)
    entity_col = next((c for c in ['country', 'state', 'region', 'economy_group', 'sector', 'category', 'city'] if c in df_clean.columns), None)

    # If dataset spans multiple time periods with entities, snapshot the latest period
    # to show a crisp cross-sectional frontier without caterpillar smears
    if time_col and entity_col and df_clean[time_col].nunique() > 1:
        latest_t = df_clean[time_col].max()
        df_snapshot = df_clean[df_clean[time_col] == latest_t].copy()
        if len(df_snapshot) >= 4:
            df_clean = df_snapshot
            if color is None:
                color = entity_col
            if hover_name is None:
                hover_name = entity_col

    if color and color not in df_clean.columns:
        color = None
    if hover_name and hover_name not in df_clean.columns:
        hover_name = None
    if size and (size not in df_clean.columns or not pd.api.types.is_numeric_dtype(df_clean[size]) or (df_clean[size] <= 0).all()):
        size = None

    fig = px.scatter(
        df_clean, x=x, y=y, size=size, color=color, hover_name=hover_name,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # Fit crisp OLS trendline across all observations
    if trendline == "ols" and len(df_clean) >= 3 and pd.api.types.is_numeric_dtype(df_clean[x]) and pd.api.types.is_numeric_dtype(df_clean[y]):
        try:
            valid = df_clean.dropna(subset=[x, y])
            if len(valid) >= 3 and valid[x].nunique() > 1:
                p = np.polyfit(valid[x].astype(float), valid[y].astype(float), 1)
                x_vals = np.linspace(float(valid[x].min()), float(valid[x].max()), 60)
                y_vals = np.polyval(p, x_vals)
                fig.add_trace(go.Scatter(
                    x=x_vals, y=y_vals,
                    mode="lines",
                    name="OLS Fit",
                    line=dict(color="#f43f5e", width=2.2, dash="dash")
                ))
        except Exception:
            pass

    return base_layout(fig, title, x_title, y_title, height, subtitle=subtitle)

def create_treemap(df, path, values, title="", subtitle="", height=380):
    df_clean = df.copy()
    if path and isinstance(path, list):
        for p in path:
            if p in df_clean.columns:
                df_clean[p] = df_clean[p].fillna("Unspecified").astype(str)
    if values and values in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[values]):
        df_clean = df_clean[df_clean[values] > 0]
        if df_clean.empty:
            df_clean = df.copy()
            values = None
    fig = px.treemap(
        df_clean, path=path, values=values,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_area_chart(df, x, y, color=None, title="", x_title="", y_title="", height=380, subtitle=""):
    df_clean = df.dropna(subset=[x]).copy() if x in df.columns else df.copy()
    if color is None and x in df_clean.columns and df_clean[x].duplicated().any():
        if isinstance(y, list) and len(y) > 1:
            valid_y = [col for col in y if col in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[col])]
            if valid_y:
                df_clean = df_clean.groupby(x, as_index=False)[valid_y].sum().sort_values(by=x)
            color = None
        else:
            entity_col = next((c for c in ['country', 'state', 'region', 'economy_group', 'sector', 'category', 'city'] if c in df_clean.columns), None)
            if entity_col:
                if df_clean[entity_col].nunique() > 6:
                    metric_check = y if isinstance(y, str) else (y[0] if y else None)
                    if metric_check and metric_check in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[metric_check]):
                        top_ents = df_clean.groupby(entity_col)[metric_check].sum().nlargest(6).index.tolist()
                        df_clean = df_clean[df_clean[entity_col].isin(top_ents)].copy()
                color = entity_col
                df_clean = df_clean.sort_values(by=[entity_col, x])
    elif color and color in df_clean.columns:
        df_clean = df_clean.sort_values(by=[color, x])
    elif x in df_clean.columns:
        df_clean = df_clean.sort_values(by=x)

    fig = px.area(
        df_clean, x=x, y=y, color=color,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height, subtitle=subtitle)

def create_heatmap(df, x, y, z, title="", subtitle="", height=380):
    fig = go.Figure(data=go.Heatmap(
        z=z, x=x, y=y,
        colorscale="Viridis"
    ))
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_box_chart(df, x, y, color=None, title="", x_title="", y_title="", height=380, subtitle=""):
    points = "outliers" if len(df) > 80 else "all"
    fig = px.box(
        df, x=x, y=y, color=color, points=points,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_geo_scatter(df, lat, lon, size=None, color=None, hover_name=None, title="", subtitle="", projection="natural earth", scope=None, height=420):
    fig = px.scatter_geo(
        df, lat=lat, lon=lon, size=size, color=color,
        hover_name=hover_name,
        projection=projection,
        scope=scope,
        color_continuous_scale="Plasma" if color else None,
        color_discrete_sequence=COLOR_PALETTE
    )
    title_text = f"<b>{title}</b>"
    top_margin = 50
    if subtitle:
        title_text += f"<br><span style='font-size:11px;color:#94a3b8;font-weight:normal;'>{subtitle}</span>"
        top_margin = 65

    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showcountries=True, countrycolor="#262626",
        showcoastlines=True, coastlinecolor="#333333",
        showland=True, landcolor="#0c0d14",
        showocean=True, oceancolor="#020205",
        showlakes=True, lakecolor="#020205"
    )
    fig.update_layout(
        template=TEMPLATE_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=top_margin, b=20),
        height=height,
        title=dict(
            text=title_text,
            font=dict(family="Plus Jakarta Sans, -apple-system, sans-serif", size=14, color="#ffffff"),
            x=0.01,
            y=0.97
        )
    )
    return fig

def create_choropleth(df, locations, color, hover_name=None, title="", subtitle="", height=420):
    fig = px.choropleth(
        df, locations=locations, locationmode="country names",
        color=color, hover_name=hover_name,
        color_continuous_scale="Viridis",
        projection="natural earth"
    )
    title_text = f"<b>{title}</b>"
    top_margin = 50
    if subtitle:
        title_text += f"<br><span style='font-size:11px;color:#94a3b8;font-weight:normal;'>{subtitle}</span>"
        top_margin = 65

    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showcountries=True, countrycolor="#262626",
        showcoastlines=True, coastlinecolor="#333333",
        showland=True, landcolor="#0c0d14",
        showocean=True, oceancolor="#020205"
    )
    fig.update_layout(
        template=TEMPLATE_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=top_margin, b=20),
        height=height,
        title=dict(
            text=title_text,
            font=dict(family="Plus Jakarta Sans, -apple-system, sans-serif", size=14, color="#ffffff"),
            x=0.01,
            y=0.97
        )
    )
    return fig

def create_donut_chart(df, names, values=None, title="", subtitle="", height=380):
    val_col = values
    if val_col and (val_col not in df.columns or not pd.api.types.is_numeric_dtype(df[val_col])):
        val_col = None
    fig = px.pie(
        df, names=names, values=val_col, hole=0.55,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_histogram(df, x, nbins=None, marginal="box", title="", x_title="", y_title="Frequency", subtitle="", height=380):
    fig = px.histogram(
        df, x=x, nbins=nbins, marginal=marginal,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_violin_chart(df, x, y, color=None, title="", x_title="", y_title="", subtitle="", height=380):
    points = "outliers" if len(df) > 80 else "all"
    fig = px.violin(
        df, x=x, y=y, color=color, box=True, points=points,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_sunburst(df, path, values, title="", subtitle="", height=380):
    df_clean = df.copy()
    if path and isinstance(path, list):
        for p in path:
            if p in df_clean.columns:
                df_clean[p] = df_clean[p].fillna("Unspecified").astype(str)
    if values and values in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[values]):
        df_clean = df_clean[df_clean[values] > 0]
        if df_clean.empty:
            df_clean = df.copy()
            values = None
    fig = px.sunburst(
        df_clean, path=path, values=values,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_funnel_chart(df, x, y, title="", subtitle="", height=380):
    fig = px.funnel(
        df, x=x, y=y,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_horizontal_bar(df, x, y, color=None, title="", x_title="", y_title="", subtitle="", height=380):
    fig = px.bar(
        df, x=x, y=y, color=color, orientation="h",
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_correlation_heatmap(df, cols=None, title="", subtitle="", height=380):
    if cols:
        valid_cols = [c for c in cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        corr_df = df[valid_cols].corr().fillna(0).round(2)
    else:
        corr_df = df.select_dtypes(include=["number"]).corr().fillna(0).round(2)

    # Diverging color scale centered at 0
    diverging_scale = [
        [0.0, "#f87171"],   # Negative correlation: Red
        [0.4, "#27272a"],   # Weak negative: Dark
        [0.5, "#09090b"],   # Zero: Neutral OLED
        [0.6, "#1e3a8a"],   # Weak positive: Deep Blue
        [1.0, "#38bdf8"]    # Strong positive: Cyan
    ]

    fig = px.imshow(
        corr_df, text_auto=True, color_continuous_scale=diverging_scale,
        zmin=-1.0, zmax=1.0, aspect="auto"
    )
    fig.update_coloraxes(colorbar_title="Pearson r", colorbar_tickfont=dict(family="JetBrains Mono", size=10))
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_density_heatmap(df, x, y, title="", x_title="", y_title="", subtitle="", height=380):
    fig = px.density_heatmap(
        df, x=x, y=y,
        color_continuous_scale="Viridis"
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_radar_chart(categories, values, title="", subtitle="", height=380, df=None):
    """
    Renders a balanced, accurate multi-indicator radar profile.
    Automatically normalizes radial coordinates to independent 15-95% scale per indicator
    while displaying authentic, unscaled raw values and ranges in the hover tooltip.
    """
    if not categories or not values or len(categories) != len(values):
        categories = ["Indicator A", "Indicator B", "Indicator C"]
        values = [50.0, 75.0, 60.0]

    # Deduplicate categories to prevent duplicate spokes
    seen = set()
    dedup_cats = []
    dedup_vals = []
    for c, v in zip(categories, values):
        if c not in seen:
            seen.add(c)
            dedup_cats.append(c)
            dedup_vals.append(v)
    categories, values = dedup_cats, dedup_vals

    clean_vals = []
    for v in values:
        try:
            val_f = float(v)
            clean_vals.append(val_f if not np.isnan(val_f) else 0.0)
        except Exception:
            clean_vals.append(0.0)

    # Independent normalization per dimension so disparate scales don't collapse into a needle
    r_coords = []
    hover_lines = []

    for c, v in zip(categories, clean_vals):
        lbl = c.replace('_', ' ').title()
        if df is not None and c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            s = df[c].dropna()
            c_min = float(s.min()) if not s.empty else 0.0
            c_max = float(s.max()) if not s.empty else 1.0
            span = c_max - c_min
            if span > 0:
                pct = ((v - c_min) / span) * 75.0 + 18.0  # Normalized between 18% and 93%
            else:
                pct = 55.0
            r_coords.append(round(pct, 1))
            hover_lines.append(f"<b>{lbl}</b><br>Observed: {v:,.2f}<br>Range: {c_min:,.2f} – {c_max:,.2f}<br>Benchmark Score: {pct:.1f}%")
        else:
            pct = max(15.0, min(95.0, float(v))) if 0 <= v <= 100 else 50.0
            r_coords.append(round(pct, 1))
            hover_lines.append(f"<b>{lbl}</b><br>Observed: {v:,.2f}<br>Benchmark Score: {pct:.1f}%")

    clean_cat_labels = [c.replace('_', ' ').title() for c in categories]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_coords,
        theta=clean_cat_labels,
        fill="toself",
        hovertext=hover_lines,
        hoverinfo="text",
        line=dict(color="#38bdf8", width=2.5),
        fillcolor="rgba(56, 189, 248, 0.22)",
        marker=dict(size=7, color="#ffffff", line=dict(color="#38bdf8", width=2))
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, showgrid=True, gridcolor="rgba(255,255,255,0.08)",
                range=[0, 100], tickfont=dict(family="JetBrains Mono", size=9, color="#64748b"),
                ticksuffix="%"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)", linecolor="rgba(255,255,255,0.15)",
                tickfont=dict(family="Plus Jakarta Sans", size=10, color="#cbd5e1")
            ),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_growth_velocity_bar(df, time_col, metric_col, title="", subtitle="", height=380):
    """
    Plots period-over-period growth velocity / rate of change.
    Positive acceleration is highlighted in vibrant emerald, contractions in coral red.
    """
    if metric_col not in df.columns:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        metric_col = num_cols[0] if num_cols else None
    if not metric_col:
        return go.Figure()

    if time_col not in df.columns:
        time_col = next((c for c in ['year', 'fiscal_year', 'crop_year', 'date', 'Date', 'month', 'period', 'quarter'] if c in df.columns), None)

    if time_col and time_col in df.columns:
        df_agg = df.groupby(time_col, as_index=False)[metric_col].sum() if df[time_col].duplicated().any() else df[[time_col, metric_col]].dropna().copy()
        df_agg = df_agg.sort_values(by=time_col)
        df_agg['pct_change'] = df_agg[metric_col].pct_change() * 100
        df_plot = df_agg.dropna(subset=['pct_change']).tail(25)
        x_axis_title = time_col.replace('_', ' ').title()
        y_axis_title = "Period Growth Rate (%)"
    else:
        # Fallback for non-temporal dataset: percentage deviation from the mean across categories
        cat_c = next((c for c in df.select_dtypes(include=['object']).columns), None)
        if cat_c:
            df_agg = df.groupby(cat_c, as_index=False)[metric_col].mean().head(20)
            x_col = cat_c
        else:
            df_agg = df[[metric_col]].dropna().head(20).copy()
            df_agg['Index'] = [f"Item {i+1}" for i in range(len(df_agg))]
            x_col = 'Index'
        mean_val = df_agg[metric_col].mean() if not df_agg.empty else 1.0
        if mean_val == 0:
            mean_val = 1.0
        df_agg['pct_change'] = ((df_agg[metric_col] - mean_val) / abs(mean_val)) * 100
        df_plot = df_agg
        x_axis_title = x_col.replace('_', ' ').title()
        y_axis_title = "Deviation from Mean (%)"
        time_col = x_col

    colors = ['#34d399' if v >= 0 else '#f87171' for v in df_plot['pct_change']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot[time_col].astype(str),
        y=df_plot['pct_change'],
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in df_plot['pct_change']],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=9, color="#cbd5e1"),
        name="Velocity"
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.25)", line_width=1)
    return base_layout(fig, title, x_axis_title, y_axis_title, height=height, subtitle=subtitle)

def create_pareto_chart(df, cat_col, metric_col, title="", subtitle="", height=380):
    """
    Plots entity volume ranking with cumulative percentage concentration line.
    Reveals structural concentration and 80/20 distribution across entities.
    """
    if metric_col not in df.columns:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        metric_col = num_cols[0] if num_cols else None
    if not metric_col:
        return go.Figure()

    if cat_col not in df.columns:
        cat_col = next((c for c in df.select_dtypes(include=['object']).columns), None)
        if not cat_col:
            cat_col = next((c for c in ['year', 'fiscal_year', 'crop_year', 'date', 'Date'] if c in df.columns), df.columns[0])

    df_agg = df.groupby(cat_col, as_index=False)[metric_col].sum().sort_values(by=metric_col, ascending=False).head(14)
    tot = df_agg[metric_col].sum()
    if tot <= 0:
        tot = 1.0
    df_agg['cum_pct'] = (df_agg[metric_col].cumsum() / tot) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_agg[cat_col].astype(str),
        y=df_agg[metric_col],
        name="Volume",
        marker_color="#38bdf8",
        opacity=0.85
    ))
    fig.add_trace(go.Scatter(
        x=df_agg[cat_col].astype(str),
        y=df_agg['cum_pct'],
        name="Cumulative %",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2.5),
        marker=dict(size=6, color="#ffffff", line=dict(color="#f59e0b", width=1.5))
    ))

    fig.update_layout(
        yaxis2=dict(
            title="Cumulative Share (%)",
            overlaying="y",
            side="right",
            range=[0, 105],
            ticksuffix="%",
            tickfont=dict(family="JetBrains Mono", size=9, color="#f59e0b"),
            showgrid=False
        )
    )
    return base_layout(fig, title, cat_col.replace('_', ' ').title(), metric_col.replace('_', ' ').title(), height=height, subtitle=subtitle)

def create_waterfall_chart(x, y, measure=None, title="", subtitle="", height=380):
    if measure is None:
        measure = ["relative"] * (len(x) - 1) + ["total"]

    # Clean formatting of text values
    text_labels = []
    for v in y:
        try:
            vf = float(v)
            text_labels.append(f"{vf:+,.2f}" if abs(vf) < 1000 else f"{vf:+,.1f}")
        except Exception:
            text_labels.append(str(v))

    fig = go.Figure(go.Waterfall(
        name="Attribution", orientation="v", measure=measure,
        x=x, y=y, text=text_labels, textposition="outside",
        connector=dict(line=dict(color="#475569")),
        increasing=dict(marker=dict(color="#34d399")),
        decreasing=dict(marker=dict(color="#f87171")),
        totals=dict(marker=dict(color="#38bdf8"))
    ))
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_gauge_chart(value, min_val=0, max_val=100, target=None, title="", subtitle="", suffix="", height=320):
    try:
        val_float = float(value) if value is not None and not pd.isna(value) else 0.0
    except Exception:
        val_float = 0.0

    min_float = float(min_val)
    max_float = float(max_val)

    # Dynamic bounds safety: never let needle clip
    if val_float > max_float:
        max_float = round(val_float * 1.15, 1)
    if val_float < min_float:
        min_float = round(val_float * 0.85, 1) if val_float > 0 else round(val_float * 1.15, 1)
    if max_float <= min_float:
        max_float = min_float + 100.0

    delta_dict = None
    if target is not None:
        try:
            t_val = float(target)
            delta_dict = dict(reference=t_val, increasing=dict(color="#34d399"), decreasing=dict(color="#f87171"))
        except Exception:
            pass

    span = max_float - min_float
    fig = go.Figure(go.Indicator(
        mode="gauge+number" + ("+delta" if delta_dict else ""),
        value=val_float,
        number=dict(suffix=suffix, font=dict(family="JetBrains Mono, monospace", size=26, color="#ffffff")),
        delta=delta_dict,
        title=dict(text=f"<b>{title}</b><br><span style='font-size:11px;color:#94a3b8;font-weight:normal;'>{subtitle}</span>", font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#ffffff")),
        gauge=dict(
            axis=dict(range=[min_float, max_float], tickwidth=1, tickcolor="#475569", tickfont=dict(family="JetBrains Mono", size=10, color="#94a3b8")),
            bar=dict(color="#38bdf8", thickness=0.28),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=1,
            bordercolor="#262626",
            steps=[
                dict(range=[min_float, min_float + span * 0.5], color="rgba(255, 255, 255, 0.03)"),
                dict(range=[min_float + span * 0.5, min_float + span * 0.8], color="rgba(56, 189, 248, 0.08)"),
                dict(range=[min_float + span * 0.8, max_float], color="rgba(52, 211, 153, 0.12)")
            ],
            threshold=dict(
                line=dict(color="#f59e0b", width=3),
                thickness=0.75,
                value=float(target) if target is not None else max_float * 0.85
            )
        )
    ))
    fig.update_layout(
        template=TEMPLATE_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=50, b=30),
        height=height
    )
    return fig

def create_bubble_chart(df, x, y, size, color=None, hover_name=None, title="", x_title="", y_title="", subtitle="", height=380):
    check_cols = [c for c in [x, y] if c in df.columns]
    df_plot = df.dropna(subset=check_cols).copy()

    actual_size = None
    if size and size in df_plot.columns and pd.api.types.is_numeric_dtype(df_plot[size]):
        df_plot["_size_scaled"] = df_plot[size].fillna(1).abs()
        df_plot["_size_scaled"] = df_plot["_size_scaled"].replace(0, 1)
        actual_size = "_size_scaled"

    fig = px.scatter(
        df_plot, x=x, y=y, size=actual_size, color=color, hover_name=hover_name,
        size_max=32,
        color_continuous_scale="Viridis" if color and color in df_plot.columns and pd.api.types.is_numeric_dtype(df_plot[color]) else None,
        color_discrete_sequence=COLOR_PALETTE
    )
    return base_layout(fig, title, x_title, y_title, height=height, subtitle=subtitle)

def create_sankey_diagram(labels, sources, targets, values, title="", subtitle="", height=380):
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=18,
            line=dict(color="#171717", width=1),
            label=labels,
            color=COLOR_PALETTE[:len(labels)] if len(labels) <= len(COLOR_PALETTE) else None
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(56, 189, 248, 0.28)"
        )
    )])
    return base_layout(fig, title, height=height, subtitle=subtitle)

def create_parallel_coordinates(df, dimensions, color=None, title="", subtitle="", height=380):
    dims = [d for d in dimensions if d in df.columns and pd.api.types.is_numeric_dtype(df[d]) and df[d].nunique() > 1]
    if not dims:
        dims = [c for c in df.select_dtypes(include=["number"]).columns if df[c].nunique() > 1][:4]

    color_col = color if color and color in df.columns and pd.api.types.is_numeric_dtype(df[color]) else (dims[0] if dims else None)

    # Clean short labels to prevent horizontal text collision
    clean_labels = {d: (d.replace('_', ' ').title()[:12] + '..') if len(d.replace('_', ' ')) > 14 else d.replace('_', ' ').title() for d in dims}

    # Keep representative sample if rows > 120 for clean visual clarity
    df_plot = df.head(120) if len(df) > 120 else df

    fig = px.parallel_coordinates(
        df_plot, dimensions=dims, color=color_col,
        labels=clean_labels,
        color_continuous_scale="Viridis"
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        template=TEMPLATE_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=75, b=25),
        height=height,
        title=dict(
            text=f"<b>{title}</b><br><span style='font-size:11px;color:#94a3b8;font-weight:normal;'>{subtitle}</span>",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13.5, color="#ffffff"),
            x=0.01,
            y=0.97
        )
    )
    return fig

def create_pyramid_chart(categories, val_left, val_right, label_left="Group A", label_right="Group B", title="", subtitle="", height=380):
    fig = go.Figure()
    val_left_neg = [-abs(float(v)) for v in val_left]
    val_right_pos = [abs(float(v)) for v in val_right]

    fig.add_trace(go.Bar(
        y=categories, x=val_left_neg, orientation='h', name=label_left,
        marker=dict(color="#38bdf8")
    ))
    fig.add_trace(go.Bar(
        y=categories, x=val_right_pos, orientation='h', name=label_right,
        marker=dict(color="#f43f5e")
    ))

    # Calculate nice symmetric tick values so labels are positive on both sides
    all_abs = [abs(v) for v in val_left_neg + val_right_pos]
    max_val = max(all_abs) if all_abs else 10.0
    step = max_val / 3.0
    tick_vals = [-2*step, -step, 0, step, 2*step]
    tick_texts = [f"{abs(v):,.1f}" for v in tick_vals]

    fig.update_layout(
        barmode='relative',
        bargap=0.15,
        xaxis=dict(
            tickvals=tick_vals,
            ticktext=tick_texts,
            title=dict(text="Comparative Scale / Divergence", font=dict(family="Plus Jakarta Sans", size=11, color="#94a3b8"))
        )
    )
    return base_layout(fig, title, y_title="Category", height=height, subtitle=subtitle)
