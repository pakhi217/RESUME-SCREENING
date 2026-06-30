"""
models/scorer.py
────────────────
Core ML engine for Resume Screening AI.

Pipeline overview
─────────────────
1.  Preprocess  → clean + tokenise both texts
2.  TF-IDF      → build sparse vectors, compute cosine similarity
3.  Embeddings  → sentence-transformer dense vectors, cosine similarity
4.  Skill       → extract and intersect skill sets per category
5.  Keywords    → extract top JD keywords, check presence in resume
6.  ATS score   → heuristic formatting / structure checks
7.  Final score → weighted combination of all signals
"""

from __future__ import annotations

import re
import math
import string
from collections import Counter
from typing import Any

import numpy as np

# ── Optional heavy imports (graceful degradation) ────────────────────────────

try:
    import nltk
    from nltk.corpus   import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem     import WordNetLemmatizer
    _NLTK = True
    # Download required corpora (silent if already present)
    for _pkg in ("punkt", "stopwords", "wordnet", "averaged_perceptron_tagger"):
        try:
            nltk.download(_pkg, quiet=True)
        except Exception:
            pass
except ImportError:
    _NLTK = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _SKLEARN = True
except ImportError:
    _SKLEARN = False

try:
    from sentence_transformers import SentenceTransformer
    _ST_MODEL: SentenceTransformer | None = None   # lazy singleton
    _ST = True
except ImportError:
    _ST = False


# ── Skill taxonomy ────────────────────────────────────────────────────────────

SKILL_TAXONOMY: dict[str, list[str]] = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go",
        "rust", "swift", "kotlin", "r", "scala", "ruby", "php", "matlab",
        "c", "dart", "lua", "perl", "haskell",
    ],
    "Web Frameworks": [
        "react", "angular", "vue", "next.js", "nuxt", "svelte", "django",
        "flask", "fastapi", "express", "spring", "laravel", "rails",
        "asp.net", "nestjs", "gatsby", "remix",
    ],
    "ML / AI": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "hugging face", "transformers", "langchain", "openai", "llm",
        "nlp", "computer vision", "deep learning", "machine learning",
        "neural network", "bert", "gpt", "xgboost", "lightgbm",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "terraform", "ansible", "jenkins", "ci/cd", "github actions",
        "helm", "argocd", "cloudformation", "lambda", "ec2", "s3",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "sqlite", "oracle", "mssql",
        "neo4j", "influxdb", "bigquery", "snowflake", "dbt",
    ],
    "Tools & Platforms": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "linux", "unix", "bash", "powershell", "figma", "postman",
        "graphql", "rest", "grpc", "kafka", "rabbitmq", "airflow",
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "analytical", "collaboration", "agile", "scrum", "kanban",
        "project management", "mentoring", "critical thinking",
    ],
}


# ── Text pre-processing ───────────────────────────────────────────────────────

