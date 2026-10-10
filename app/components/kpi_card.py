"""
Reusable Component: Executive KPI Metric Card
Renders a high-contrast, institutional metric tile with tabular figures, status indicators, and context.
Designed for executive readability, zero visual clutter, and precision data visualization.
"""

import streamlit as st
try:
    from app.components.html_utils import render_html
except (ImportError, ModuleNotFoundError):
    from .html_utils import render_html

def _infer_icon(label: str) -> str:
    lbl = label.lower()
    if any(k in lbl for k in ["gdp", "revenue", "income", "usd", "rs", "inr", "crore", "market", "turnover", "spend", "cost", "expenditure"]):
        return "💰"
    elif any(k in lbl for k in ["growth", "rate", "percent", "%", "inflation", "cpi", "index", "ratio", "change", "expansion"]):
        return "📈"
    elif any(k in lbl for k in ["power", "energy", "solar", "wind", "grid", "capacity", "gw", "mw", "electricity", "generation"]):
        return "⚡"
    elif any(k in lbl for k in ["population", "people", "citizen", "worker", "labor", "demographic", "census", "resident"]):
        return "👥"
    elif any(k in lbl for k in ["crop", "agriculture", "food", "harvest", "yield", "tonnes", "wheat", "rice"]):
        return "🌾"
    elif any(k in lbl for k in ["temp", "climate", "co2", "emission", "rainfall", "monsoon", "carbon", "warm"]):
        return "🌡️"
    elif any(k in lbl for k in ["health", "hospital", "nutrition", "mortality", "birth", "medical"]):
        return "🏥"
    elif any(k in lbl for k in ["sovereign", "ministry", "central bank", "rbi", "government", "policy"]):
        return "🏛️"
    elif any(k in lbl for k in ["station", "highway", "rail", "freight", "transport", "km"]):
        return "🚆"
    return "📊"

def render_kpi(label, value, delta=None, delta_text="", footnote=None, status="neutral", icon=None):
    """
    Renders an executive metric card.
    label: str (Indicator Title)
    value: str or number (Formatted Value)
    delta: str or None (e.g. "+7.2% Real YoY")
    delta_text: str or None (Fallback subtext)
    footnote: str or None (Benchmark context)
    status: "pos", "neg", "neutral", "gold"
    icon: str or None (Optional override icon)
    """
    delta_class = "delta-neutral"
    status_icon = "●"
    top_color = "#38bdf8"

    if status == "pos":
        delta_class = "delta-pos"
        status_icon = "▲"
        top_color = "#34d399"
    elif status == "neg":
        delta_class = "delta-neg"
        status_icon = "▼"
        top_color = "#f87171"
    elif status == "gold":
        delta_class = "badge-showcase"
        status_icon = "★"
        top_color = "#facc15"

    metric_icon = icon or _infer_icon(label)
    effective_delta = delta or delta_text
    
    delta_html = ""
    if effective_delta:
        delta_html = f'<span class="kpi-delta {delta_class}"><span>{status_icon}</span> {effective_delta}</span>'

    footnote_html = ""
    if footnote:
        footnote_html = f'<div class="kpi-footnote">{footnote}</div>'
    html = f"""<div class="kpi-container" style="border-top: 2px solid {top_color} !important;">
<div class="kpi-label">
<span>{label}</span>
<span style="font-size: 0.95rem; opacity: 0.85;">{metric_icon}</span>
</div>
<div class="kpi-value">{value}</div>
<div>{delta_html}</div>
{footnote_html}
</div>"""
    render_html(html)
