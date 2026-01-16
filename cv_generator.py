from models import CVWithPersonalInfo
from pathlib import Path
from llm import LLM


def generate_cv(
    base_cv: CVWithPersonalInfo, job_description: str, user_story: str
) -> CVWithPersonalInfo:
    """Generate a tailored CV based on the base CV and job description."""
    llm = LLM(provider="ollama")

    new_cv = llm.generate_cv(
        user_story=user_story,
        job_description=job_description,
        base_cv=base_cv.into_cv(),
    )

    new_cv_with_personal_info = CVWithPersonalInfo.from_cv(
        new_cv,
        full_name=base_cv.full_name,
        email=base_cv.email,
        phone=base_cv.phone,
        links=base_cv.links,
    )

    return new_cv_with_personal_info
