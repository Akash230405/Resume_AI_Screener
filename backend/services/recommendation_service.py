def generate_recommendation(
    matched_skills,
    missing_skills
):

    recommendation = ""

    if len(matched_skills) >= 5:

        recommendation += (
            "Strong candidate with good skill alignment. "
        )

    elif len(matched_skills) >= 3:

        recommendation += (
            "Candidate matches several required skills. "
        )

    else:

        recommendation += (
            "Candidate needs additional skill development. "
        )

    if missing_skills:

        recommendation += (
            "Recommended to learn: "
            + ", ".join(missing_skills)
            + "."
        )

    return recommendation