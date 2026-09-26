import re
from collections import Counter


SKILLS = {
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "flask",
    "django",
    "react",
    "node",
    "git",
    "github",
    "rest api",
    "api",
    "machine learning",
    "artificial intelligence",
    "ai",
    "data science",
    "pandas",
    "numpy",
    "communication",
    "teamwork",
    "problem solving",
}


def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    text = clean_text(text)
    found = set()

    for skill in SKILLS:
        if skill in text:
            found.add(skill)

    return sorted(found)


def calculate_match(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "match_level": "Not enough information",
            "recommendation": "Add technical skills to the job description."
        }

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    score = round((len(matched) / len(job_skills)) * 100)

    if score >= 80:
        level = "Excellent Match"
        recommendation = "Your profile is a strong match for this opportunity."
    elif score >= 60:
        level = "Good Match"
        recommendation = "Consider improving a few missing skills before applying."
    elif score >= 40:
        level = "Needs Improvement"
        recommendation = "Build skills: " + ", ".join(sorted(missing)[:5])
    else:
        level = "Low Match"
        recommendation = "Focus on the key skills required for this role."

    return {
        "match_percentage": score,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "match_level": level,
        "recommendation": recommendation,
    }