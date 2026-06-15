// Resume Analysis

document
.getElementById("resumeForm")
.addEventListener(
    "submit",
    async function(e){

        e.preventDefault();

        try{

            const formData = new FormData();

            formData.append(
                "resume",
                document.getElementById(
                    "resume"
                ).files[0]
            );

            formData.append(
                "job_description",
                document.getElementById(
                    "jobDescription"
                ).value
            );

            const response = await fetch(
                "http://127.0.0.1:5000/resume/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data =
            await response.json();

            document.getElementById(
            "result"
            ).innerHTML = `
            <h2>Analysis Result</h2>

            <p><strong>File:</strong> ${data.filename}</p>

            <p><strong>Score:</strong> ${data.score}%</p>

            <p><strong>Status:</strong> ${data.status}</p>

            <p>
                <strong>Matched Skills:</strong>
                ${data.matched_skills.join(", ")}
            </p>

            <p>
                <strong>Missing Skills:</strong>
                ${data.missing_skills.join(", ")}
            </p>
            <p>
                <strong>Recommendation:</strong>
                ${data.recommendation}
            </p>
        `;

        }
        catch(error){

            console.error(error);

            document.getElementById(
                "result"
            ).innerHTML =
            `<h3>Error: ${error.message}</h3>`;
        }

    }
);


// Candidate Ranking
async function loadCandidates(){

    try{

        const response = await fetch(
            "http://127.0.0.1:5000/resume/candidates"
        );

        const data = await response.json();

        const tbody =
        document.querySelector(
            "#candidateTable tbody"
        );

        tbody.innerHTML = "";

        data.forEach(
            (candidate,index)=>{

                tbody.innerHTML += `
                <tr>

                    <td>${index + 1}</td>

                    <td>
                        <button
                        onclick="loadCandidateDetails('${candidate.filename}')">
                        ${candidate.filename}
                        </button>
                    </td>

                    <td>${candidate.score}%</td>

                    <td>${candidate.status}</td>

                </tr>
                `;
            }
        );

    }
    catch(error){

        console.error(error);

        alert(
            "Unable to load candidates"
        );
    }

}



async function loadAnalytics(){

    try{

        const response = await fetch(
            "http://127.0.0.1:5000/resume/analytics"
        );

        const data =
        await response.json();

        document.getElementById(
            "analytics"
        ).innerHTML = `

            <p>
                <strong>Total Resumes:</strong>
                ${data.total_resumes}
            </p>

            <p>
                <strong>Average Score:</strong>
                ${data.average_score}%
            </p>

            <p>
                <strong>Highest Score:</strong>
                ${data.highest_score}%
            </p>

            <p>
                <strong>Lowest Score:</strong>
                ${data.lowest_score}%
            </p>

            <p>
                <strong>Shortlisted:</strong>
                ${data.shortlisted}
            </p>

            <p>
                <strong>Rejected:</strong>
                ${data.rejected}
            </p>

        `;

    }
    catch(error){

        console.error(error);

        alert(
            "Unable to load analytics"
        );

    }

}


async function loadCandidateDetails(filename){

    try{

        const response = await fetch(
            `http://127.0.0.1:5000/resume/candidate/${filename}`
        );

        const data = await response.json();

        document.getElementById(
            "candidateDetails"
        ).innerHTML = `
            <h3>Candidate Details</h3>

            <p>
                <strong>Resume:</strong>
                ${data.filename}
            </p>

            <p>
                <strong>Score:</strong>
                ${data.score}%
            </p>

            <p>
                <strong>Status:</strong>
                ${data.status}
            </p>

            <p>
                <strong>Matched Skills:</strong>
                ${(data.matched_skills || []).join(", ")}
            </p>

            <p>
                <strong>Missing Skills:</strong>
                ${(data.missing_skills || []).join(", ")}
            </p>

            <p>
                <strong>Recommendation:</strong>
                ${data.recommendation || "No recommendation available"}
            </p>

            <p>
                <a
                    href="http://127.0.0.1:5000/resume/download/${data.filename}"
                    target="_blank"
                >
                    DOWNLOAD RESUME
                </a>
            </p>
        `;

    }
    catch(error){

        console.error(error);

        alert(
            "Unable to load candidate details"
        );

    }



    function downloadResume(filename){

        window.location.href =
        `http://127.0.0.1:5000/resume/download/${filename}`;

}

}