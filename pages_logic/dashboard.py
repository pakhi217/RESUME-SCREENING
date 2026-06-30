"""
pages_logic/dashboard.py
─────────────────────────
🏠 Dashboard — overview page with KPIs, quick actions, and recent activity.
"""

from __future__ import annotations
import streamlit as st
from utils.helpers import page_header, metric_card, card, badge, section_divider
from utils.state import set_nav


def render() -> None:
    page_header(
        "Dashboard",
        "Overview of your resume screening pipeline",
        icon="🏠",
    )

    resumes   = st.session_state.resumes
    results   = st.session_state.analysis_results
    has_jd    = bool(st.session_state.jd_text.strip())
    n_resumes = len(resumes)
    n_results = len(results)

    avg_match = (
        sum(r["overall_match"] for r in results.values()) / n_results
        if n_results else 0
    )
    top_score = max((r["overall_match"] for r in results.values()), default=0)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("📄", str(n_resumes), "Resumes Uploaded"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("💼", "Ready" if has_jd else "Empty", "Job Description"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("📊", f"{avg_match:.0f}%", "Avg. Match Score"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("🏆", f"{top_score:.0f}%", "Top Candidate Score"), unsafe_allow_html=True)

    section_divider("Quick Actions")

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-size:1.5rem;margin-bottom:.5rem">📤</div>
          <div style="font-weight:600;margin-bottom:.3rem">Upload Resumes</div>
          <div style="color:#94a3b8;font-size:.82rem;margin-bottom:1rem">
            Drag & drop PDF or DOCX resumes — bulk upload supported.
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to Upload →", key="qa_upload", use_container_width=True):
            set_nav("Resume Upload"); st.rerun()

    with a2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-size:1.5rem;margin-bottom:.5rem">💼</div>
          <div style="font-weight:600;margin-bottom:.3rem">Add Job Description</div>
          <div style="color:#94a3b8;font-size:.82rem;margin-bottom:1rem">
            Paste, upload, or pick a sample JD to screen against.
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to JD →", key="qa_jd", use_container_width=True):
            set_nav("Job Description"); st.rerun()

    with a3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-size:1.5rem;margin-bottom:.5rem">🚀</div>
          <div style="font-weight:600;margin-bottom:.3rem">Run Analysis</div>
          <div style="color:#94a3b8;font-size:.82rem;margin-bottom:1rem">
            Score candidates with TF-IDF + semantic embeddings.
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to Analysis →", key="qa_analysis", use_container_width=True):
            set_nav("Analysis"); st.rerun()

    # ── Recent Candidates ────────────────────────────────────────────────────
    if results:
        section_divider("Recent Candidates")
        sorted_results = sorted(results.items(), key=lambda kv: kv[1]["overall_match"], reverse=True)
        for i, (name, r) in enumerate(sorted_results[:5]):
            color = "#4ade80" if r["overall_match"] >= 70 else "#fbbf24" if r["overall_match"] >= 45 else "#f87171"
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "▫️"
            st.markdown(f"""
            <div class="leaderboard-row">
              <span style="margin-right:.75rem;font-size:1.1rem">{medal}</span>
              <div style="flex:1">
                <div style="font-weight:600">{name}</div>
                <div style="color:#64748b;font-size:.78rem">ATS: {r['ats_score']:.0f}% · Skills: {r['skill_match']:.0f}%</div>
              </div>
              <div style="font-size:1.2rem;font-weight:700;color:{color}">{r['overall_match']:.0f}%</div>
            </div>""", unsafe_allow_html=True)
    else:
        section_divider("Getting Started")
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2.5rem">
          <div style="font-size:2rem;margin-bottom:1rem">✨</div>
          <div style="font-weight:600;margin-bottom:.5rem">No analysis yet</div>
          <div style="color:#94a3b8;font-size:.85rem">
            Upload resumes and a job description, then run the analysis to see results here.
          </div>
        </div>""", unsafe_allow_html=True)
