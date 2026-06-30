"""
pages_logic/ranking.py
────────────────────────
🏆 Candidate Ranking — leaderboard with search, filters, sorting,
candidate comparison, and CSV export.
"""

from __future__ import annotations
import streamlit as st

from utils.helpers import page_header, section_divider, badge, score_color
from utils.charts import candidate_comparison_bar, multi_metric_radar
from models.report_generator import generate_csv_report


def render() -> None:
    page_header(
        "Candidate Ranking",
        "Leaderboard of all screened candidates, ranked by overall match",
        icon="🏆",
    )

    results = st.session_state.analysis_results
    if not results:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem">
          <div style="font-size:2.5rem;margin-bottom:1rem">🏆</div>
          <div style="font-weight:600;margin-bottom:.5rem">No candidates ranked yet</div>
          <div style="color:#94a3b8;font-size:.85rem">
            Run an analysis first to see the leaderboard here.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filters / Search / Sort ──────────────────────────────────────────────
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search = st.text_input("🔍 Search candidates", placeholder="Type a candidate name...")
    with f2:
        min_score = st.slider("Min. Match %", 0, 100, 0)
    with f3:
        sort_by = st.selectbox("Sort by", ["Overall Match", "ATS Score", "Skill Match", "Experience"])

    sort_key_map = {
        "Overall Match": "overall_match",
        "ATS Score":     "ats_score",
        "Skill Match":   "skill_match",
        "Experience":    "experience",
    }
    sort_key = sort_key_map[sort_by]

    # Filter + sort
    items = [
        (name, r) for name, r in results.items()
        if (search.lower() in name.lower() if search else True)
        and r["overall_match"] >= min_score
    ]
    items.sort(key=lambda kv: kv[1][sort_key], reverse=True)

    if not items:
        st.warning("No candidates match the current filters.")
        return

    # ── Leaderboard Table ────────────────────────────────────────────────────
    section_divider(f"Leaderboard ({len(items)} candidates)")

    for i, (name, r) in enumerate(items):
        rank = i + 1
        is_best = (rank == 1)
        rank_color = "#fbbf24" if rank == 1 else "#94a3b8" if rank == 2 else "#cd7f32" if rank == 3 else "#475569"
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        match_color = score_color(r["overall_match"])

        recommendation = (
            "Strong Hire" if r["overall_match"] >= 80 else
            "Hire" if r["overall_match"] >= 60 else
            "Consider" if r["overall_match"] >= 40 else
            "Not a Fit"
        )
        rec_badge_color = {
            "Strong Hire": "green", "Hire": "blue", "Consider": "amber", "Not a Fit": "red"
        }[recommendation]

        skills_preview = ", ".join(
            s for lst in r.get("resume_skills", {}).values() for s in lst
        )[:60] or "—"

        row_class = "leaderboard-row gold" if is_best else "leaderboard-row"
        st.markdown(f"""
        <div class="{row_class}">
          <div class="rank-badge" style="background:rgba(255,255,255,.06);color:{rank_color}">{medal if rank<=3 else rank}</div>
          <div style="flex:1.5">
            <div style="font-weight:700;font-size:.92rem">{name}</div>
            <div style="color:#64748b;font-size:.75rem;margin-top:2px">{skills_preview}</div>
          </div>
          <div style="flex:1;text-align:center">
            <div style="font-weight:700;color:{match_color};font-size:1rem">{r['overall_match']:.0f}%</div>
            <div style="color:#475569;font-size:.7rem">MATCH</div>
          </div>
          <div style="flex:1;text-align:center">
            <div style="font-weight:600;color:#e2e8f0;font-size:.9rem">{r['ats_score']:.0f}%</div>
            <div style="color:#475569;font-size:.7rem">ATS</div>
          </div>
          <div style="flex:1;text-align:center">
            <div style="font-weight:600;color:#e2e8f0;font-size:.9rem">{r['skill_match']:.0f}%</div>
            <div style="color:#475569;font-size:.7rem">SKILLS</div>
          </div>
          <div style="flex:1;text-align:center">
            <div style="font-weight:600;color:#e2e8f0;font-size:.9rem">{r['experience']:.0f}%</div>
            <div style="color:#475569;font-size:.7rem">EXPERIENCE</div>
          </div>
          <div style="flex:1.2;text-align:right">
            <span class="badge badge-{rec_badge_color}">{recommendation}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Comparison Chart ─────────────────────────────────────────────────────
    section_divider("Visual Comparison")
    names_list = [name for name, _ in items]
    scores_list = [r["overall_match"] for _, r in items]

    cmp_col1, cmp_col2 = st.columns(2)
    with cmp_col1:
        st.plotly_chart(candidate_comparison_bar(names_list, scores_list), use_container_width=True)
    with cmp_col2:
        compare_data = [{"name": n, "result": r} for n, r in items[:5]]
        st.plotly_chart(multi_metric_radar(compare_data), use_container_width=True)

    # ── Export ───────────────────────────────────────────────────────────────
    section_divider("Export Results")
    e1, e2 = st.columns(2)
    with e1:
        csv_data = generate_csv_report([{"name": n, "result": r} for n, r in items])
        st.download_button(
            "⬇️ Download Ranked Results (CSV)",
            data=csv_data,
            file_name="candidate_ranking.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with e2:
        st.button("📊 Download Full Comparison Report", use_container_width=True, disabled=True,
                   help="Coming soon — combine all candidate PDFs into one report.")
