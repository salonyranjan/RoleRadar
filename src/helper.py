import fitz  # PyMuPDF
import os
import json
import time
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the 2026 Unified Google Gen AI Client
# This client is optimized for high-concurrency agentic workflows
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF stream using PyMuPDF.
    Includes a seek(0) to ensure the stream is read from the start if re-run.
    """
    try:
        uploaded_file.seek(0)
        file_content = uploaded_file.read()
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            # Join pages with form feed character for clean separation
            text = chr(12).join([page.get_text() for page in doc])
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def get_role_radar_analysis(resume_text, retries=3):
    """
    Performs a single-pass, context-aware analysis using Gemini 2.5 Flash-Lite.
    Optimized for 2026 Free Tier limits (15 RPM / 1M TPM).
    """
    # SAFETY: Trim resume text to ~8,000 characters to stay under TPM (Tokens Per Minute) burst limits.
    # Most 2-3 page resumes are well under this limit.
    safe_resume_context = resume_text[:8000]

    prompt = f"""
    You are an expert Career Strategist. Analyze the following resume for 2026 tech market alignment.
    Return ONLY a valid JSON object with these EXACT keys:
    
    1. "summary": A 3-sentence high-level professional overview.
    2. "gaps": 3-5 technical or soft skill gaps specifically for AI, ML, or Full-Stack roles.
    3. "roadmap": A concise 6-month step-by-step learning and project plan.
    4. "keywords": 3-4 primary job titles for search, returned as a comma-separated string.

    Resume Context:
    {safe_resume_context}
    """

    for attempt in range(retries):
        try:
            # Using 'gemini-2.5-flash-lite' for higher quota limits and lower latency
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=1000,
                    temperature=0.1, # Critical for stable JSON output
                    response_mime_type="application/json" 
                )
            )
            
            # Sanitization: Clean potential markdown backticks
            raw_text = response.text.strip()
            clean_json = re.sub(r'^```json\s*|```$', '', raw_text, flags=re.MULTILINE)
            
            return json.loads(clean_json)

        except Exception as e:
            error_msg = str(e).lower()
            # 2026 Quota Handling: If rate limited, wait 12s to clear the burst bucket
            if ("429" in error_msg or "resource_exhausted" in error_msg) and attempt < retries - 1:
                time.sleep(12) 
                continue
            
            # Final Fallback Data Structure if all retries fail
            return {
                "summary": "The Radar is currently experiencing high traffic. Please try again in 60 seconds.",
                "gaps": "Scan pending...",
                "roadmap": "Strategic plan generation delayed.",
                "keywords": "Software Engineer, AI Developer",
                "error": str(e)
            }

def ask_gemini(prompt, max_tokens=250):
    """
    A lightweight wrapper for simple, single-turn tasks.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.5
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Radar Error: {str(e)}"