import streamlit as st
import pandas as pd
from utils.data_loader import load_jobs, get_filter_options, apply_filters
from utils.recommender import recommend_by_text, why_recommended, skill_gap
from utils.charts import match_gauge

st.set_page_config(page_title="Job Recommendations", page_icon="🎯", layout="wide")

st.title("🎯 Job Recommendations")
st.caption("Search by job title or by the skills you have — powered by TF-IDF + Linear Kernel similarity.")

df = load_jobs()
options = get_filter_options(df)

# ---------- Sidebar filters ----------
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    location = st.selectbox("Location", ["All"] + options["locations"])
    work_type = st.selectbox("Work Type", ["All"] + options["work_types"])
    experience = st.selectbox("Experience", ["All"] + options["experience"])
    top_n = st.slider("Number of results", 5, 50, 15)

filtered_df = apply_filters(df, location, work_type, experience)

# ---------- Search controls ----------
search_mode = st.radio("Search By", ["Job Title", "Skills"], horizontal=True)

if search_mode == "Job Title":
    query = st.text_input("Enter Job Title", placeholder="e.g. Data Scientist")
    query_skills = []
else:
    query = st.text_input("Enter Skills (comma-separated)", placeholder="e.g. Python, SQL, Machine Learning")
    query_skills = [s.strip() for s in query.split(",") if s.strip()]

run = st.button("🔍 Find Matching Jobs", type="primary", use_container_width=False)

st.markdown("---")

if run and query.strip():
    if filtered_df.empty:
        st.warning("No jobs match your selected filters. Try widening them.")
    else:
        results = recommend_by_text(filtered_df, query, top_n=top_n)

        if results.empty:
            st.warning("No matching jobs found. Try different keywords or skills.")
        else:
            st.success(f"Found **{len(results)}** matching jobs")

            # ---------- CSV download ----------
            export_cols = ["title", "company", "location", "work_type", "experience",
                            "skills", "match_pct"]
            export_cols = [c for c in export_cols if c in results.columns]
            csv = results[export_cols].to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Recommendations as CSV",
                data=csv,
                file_name="job_recommendations.csv",
                mime="text/csv",
            )

            st.markdown("###")

            # ---------- Job cards ----------
            for _, job in results.iterrows():
                match_pct = job.get("match_pct", 0)
                with st.container(border=True):
                    top_l, top_r = st.columns([4, 1])
                    with top_l:
                        st.markdown(f"#### {job['title']}")
                        st.markdown(f"**{job['company']}** &nbsp;·&nbsp; 📍 {job['location']}")
                        badges = f"`{job['work_type']}`  `{job['experience']}`"
                        st.markdown(badges)
                    with top_r:
                        st.metric("Match", f"{match_pct}%")

                    with st.expander("📋 Job Details"):
                        st.write(job.get("description", "No description available."))
                        st.markdown(f"**Required Skills:** {job['skills']}")
                        if "salary_min" in job and "salary_max" in job and pd.notna(job.get("salary_min")):
                            st.markdown(f"**Salary Range:** ${int(job['salary_min']):,} – ${int(job['salary_max']):,}")

                    reasons = why_recommended(job, query_skills if query_skills else query.split())
                    with st.expander("💡 Why Recommended"):
                        if reasons:
                            st.write("This job was recommended because it matches these of your terms:")
                            st.markdown(" ".join(f"`{r}`" for r in reasons))
                        else:
                            st.write("Matched based on overall text similarity between your query and the job description.")

                    if query_skills:
                        with st.expander("🧩 Skill Gap Analysis"):
                            gap = skill_gap(job, query_skills)
                            gc1, gc2 = st.columns(2)
                            with gc1:
                                st.markdown("**✅ Skills you have:**")
                                st.markdown(" ".join(f"`{s}`" for s in gap["matched"]) or "_None matched_")
                            with gc2:
                                st.markdown("**📚 Skills to learn:**")
                                st.markdown(" ".join(f"`{s}`" for s in gap["missing"]) or "_None — full match!_")
                            st.progress(gap["match_pct"] / 100, text=f"Skill coverage: {gap['match_pct']}%")

elif run:
    st.warning("Please enter a job title or skills to search.")
else:
    st.info("Enter a search above and click **Find Matching Jobs** to get AI-powered recommendations.")