def _clean(text: str) -> str:
    """Lower-case, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _tokenize(text: str) -> list[str]:
    """Tokenize with NLTK if available, else simple split."""
    cleaned = _clean(text)
    if _NLTK:
        try:
            tokens = word_tokenize(cleaned)
            stop   = set(stopwords.words("english"))
            lemma  = WordNetLemmatizer()
            return [lemma.lemmatize(t) for t in tokens
                    if t not in stop and len(t) > 1]
        except Exception:
            pass
    # Fallback: basic split
    stop_basic = {
        "a","an","the","and","or","in","on","at","to","for","of","with",
        "by","from","is","are","was","were","be","been","being","have",
        "has","had","do","does","did","will","would","should","could","may",
        "might","can","that","this","these","those","it","its","as","if",
    }
    return [w for w in cleaned.split() if w not in stop_basic and len(w) > 1]


# ── Skill extraction ──────────────────────────────────────────────────────────

def extract_skills(text: str) -> dict[str, list[str]]:
    """
    Search for known skills in raw text.
    Returns dict of category → [found skills].
    """
    text_lower = text.lower()
    found: dict[str, list[str]] = {}
    for category, skills in SKILL_TAXONOMY.items():
        matched = [s for s in skills if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
        if matched:
            found[category] = matched
    return found


def skill_match_score(resume_skills: dict, jd_skills: dict) -> float:
    """
    Fraction of JD skills present in resume (macro-average across categories).
    """
    scores: list[float] = []
    for cat, jd_list in jd_skills.items():
        if not jd_list:
            continue
        res_list = resume_skills.get(cat, [])
        overlap  = len(set(res_list) & set(jd_list))
        scores.append(overlap / len(jd_list))
    return (sum(scores) / len(scores) * 100) if scores else 0.0


# ── TF-IDF similarity ─────────────────────────────────────────────────────────

def tfidf_similarity(text_a: str, text_b: str) -> float:
    """
    Build a 2-document TF-IDF matrix and compute cosine similarity.
    Returns a value in [0, 100].
    """
    if not _SKLEARN:
        # Fallback: Jaccard similarity on tokens
        set_a = set(_tokenize(text_a))
        set_b = set(_tokenize(text_b))
        if not set_a or not set_b:
            return 0.0
        return len(set_a & set_b) / len(set_a | set_b) * 100

    # Step 1: vectorise both texts with TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),   # unigrams + bigrams capture phrases
        max_features=8000,
    )
    try:
        matrix = vectorizer.fit_transform([text_a, text_b])
        # Step 2: cosine similarity between the two sparse vectors
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(sim) * 100
    except Exception:
        return 0.0


# ── Sentence-Transformer similarity ──────────────────────────────────────────

def semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Dense-vector cosine similarity using a small sentence-transformer model.
    Falls back to TF-IDF similarity if the library is unavailable.
    """
    global _ST_MODEL

    if not _ST:
        return tfidf_similarity(text_a, text_b)

    try:
        if _ST_MODEL is None:
            # Lazy load — 'all-MiniLM-L6-v2' is fast (~80 MB) and accurate
            _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

        # Truncate to 512 words to stay within model token limit
        def trunc(t: str, n: int = 512) -> str:
            return " ".join(t.split()[:n])

        emb_a, emb_b = _ST_MODEL.encode([trunc(text_a), trunc(text_b)])

        # Manual cosine (avoids an extra scipy import)
        dot   = float(np.dot(emb_a, emb_b))
        norm  = float(np.linalg.norm(emb_a) * np.linalg.norm(emb_b))
        score = (dot / norm) if norm > 0 else 0.0
        return max(0.0, score) * 100
    except Exception:
        return tfidf_similarity(text_a, text_b)


# ── Keyword extraction & match ────────────────────────────────────────────────

def top_keywords(text: str, n: int = 30) -> list[str]:
    """
    Extract the n most informative tokens from a text using term frequency,
    filtering stop-words and very short tokens.
    """
    tokens = _tokenize(text)
    freq   = Counter(tokens)
    return [w for w, _ in freq.most_common(n)]


def keyword_match_score(resume_text: str, jd_text: str) -> tuple[float, list[str], list[str]]:
    """
    Check how many top JD keywords appear in the resume.
    Returns (score_pct, found_keywords, missing_keywords).
    """
    jd_kws      = set(top_keywords(jd_text, 40))
    resume_kws  = set(_tokenize(resume_text))
    found       = list(jd_kws & resume_kws)
    missing     = list(jd_kws - resume_kws)
    score       = (len(found) / len(jd_kws) * 100) if jd_kws else 0.0
    return score, found, missing


# ── Experience heuristic ──────────────────────────────────────────────────────

def experience_score(resume_text: str, jd_text: str) -> float:
    """
    Heuristic: count year references in resume vs years required in JD.
    Returns score in [0, 100].
    """
    jd_years_req_match = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?', jd_text.lower()
    )
    resume_years_match = re.findall(
        r'(\d{4})', resume_text
    )

    # Estimate candidate experience from year span in resume
    years_in_resume = [int(y) for y in resume_years_match
                       if 1990 <= int(y) <= 2025]
    if years_in_resume:
        exp_span = max(years_in_resume) - min(years_in_resume)
    else:
        exp_span = 0

    req = max((int(y) for y in jd_years_req_match), default=2)
    if req == 0:
        return 80.0
    return min(100.0, (exp_span / req) * 100)


# ── ATS / formatting score ────────────────────────────────────────────────────

_ATS_SECTIONS = [
    "experience", "education", "skills", "projects",
    "summary", "objective", "certifications", "awards",
    "publications", "languages", "volunteering",
]

_ATS_CONTACT = [
    r'[\w\.-]+@[\w\.-]+\.\w+',   # email
    r'\+?\d[\d\s\-\(\)]{7,}',    # phone
    r'linkedin\.com',
    r'github\.com',
]


