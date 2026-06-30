"""
app.py
──────
Resume Screening AI — Main Application Entry Point

A premium, production-ready ATS-style resume screening platform built with
Streamlit. Handles routing between the landing page and the main dashboard
application (multi-page via sidebar navigation).

Run locally:
    streamlit run app.py

Deploy:
    Push to GitHub → Streamlit Community Cloud → point to app.py
"""

from __future__ import annotations
import streamlit as st

from utils.helpers import load_css, page_header, metric_card, card, badge
from utils.state import init_session_state, go_to_app, set_nav

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Resume Screening AI | Premium ATS Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Init ───────────────────────────────────────────────────────────────────────
init_session_state()
load_css()


# ════════════════════════════════════════════════════════════════════════════
#  LANDING PAGE
# ════════════════════════════════════════════════════════════════════════════

def render_landing() -> None:
    """Render the marketing / landing page shown before entering the app."""

    # Hide sidebar entirely on landing page
    st.markdown("""
    <style>
      [data-testid="stSidebar"] { display: none !important; }
      [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Top nav bar ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:1rem 0 2rem;">
      <div style="display:flex;align-items:center;gap:.6rem;font-weight:700;font-size:1.1rem;">
        <span style="font-size:1.4rem">🧠</span>
        <span>ScreenAI</span>
        <span class="badge badge-purple" style="margin-left:.4rem">PRO</span>
      </div>
      <div style="display:flex;gap:1.5rem;color:#94a3b8;font-size:.85rem;font-weight:500;">
        <span>Features</span><span>How it works</span><span>Pricing</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section animate-fade-up">
      <div class="hero-logo">🧠✨</div>
      <h1 class="hero-title">Screen Resumes Like a<br>Fortune 500 ATS</h1>
      <p class="hero-sub">
        AI-powered resume screening that combines semantic embeddings, TF-IDF
        similarity, and skill-graph matching to rank candidates in seconds —
        not hours.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        if st.button("🚀  Get Started", use_container_width=True, key="hero_cta"):
            go_to_app()
            st.rerun()

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── Animated Stats ───────────────────────────────────────────────────────
    stat_cols = st.columns(4)
    stats = [
        ("10,000+", "Resumes Screened"),
        ("94.2%", "Matching Accuracy"),
        ("3.2s", "Avg. Analysis Time"),
        ("500+", "Companies Trust Us"),
    ]
    for col, (num, label) in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center" class="animate-fade-up">
              <div class="stat-number">{num}</div>
              <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:3.5rem'></div>", unsafe_allow_html=True)

    # ── Feature Cards ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem">
      <h2 style="font-size:1.6rem;font-weight:700;margin-bottom:.5rem">
        Everything recruiters need
      </h2>
      <p style="color:#94a3b8;font-size:.9rem">
        From semantic matching to ATS scoring — one platform, zero spreadsheets.
      </p>
    </div>""", unsafe_allow_html=True)

    features = [
        ("🎯", "Semantic Matching", "Sentence-transformer embeddings understand context, not just keywords."),
        ("📊", "ATS Scoring", "Heuristic structure & formatting checks mirror real applicant tracking systems."),
        ("🏆", "Smart Ranking", "Auto-rank candidates with a weighted, explainable scoring model."),
        ("🧩", "Skill Graphs", "Extract and visualize skills across 7 technical & soft-skill categories."),
        ("📄", "PDF Reports", "Generate polished, shareable candidate reports in one click."),
        ("⚡", "Bulk Upload", "Drag-and-drop dozens of resumes — PDF & DOCX both supported."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card animate-fade-up">
              <div class="feature-icon">{icon}</div>
              <div class="feature-title">{title}</div>
              <div class="feature-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── Bottom CTA ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card animate-glow" style="text-align:center;padding:3rem 2rem">
      <h2 style="font-size:1.4rem;font-weight:700;margin-bottom:.5rem">
        Ready to upgrade your screening process?
      </h2>
      <p style="color:#94a3b8;font-size:.9rem;margin-bottom:1.5rem">
        No credit card. No setup. Just upload and analyze.
      </p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("Launch Dashboard →", use_container_width=True, key="bottom_cta"):
            go_to_app()
            st.rerun()

    st.markdown("""
    <div style="text-align:center;color:#475569;font-size:.78rem;padding:3rem 0 1rem">
      Built with Python · Streamlit · Sentence Transformers · scikit-learn
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION (app mode)
# ════════════════════════════════════════════════════════════════════════════

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("📄", "Resume Upload"),
    ("💼", "Job Description"),
    ("📊", "Analysis"),
    ("🏆", "Candidate Ranking"),
    ("⚙️", "Settings"),
]


def render_sidebar() -> str:
    """Render sidebar nav; return the selected page name."""
    with st.sidebar:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:.6rem;padding:0 .5rem 1.5rem;">
          <span style="font-size:1.5rem">🧠</span>
          <span style="font-weight:700;font-size:1.05rem">ScreenAI</span>
        </div>
        """, unsafe_allow_html=True)

        selected = st.session_state.active_nav
        for icon, label in NAV_ITEMS:
            is_active = (selected == label)
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{label}",
                         use_container_width=True, type=btn_type):
                set_nav(label)
                st.rerun()

        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        # Quick status panel
        n_resumes = len(st.session_state.resumes)
        has_jd = bool(st.session_state.jd_text.strip())
        st.markdown(f"""
        <div style="padding:.75rem .5rem;font-size:.78rem;color:#64748b">
          <div style="margin-bottom:.4rem">📄 Resumes: <b style="color:#a78bfa">{n_resumes}</b></div>
          <div style="margin-bottom:.4rem">💼 JD Ready: <b style="color:{'#4ade80' if has_jd else '#f87171'}">{'Yes' if has_jd else 'No'}</b></div>
          <div>📊 Analyzed: <b style="color:{'#4ade80' if st.session_state.analyzed else '#f87171'}">{'Yes' if st.session_state.analyzed else 'No'}</b></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("⬅️  Back to Landing", use_container_width=True, key="back_landing"):
            st.session_state.page = "landing"
            st.rerun()

    return selected


# ════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTER
# ════════════════════════════════════════════════════════════════════════════

def render_app() -> None:
    """Render the main multi-page application shell."""
    active = render_sidebar()

    if active == "Dashboard":
        from pages_logic import dashboard
        dashboard.render()
    elif active == "Resume Upload":
        from pages_logic import resume_upload
        resume_upload.render()
    elif active == "Job Description":
        from pages_logic import job_description
        job_description.render()
    elif active == "Analysis":
        from pages_logic import analysis
        analysis.render()
    elif active == "Candidate Ranking":
        from pages_logic import ranking
        ranking.render()
    elif active == "Settings":
        from pages_logic import settings
        settings.render()


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "landing":
    render_landing()
else:
    render_app()
