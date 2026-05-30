import os
import json
import logging
import re
import pandas as pd
from typing import List, Dict, Any, Union
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger("ingest")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using pypdf.
    
    Args:
        pdf_path (str): Absolute or relative path to the PDF file.
        
    Returns:
        str: Extracted text.
    """
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
        return "\n".join(text_parts).strip()
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path}: {e}")
        return ""

def load_job_description(file_path: str) -> str:
    """
    Loads and reads the job description from a text or PDF file.
    
    Args:
        file_path (str): Path to the job description file.
        
    Returns:
        str: Normalized job description text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Job description file not found at: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        # Default text reading
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()

def parse_resume_with_llm(raw_text: str, filename: str) -> Dict[str, Any]:
    """
    Uses Google Gemini to parse unstructured resume text into our standardized fields.
    Falls back to a robust heuristic parser if Gemini is disabled or fails.
    
    Args:
        raw_text (str): Raw extracted text from resume.
        filename (str): Source filename.
        
    Returns:
        Dict[str, Any]: Standardized candidate profile dict.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    enabled = api_key and api_key.strip() != "" and api_key.strip() != "your_key_here"
    
    if enabled:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={"response_mime_type": "application/json"}
            )
            
            prompt = f"""You are a resume parsing assistant. Parse the following raw resume text and return ONLY valid JSON:
{{
  "name": "Candidate Name (string)",
  "current_title": "Professional Title (string)",
  "years_experience": float representing total years of experience,
  "skills": ["list", "of", "skills"],
  "education": "Degree, major, university (string)",
  "summary": "Professional summary (string)",
  "projects": "Key projects/achievements (string)",
  "github_url": "GitHub URL if present (string)",
  "linkedin_activity": "LinkedIn profile/activity details (string)"
}}

