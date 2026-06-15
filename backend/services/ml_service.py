from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_cleaner import clean_text
from backend.services.skill_service import extract_skills


def calculate_score(
    resume_text,
    job_description
):

    resume_text = clean_text(
        resume_text
    )

    job_description = clean_text(
        job_description
    )

    # TF-IDF Similarity

    data = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        data
    )

    tfidf_score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0] * 100

    # Skill Match Score

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    if len(job_skills) > 0:

        matched_skills = len(
            set(resume_skills)
            &
            set(job_skills)
        )

        skill_score = (
            matched_skills /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0

    # Final Hybrid Score

    final_score = (
        (0.7 * skill_score)
        +
        (0.3 * tfidf_score)
    )

    return round(
        final_score,
        2
    )