"""
matcher.py — Resume matching logic for JobLens.

Pure matching functions callable without any terminal interaction.
Does NOT import repository.py — skills are passed in by the caller.
PDF path constants live in cli.py, not here.
"""

from pypdf import PdfReader


DISPLAY_NAMES = {
    "sql": "SQL",
    "aws": "AWS",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "github": "GitHub",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "postgresql": "PostgreSQL",
}


# to show skills properly, eg AWS might show as Aws, so this will help with that
def format_skill(skill):
    return DISPLAY_NAMES.get(skill, skill.title())


def extract_pdf_text(pdf_path):
    """
    Extract text from all pages of a PDF file.

    Parameters
    ----------
    pdf_path : str – path to the PDF file

    Returns
    -------
    str – the concatenated text content of every page
    """
    reader = PdfReader(pdf_path)

    # Loop through each page and accumulate its content
    resume_text = ""
    for index, page in enumerate(reader.pages):
        resume_text += page.extract_text()
    return resume_text


def extract_skills(text, stored_skills):
    extracted_skills = set()
    for skill in stored_skills:
        if skill in text:
            extracted_skills.add(skill)
    
    return extracted_skills

def calculate_match_score(matched, jd_skills):
    if not jd_skills:
        return 0

    return (len(matched) / len(jd_skills)) * 100


def match_resume(resume_text, job_description, skills):
    """
    Match a resume against a job description.

    Parameters
    ----------
    resume_text     : str  – full text extracted from the resume PDF
    job_description : str  – the job description text
    skills          : set  – set of skill strings to look for

    Returns
    -------
    dict with keys: score, matched, missing, jd_skills
    """
    resume_skills = extract_skills(resume_text.lower(), skills)
    jd_skills = extract_skills(job_description.lower(), skills)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = calculate_match_score(matched, jd_skills)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "jd_skills": jd_skills,
    }
