import streamlit as st
from utils.data_loader import load_jobs, get_filter_options
from utils.charts import (
    top_skills_chart, top_locations_chart,
    experience_distribution_chart, work_type_chart,
)

st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Global CSS — ported from the Nexora landing page design
# ============================================================
st.markdown("""
<style>
    :root{
        --bg: #08080b;
        --card: #131318;
        --card-2: #17171e;
        --border: #24242d;
        --text-dim: #9a9aa8;
        --text-dimmer: #6c6c78;
        --purple: #8b5cf6;
        --purple-2: #6d28d9;
        --purple-soft: rgba(139,92,246,0.14);
    }

    .stApp { background-color: var(--bg); }
    section[data-testid="stSidebar"]{
        background-color: #0a0a0f;
        border-right: 1px solid var(--border);
    }

    /* ---- eyebrow badge ---- */
    .eyebrow{
        display:inline-flex; align-items:center; gap:8px;
        background:var(--card); border:1px solid var(--border);
        padding:6px 14px; border-radius:999px; font-size:.78rem; color:var(--text-dim);
        margin-bottom:18px;
    }

    /* ---- hero glow + title ---- */
    .hero-glow{ position:relative; padding:6px 0 4px 0; }
    .hero-glow::before{
        content:""; position:absolute; top:-60px; left:-60px;
        width:320px; height:320px; border-radius:50%;
        background: radial-gradient(circle, rgba(139,92,246,0.30) 0%, rgba(139,92,246,0) 70%);
        filter: blur(40px); z-index:-1; pointer-events:none;
    }
    .hero-title{ font-size:3rem; line-height:1.08; font-weight:800; letter-spacing:-0.02em; color:#fff; }
    .hero-title .accent{
        background:linear-gradient(90deg,#a78bfa,#7c3aed);
        -webkit-background-clip:text; background-clip:text; color:transparent;
    }
    .hero-desc{ color:var(--text-dim); font-size:1rem; line-height:1.6; max-width:480px; margin:16px 0 8px; }

    .trust-row{ display:flex; align-items:center; gap:12px; margin-top:18px; font-size:.82rem; color:var(--text-dim); }
    .trust-row .stars{ color:#f5b942; }

    /* ---- buttons ---- */
    .stButton > button{
        background: linear-gradient(135deg,var(--purple),var(--purple-2));
        color:#fff; border:none; border-radius:9px; font-weight:600;
        padding:0.55rem 1.1rem;
        transition: box-shadow .15s ease, transform .15s ease;
    }
    .stButton > button:hover{ box-shadow:0 6px 18px rgba(139,92,246,0.4); transform:translateY(-1px); }

    /* ---- generic card ---- */
    .metric-card{
        background: linear-gradient(135deg, #1a1f2c 0%, #161a23 100%);
        border:1px solid var(--border); border-radius:14px; padding:18px 20px;
        transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
    }
    .metric-card:hover{ transform:translateY(-3px); border-color:var(--purple); box-shadow:0 8px 22px rgba(139,92,246,0.22); }
    .metric-label{ color:var(--text-dim); font-size:.78rem; font-weight:600; letter-spacing:.04em; text-transform:uppercase; }
    .metric-value{ color:#fff; font-size:1.9rem; font-weight:800; margin-top:4px; }
    .metric-delta{ color:#4ade80; font-size:.72rem; margin-top:4px; }

    /* ---- tool / feature cards ---- */
    .tool-card{
        background:var(--card); border:1px solid var(--border); border-radius:14px;
        padding:20px 18px; height:100%;
        transition: border-color .15s ease, transform .15s ease;
    }
    .tool-card:hover{ border-color:var(--purple); transform:translateY(-3px); }
    .tool-icon{
        width:36px; height:36px; border-radius:10px; background:var(--purple-soft);
        color:#a78bfa; display:flex; align-items:center; justify-content:center;
        font-size:1rem; margin-bottom:14px;
    }
    .tool-card h4{ color:#fff; font-size:.95rem; font-weight:700; margin:0 0 6px 0; }
    .tool-card p{ color:var(--text-dim); font-size:.8rem; line-height:1.45; margin:0; }

    /* ---- section headers ---- */
    .section-head{ text-align:center; max-width:560px; margin:36px auto 28px; }
    .section-head h2{ color:#fff; font-size:1.7rem; font-weight:700; letter-spacing:-.01em; margin-bottom:8px; }
    .section-head p{ color:var(--text-dim); font-size:.88rem; }

    /* ---- testimonials ---- */
    .t-card{ background:var(--card); border:1px solid var(--border); border-radius:14px; padding:20px; height:100%; }
    .t-card .quote{ color:#5a5a68; font-size:1.4rem; line-height:1; margin-bottom:8px; }
    .t-card p{ font-size:.85rem; color:#d4d4dc; line-height:1.5; margin-bottom:14px; }
    .t-author{ display:flex; align-items:center; gap:10px; }
    .t-author .av{ width:32px; height:32px; border-radius:50%; background:var(--card-2); }
    .t-author .name{ font-size:.8rem; font-weight:600; color:#fff; }
    .t-author .role{ font-size:.7rem; color:var(--text-dim); }

    /* ---- CTA banner ---- */
    .cta-banner{
        background: linear-gradient(135deg, #2a1560, #4c1d95 45%, #1a0b3a);
        border-radius:20px; padding:36px 40px; margin:20px 0;
    }
    .cta-banner h3{ color:#fff; font-size:1.5rem; font-weight:700; margin-bottom:6px; }
    .cta-banner p{ color:#d8cdf5; font-size:.85rem; margin-bottom:14px; }
    .cta-checks{ display:flex; gap:20px; flex-wrap:wrap; font-size:.78rem; color:#e4dcf8; }

    /* ---- job cards ---- */
    .job-card{
        background:var(--card); border:1px solid var(--border); border-radius:14px;
        padding:16px 18px; margin-bottom:12px;
        transition: border-color .15s ease, box-shadow .15s ease;
    }
    .job-card:hover{ border-color:var(--purple); box-shadow:0 6px 16px rgba(139,92,246,0.15); }
    .job-title{ color:#fff; font-weight:700; font-size:1rem; }
    .job-company{ color:#a78bfa; font-weight:600; font-size:.85rem; }
    .job-meta{ color:var(--text-dim); font-size:.78rem; margin-top:2px; }

    /* ---- footer ---- */
    .footer{
        border-top:1px solid var(--border); margin-top:40px; padding-top:24px;
        text-align:center; color:var(--text-dimmer); font-size:.8rem;
    }
    .footer a{ color:var(--text-dim); text-decoration:none; margin:0 8px; }
    .footer a:hover{ color:#fff; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load data
# ============================================================
try:
    df = load_jobs()
except Exception as e:
    st.error(f"Could not load dataset: {e}")
    st.info("Run `python data/generate_sample_data.py` to create a sample dataset, "
            "or place your own file at `data/jobs.csv`.")
    st.stop()

options = get_filter_options(df)

# ============================================================
# Sidebar — filters
# ============================================================
with st.sidebar:
    st.markdown("### 🎛️ Filters")
    location = st.selectbox("Location", ["All"] + options["locations"], key="g_location")
    work_type = st.selectbox("Work Type", ["All"] + options["work_types"], key="g_work_type")
    experience = st.selectbox("Experience", ["All"] + options["experience"], key="g_experience")
    st.divider()
    st.caption("Use the pages in the sidebar navigation above to search jobs, "
               "analyze your resume, or view your career roadmap.")

filtered_df = df.copy()
if location != "All":
    filtered_df = filtered_df[filtered_df["location"] == location]
if work_type != "All":
    filtered_df = filtered_df[filtered_df["work_type"] == work_type]
if experience != "All":
    filtered_df = filtered_df[filtered_df["experience"] == experience]

# ============================================================
# Hero
# ============================================================
st.markdown('<div class="hero-glow">', unsafe_allow_html=True)
st.markdown('<span class="eyebrow">⚡ AI THAT WORKS FOR YOU</span>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Find the Job.<br>Get the <span class="accent">Match.</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-desc">The AI Job Recommendation System matches you to roles using your skills, '
    'resume, and preferences — faster and more precisely than manual search.</p>',
    unsafe_allow_html=True,
)

col_a, col_b, _ = st.columns([1, 1, 3])
with col_a:
    st.button("🎯 Get Recommendations", use_container_width=True)
with col_b:
    st.button("📄 Analyze My Resume", use_container_width=True)

st.markdown(f"""
<div class="trust-row">
    <span class="stars">★★★★★</span> 4.9/5 &nbsp;•&nbsp; {len(df):,} jobs indexed &nbsp;•&nbsp; {df['company'].nunique():,} companies
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# Tools grid (Nexora "All the tools you need" section)
# ============================================================
st.markdown("""
<div class="section-head">
    <h2>Everything you need to land the role</h2>
    <p>From matching to preparation, in one place.</p>
</div>
""", unsafe_allow_html=True)

tools = [
    ("🎯", "Job Matching", "AI-ranked roles based on your skills, experience, and preferences."),
    ("📄", "Resume Analyzer", "Upload your resume and get an instant compatibility score."),
    ("🧭", "Career Roadmap", "See the path from your current skills to your target role."),
    ("🛠️", "Skill Gap Finder", "Discover the most in-demand skills missing from your profile."),
    ("🤖", "AI Assistant", "Ask questions about jobs, skills, or career advice, in plain language."),
]
t_cols = st.columns(5)
for col, (icon, title, desc) in zip(t_cols, tools):
    with col:
        st.markdown(f"""
        <div class="tool-card">
            <div class="tool-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("###")
st.markdown("---")

# ============================================================
# Dashboard metrics (Nexora "stat card" style, real data)
# ============================================================
st.subheader("📊 Market Overview")
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("TOTAL JOBS", f"{len(df):,}"),
    ("COMPANIES", f"{df['company'].nunique():,}"),
    ("LOCATIONS", f"{df['location'].nunique():,}"),
    ("SKILLS TRACKED", f"{len(set(s for lst in df['skills_list'] for s in lst)):,}"),
]
for col, (label, value) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("###")

row1c1, row1c2 = st.columns(2)
with row1c1:
    st.plotly_chart(top_skills_chart(df), use_container_width=True)
with row1c2:
    st.plotly_chart(top_locations_chart(df), use_container_width=True)

row2c1, row2c2 = st.columns(2)
with row2c1:
    st.plotly_chart(experience_distribution_chart(df), use_container_width=True)
with row2c2:
    st.plotly_chart(work_type_chart(df), use_container_width=True)

st.markdown("---")

# ============================================================
# Featured jobs
# ============================================================
st.subheader("🛍️ Featured Job Matches")
preview_df = filtered_df.head(4) if len(filtered_df) else df.head(4)
if len(preview_df) == 0:
    st.info("No jobs match the current filters. Try adjusting them in the sidebar.")
else:
    for _, row in preview_df.iterrows():
        skills_preview = ", ".join(row["skills_list"][:5]) if "skills_list" in row else ""
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">{row.get('title', 'Untitled Role')}</div>
            <div class="job-company">{row.get('company', 'Unknown Company')}</div>
            <div class="job-meta">📍 {row.get('location', '—')} &nbsp;•&nbsp; 💼 {row.get('work_type', '—')} &nbsp;•&nbsp; 🎓 {row.get('experience', '—')}</div>
            <div class="job-meta">🛠️ {skills_preview}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# Testimonials (Nexora "Loved by teams worldwide" section)
# ============================================================
st.markdown("""
<div class="section-head">
    <h2>Loved by job seekers</h2>
    <p>People are finding better-fit roles, faster.</p>
</div>
""", unsafe_allow_html=True)

testimonials = [
    ("Went from 200 blind applications to 12 targeted ones. The match scores actually meant something.", "Sarah Chen", "Data Analyst"),
    ("The skill gap finder told me exactly what to learn next. Landed an interview two weeks later.", "David Lee", "Backend Engineer"),
    ("Resume analyzer caught formatting issues I'd missed for months. Simple, but it worked.", "Priya Patel", "Product Designer"),
]
tt_cols = st.columns(3)
for col, (quote, name, role) in zip(tt_cols, testimonials):
    with col:
        st.markdown(f"""
        <div class="t-card">
            <div class="quote">"</div>
            <p>{quote}</p>
            <div class="t-author">
                <div class="av"></div>
                <div><div class="name">{name}</div><div class="role">{role}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("###")

# ============================================================
# AI Chat Assistant (native Streamlit chat)
# ============================================================
st.subheader("🤖 AI Job Assistant")
st.caption("Ask about roles, skills, or how to improve your match score.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi! Ask me things like 'What skills are trending?' or 'Show me remote jobs.'"}
    ]

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_msg = st.chat_input("Type your question...")
if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    lower_msg = user_msg.lower()
    if "remote" in lower_msg:
        remote_count = len(df[df["work_type"].str.lower() == "remote"]) if "work_type" in df else 0
        reply = f"There are currently {remote_count} remote jobs in the dataset. Try the Work Type filter in the sidebar to explore them."
    elif "skill" in lower_msg:
        all_skills = [s for lst in df["skills_list"] for s in lst]
        top_skill = max(set(all_skills), key=all_skills.count) if all_skills else "N/A"
        reply = f"The most in-demand skill right now is **{top_skill}**. Check the 'Top Skills' chart above for the full breakdown."
    elif "resume" in lower_msg:
        reply = "Head to the **📄 Resume Analyzer** page in the sidebar to upload your resume and get an instant match score."
    else:
        reply = "I can help with job matches, trending skills, and resume analysis. Try asking about a specific skill, location, or work type."

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("---")

# ============================================================
# CTA banner
# ============================================================
st.markdown("""
<div class="cta-banner">
    <h3>Ready to find your next role?</h3>
    <p>Set your filters, upload your resume, and let the AI do the matching.</p>
    <div class="cta-checks">
        <span>✓ Free to use</span>
        <span>✓ No account required</span>
        <span>✓ Instant match scores</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.info("👉 Head to **🎯 Job Recommendations** in the sidebar to search by title or skills, "
        "or **📄 Resume Analyzer** to upload your resume and get instant matches.")


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<style>

.footer-box{
    background:#111827;
    padding:40px;
    border-radius:12px;
    margin-top:60px;
}

.footer-title{
    color:white;
    font-size:20px;
    font-weight:700;
    margin-bottom:15px;
}

.footer-desc{
    color:#d1d5db;
    font-size:17px;
    line-height:1.7;
}

.footer-copy{
    text-align:center;
    color:#9ca3af;
    font-size:20px;
    padding-top:20px;
}

hr{
    border:0.5px solid #374151;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="footer-box">', unsafe_allow_html=True)

# -------------------------
# Four Columns
# -------------------------

col1, col2, col3, col4 = st.columns([3.5, 2, 2, 2])

# ==========================
# Column 1
# ==========================

with col1:
    st.markdown('<div class="footer-title">🤖 AI Job Recommender</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-desc">'
        'Helping students and professionals discover the best career '
        'opportunities using Artificial Intelligence.'
        '</div>',
        unsafe_allow_html=True,
    )

# ==========================
# Column 2
# ==========================

with col2:
    st.markdown('<div class="footer-title">Quick Links</div>',
                unsafe_allow_html=True)

    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Job_Recommendations.py", label="💼 Jobs")
    st.page_link("pages/2_Resume_Analyzer.py", label="📄 Resume Analyzer")
    st.page_link("pages/3_Career_Roadmap.py", label="🗺️ Career Roadmap")

# ==========================
# Column 3
# ==========================

with col3:
    st.markdown('<div class="footer-title">Support</div>',
                unsafe_allow_html=True)

    st.page_link("pages/98_Privacy.py", label="🔒 Privacy Policy")
    st.page_link("pages/99_Contact.py", label="📞 Contact")
    st.page_link("pages/100_About.py", label="ℹ️ About")


# ==========================
# Column 4
# ==========================

with col4:
    st.markdown('<div class="footer-title">Developer</div>',
                unsafe_allow_html=True)

    st.markdown("👨‍💻 **Ayush Yadav**")

    st.markdown(
        "📧 [ayushdatsci@gmail.com](mailto:ayushdatsci@gmail.com)"
    )

    st.link_button(
        "💻 GitHub",
        "https://github.com/aayushyadv",
        use_container_width=True
    )

    st.link_button(
        "🌐 Portfolio",
        "https://aayushyadv.github.io/",
        use_container_width=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
<div class="footer-copy">
© 2026 AI Job Recommender • Made with ❤️ using Python, Streamlit & Machine Learning
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
