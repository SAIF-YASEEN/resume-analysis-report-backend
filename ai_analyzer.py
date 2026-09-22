import json
import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")


# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_resume_with_ai(resume_text):

    prompt = f"""
You are a professional AI resume analyzer.

Analyze the resume below and extract information accurately.

IMPORTANT RULES:

1. Only use information actually present in the resume.

2. Never invent companies, dates, degrees, skills,
   projects, certifications, or experience.

3. If information is missing, return null or an empty array.

4. Understand different resume section names.

5. Normalize technology names where appropriate.

Examples:
React.js -> React
Express.js -> Express
Node.js -> Node.js
MongoDB -> MongoDB

6. Separate technical skills from soft skills.

7. Extract complete professional experience.

8. Extract projects with their names, descriptions,
   technologies, and important highlights.

9. Extract education accurately.

10. Extract certifications accurately.

11. Extract languages if they are mentioned.

12. Identify strengths based only on evidence in the resume.

13. Identify weaknesses or missing areas carefully.
    Do not invent weaknesses.

14. Provide practical resume improvement suggestions.

15. Estimate an ATS score from 0-100 based on:

    - Resume structure
    - Readability
    - Keyword usage
    - Completeness
    - Skills
    - Experience descriptions
    - Project descriptions
    - Education
    - Contact information

16. The ATS score is an estimate of resume quality.
    It is NOT a prediction of hiring success.

17. Return ONLY valid JSON.

18. Do not use Markdown.

19. Do not use ```json.

20. Make sure the result can be parsed using
    Python json.loads().

Return this exact JSON structure:

{{
    "personal": {{
        "name": null,
        "email": null,
        "phone": null,
        "location": null,
        "linkedin": null,
        "github": null,
        "portfolio": null
    }},

    "summary": null,

    "skills": {{
        "technical": [],
        "soft": [],
        "tools": [],
        "frameworks": [],
        "databases": []
    }},

    "education": [
        {{
            "degree": null,
            "institution": null,
            "location": null,
            "start_date": null,
            "end_date": null,
            "details": null
        }}
    ],

    "experience": [
        {{
            "job_title": null,
            "company": null,
            "location": null,
            "start_date": null,
            "end_date": null,
            "current": false,
            "responsibilities": [],
            "technologies": []
        }}
    ],

    "projects": [
        {{
            "name": null,
            "description": null,
            "technologies": [],
            "highlights": []
        }}
    ],

    "certifications": [
        {{
            "name": null,
            "issuer": null,
            "date": null
        }}
    ],

    "languages": [],

    "strengths": [],

    "weaknesses": [],

    "missing_sections": [],

    "ats_score": 0,

    "ats_feedback": [],

    "improvements": []
}}

RESUME:

{resume_text}
"""

    try:

        print("\n==============================")
        print("Sending resume to Gemini AI...")
        print("==============================")

        # Gemini Interactions API
        interaction = client.interactions.create(model="gemini-3.6-flash", input=prompt)

        result_text = interaction.output_text

        print("\n==============================")
        print("Gemini response received")
        print("==============================")

        print(result_text)

        print("==============================\n")

        if not result_text:
            raise ValueError("Gemini returned an empty response")

        # Convert AI response into Python dictionary
        try:

            result = json.loads(result_text)

        except json.JSONDecodeError:

            print("Gemini returned JSON with formatting issues.")

            cleaned = result_text.strip()

            # Remove accidental Markdown code fences
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]

            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            result = json.loads(cleaned)

        print("\nAI JSON successfully parsed!")

        return result

    except Exception as error:

        print("\n==============================")
        print("Gemini API Error:")
        print(error)
        print("==============================\n")

        raise