def ats_score(resume_text: str) -> float:
    """
    Estimate ATS-friendliness by checking:
    • Presence of standard section headings
    • Contact information completeness
    • Length adequacy
    • No excessively short lines (table/column artefacts)
    Returns a score in [0, 100].
    """
    text_lower = resume_text.lower()
    total      = 0.0
    earned     = 0.0

    # 1. Section headings (40 pts)
    total  += 40
    earned += sum(4 for s in _ATS_SECTIONS if s in text_lower)

    # 2. Contact info (20 pts)
    total  += 20
    earned += sum(
        5 for pattern in _ATS_CONTACT
        if re.search(pattern, resume_text, re.IGNORECASE)
    )

    # 3. Word count adequacy (20 pts)
    total  += 20
    word_count = len(resume_text.split())
    if word_count >= 400:
        earned += 20
    elif word_count >= 200:
        earned += 10

    # 4. No gibberish (line quality) (20 pts)
    total  += 20
    lines  = [l for l in resume_text.split('\n') if l.strip()]
    if lines:
        long_lines = sum(1 for l in lines if len(l.split()) >= 5)
        earned += min(20, (long_lines / len(lines)) * 20)

    return round(earned / total * 100, 1) if total else 0.0


# ── Education heuristic ───────────────────────────────────────────────────────

def education_score(resume_text: str, jd_text: str) -> float:
    """
    Check if required education level in JD appears in resume.
    """
    edu_keywords = {
        "phd": 100, "doctorate": 100, "ph.d": 100,
        "master": 85,  "msc": 85, "m.s": 85, "mba": 85,
        "bachelor": 70, "b.s": 70, "b.e": 70, "btech": 70, "b.tech": 70,
        "associate": 50, "diploma": 45,
    }
    jd_lower  = jd_text.lower()
    res_lower = resume_text.lower()

    # Find highest edu level required in JD
    req_level = 0
    for kw, lvl in edu_keywords.items():
        if kw in jd_lower:
            req_level = max(req_level, lvl)

    if req_level == 0:
        return 80.0   # no specific requirement → assume pass

    # Find highest edu level in resume
    res_level = 0
    for kw, lvl in edu_keywords.items():
        if kw in res_lower:
            res_level = max(res_level, lvl)

    if res_level == 0:
        return 20.0   # education section missing

    return min(100.0, (res_level / req_level) * 100)


# ── Master scorer ─────────────────────────────────────────────────────────────

# Weighted combination of individual signals
_WEIGHTS = {
    "tfidf":     0.20,
    "semantic":  0.30,
    "skills":    0.25,
    "keywords":  0.10,
    "experience":0.10,
    "education": 0.05,
}


def score_resume(
    resume_text: str,
    jd_text: str,
    use_semantic: bool = True,
) -> dict[str, Any]:
    """
    Full scoring pipeline.  Returns a dict with all sub-scores and metadata.

    Parameters
    ----------
    resume_text  : plain-text resume
    jd_text      : plain-text job description
    use_semantic : whether to run the sentence-transformer (slower)

    Returns
    -------
    {
      "overall_match": float,       # 0-100
      "ats_score":     float,
      "tfidf_sim":     float,
      "semantic_sim":  float,
      "skill_match":   float,
      "keyword_match": float,
      "experience":    float,
      "education":     float,
      "resume_skills": dict,
      "jd_skills":     dict,
      "top_keywords":  list,
      "found_keywords":list,
      "missing_keywords":list,
      "word_count":    int,
      "summary":       str,
    }
    """
    # 1. Individual signal computation
    tfidf_sim   = tfidf_similarity(resume_text, jd_text)
    sem_sim     = semantic_similarity(resume_text, jd_text) if use_semantic else tfidf_sim
    res_skills  = extract_skills(resume_text)
    jd_skills   = extract_skills(jd_text)
    skill_m     = skill_match_score(res_skills, jd_skills)
    kw_score, found_kw, miss_kw = keyword_match_score(resume_text, jd_text)
    exp_score   = experience_score(resume_text, jd_text)
    edu_score   = education_score(resume_text, jd_text)
    ats         = ats_score(resume_text)

    # 2. Weighted overall score
    overall = (
        tfidf_sim    * _WEIGHTS["tfidf"]
        + sem_sim    * _WEIGHTS["semantic"]
        + skill_m    * _WEIGHTS["skills"]
        + kw_score   * _WEIGHTS["keywords"]
        + exp_score  * _WEIGHTS["experience"]
        + edu_score  * _WEIGHTS["education"]
    )
    overall = round(min(100.0, max(0.0, overall)), 1)

    # 3. Auto summary
    summary = _build_summary(overall, skill_m, ats, res_skills)

    return {
        "overall_match":    overall,
        "ats_score":        round(ats, 1),
        "tfidf_sim":        round(tfidf_sim, 1),
        "semantic_sim":     round(sem_sim, 1),
        "skill_match":      round(skill_m, 1),
        "keyword_match":    round(kw_score, 1),
        "experience":       round(exp_score, 1),
        "education":        round(edu_score, 1),
        "resume_skills":    res_skills,
        "jd_skills":        jd_skills,
        "top_keywords":     top_keywords(jd_text, 20),
        "found_keywords":   found_kw[:20],
        "missing_keywords": miss_kw[:20],
        "word_count":       len(resume_text.split()),
        "summary":          summary,
    }


