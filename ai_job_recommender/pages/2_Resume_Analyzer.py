import streamlit as st
from utils.data_loader import load_jobs, get_all_skills
from utils.resume_parser import extract_text, extract_skills, extract_candidate_name
from utils.recommender import recommend_by_resume, skill_gap
from utils.charts import match_gauge

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Resume Analyzer")
st.caption("Upload your resume (PDF or DOCX) to extract your skills and get instant AI-matched job recommendations.")

df = load_jobs()
known_skills = get_all_skills(df)

uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded:
    with st.spinner("Extracting text and analyzing your resume..."):
        resume_text = extract_text(uploaded)
        candidate_name = extract_candidate_name(resume_text)
        extracted_skills = extract_skills(resume_text, known_skills)

    if not resume_text.strip():
        st.error("Couldn't extract text from this file. Try a different PDF/DOCX (scanned images aren't supported).")
        st.stop()

    st.success(f"Resume parsed successfully for **{candidate_name}**")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🧠 Extracted Skills")
        if extracted_skills:
            st.markdown(" ".join(f"`{s}`" for s in extracted_skills))
        else:
            st.warning("No known skills detected. Try selecting skills manually below.")
        manual_skills = st.multiselect(
            "Add / adjust skills manually",
            options=known_skills,
            default=extracted_skills,
        )

    with col2:
        with st.expander("📃 Extracted Resume Text (preview)"):
            st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

    st.markdown("---")
    st.subheader("🎯 Top Job Matches for Your Resume")

    top_n = st.slider("Number of results", 5, 30, 10)
    results = recommend_by_resume(df, resume_text, top_n=top_n)

    if results.empty:
        st.info("No strong matches found from your resume text — try adding more detail or selecting skills manually.")
    else:
        for _, job in results.iterrows():
            with st.container(border=True):
                left, right = st.columns([4, 1])
                with left:
                    st.markdown(f"#### {job['title']}")
                    st.markdown(f"**{job['company']}** &nbsp;·&nbsp; 📍 {job['location']}")
                    st.markdown(f"`{job['work_type']}`  `{job['experience']}`")
                with right:
                    st.metric("Match", f"{job.get('match_pct', 0)}%")

                gap = skill_gap(job, manual_skills)
                gc1, gc2 = st.columns(2)
                with gc1:
                    st.markdown("**✅ You have:**")
                    st.markdown(" ".join(f"`{s}`" for s in gap["matched"]) or "_None matched_")
                with gc2:
                    st.markdown("**📚 Gap to fill:**")
                    st.markdown(" ".join(f"`{s}`" for s in gap["missing"]) or "_Full match!_")
                st.progress(gap["match_pct"] / 100, text=f"Skill coverage: {gap['match_pct']}%")

        export_cols = ["title", "company", "location", "work_type", "experience", "skills", "match_pct"]
        export_cols = [c for c in export_cols if c in results.columns]
        csv = results[export_cols].to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download These Matches as CSV", data=csv,
                            file_name="resume_job_matches.csv", mime="text/csv")
else:
    st.info("👆 Upload a PDF or DOCX resume to get started.")
    st.markdown("""
    **What happens next:**
    1. We extract the raw text from your resume
    2. We detect known industry skills mentioned in it
    3. We run it through the same TF-IDF recommendation engine used for job search
    4. You get ranked job matches with a skill-gap breakdown for each
    """)
