from flask import Blueprint, request,send_file
from backend.controllers.resume_controller import upload_resume
from backend.services.ml_service import calculate_score
from backend.services.skill_service import extract_skills
from backend.services.resume_parser import extract_text_from_pdf
from backend.services.recommendation_service import generate_recommendation
from backend.database.db import scores
from datetime import datetime
import os

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/upload", methods=["POST"])
def upload():
    return upload_resume(request)


@resume_bp.route("/score", methods=["POST"])
def score():

    data = request.get_json()

    resume = data.get("resume")
    job_description = data.get("job_description")

    result = calculate_score(
        resume,
        job_description
    )

    scores.insert_one({
        "resume": resume,
        "job_description": job_description,
        "match_percentage": result,
        "created_at": datetime.utcnow()
    })

    return {
        "match_percentage": result
    }


@resume_bp.route("/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return {
            "error": "Resume file missing"
        }, 400

    file = request.files["resume"]

    job_description = request.form.get(
        "job_description"
    )

    if not job_description:
        return {
            "error": "Job description required"
        }, 400

    os.makedirs(
        "uploads/resumes",
        exist_ok=True
    )

    filepath = os.path.join(
        "uploads/resumes",
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text_from_pdf(
        filepath
    )

    # DEBUG
    print("\n========== RESUME TEXT ==========")
    print(resume_text[:1000])
    print("=================================\n")

    print("Resume Length:", len(resume_text))

    score = calculate_score(
        resume_text,
        job_description
    )

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matched_skills = list(
        set(resume_skills) &
        set(job_skills)
    )

    missing_skills = list(
        set(job_skills) -
        set(resume_skills)
    )
    recommendation = generate_recommendation(
    matched_skills,
    missing_skills
    )

    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)
    print("Matched Skills:", matched_skills)
    print("Missing Skills:", missing_skills)

    status = (
        "Shortlisted"
        if score >= 60
        else "Rejected"
    )

    scores.insert_one({
        "filename": file.filename,
        "resume_text": resume_text,
        "job_description": job_description,
        "score": score,
        "status": status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "created_at": datetime.utcnow()
    })

    return {
        "filename": file.filename,
        "score": score,
        "status": status,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }


@resume_bp.route("/candidates", methods=["GET"])
def get_candidates():

    candidates = []

    docs = scores.find().sort(
        "score",
        -1
    )

    for doc in docs:

        candidates.append({
            "filename": doc.get(
                "filename",
                ""
            ),
            "score": doc.get(
                "score",
                0
            ),
            "status": doc.get(
                "status",
                ""
            )
        })

    return candidates

@resume_bp.route("/analytics", methods=["GET"])
def analytics():

    docs = list(scores.find())

    total_resumes = len(docs)

    if total_resumes == 0:

        return {
            "total_resumes": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "shortlisted": 0,
            "rejected": 0
        }

    score_list = [
        doc.get("score", 0)
        for doc in docs
    ]

    shortlisted = len([
        doc for doc in docs
        if doc.get("status") == "Shortlisted"
    ])

    rejected = len([
        doc for doc in docs
        if doc.get("status") == "Rejected"
    ])

    return {
        "total_resumes": total_resumes,
        "average_score": round(
            sum(score_list) / total_resumes,
            2
        ),
        "highest_score": max(score_list),
        "lowest_score": min(score_list),
        "shortlisted": shortlisted,
        "rejected": rejected
    }


@resume_bp.route(
    "/download/<filename>",
    methods=["GET"]
)
def download_resume(filename):

    filepath = os.path.join(
        "uploads/resumes",
        filename
    )

    if not os.path.exists(filepath):

        return {
            "error": "Resume not found"
        }, 404

    return send_file(
        filepath,
        as_attachment=True
    )

@resume_bp.route(
    "/candidate/<filename>",
    methods=["GET"]
)
def get_candidate(filename):

    candidate = scores.find_one({
        "filename": filename
    })

    if not candidate:

        return {
            "error": "Candidate not found"
        }, 404

    return {
        "filename": candidate.get(
            "filename",
            ""
        ),
        "score": candidate.get(
            "score",
            0
        ),
        "status": candidate.get(
            "status",
            ""
        ),
        "matched_skills": candidate.get(
            "matched_skills",
            []
        ),
        "missing_skills": candidate.get(
            "missing_skills",
            []
        ),
        "recommendation": candidate.get(
            "recommendation",
            ""
        )
    }

