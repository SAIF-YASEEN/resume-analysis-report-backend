from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from resume_parser import analyze_resume
from ai_analyzer import analyze_resume_with_ai

app = FastAPI(title="AI Resume Analyzer API")


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Root Route
# ==============================


@app.get("/")
def root():

    return {"success": True, "message": "AI Resume Analyzer API is running"}


# ==============================
# Resume Analysis
# ==============================


@app.post("/api/resumes/analyze")
async def analyze_resume_endpoint(file: UploadFile = File(...)):

    print("\n==============================")
    print("Backend received resume")
    print("==============================")

    print("Filename:", file.filename)

    print("Content Type:", file.content_type)

    try:

        # ==============================
        # Read uploaded file
        # ==============================

        contents = await file.read()

        print("File Size:", len(contents), "bytes")

        # ==============================
        # Extract resume text
        # ==============================

        resume_text = analyze_resume(contents, file.filename)

        print("\nText extracted successfully!")

        # ==============================
        # Send text to Gemini AI
        # ==============================

        ai_result = analyze_resume_with_ai(resume_text)

        # ==============================
        # Display AI result
        # ==============================

        print("\n==============================")
        print("AI ANALYSIS RESULT")
        print("==============================")

        print("Name:", ai_result["personal"]["name"])

        print("Email:", ai_result["personal"]["email"])

        print("Phone:", ai_result["personal"]["phone"])

        print("ATS Score:", ai_result["ats_score"])

        print("\nSkills:", ai_result["skills"])

        print("\nExperience:", ai_result["experience"])

        print("\nProjects:", ai_result["projects"])

        print("\nEducation:", ai_result["education"])

        print("\nCertifications:", ai_result["certifications"])

        print("\nStrengths:", ai_result["strengths"])

        print("\nWeaknesses:", ai_result["weaknesses"])

        print("\nImprovements:", ai_result["improvements"])

        print("==============================\n")

        # ==============================
        # Send result to React
        # ==============================

        response = {
            "success": True,
            "message": "Resume analyzed successfully",
            "filename": file.filename,
            "data": ai_result,
        }

        print("Sending AI analysis to frontend...")

        return response

    except ValueError as error:

        print("Validation Error:", error)

        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:

        print("ERROR:", error)

        raise HTTPException(status_code=500, detail="Failed to analyze resume")
