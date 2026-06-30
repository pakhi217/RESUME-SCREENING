"""
utils/helpers.py
────────────────
Shared helper utilities for Resume Screening AI.
Covers: CSS injection, HTML components, color math, formatting.
"""

from __future__ import annotations
import os
import re
import math
import base64
import pathlib
import streamlit as st


# ── CSS ───────────────────────────────────────────────────────────────────────

def load_css() -> None:
    """Inject global stylesheet into every Streamlit page."""
    css_path = pathlib.Path(__file__).parent.parent / "css" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


# ── HTML Components ───────────────────────────────────────────────────────────

def card(content: str, extra_class: str = "") -> str:
    """Wrap content in a glassmorphism card."""
    return f'<div class="glass-card {extra_class}">{content}</div>'


def metric_card(icon: str, value: str, label: str, delta: str = "") -> str:
    """Render a KPI metric card with optional delta."""
    delta_html = (
        f'<span style="font-size:.75rem;color:#4ade80;margin-left:.5rem">▲ {delta}</span>'
        if delta else ""
    )
    return f"""
    <div class="metric-card animate-fade-up">
      <div class="metric-icon">{icon}</div>
      <div class="metric-value">{value}{delta_html}</div>
      <div class="metric-label">{label}</div>
    </div>"""


def badge(text: str, color: str = "purple") -> str:
    """Render a small colored badge/pill."""
    return f'<span class="badge badge-{color}">{text}</span>'


def page_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a consistent page header."""
    icon_html = f'<span style="margin-right:.5rem">{icon}</span>' if icon else ""
    st.markdown(f"""
    <div class="page-header animate-fade-up">
      <h1>{icon_html}{title}</h1>
      {'<p>' + subtitle + '</p>' if subtitle else ''}
    </div>""", unsafe_allow_html=True)


def section_divider(label: str = "") -> None:
    """Render a subtle section divider with optional label."""
    if label:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1rem;margin:1.5rem 0">
          <hr style="flex:1;border-top:1px solid rgba(255,255,255,.06);margin:0">
          <span style="font-size:.7rem;font-weight:600;color:#475569;
                       text-transform:uppercase;letter-spacing:.1em;white-space:nowrap">
            {label}
          </span>
          <hr style="flex:1;border-top:1px solid rgba(255,255,255,.06);margin:0">
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<hr>', unsafe_allow_html=True)


# ── Score / Progress Rings ────────────────────────────────────────────────────

def score_color(score: float) -> str:
    """Return a hex color based on score (0–100)."""
    if score >= 75:
        return "#4ade80"   # green
    elif score >= 50:
        return "#fbbf24"   # amber
    elif score >= 30:
        return "#fb923c"   # orange
    else:
        return "#f87171"   # red


def svg_ring(score: float, label: str, size: int = 120) -> str:
    """
    Generate an SVG circular progress ring.
    Uses stroke-dasharray math for the arc fill.
    """
    radius    = (size / 2) - 10
    circ      = 2 * math.pi * radius
    filled    = (score / 100) * circ
    color     = score_color(score)
    cx = cy   = size / 2
    font_size = size * 0.18

    return f"""
    <div class="score-ring-container">
      <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <!-- Track ring -->
        <circle cx="{cx}" cy="{cy}" r="{radius}"
          fill="none" stroke="rgba(255,255,255,.06)" stroke-width="8"/>
        <!-- Filled arc -->
        <circle cx="{cx}" cy="{cy}" r="{radius}"
          fill="none" stroke="{color}" stroke-width="8"
          stroke-linecap="round"
          stroke-dasharray="{filled:.1f} {circ:.1f}"
          transform="rotate(-90 {cx} {cy})"/>
        <!-- Score text -->
        <text x="{cx}" y="{cy + font_size * .38}"
          text-anchor="middle" fill="{color}"
          font-size="{font_size}px" font-weight="700"
          font-family="Inter, sans-serif">{score:.0f}%</text>
      </svg>
      <div class="score-ring-label">{label}</div>
    </div>"""


# ── Skill Bar ─────────────────────────────────────────────────────────────────

def skill_bar(name: str, pct: float) -> str:
    """Render an animated horizontal skill bar."""
    color = score_color(pct)
    return f"""
    <div class="skill-bar-container">
      <div class="skill-bar-header">
        <span style="color:var(--text-primary);font-weight:500">{name}</span>
        <span style="color:{color};font-weight:600">{pct:.0f}%</span>
      </div>
      <div class="skill-bar-track">
        <div class="skill-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color}99,{color})"></div>
      </div>
    </div>"""


# ── Notification Toast ────────────────────────────────────────────────────────

def toast_success(msg: str) -> None:
    st.markdown(f"""
    <div style="background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.25);
                border-radius:10px;padding:.75rem 1rem;display:flex;align-items:center;
                gap:.6rem;margin:.5rem 0;animation:fadeInUp .3s ease">
      <span style="font-size:1rem">✅</span>
      <span style="font-size:.85rem;color:#4ade80;font-weight:500">{msg}</span>
    </div>""", unsafe_allow_html=True)


def toast_warning(msg: str) -> None:
    st.markdown(f"""
    <div style="background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);
                border-radius:10px;padding:.75rem 1rem;display:flex;align-items:center;
                gap:.6rem;margin:.5rem 0">
      <span style="font-size:1rem">⚠️</span>
      <span style="font-size:.85rem;color:#fbbf24;font-weight:500">{msg}</span>
    </div>""", unsafe_allow_html=True)


def toast_error(msg: str) -> None:
    st.markdown(f"""
    <div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);
                border-radius:10px;padding:.75rem 1rem;display:flex;align-items:center;
                gap:.6rem;margin:.5rem 0">
      <span style="font-size:1rem">❌</span>
      <span style="font-size:.85rem;color:#f87171;font-weight:500">{msg}</span>
    </div>""", unsafe_allow_html=True)


def toast_info(msg: str) -> None:
    st.markdown(f"""
    <div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.25);
                border-radius:10px;padding:.75rem 1rem;display:flex;align-items:center;
                gap:.6rem;margin:.5rem 0">
      <span style="font-size:1rem">ℹ️</span>
      <span style="font-size:.85rem;color:#60a5fa;font-weight:500">{msg}</span>
    </div>""", unsafe_allow_html=True)


# ── Formatting ────────────────────────────────────────────────────────────────

def fmt_pct(val: float) -> str:
    return f"{val:.1f}%"


def fmt_score(val: float) -> str:
    return f"{val:.0f}"


def clean_text(text: str) -> str:
    """Strip extra whitespace and non-printable chars."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    return text.strip()


# ── File Utils ────────────────────────────────────────────────────────────────

def save_uploaded_file(uploaded_file, dest_dir: str = "resumes") -> str:
    """Save a Streamlit UploadedFile to disk; return the file path."""
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, uploaded_file.name)
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest


def file_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def download_button(label: str, data: bytes, filename: str, mime: str) -> None:
    """Styled download button wrapping st.download_button."""
    st.download_button(
        label=f"⬇️  {label}",
        data=data,
        file_name=filename,
        mime=mime,
    )
