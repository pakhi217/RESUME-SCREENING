"""
utils/state.py
───────────────
Centralised Streamlit session-state initialisation and helpers.
Keeps all cross-page shared state in one predictable place.
"""

from __future__ import annotations
import streamlit as st


def init_session_state() -> None:
    """Initialise all session-state keys used across the app (idempotent)."""
    defaults = {
        "page":              "landing",     # current view: landing | app
        "active_nav":        "Dashboard",   # active sidebar nav item
        "resumes":           [],            # list of {"name","text","bytes","filename"}
        "jd_text":           "",
        "jd_title":          "",
        "analysis_results":  {},            # {candidate_name: result_dict}
        "analyzed":          False,
        "dark_mode":         True,
        "selected_candidate":None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis() -> None:
    st.session_state.analysis_results = {}
    st.session_state.analyzed = False


def go_to_app() -> None:
    st.session_state.page = "app"


def set_nav(page_name: str) -> None:
    st.session_state.active_nav = page_name
