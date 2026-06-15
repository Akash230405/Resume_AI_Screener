import os
from backend.services.resume_parser import extract_text_from_pdf


UPLOAD_FOLDER = "uploads/resumes"


def upload_resume(request):

    if "resume" not in request.files:
        return {"error":"No resume uploaded"},400


    file = request.files["resume"]


    if file.filename == "":
        return {"error":"No file selected"},400


    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    file.save(filepath)


    text = extract_text_from_pdf(filepath)


    return {
        "message":"Resume uploaded",
        "file":file.filename,
        "text":text[:300]
    }