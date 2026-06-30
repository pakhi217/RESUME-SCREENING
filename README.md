# 🧠 ScreenAI — Resume Screening AI

<div align="center">

**A premium, production-ready ATS-style resume screening platform powered by NLP & semantic search.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-Embeddings-8B5CF6?style=for-the-badge)](https://www.sbert.net/)
[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack)

</div>

---


## ✨ Features

### 🎯 Core Screening
- **Semantic Matching** — Sentence-transformer embeddings (`all-MiniLM-L6-v2`) capture contextual meaning beyond keywords
- **TF-IDF Cosine Similarity** — classic vector-space matching as a complementary signal
- **Skill Graph Extraction** — auto-detects skills across 7 taxonomies (languages, frameworks, ML/AI, cloud, databases, tools, soft skills)
- **ATS Compatibility Score** — heuristic structure/formatting checks mirroring real applicant tracking systems
- **Keyword Density Analysis** — surfaces missing JD keywords your resume should include
- **Experience & Education Heuristics** — parses years of experience and degree level alignment

### 🏆 Candidate Management
- **Bulk Resume Upload** — drag & drop, multi-file, PDF + DOCX support
- **Smart Leaderboard** — auto-ranked, searchable, filterable, sortable
- **Candidate Comparison** — multi-metric radar overlay for up to 5 candidates side-by-side
- **Hiring Recommendations** — Strong Hire / Hire / Consider / Not a Fit labels

### 📊 Reporting & Export
- **PDF Reports** — polished, shareable per-candidate analysis reports
- **CSV Export** — full ranked results for spreadsheet workflows
- **AI Suggestions** — missing skills, resume improvements, keywords to add, certification recommendations, interview readiness score

### 🎨 Premium UI/UX
- Dark-mode-first glassmorphism design system
- Animated circular progress rings for every score dimension
- Interactive Plotly charts (radar, pie, bar) with custom dark theming
- Smooth hover transitions, gradient buttons, soft shadows
- Fully responsive layout

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / App Framework** | Streamlit, Streamlit Extras, Custom CSS |
| **Data Processing** | Pandas, NumPy |
| **Classic ML** | scikit-learn (TF-IDF, Cosine Similarity) |
| **NLP** | NLTK (tokenization, stopwords, lemmatization) |
| **Semantic Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Visualization** | Plotly (radar / pie / bar charts) |
| **Document Parsing** | PyPDF2, python-docx |
| **Reporting** | fpdf2 (PDF generation), CSV |

---

## 📂 Folder Structure

```
Resume-Screening-AI/
│
├── app.py                      # Main entry point — landing page + routing
├── requirements.txt
├── README.md
│
├── pages_logic/                # Page-level view logic (custom sidebar nav)
│   ├── dashboard.py             #   🏠 Dashboard
│   ├── resume_upload.py         #   📄 Resume Upload
│   ├── job_description.py       #   💼 Job Description
│   ├── analysis.py              #   📊 AI Analysis
│   ├── ranking.py                #   🏆 Candidate Ranking
│   └── settings.py               #   ⚙️ Settings
│
├── models/                      # ML & document generation logic
│   ├── scorer.py                 #   TF-IDF, embeddings, skill matching, scoring
│   └── report_generator.py       #   PDF + CSV report builders
│
├── utils/                       # Shared utilities
│   ├── helpers.py                 #   CSS injection, HTML components
│   ├── charts.py                  #   Plotly chart factory
│   ├── text_extractor.py          #   PDF/DOCX text extraction
│   ├── sample_data.py             #   Bundled sample job descriptions
│   └── state.py                   #   Session-state management
│
├── css/
│   └── styles.css                # Global design system stylesheet
│
├── assets/                      # Screenshots, logos, demo GIFs
├── resumes/                     # (runtime) uploaded resume cache
└── reports/                     # (runtime) generated report cache
```

---

## 🧮 Machine Learning Pipeline

The scoring engine (`models/scorer.py`) combines six independent signals into a weighted final score:

```
Overall Match = 0.30 × Semantic Similarity (Sentence-Transformers)
              + 0.20 × TF-IDF Cosine Similarity
              + 0.25 × Skill Match (taxonomy intersection)
              + 0.10 × Keyword Match
              + 0.10 × Experience Heuristic
              + 0.05 × Education Heuristic
```

**Step-by-step:**
1. **Preprocessing** — lowercase, strip punctuation, tokenize, remove stopwords, lemmatize (NLTK)
2. **TF-IDF Vectorization** — `TfidfVectorizer` with unigrams + bigrams builds sparse vectors for resume & JD; cosine similarity computed via scikit-learn
3. **Semantic Embeddings** — `all-MiniLM-L6-v2` encodes both texts into dense 384-dim vectors; cosine similarity captures contextual/semantic meaning
4. **Skill Extraction** — regex-based matching against a curated taxonomy of 100+ skills across 7 categories
5. **Keyword Analysis** — term-frequency extraction of top JD keywords, checked for presence in resume
6. **ATS Scoring** — heuristic checks for section headings, contact info, word count, and line structure
7. **AI Suggestions** — rule-based engine generates missing skills, resume improvements, keyword recommendations, and certification suggestions

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/Resume-Screening-AI.git
cd Resume-Screening-AI

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> **Note:** On first run, NLTK will download required corpora (`punkt`, `stopwords`, `wordnet`) automatically. The sentence-transformer model (~80MB) downloads on first semantic analysis.

---

## Author
**PAKHI SAXENA**

BTech ECE Student


## 🗺️ Future Scope

- [ ] Multi-language resume support (non-English NLP pipelines)
- [ ] LLM-powered (GPT/Claude) qualitative resume critique
- [ ] Resume parsing with named-entity recognition (spaCy) for structured field extraction
- [ ] Bias & fairness auditing dashboard for screening decisions
- [ ] Integration with ATS platforms (Greenhouse, Lever) via API
- [ ] Persistent database (PostgreSQL) for candidate history across sessions
- [ ] Authentication & multi-recruiter team workspaces
- [ ] Resume version comparison (track improvements over time)
- [ ] Chrome extension for one-click LinkedIn profile screening

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Built with ❤️ using Python, Streamlit & Sentence Transformers

</div>
