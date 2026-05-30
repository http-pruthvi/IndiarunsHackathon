import os
import pandas as pd
from typing import List, Dict, Any, Union

def load_job_description(file_path: str) -> str:
    """
    Loads and reads the job description from a text file.
    
    Args:
        file_path (str): Path to the job description file.
        
    Returns:
        str: Normalized job description text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Job description file not found at: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif ext == ".pdf":
        # Fallback basic PDF reading in case fpdf2 is only for writing,
        # but for safety let's write simple reader or raise error if dependencies are missing.
        try:
            # If pypdf is not available, we can just try to read it as text or warn
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Could not parse PDF file {file_path}: {e}")
    else:
        # Default text reading for other types
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()

def load_candidates(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads the candidates CSV and normalizes the columns.
    
    Args:
        file_path (str): Path to the candidates CSV file.
        
    Returns:
        List[Dict[str, Any]]: A list of normalized candidate profile dicts.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Candidates file not found at: {file_path}")
        
    df = pd.read_csv(file_path)
    
    # Required columns in the raw input CSV
    required_cols = [
        "candidate_id", "name", "current_title", "years_experience",
        "skills", "education", "summary", "github_url", "linkedin_activity", "projects"
    ]
    
    # Validate columns
    for col in required_cols:
        if col not in df.columns:
            df[col] = "" # Fill missing columns with blank
            
    candidates: List[Dict[str, Any]] = []
    
    for _, row in df.iterrows():
        # Parse years experience as a float
        try:
            years = float(row["years_experience"])
            if pd.isna(years):
                years = 0.0
        except (ValueError, TypeError):
            years = 0.0
            
        # Parse skills to a list
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
    # Test ingestion
    try:
        jd = load_job_description("data/job_description.txt")
        print(f"Loaded JD successfully. Length: {len(jd)} chars.")
        cands = load_candidates("data/candidates.csv")
        print(f"Loaded {len(cands)} candidates successfully.")
        print(f"Sample Candidate: {cands[0]['name']}, Experience: {cands[0]['years_experience']} yrs, Skills: {cands[0]['skills']}")
    except Exception as e:
        print(f"Ingestion test failed: {e}")
