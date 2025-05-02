# 🎓 JHU Career‑Match (Streamlit Demo)

AI‑powered prototype that lets Johns Hopkins University students:

1. **Upload a CV** (PDF or DOCX)  
2. **See top‑matching job postings** (demo fallback list)  
3. **Receive personalized career advice**  
4. **Generate a tailored cover letter**  
5. **Generate a concise intro email** to a recruiter / hiring manager

*Built for an MBA class deliverable – swap in real parsing / search APIs as desired.*

---

## ✨ Quick Demo (Local)

```bash
# 1) Create and activate a virtual environment  (optional but recommended)
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run the Streamlit app
streamlit run career_match_app.py