def _build_summary(overall: float, skill_m: float, ats: float, skills: dict) -> str:
    """Generate a one-paragraph qualitative summary of the candidate."""
    level = (
        "an excellent" if overall >= 75 else
        "a good"       if overall >= 55 else
        "a moderate"   if overall >= 35 else
        "a weak"
    )
    total_skills = sum(len(v) for v in skills.values())
    cats = list(skills.keys())[:3]
    cats_str = ", ".join(cats) if cats else "general"

    return (
        f"This candidate is {level} match for the role with an overall score of {overall:.0f}%. "
        f"They demonstrate {total_skills} relevant skills across {cats_str} domains. "
        f"Their ATS compatibility score is {ats:.0f}%, "
        f"{'indicating a well-structured resume' if ats >= 70 else 'suggesting formatting improvements are needed'}. "
        f"Skill alignment is {skill_m:.0f}%, "
        f"{'showing strong technical alignment' if skill_m >= 60 else 'highlighting gaps to address before applying'}."
    )


# ── AI Suggestions ────────────────────────────────────────────────────────────

def generate_suggestions(result: dict) -> dict[str, list[str]]:
    """
    Rule-based AI suggestions derived from the scoring result.
    Returns categorised suggestion lists.
    """
    missing_skills: list[str] = []
    improvements:   list[str] = []
    keywords_add:   list[str] = []
    certifications: list[str] = []

    # Missing skills
    jd_skills  = result.get("jd_skills", {})
    res_skills = result.get("resume_skills", {})
    for cat, skills in jd_skills.items():
        res_cat = res_skills.get(cat, [])
        gap     = [s for s in skills if s not in res_cat]
        missing_skills.extend(gap[:3])

    # Structural improvements
    if result["ats_score"] < 70:
        improvements.append("Add clear section headings: Experience, Education, Skills, Projects.")
    if result["word_count"] < 300:
        improvements.append("Resume seems too short — expand with quantified achievements.")
    if result["keyword_match"] < 50:
        improvements.append("Mirror language from the job description more closely.")
    if result["education"] < 60:
        improvements.append("Clearly state your degree, institution, and graduation year.")
    if result["experience"] < 50:
        improvements.append("Highlight years of relevant experience and project timelines.")
    if result["semantic_sim"] < 40:
        improvements.append("Align your summary/objective section with the JD's key requirements.")

    # Keywords to add
    keywords_add = result.get("missing_keywords", [])[:12]

    # Cert recommendations (domain-aware)
    all_jd_skills = " ".join(
        s for lst in jd_skills.values() for s in lst
    ).lower()
    if any(c in all_jd_skills for c in ["aws","cloud","azure","gcp"]):
        certifications.append("AWS Solutions Architect / Google Professional Cloud Architect")
    if any(c in all_jd_skills for c in ["kubernetes","docker","devops"]):
        certifications.append("Certified Kubernetes Administrator (CKA)")
    if any(c in all_jd_skills for c in ["machine learning","deep learning","ai","nlp"]):
        certifications.append("Google TensorFlow Developer Certificate / Coursera ML Specialization")
    if any(c in all_jd_skills for c in ["security","cybersecurity"]):
        certifications.append("CompTIA Security+ / CISSP")
    if not certifications:
        certifications.append("Relevant industry certification for your domain")

    # Interview readiness (composite)
    readiness = round(
        result["overall_match"] * 0.5 + result["ats_score"] * 0.3 + result["skill_match"] * 0.2
    )

    return {
        "missing_skills":    missing_skills[:10],
        "improvements":      improvements,
        "keywords_to_add":   keywords_add,
        "certifications":    certifications,
        "interview_readiness": readiness,
    }
