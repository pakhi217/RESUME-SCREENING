"""
utils/charts.py
───────────────
Plotly chart factory for Resume Screening AI.
All charts share the dark glassmorphism design language.
"""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Any

# ── Shared theme ──────────────────────────────────────────────────────────────

_COLORS = {
    "purple": "#8b5cf6",
    "blue":   "#3b82f6",
    "cyan":   "#06b6d4",
    "green":  "#4ade80",
    "amber":  "#fbbf24",
    "red":    "#f87171",
    "pink":   "#f472b6",
}

_PALETTE = list(_COLORS.values())

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(17,17,24,.8)",
        bordercolor="rgba(255,255,255,.06)",
        borderwidth=1,
        font=dict(size=11),
    ),
)

_AXIS_BASE = dict(
    gridcolor="rgba(255,255,255,.05)",
    zerolinecolor="rgba(255,255,255,.08)",
    tickfont=dict(size=11),
)


def _layout(**kwargs) -> dict:
    d = {**_LAYOUT_BASE}
    d.update(kwargs)
    return d


# ── Radar chart ───────────────────────────────────────────────────────────────

def radar_chart(categories: list[str], values: list[float], title: str = "Skill Radar") -> go.Figure:
    """Radar / spider chart for multi-dimensional score display."""
    cats = categories + [categories[0]]    # close the polygon
    vals = values + [values[0]]

    fig = go.Figure(go.Scatterpolar(
        r=vals,
        theta=cats,
        fill="toself",
        fillcolor="rgba(139,92,246,.18)",
        line=dict(color=_COLORS["purple"], width=2),
        marker=dict(size=5, color=_COLORS["purple"]),
        hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text=title, font=dict(size=14, color="#f1f5f9"))),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,.07)",
                tickfont=dict(size=9, color="#475569"),
                ticksuffix="%",
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,.05)",
                tickfont=dict(size=10, color="#94a3b8"),
            ),
        ),
    )
    return fig


# ── Skill distribution pie ────────────────────────────────────────────────────

def skill_pie(skills_by_cat: dict[str, list[str]], title: str = "Skill Distribution") -> go.Figure:
    """Donut pie chart of skills per category."""
    labels = list(skills_by_cat.keys())
    values = [len(v) for v in skills_by_cat.values()]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=_PALETTE, line=dict(color="rgba(0,0,0,.2)", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{value} skills (%{percent})<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text=title, font=dict(size=14, color="#f1f5f9"))),
        showlegend=True,
    )
    return fig


# ── Horizontal skill bars ─────────────────────────────────────────────────────

def skill_bar_chart(skills: list[str], scores: list[float], title: str = "Skill Scores") -> go.Figure:
    """Horizontal bar chart for individual skill strengths."""
    colors = [_COLORS["green"] if s >= 70 else _COLORS["amber"] if s >= 40 else _COLORS["red"]
              for s in scores]

    fig = go.Figure(go.Bar(
        y=skills,
        x=scores,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(0,0,0,.15)", width=1),
            cornerradius=6,
        ),
        text=[f"{s:.0f}%" for s in scores],
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text=title, font=dict(size=14, color="#f1f5f9"))),
        xaxis=dict(**_AXIS_BASE, range=[0, 110], ticksuffix="%"),
        yaxis=dict(**_AXIS_BASE, autorange="reversed"),
        height=max(250, len(skills) * 38),
    )
    return fig


# ── Score comparison bar ──────────────────────────────────────────────────────

def score_comparison_bar(
    categories: list[str],
    scores: list[float],
    title: str = "Score Breakdown",
) -> go.Figure:
    """Vertical grouped bar chart comparing score dimensions."""
    grad_colors = [
        f"rgba({int(r)},{int(g)},{int(b)},0.85)"
        for r, g, b in [
            (139, 92, 246), (59, 130, 246), (6, 182, 212),
            (74, 222, 128), (251, 191, 36), (248, 113, 113), (244, 114, 182),
        ]
    ][:len(categories)]

    fig = go.Figure(go.Bar(
        x=categories,
        y=scores,
        marker=dict(
            color=grad_colors,
            line=dict(color="rgba(0,0,0,.1)", width=1),
            cornerradius=8,
        ),
        text=[f"{s:.0f}%" for s in scores],
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text=title, font=dict(size=14, color="#f1f5f9"))),
        xaxis=dict(**_AXIS_BASE),
        yaxis=dict(**_AXIS_BASE, range=[0, 115], ticksuffix="%"),
        height=320,
    )
    return fig


