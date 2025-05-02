"""
JHU Career‑Match — Streamlit Prototype (v0.2)
=============================================
Upload a CV ➜ get top matching jobs ➜ generate cover letter + intro email.

Run:
    streamlit run career_match_app.py
Dependencies listed in requirements.txt.
"""

from __future__ import annotations
import json, uuid
from pathlib import Path
from typing import List, Dict, Any

import streamlit as st
import pandas as pd
import numpy as np

# ---------------- Configuration ---------------- #
st.set_page_config(page_title="JHU Career‑Match", page_icon="🎓", layout="centered")

MEMORY_FILE = Path("user_memory.json")
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text("{}")

def _load_memory() -> Dict[str, Any]:
    return json.loads(MEMORY_FILE.read_text())

def _save_memory(mem: Dict[str, Any]):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

# ---------------- Tool Layer ------------------- #
def parse_cv(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Dummy CV parser (replace with WindSurf/OpenAI)."""
    import time; time.sleep(1)
    skills = ["Python", "Data Analysis", "SQL", "Machine Learning", "Leadership", "Project Management"]
    return {"id": str(uuid.uuid4()), "name": filename, "skills": skills, "raw_text": "(full CV text here)"}

def _load_static_jobs() -> pd.DataFrame:
    data = [
        {"job_id": "1", "title": "Data Analyst", "company": "Acme Corp", "location": "Baltimore, MD", "keywords": "Python SQL Excel"},
        {"job_id": "2", "title": "Product Manager", "company": "TechNova", "location": "Remote", "keywords": "Agile Roadmaps Leadership"},
        {"job_id": "3", "title": "Machine Learning Engineer", "company": "DeepAI", "location": "Washington, DC", "keywords": "Machine Learning Python TensorFlow"},
        {"job_id": "4", "title": "Business Analyst", "company": "FinServe", "location": "New York, NY", "keywords": "SQL PowerBI Finance"},
    ]
    return pd.DataFrame(data)

def external_job_search(skills: List[str]) -> pd.DataFrame:
    try:
        raise RuntimeError("Live job search not implemented – using fallback list")
    except Exception as err:
        st.info(f"🔄 Job search fallback activated: {err}")
        return _load_static_jobs()

def embed_text_batch(texts: List[str]) -> np.ndarray:
    rng = np.random.default_rng(seed=42)
    return rng.random((len(texts), 384))

def match_jobs(cv: Dict[str, Any], jobs: pd.DataFrame, top_k: int = 3) -> pd.DataFrame:
    cv_vec = embed_text_batch([" ".join(cv["skills"])])[0]
    job_vecs = embed_text_batch(jobs["keywords"].tolist())
    sims = (job_vecs @ cv_vec) / (np.linalg.norm(job_vecs, axis=1) * np.linalg.norm(cv_vec) + 1e-9)
    jobs = jobs.copy()
    jobs["score"] = sims
    return jobs.sort_values("score", ascending=False).head(top_k)

def generate_career_advice(cv: Dict[str, Any], top_jobs: pd.DataFrame) -> str:
    return (f"Based on your strengths in {', '.join(cv['skills'][:3])}, consider bolstering "
            f"hands‑on SQL projects and joining JHU's Data Science Club to prepare for roles like "
            f"{top_jobs.iloc[0]['title']}.")

def generate_cover_letter(cv: Dict[str, Any], job_row: pd.Series) -> str:
    return (f"Dear Hiring Manager,\n\n"
            f"My background in {', '.join(cv['skills'][:3])} and recent projects at JHU make me an "
            f"excellent fit for the {job_row['title']} role at {job_row['company']}. "
            f"I am excited about the opportunity to contribute and grow with your team.\n\n"
            f"Sincerely,\nStudent Name")

def generate_email(cv: Dict[str, Any], job_row: pd.Series) -> str:
    return (f"Subject: Application for {job_row['title']} – {cv['name'].split('.')[0]}\n\n"
            f"Hi there,\n\n"
            f"I’m a JHU student with a strong foundation in {', '.join(cv['skills'][:2])} and "
            f"hands‑on experience in {cv['skills'][2]}. After reviewing the opening for a "
            f"{job_row['title']} at {job_row['company']}, I believe my background aligns well with "
            f"your needs. I’ve attached my résumé for your convenience and would welcome the chance "
            f"to discuss how I can contribute to your team.\n\n"
            f"Thanks for your time and consideration!\n\nBest regards,\nStudent Name")

# ---------------- Streamlit UI ------------------ #
def main():
    st.header("🎓 JHU Career‑Match: Your AI Job‑Hunt Copilot")

    uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        cv = parse_cv(uploaded_file.read(), uploaded_file.name)
        st.success("CV uploaded and parsed successfully!")
        st.write("**Extracted Key Skills:**", ", ".join(cv["skills"]))

        mem = _load_memory()
        mem["latest_cv"] = cv
        _save_memory(mem)

        job_df = external_job_search(cv["skills"])
        top_matches = match_jobs(cv, job_df)
        st.subheader("Top Job Recommendations")
        st.dataframe(top_matches[["title", "company", "location", "score"]])

        st.subheader("Career Path Suggestions")
        st.write(generate_career_advice(cv, top_matches))

        st.subheader("Generate Tailored Cover Letter")
        for _, row in top_matches.iterrows():
            if st.button(f"Create cover letter for {row['title']} at {row['company']}"):
                st.code(generate_cover_letter(cv, row), language="markdown")

        st.subheader("Generate Intro Email")
        for _, row in top_matches.iterrows():
            if st.button(f"Create email for {row['title']} at {row['company']}"):
                st.code(generate_email(cv, row), language="markdown")

        st.caption("Tip: update your CV anytime to refresh recommendations.")
    else:
        st.info("👆 Upload a résumé to get started.")

if __name__ == "__main__":
    main()