"""
Generates a synthetic jobs dataset (data/jobs.csv) so the app runs out of the box.
Replace this file's output with your real dataset (same column names) at any time.

Run:  python data/generate_sample_data.py
"""
import random
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

SKILLS_POOL = [
    "Python", "SQL", "Java", "JavaScript", "React", "Node.js", "AWS", "Azure",
    "GCP", "Docker", "Kubernetes", "Machine Learning", "Deep Learning", "TensorFlow",
    "PyTorch", "NLP", "Computer Vision", "Data Analysis", "Excel", "Power BI",
    "Tableau", "Spark", "Hadoop", "Airflow", "Git", "REST APIs", "GraphQL",
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "Linux", "CI/CD", "Terraform",
    "C++", "C#", ".NET", "Django", "Flask", "FastAPI", "Kafka", "Snowflake",
    "dbt", "Scikit-learn", "Pandas", "NumPy", "R", "Statistics", "A/B Testing",
    "Product Management", "Agile", "Scrum", "Communication", "Leadership",
    "Project Management", "UX Design", "Figma", "HTML/CSS", "TypeScript",
    "Go", "Rust", "Swift", "Kotlin", "Android", "iOS", "Salesforce", "SAP",
    "Cybersecurity", "Networking", "DevOps", "Data Engineering", "ETL",
    "Business Analysis", "Financial Modeling",
]  # 71 skills

TITLES = [
    "Data Scientist", "Data Analyst", "Machine Learning Engineer", "Software Engineer",
    "Backend Developer", "Frontend Developer", "Full Stack Developer", "DevOps Engineer",
    "Cloud Engineer", "Data Engineer", "Business Analyst", "Product Manager",
    "AI Engineer", "NLP Engineer", "Cybersecurity Analyst", "Project Manager",
    "UX Designer", "Systems Administrator", "QA Engineer", "Site Reliability Engineer",
]

WORK_TYPES = ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
EXPERIENCE = ["Entry Level", "Mid Level", "Senior Level", "Lead/Manager"]

N_JOBS = 15886
N_LOCATIONS = 3010
N_COMPANIES = 5976

locations = [f"{fake.city()}, {fake.state_abbr()}" for _ in range(N_LOCATIONS)]
companies = [fake.company() for _ in range(N_COMPANIES)]

rows = []
for i in range(N_JOBS):
    title = random.choice(TITLES)
    n_skills = random.randint(4, 9)
    skills = random.sample(SKILLS_POOL, n_skills)
    exp = random.choice(EXPERIENCE)
    rows.append({
        "job_id": i + 1,
        "title": title,
        "company": random.choice(companies),
        "location": random.choice(locations),
        "work_type": random.choice(WORK_TYPES),
        "experience": exp,
        "skills": ", ".join(skills),
        "description": f"We are looking for a {title} with experience in {', '.join(skills[:3])}. "
                        f"This is a {exp.lower()} role focused on delivering high quality solutions.",
        "salary_min": random.randint(40, 120) * 1000,
        "salary_max": random.randint(120, 220) * 1000,
        "posted_days_ago": random.randint(0, 60),
    })

df = pd.DataFrame(rows)
df.to_csv("data/jobs.csv", index=False)
print(f"Generated {len(df)} jobs -> data/jobs.csv")
print(f"Unique companies: {df['company'].nunique()}")
print(f"Unique locations: {df['location'].nunique()}")
print(f"Unique skills: {len(SKILLS_POOL)}")