# ── Multi-candidate comparison ────────────────────────────────────────────────

def candidate_comparison_bar(
    names: list[str],
    scores: list[float],
    metric: str = "Overall Match",
) -> go.Figure:
    """Bar chart ranking multiple candidates by a single metric."""
    sorted_pairs = sorted(zip(scores, names), reverse=True)
    s_scores, s_names = zip(*sorted_pairs) if sorted_pairs else ([], [])

    colors = [
        (_COLORS["purple"] if i == 0 else
         _COLORS["blue"]   if i == 1 else
         _COLORS["cyan"])
        for i in range(len(s_names))
    ]

    fig = go.Figure(go.Bar(
        x=list(s_names),
        y=list(s_scores),
        marker=dict(color=colors, cornerradius=10),
        text=[f"{v:.1f}%" for v in s_scores],
        textposition="outside",
        textfont=dict(size=12, color="#f1f5f9"),
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text=f"Candidate Ranking — {metric}", font=dict(size=14, color="#f1f5f9"))),
        xaxis=dict(**_AXIS_BASE),
        yaxis=dict(**_AXIS_BASE, range=[0, 110], ticksuffix="%"),
        height=340,
    )
    return fig


# ── Multi-metric grouped bar (candidate comparison) ───────────────────────────

def multi_metric_radar(
    candidates: list[dict],          # [{'name': str, 'result': dict}]
    metrics: list[str] | None = None,
) -> go.Figure:
    """Overlapping radar charts for ≤ 5 candidates."""
    if metrics is None:
        metrics = ["overall_match", "ats_score", "skill_match",
                   "keyword_match", "experience", "education"]

    labels = [m.replace("_", " ").title() for m in metrics]
    palette = [_COLORS["purple"], _COLORS["blue"], _COLORS["cyan"],
               _COLORS["green"], _COLORS["amber"]]

    fig = go.Figure()
    for i, cand in enumerate(candidates[:5]):
        r = cand["result"]
        vals = [r.get(m, 0) for m in metrics]
        vals_closed = vals + [vals[0]]
        labs_closed = labels + [labels[0]]
        color = palette[i % len(palette)]

        fig.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=labs_closed,
            fill="toself",
            fillcolor=color.replace(")", ",.12)").replace("rgb", "rgba"),
            line=dict(color=color, width=2),
            name=cand["name"],
            hovertemplate=f"{cand['name']}<br>%{{theta}}: %{{r:.1f}}%<extra></extra>",
        ))

    fig.update_layout(
        **_layout(title=dict(text="Candidate Comparison Radar", font=dict(size=14, color="#f1f5f9"))),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="rgba(255,255,255,.07)",
                            tickfont=dict(size=9, color="#475569"),
                            ticksuffix="%"),
            angularaxis=dict(gridcolor="rgba(255,255,255,.05)",
                             tickfont=dict(size=10, color="#94a3b8")),
        ),
        height=430,
    )
    return fig


# ── Keyword density bar ───────────────────────────────────────────────────────

def keyword_density_chart(keywords: list[str], found: list[str]) -> go.Figure:
    """Show which JD keywords are found vs. missing in the resume."""
    found_set = set(found)
    colors = [_COLORS["green"] if k in found_set else _COLORS["red"] for k in keywords]

    fig = go.Figure(go.Bar(
        y=keywords,
        x=[1] * len(keywords),
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,.1)", width=1), cornerradius=4),
        text=["✓ Found" if k in found_set else "✗ Missing" for k in keywords],
        textposition="inside",
        textfont=dict(size=10, color="#ffffff"),
        hovertemplate="%{y}<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title=dict(text="Keyword Coverage", font=dict(size=14, color="#f1f5f9"))),
        xaxis=dict(visible=False),
        yaxis=dict(**_AXIS_BASE, autorange="reversed"),
        height=max(250, len(keywords) * 28),
        showlegend=False,
    )
    return fig
