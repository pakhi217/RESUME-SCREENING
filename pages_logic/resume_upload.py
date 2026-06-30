"""
pages_logic/resume_upload.py
─────────────────────────────
📄 Resume Upload — drag & drop multi-file upload with preview & thumbnails.
"""

from __future__ import annotations
import streamlit as st
from utils.helpers import page_header, section_divider, toast_success, toast_error, toast_info
from utils.text_extractor import extract_text


def render() -> None:
    page_header(
        "Resume Upload",
        "Upload candidate resumes — PDF and DOCX supported",
        icon="📄",
    )

    uploaded_files = st.file_uploader(
        "Drag & drop resumes here, or click to browse",
        type=["pdf", "docx", "doc", "txt"],
        accept_multiple_files=True,
        key="resume_uploader",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        process = st.button("⚡ Process Files", use_container_width=True, disabled=not uploaded_files)
    with col2:
        if st.session_state.resumes:
            if st.button("🗑️ Clear All", key="clear_resumes"):
                st.session_state.resumes = []
                st.session_state.analysis_results = {}
                st.session_state.analyzed = False
                st.rerun()

    if process and uploaded_files:
        with st.spinner("Extracting text from resumes..."):
            new_resumes = []
            errors = []
            for f in uploaded_files:
                try:
                    file_bytes = f.getvalue()
                    text = extract_text(file_bytes, f.name)
                    if len(text.strip()) < 30:
                        errors.append(f.name)
                        continue
                    new_resumes.append({
                        "name": f.name.rsplit(".", 1)[0],
                        "filename": f.name,
                        "text": text,
                        "size_kb": round(len(file_bytes) / 1024, 1),
                        "ext": f.name.rsplit(".", 1)[-1].upper(),
                    })
                except Exception as e:
                    errors.append(f.name)

            # Merge with existing, dedupe by filename
            existing_names = {r["filename"] for r in st.session_state.resumes}
            for r in new_resumes:
                if r["filename"] not in existing_names:
                    st.session_state.resumes.append(r)

        if new_resumes:
            toast_success(f"Successfully processed {len(new_resumes)} resume(s).")
        if errors:
            toast_error(f"Could not extract text from: {', '.join(errors)}")

    # ── Resume Cards / Thumbnails ────────────────────────────────────────────
    if st.session_state.resumes:
        section_divider(f"Uploaded Resumes ({len(st.session_state.resumes)})")

        cols = st.columns(3)
        for i, r in enumerate(st.session_state.resumes):
            ext_color = {"PDF": "red", "DOCX": "blue", "DOC": "blue", "TXT": "green"}.get(r["ext"], "purple")
            word_count = len(r["text"].split())
            with cols[i % 3]:
                st.markdown(f"""
                <div class="glass-card animate-fade-up" style="margin-bottom:1rem">
                  <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:.75rem">
                    <div style="font-size:1.6rem">📄</div>
                    <span class="badge badge-{ext_color}">{r['ext']}</span>
                  </div>
                  <div style="font-weight:600;font-size:.9rem;margin-bottom:.3rem;
                              white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                    {r['name']}
                  </div>
                  <div style="color:#64748b;font-size:.78rem;margin-bottom:.5rem">
                    {r['size_kb']} KB · {word_count} words
                  </div>
                  <div style="color:#94a3b8;font-size:.75rem;line-height:1.5;
                              max-height:60px;overflow:hidden">
                    {r['text'][:140]}…
                  </div>
                </div>""", unsafe_allow_html=True)

                if st.button("🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                    st.session_state.resumes.pop(i)
                    st.rerun()

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        toast_info(f"{len(st.session_state.resumes)} resume(s) ready. Head to Job Description next.")
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem">
          <div style="font-size:2.5rem;margin-bottom:1rem">📭</div>
          <div style="font-weight:600;margin-bottom:.5rem">No resumes uploaded yet</div>
          <div style="color:#94a3b8;font-size:.85rem">
            Drag and drop one or more resumes above to get started.
          </div>
        </div>""", unsafe_allow_html=True)
