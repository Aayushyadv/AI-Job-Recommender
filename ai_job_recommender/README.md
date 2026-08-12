# 💼 AI Job Recommendation System

A modern, LinkedIn-style AI-powered job recommendation platform built with **Streamlit**,
**TF-IDF + Linear Kernel similarity**, and resume intelligence.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎨 **Modern dark, LinkedIn-style UI** with a metrics dashboard
- 🎛️ **Sidebar filters** — Location, Work Type, Experience
- 🔎 **Search by Job Title** or **Search by Skills**
- 🤖 **TF-IDF + Linear Kernel** recommendation engine
- 📊 **Match percentage** per job
- 💡 **"Why Recommended"** explanation per result
- 🧩 **Skill Gap Analysis** (skills you have vs. skills to learn)
- ⬇️ **Download recommendations as CSV**
- 📈 **Charts**: Top Skills, Top Locations, Experience Distribution, Work Type
- 🗂️ **Job detail cards** with description & salary range
- 📄 **Resume upload** (PDF / DOCX)
- 🧠 **AI resume skill extraction**
- 🎯 **Resume-to-job matching**
- 🚀 **Career roadmap** generator with skill-gap based learning steps
- 📚 **Learning resource recommendations** per missing skill

## 🗂️ Project Structure

```
ai_job_recommender/
├── app.py                          # Home page — dashboard, metrics, charts
├── pages/
│   ├── 1_🎯_Job_Recommendations.py # Search by title/skills, match %, CSV export
│   ├── 2_📄_Resume_Analyzer.py     # Resume upload, skill extraction, matching
│   └── 3_🚀_Career_Roadmap.py      # Target-role roadmap & learning path
├── utils/
│   ├── data_loader.py              # CSV loading, column mapping, filtering, caching
│   ├── recommender.py              # TF-IDF engine, match %, why-recommended, skill gap
│   ├── resume_parser.py            # PDF/DOCX text + skill extraction
│   └── charts.py                   # Plotly chart builders (dark themed)
├── data/
│   ├── generate_sample_data.py     # Synthetic dataset generator (demo data)
│   └── jobs.csv                    # Job dataset (swap in your real data here)
├── .streamlit/
│   └── config.toml                 # Dark theme configuration
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone <your-repo-url>
cd ai_job_recommender
pip install -r requirements.txt
```

### 2. Provide your data

The app expects `data/jobs.csv` with (at minimum) these columns — alternate
common names are auto-mapped (see `utils/data_loader.py::COLUMN_ALIASES`):

| Column        | Description                                  |
|---------------|-----------------------------------------------|
| `title`       | Job title                                     |
| `company`     | Company name                                  |
| `location`    | City/state                                    |
| `work_type`   | Full-time / Contract / Remote / etc.          |
| `experience`  | Entry / Mid / Senior / Lead                   |
| `skills`      | Comma-separated skills                        |
| `description` | Full job description (optional but recommended) |
| `salary_min` / `salary_max` | Optional salary range              |

No dataset yet? Generate a synthetic one to try the app immediately:

```bash
python data/generate_sample_data.py
```

### 3. Run the app

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (typically `http://localhost:8501`).

## 🧠 How the Recommendation Engine Works

1. Each job's **title + skills + description** are combined into one text field.
2. A **TF-IDF vectorizer** (with English stop-word removal and 1-2 grams) is fit
   across the whole job corpus, cached with `st.cache_resource` for performance.
3. A user's **search query, skill list, or resume text** is vectorized the same way.
4. **Linear Kernel** (equivalent to cosine similarity on TF-IDF vectors) scores
   every job against the query.
5. Scores are normalized to a **0–100% match score** and sorted descending.
6. **"Why Recommended"** surfaces the overlapping skills/keywords that drove the match.
7. **Skill Gap Analysis** diffs the job's required skills against the user's
   known skills to show what's already covered and what to learn next.

## 📄 Resume Analysis Pipeline

1. Upload a **PDF** (via `pdfplumber`) or **DOCX** (via `docx2txt`).
2. Raw text is extracted and scanned against the dataset's known skill vocabulary
   using word-boundary regex matching (so "R" doesn't match inside "Marketing", etc.).
3. Extracted skills are shown and are editable via a multiselect.
4. The full resume text is run through the same TF-IDF engine used for job search
   to produce ranked job matches with per-job skill-gap breakdowns.

## 🎨 Customization

- **Theme**: edit `.streamlit/config.toml`.
- **Learning resources**: extend the `LEARNING_LINKS` dict in
  `pages/3_🚀_Career_Roadmap.py` with your preferred courses/platforms.
- **Skill vocabulary**: derived automatically from the `skills` column of your
  dataset — no manual list to maintain.

## 🛣️ Roadmap Ideas

- Swap TF-IDF for sentence-transformer embeddings for semantic matching
- Add authentication + saved searches / favorited jobs
- Add a job-application tracker
- Deploy to Streamlit Community Cloud / Docker

## 📜 License

MIT — use freely for personal or commercial projects.
