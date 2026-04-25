skills_list = [
    "python", "machine learning", "sql", "excel", "react",
    "java", "spring boot", "fastapi", "data analysis",
    "pandas", "numpy", "power bi", "deep learning",
    "nlp", "tensorflow", "docker", "aws"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))