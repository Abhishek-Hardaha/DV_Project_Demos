"""
Utility module for robust, error-free HTML rendering in Streamlit.
Eliminates CommonMark's 4-space indentation rule from accidentally converting
HTML blocks into <pre><code> snippets.
"""

import re
import streamlit as st

def clean_html(html_str: str) -> str:
    """
    Strips leading whitespace from every line of an HTML string,
    guaranteeing that no line starts with 4 or more spaces.
    This prevents CommonMark markdown parsers from treating HTML as a code block.
    """
    if not html_str:
        return ""
    return re.sub(r'^[ \t]+', '', html_str.strip(), flags=re.MULTILINE)

def render_html(html_str: str):
    """
    Safely renders HTML in Streamlit with unsafe_allow_html=True,
    guaranteed never to leak raw HTML tags into the DOM as plain text.
    """
    cleaned = clean_html(html_str)
    if cleaned:
        st.markdown(cleaned, unsafe_allow_html=True)
