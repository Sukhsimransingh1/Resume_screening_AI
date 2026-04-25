from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from backend.parser import extract_text
from backend.utils import clean_text, extract_experience
from backend.model import calculate_similarity
from backend.skills import extract_skills

app = FastAPI()

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def calculate_skill_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0

    matched = set(resume_skills) & set(jd_skills)
    score = len(matched) / len(jd_skills)

    return round(score * 100, 2)


def calculate_experience_score(resume_exp, jd_exp):
    if jd_exp == 0:
        return 100.0

    if resume_exp >= jd_exp:
        return 100.0

    return round((resume_exp / jd_exp) * 100, 2)


@app.get("/")
def home():
    return {"message": "Resume Screening AI Backend Running"}


@app.post("/upload/")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    resume_text = extract_text(file_path)

    # Clean text
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    # BERT similarity
    bert_score = calculate_similarity(cleaned_resume, cleaned_jd)

    # Skill extraction
    resume_skills = extract_skills(cleaned_resume)
    jd_skills = extract_skills(cleaned_jd)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # Skill score
    skill_score = calculate_skill_score(resume_skills, jd_skills)

    # Experience extraction
    resume_exp = extract_experience(cleaned_resume)
    jd_exp = extract_experience(cleaned_jd)

    # Experience score
    experience_score = calculate_experience_score(resume_exp, jd_exp)

    # Final weighted score
    final_score = round(
        (skill_score * 0.4) +
        (experience_score * 0.2) +
        (bert_score * 0.4),
        2
    )

    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Add {skill} to your skillset or include relevant project experience."
        )

    if resume_exp < jd_exp:
        suggestions.append(
            f"Increase experience from {resume_exp} to {jd_exp}+ years or highlight relevant projects."
        )

    if bert_score < 60:
        suggestions.append(
            "Resume is not well aligned with the job description. Tailor keywords and project descriptions."
        )
    elif 60 <= bert_score < 80:
        suggestions.append(
            "Good match, but you can improve by aligning your resume wording more closely with the job description."
        )

    return {
        "final_score": final_score,
        "bert_score": bert_score,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "resume_experience": resume_exp,
        "jd_experience": jd_exp,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }