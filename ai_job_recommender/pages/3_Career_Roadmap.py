import streamlit as st
from utils.data_loader import load_jobs, get_all_skills

st.set_page_config(page_title="Career Roadmap", page_icon="🚀", layout="wide")

st.title("🚀 Career Roadmap")
st.caption("Pick a target job title, tell us what you already know, and get a personalized learning roadmap.")

df = load_jobs()
known_skills = get_all_skills(df)
titles = sorted(df["title"].dropna().unique().tolist())

# Free, well-known learning resources mapped per skill (extend as needed)
LEARNING_LINKS = {
    "python": ("Python for Everybody (Coursera)", "https://www.coursera.org/specializations/python"),
    "sql": ("SQL for Data Science (Coursera)", "https://www.coursera.org/learn/sql-for-data-science"),
    "machine learning": ("Machine Learning Specialization (Coursera)", "https://www.coursera.org/specializations/machine-learning-introduction"),
    "deep learning": ("Deep Learning Specialization (Coursera)", "https://www.coursera.org/specializations/deep-learning"),
    "aws": ("AWS Cloud Practitioner Essentials", "https://aws.amazon.com/training/"),
    "docker": ("Docker Official Getting Started Guide", "https://docs.docker.com/get-started/"),
    "kubernetes": ("Kubernetes Basics", "https://kubernetes.io/docs/tutorials/kubernetes-basics/"),
    "react": ("React Official Docs & Tutorial", "https://react.dev/learn"),
    "tensorflow": ("TensorFlow Official Tutorials", "https://www.tensorflow.org/tutorials"),
    "pytorch": ("PyTorch Official Tutorials", "https://pytorch.org/tutorials/"),
    "data analysis": ("Google Data Analytics Certificate", "https://www.coursera.org/professional-certificates/google-data-analytics"),
    "power bi": ("Microsoft Power BI Learning Path", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"),
    "tableau": ("Tableau Free Training", "https://www.tableau.com/learn/training"),
}

DEFAULT_LINK = ("Search on Coursera", "https://www.coursera.org/search?query=")


def learning_resource(skill: str):
    key = skill.lower()
    if key in LEARNING_LINKS:
        return LEARNING_LINKS[key]
    label, base_url = DEFAULT_LINK
    return (f"{label}: {skill}", base_url + skill.replace(" ", "%20"))


col1, col2 = st.columns(2)
with col1:
    target_title = st.selectbox("🎯 Target Job Title", titles)
with col2:
    current_skills = st.multiselect("🧠 Skills you already have", options=known_skills)

if st.button("🗺️ Generate Roadmap", type="primary"):
    target_jobs = df[df["title"] == target_title]
    required_skills = set()
    for lst in target_jobs["skills_list"]:
        required_skills.update(lst)

    current_lower = set(s.lower() for s in current_skills)
    have = sorted([s for s in required_skills if s.lower() in current_lower])
    missing = sorted([s for s in required_skills if s.lower() not in current_lower])

    readiness = round(len(have) / len(required_skills) * 100, 1) if required_skills else 0

    st.markdown("---")
    st.subheader(f"Roadmap to become a {target_title}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Skills Required", len(required_skills))
    m2.metric("Skills You Have", len(have))
    m3.metric("Readiness", f"{readiness}%")
    st.progress(readiness / 100)

    st.markdown("### ✅ Skills You Already Have")
    st.markdown(" ".join(f"`{s}`" for s in have) or "_None yet — every skill below is a growth opportunity!_")

    st.markdown("### 📚 Skills to Learn Next")
    if missing:
        for i, skill in enumerate(missing, start=1):
            label, url = learning_resource(skill)
            with st.container(border=True):
                st.markdown(f"**Step {i}: {skill}**")
                st.markdown(f"[{label}]({url})")
    else:
        st.success("You already meet the skill profile for this role. 🎉")

    st.markdown("---")
    st.info(f"💡 Tip: Once you've closed these gaps, head to **🎯 Job Recommendations** "
            f"and search '{target_title}' to see how your new match score improves.")
else:
    st.info("Select a target role and your current skills, then click **Generate Roadmap**.")
