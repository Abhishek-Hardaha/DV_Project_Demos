"""
Reusable Component: Executive Platform Header & Breadcrumb Bar
Delivers an institutional, custom-designed command header across all views.
"""

try:
    from app.components.html_utils import render_html
except (ImportError, ModuleNotFoundError):
    from .html_utils import render_html

def render_header(title="Data Visualization Intelligence Suite", subtitle=None, active_view=None, meta_chips=None):
    """
    Renders a bespoke executive header with status pills, breadcrumb navigation, and institutional styling.
    Guaranteed zero markdown code block formatting artifacts.
    """
    sub_html = f'<div class="hero-subtitle" style="font-size: 0.95rem; color: #94a3b8; line-height: 1.5; max-width: 900px; margin-top: 6px;">{subtitle}</div>' if subtitle else ""
    
    view_pill = ""
    if active_view:
        view_pill = f'<span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.3); letter-spacing: 0.04em;">{active_view.upper()}</span>'

    chips_html = ""
    if meta_chips:
        chips_items = "".join([f'<span class="badge badge-live" style="margin: 0;">{chip}</span>' for chip in meta_chips])
        chips_html = f'<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px;">{chips_items}</div>'

    html = f"""<div class="hero-container" style="background: linear-gradient(135deg, #09090d 0%, #0d0f17 50%, #07070a 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 26px 30px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7);">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 8px;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="background: rgba(16, 185, 129, 0.15); color: #34d399; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(16, 185, 129, 0.35); letter-spacing: 0.04em; display: inline-flex; align-items: center; gap: 5px;">
<span style="width: 6px; height: 6px; border-radius: 50%; background: #34d399; box-shadow: 0 0 6px #34d399;"></span>
VERIFIED OFFICIAL DATA
</span>
{view_pill}
</div>
<div style="font-size: 0.76rem; color: #64748b; font-weight: 600; letter-spacing: 0.03em;">
OFFICIAL PUBLIC DATA PLATFORM
</div>
</div>
<div class="hero-title" style="font-size: 2.15rem; font-weight: 800; letter-spacing: -0.025em; margin: 6px 0 10px 0; background: linear-gradient(to right, #ffffff 30%, #7dd3fc 70%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
{title}
</div>
{sub_html}
{chips_html}
</div>"""
    render_html(html)