FILENAME: {filename}
RAW TEXT:
{raw_text}
"""
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Sanitize JSON block quotes if returned
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            # Return with default guarantees
            return {
                "candidate_id": os.path.splitext(filename)[0].upper(),
                "name": str(data.get("name", os.path.splitext(filename)[0].replace("_", " ").title())).strip(),
                "current_title": str(data.get("current_title", "Software Engineer")).strip(),
                "years_experience": float(data.get("years_experience", 3.0)),
                "skills": list(data.get("skills", [])),
                "skills_raw": ", ".join(data.get("skills", [])),
                "education": str(data.get("education", "")).strip(),
                "summary": str(data.get("summary", "")).strip(),
                "projects": str(data.get("projects", "")).strip(),
                "github_url": str(data.get("github_url", "")).strip(),
                "linkedin_activity": str(data.get("linkedin_activity", "")).strip()
            }
        except Exception as e:
            logger.warning(f"LLM resume parsing failed for {filename}: {e}. Triggering local heuristic fallback.")
            
    # --- HEURISTIC FALLBACK PARSER ---
    # Extract candidate name from filename (e.g. emily_chen.pdf -> Emily Chen)
    name_clean = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").title()
    
    # Try to extract title from first few non-empty lines
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    extracted_title = "Machine Learning Engineer" if len(lines) < 2 else lines[1][:50]
    if len(extracted_title) < 5 or any(kw in extracted_title.lower() for kw in ["resume", "cv", "portfolio"]):
        extracted_title = "ML Practitioner"
        
    # Extract years of experience using regex
    years = 3.0
    match_years = re.search(r'(\d+(?:\.\d+)?)\+?\s*years?', raw_text, re.IGNORECASE)
    if match_years:
        try:
            years = float(match_years.group(1))
        except ValueError:
            pass
            
    # Extract skills by matching standard tech terms
    common_terms = ["Python", "PyTorch", "TensorFlow", "JAX", "MLOps", "Docker", "Kubernetes", "AWS", "SQL", "Spark", "Git", "NLP", "LLMs", "React"]
    found_skills = [term for term in common_terms if term.lower() in raw_text.lower()]
    
    # Extract links
    github = ""
    match_gh = re.search(r'(https?://github\.com/\S+)', raw_text, re.IGNORECASE)
    if match_gh:
        github = match_gh.group(1).rstrip(",.")
        
    linkedin = ""
    match_li = re.search(r'(https?://linkedin\.com/\S+)', raw_text, re.IGNORECASE)
    if match_li:
        linkedin = f"Profile: {match_li.group(1).rstrip(',.')}"
        
    return {
        "candidate_id": os.path.splitext(filename)[0].upper(),
        "name": name_clean,
        "current_title": extracted_title,
        "years_experience": years,
        "skills": found_skills,
        "skills_raw": ", ".join(found_skills),
        "education": "Education details (see raw resume)" if len(lines) > 2 else "",
        "summary": raw_text[:300] + "...",
        "projects": "Project details (see raw resume)",
        "github_url": github,
        "linkedin_activity": linkedin or "LinkedIn activity not assessed"
    }

def load_candidates(path: str) -> List[Dict[str, Any]]:
    """
    Loads candidate profiles. Supports:
    1. CSV file containing candidate rows (legacy CSV ingestion).
    2. Directory of candidate resume files (.pdf, .txt, .md), parsing them with Gemini.
    
    Args:
        path (str): Path to candidates CSV or folder of resumes.
        
    Returns:
        List[Dict[str, Any]]: Standardized candidate profile lists.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Candidates path not found at: {path}")
        
    # Scenario A: Path is a Directory (Folder of raw PDFs/Texts)
    if os.path.isdir(path):
        logger.info(f"Loading candidates from directory: {path}")
        candidates: List[Dict[str, Any]] = []
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        valid_extensions = [".pdf", ".txt", ".md"]
        resume_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if not resume_files:
            logger.warning(f"No valid resume files (.pdf, .txt, .md) found in: {path}")
            return []
            
        logger.info(f"Found {len(resume_files)} resumes to parse.")
        for r_file in resume_files:
            full_path = os.path.join(path, r_file)
            ext = os.path.splitext(r_file)[1].lower()
            
            logger.info(f"Parsing raw resume: {r_file}")
            if ext == ".pdf":
                raw_text = extract_text_from_pdf(full_path)
            else:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read().strip()
                    
            if not raw_text:
                logger.warning(f"Extracted text was empty for {r_file}. Skipping.")
                continue
                
            # Call our Gemini / Heuristic Parser
            parsed_profile = parse_resume_with_llm(raw_text, r_file)
            candidates.append(parsed_profile)
            
        return candidates
        
    # Scenario B: Path is a CSV File
    else:
        logger.info(f"Loading candidates from CSV database: {path}")
        df = pd.read_csv(path)
        required_cols = [
            "candidate_id", "name", "current_title", "years_experience",
            "skills", "education", "summary", "github_url", "linkedin_activity", "projects"
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
                
        candidates = []
        for _, row in df.iterrows():
            try:
                years = float(row["years_experience"])
                if pd.isna(years):
                    years = 0.0
            except (ValueError, TypeError):
                years = 0.0
                
            skills_raw = str(row["skills"]) if not pd.isna(row["skills"]) else ""
            skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
            
            candidates.append({
                "candidate_id": str(row["candidate_id"]).strip(),
                "name": str(row["name"]).strip(),
                "current_title": str(row["current_title"]).strip(),
                "years_experience": years,
                "skills": skills_list,
                "skills_raw": skills_raw,
                "education": str(row["education"]).strip() if not pd.isna(row["education"]) else "",
                "summary": str(row["summary"]).strip() if not pd.isna(row["summary"]) else "",
                "github_url": str(row["github_url"]).strip() if not pd.isna(row["github_url"]) else "",
                "linkedin_activity": str(row["linkedin_activity"]).strip() if not pd.isna(row["linkedin_activity"]) else "",
                "projects": str(row["projects"]).strip() if not pd.isna(row["projects"]) else ""
            })
        return candidates

if __name__ == "__main__":
    # Test directory check
    print("Ingest loaded successfully.")
