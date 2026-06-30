"""
pages_logic/settings.py
─────────────────────────
⚙️ Settings — theme toggle, scoring weight info, data management.
"""

from __future__ import annotations
import streamlit as st
from utils.helpers import page_header, section_divider, toast_success, toast_info


def render() -> None:
    page_header(
        "Settings",
        "Configure your screening preferences",
        icon="⚙️",
    )

    # ── Appearance ───────────────────────────────────────────────────────────
    section_divider("Appearance")
    col1, col2 = st.columns(2)
    with col1:
        dark = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            toast_info("Theme preference updated. (Dark mode is the optimized default experience.)")
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding:1rem">
          <div style="color:#94a3b8;font-size:.8rem">
            ScreenAI is designed dark-first for reduced eye strain during long
            screening sessions, matching modern SaaS dashboards like Linear and Vercel.
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Scoring Model Info ───────────────────────────────────────────────────
    section_divider("Scoring Model")
    st.markdown("""
    <div class="glass-card">
      <div style="font-weight:600;margin-bottom:1rem">Weighted Scoring Formula</div>
      <div style="color:#94a3b8;font-size:.85rem;line-height:2">
        🔹 Semantic Similarity (Sentence Transformers) — <b style="color:#a78bfa">30%</b><br>
        🔹 TF-IDF Cosine Similarity — <b style="color:#a78bfa">20%</b><br>
        🔹 Skill Match — <b style="color:#a78bfa">25%</b><br>
        🔹 Keyword Match — <b style="color:#a78bfa">10%</b><br>
        🔹 Experience Match — <b style="color:#a78bfa">10%</b><br>
        🔹 Education Match — <b style="color:#a78bfa">5%</b>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Data Management ──────────────────────────────────────────────────────
    section_divider("Data Management")
    d1, d2, d3 = st.columns(3)
    with d1:
        if st.button("🗑️ Clear All Resumes", use_container_width=True):
            st.session_state.resumes = []
            st.session_state.analysis_results = {}
            st.session_state.analyzed = False
            toast_success("All resumes cleared.")
    with d2:
        if st.button("🗑️ Clear Job Description", use_container_width=True):
            st.session_state.jd_text = ""
            st.session_state.jd_title = ""
            toast_success("Job description cleared.")
    with d3:
        if st.button("🔄 Reset Everything", use_container_width=True):
            for key in ["resumes", "jd_text", "jd_title", "analysis_results", "analyzed"]:
                st.session_state[key] = [] if key == "resumes" else (
                    {} if key == "analysis_results" else (
                        False if key == "analyzed" else ""
                    )
                )
            toast_success("Application state reset.")

    # ── About ────────────────────────────────────────────────────────────────
    section_divider("About")
    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:2rem">
      <div style="font-size:1.5rem;margin-bottom:.5rem">🧠</div>
      <div style="font-weight:700;margin-bottom:.3rem">Resume Screening AI</div>
      <div style="color:#64748b;font-size:.8rem">Version 1.0.0 · Built with Streamlit, scikit-learn & Sentence Transformers</div>
    </div>""", unsafe_allow_html=True)
