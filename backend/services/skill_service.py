SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "react",
    "nodejs",
    "mongodb",
    "mysql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "machine learning",
    "deep learning",
    "data science",
    "tensorflow",
    "pandas",
    "numpy",
    "sql",
    "git",
    "github"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills