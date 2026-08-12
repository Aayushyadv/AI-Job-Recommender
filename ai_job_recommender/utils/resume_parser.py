"""Resume text extraction (PDF/DOCX) and skill extraction against the known skill vocabulary."""
import io
import re
import pdfplumber
import docx2txt


def extract_text(uploaded_file) -> str:
    """Extract raw text from an uploaded PDF or DOCX file (Streamlit UploadedFile)."""
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".pdf"):
        text = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)

    if name.endswith(".docx"):
        return docx2txt.process(io.BytesIO(data)) or ""

    # plain text fallback
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def extract_skills(resume_text: str, known_skills: list) -> list:
    """Match known skills against resume text using word-boundary matching (case-insensitive)."""
    text_lower = resume_text.lower()
    found = []
    for skill in known_skills:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def extract_candidate_name(resume_text: str) -> str:
    """Best-effort guess at the candidate's name: first non-empty line, if short enough."""
    for line in resume_text.strip().split("\n"):
        line = line.strip()
        if 0 < len(line) <= 40 and not any(ch.isdigit() for ch in line) and "@" not in line:
            return line
    return "Candidate"
