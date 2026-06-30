"""
pages_logic/job_description.py
────────────────────────────────
💼 Job Description — paste, upload, or select sample JD with char counter.
"""

from __future__ import annotations
import streamlit as st
from utils.helpers import page_header, section_divider, toast_success
from utils.text_extractor import extract_text
from utils.sample_data import get_sample_titles, get_sample_jd


def render() -> None:
    page_header(
        "Job Description",
        "Define the role you're screening candidates against",
        icon="💼",
    )

    tab1, tab2, tab3 = st.tabs(["✍️ Paste Text", "📁 Upload File", "📋 Sample JDs"])

    # ── Tab 1: Paste ─────────────────────────────────────────────────────────
    with tab1:
        title = st.text_input("Job Title", value=st.session_state.jd_title,
                               placeholder="e.g. Senior Python Backend Engineer")
        text = st.text_area(
            "Job Description",
            value=st.session_state.jd_text,
            height=320,
            placeholder="Paste the full job description here, including responsibilities and requirements...",
        )
        char_count = len(text)
        word_count = len(text.split())
        st.markdown(f"""
        <div style="display:flex;gap:1.5rem;color:#64748b;font-size:.78rem;margin-top:-.5rem">
          <span>📝 {char_count} characters</span>
          <span>📖 {word_count} words</span>
        </div>""", unsafe_allow_html=True)

        if st.button("💾 Save Job Description", key="save_jd_text", use_container_width=False):
            if text.strip():
                st.session_state.jd_text = text
                st.session_state.jd_title = title or "Untitled Role"
                toast_success("Job description saved successfully.")
            else:
                st.warning("Please enter a job description before saving.")

    # ── Tab 2: Upload ────────────────────────────────────────────────────────
    with tab2:
        jd_file = st.file_uploader(
            "Upload Job Description file",
            type=["pdf", "docx", "txt"],
            key="jd_file_uploader",
        )
        jd_title_upload = st.text_input("Job Title (optional)", key="jd_title_upload",
                                         placeholder="e.g. ML Engineer")
        if jd_file and st.button("⚡ Extract & Save", key="extract_jd"):
            with st.spinner("Extracting job description text..."):
                text = extract_text(jd_file.getvalue(), jd_file.name)
            if len(text.strip()) > 20:
                st.session_state.jd_text = text
                st.session_state.jd_title = jd_title_upload or jd_file.name.rsplit(".", 1)[0]
                toast_success("Job description extracted and saved.")
                st.text_area("Preview", text, height=200, disabled=True)
            else:
                st.error("Couldn't extract readable text from this file.")

    # ── Tab 3: Sample JDs ────────────────────────────────────────────────────
    with tab3:
        sample_title = st.selectbox("Choose a sample job description", get_sample_titles())
        sample_text = get_sample_jd(sample_title)
        st.text_area("Preview", sample_text, height=280, disabled=True, key="sample_preview")
        if st.button("✅ Use This Sample", key="use_sample"):
            st.session_state.jd_text = sample_text
            st.session_state.jd_title = sample_title
            toast_success(f"Loaded sample JD: {sample_title}")

    # ── Current JD Status ────────────────────────────────────────────────────
    section_divider("Current Job Description")
    if st.session_state.jd_text.strip():
        wc = len(st.session_state.jd_text.split())
        st.markdown(f"""
        <div class="glass-card animate-fade-up">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem">
            <div style="font-weight:700;font-size:1rem">{st.session_state.jd_title or 'Untitled Role'}</div>
            <span class="badge badge-green">✓ Ready for Analysis</span>
          </div>
          <div style="color:#64748b;font-size:.78rem;margin-bottom:.75rem">{wc} words</div>
          <div style="color:#94a3b8;font-size:.83rem;line-height:1.6;max-height:120px;overflow:hidden">
            {st.session_state.jd_text[:400]}…
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2.5rem">
          <div style="font-size:2rem;margin-bottom:1rem">📋</div>
          <div style="font-weight:600;margin-bottom:.5rem">No job description set</div>
          <div style="color:#94a3b8;font-size:.85rem">
            Use one of the tabs above to add a job description.
          </div>
        </div>""", unsafe_allow_html=True)
