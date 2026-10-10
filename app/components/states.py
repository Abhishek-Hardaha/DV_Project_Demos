"""
Reusable Component: State Indicators & Empty State Renderers
Provides purpose-built analytical feedback for searches, filters, loading, and offline fallbacks.
"""

import streamlit as st
try:
    from app.components.html_utils import render_html
except (ImportError, ModuleNotFoundError):
    from .html_utils import render_html

def render_empty_state(title="No Observations Found", description="No verified records match the active filter criteria. Try adjusting your time horizon or categorical selections.", icon="🔍"):
    """
    Renders an elegant empty state container.
    """
    html = f"""
    <div class="empty-state-box">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-description">{description}</div>
    </div>
    """
    render_html(html)

def render_cache_notice(source_org, timestamp="Verified Release"):
    """
    Renders an offline fallback or cache guarantee notice.
    """
    html = f"""
    <div style="display: flex; align-items: center; justify-content: space-between; background: #050505; border: 1px solid #171717; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #94a3b8;">
            <span class="auth-live-dot"></span>
            <span><b>Sovereign Cache Verified:</b> Sourced from <code>{source_org}</code> ({timestamp}). Zero synthetic fallbacks.</span>
        </div>
        <span class="offline-cache-badge">AUTHENTIC ARCHIVE</span>
    </div>
    """
    render_html(html)
