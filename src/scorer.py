import re
from rapidfuzz import fuzz
from typing import List, Dict, Any

# Predefined target skills extracted from the Senior ML Engineer Job Description
TARGET_SKILLS = [
    "Python", "C++", "SQL", "Spark", "Pandas", "NumPy",
    "PyTorch", "TensorFlow", "JAX", "HuggingFace", "LangChain",
    "Deep Learning", "NLP", "Transformers", "Large Language Models", "LLMs", "Computer Vision", "Reinforcement Learning",
    "MLOps", "Docker", "Kubernetes", "AWS", "SageMaker", "Triton", "TensorRT", "ONNX", "MLflow", "CI/CD",
    "Vector Databases", "Pinecone", "Milvus", "Qdrant"
]

# Core target roles for fuzzy title matching
TARGET_TITLES = [
    "Senior Machine Learning Engineer",
    "Senior ML Engineer",
    "Lead Machine Learning Engineer",
    "Senior Deep Learning Engineer",
    "Principal AI Architect",
    "Senior ML Infrastructure Engineer",
    "AI Research Scientist",
    "Machine Learning Engineer",
    "ML Engineer"
]

def calculate_skills_score(candidate_skills: List[str]) -> float:
    """
    Computes a skills match score from 0 to 100 using exact and fuzzy matching.
    
    Args:
        candidate_skills (List[str]): List of skills from the candidate profile.
        
    Returns:
        float: Skills match score (0-100).
    """
    if not candidate_skills:
        return 0.0
        
    matched_count = 0.0
    
    for cand_skill in candidate_skills:
        cand_skill_lower = cand_skill.lower().strip()
        best_ratio = 0.0
        
        for target in TARGET_SKILLS:
            target_lower = target.lower()
            # Exact match check
            if cand_skill_lower == target_lower:
                best_ratio = 100.0
                break
                
            # Fuzzy match check
            ratio = fuzz.token_sort_ratio(cand_skill_lower, target_lower)
            if ratio > best_ratio:
                best_ratio = ratio
                
        # If the match quality is high, increment our match count
        if best_ratio >= 80.0:
            matched_count += 1.0
        elif best_ratio >= 60.0:
            # Partial credit
            matched_count += 0.5
            
    # Normalize the score: matching 8 key skills represents a perfect match (100)
    ideal_match_count = 8.0
    score = (matched_count / ideal_match_count) * 100.0
    return min(100.0, max(0.0, score))

def calculate_experience_score(years_exp: float, current_title: str) -> float:
    """
    Calculates the experience relevance score by combining quantitative years of experience
    and qualitative title match.
    
    Args:
        years_exp (float): Number of years of experience.
        current_title (str): Candidate's current professional title.
        
    Returns:
        float: Experience score (0-100).
    """
    # 1. Years of Experience Score (JD asks for 5+ years)
    target_years = 5.0
    if years_exp >= target_years:
        # Base 85 for meeting target, plus 3 points for each extra year, capped at 100
        years_score = 85.0 + (years_exp - target_years) * 3.0
    else:
        # Scale down linearly if less than target
        years_score = (years_exp / target_years) * 85.0
        
    years_score = min(100.0, max(0.0, years_score))
    
    # 2. Title Relevance Score using fuzzy matching against target titles
    best_title_ratio = 0.0
    title_lower = current_title.lower().strip()
    
    for target_title in TARGET_TITLES:
        ratio = fuzz.token_sort_ratio(title_lower, target_title.lower())
        if ratio > best_title_ratio:
            best_title_ratio = ratio
            
    # Adjust score based on fuzzy ratio
    title_score = float(best_title_ratio)
    
    # Blend: 50% years of experience, 50% title relevance
    blended_score = 0.5 * years_score + 0.5 * title_score
    return blended_score

def calculate_behavioral_score(candidate: Dict[str, Any]) -> float:
    """
    Calculates behavioral score (0-100) based on simulated GitHub and LinkedIn activities.
    
    Args:
        candidate (Dict[str, Any]): Normalized candidate dictionary.
        
    Returns:
        float: Behavioral score (0-100).
    """
    summary = candidate.get("summary", "").lower()
    projects = candidate.get("projects", "").lower()
    li_activity = candidate.get("linkedin_activity", "").lower()
    
    # Base starting score
    github_score = 50.0
    linkedin_score = 50.0
    
    # Analyze GitHub signals
    if "open source" in summary or "open source" in projects:
        github_score += 20.0
    if "contributor to" in summary or "contributor to" in projects:
        github_score += 15.0
    if "stars" in projects or "stars" in summary:
        github_score += 15.0
        
    # Analyze LinkedIn signals
    if "active" in li_activity or "frequently posts" in li_activity:
        linkedin_score += 20.0
    if "followers" in li_activity:
        # Extract potential follower count
        match = re.search(r'(\d+)k followers', li_activity)
        if match:
            followers = int(match.group(1))
            linkedin_score += min(20.0, followers * 1.5)
        else:
            linkedin_score += 10.0
    if "speaker" in li_activity or "moderates" in li_activity:
        linkedin_score += 10.0
        
    # Cap scores at 100
    github_score = min(100.0, github_score)
    linkedin_score = min(100.0, linkedin_score)
    
    # Blend: 50% GitHub activity, 50% LinkedIn activity
    return 0.5 * github_score + 0.5 * linkedin_score

def compute_hybrid_scores(candidates: List[Dict[str, Any]], semantic_scores: List[float]) -> List[Dict[str, Any]]:
    """
    Computes and adds individual scores and final hybrid score to all candidates.
    
    Args:
        candidates (List[Dict[str, Any]]): List of normalized candidates.
        semantic_scores (List[float]): Cosine similarity scores from embedding module.
        
    Returns:
        List[Dict[str, Any]]: Candidates with score fields populated.
    """
    for idx, candidate in enumerate(candidates):
        sem_score = semantic_scores[idx]
        skills_score = calculate_skills_score(candidate["skills"])
        exp_score = calculate_experience_score(candidate["years_experience"], candidate["current_title"])
        beh_score = calculate_behavioral_score(candidate)
        
        # Weighted hybrid scoring:
        # 40% Semantic Similarity, 25% Skills, 20% Experience, 15% Behavioral
        hybrid_score = (
            0.40 * sem_score +
            0.25 * skills_score +
            0.20 * exp_score +
            0.15 * beh_score
        )
        
        candidate["semantic_score"] = round(sem_score, 2)
        candidate["skills_score"] = round(skills_score, 2)
        candidate["experience_score"] = round(exp_score, 2)
        candidate["behavior_score"] = round(beh_score, 2)
        candidate["hybrid_score"] = round(hybrid_score, 2)
        
    return candidates

if __name__ == "__main__":
    # Test scoring with dummy data
    cand = {
        "current_title": "Senior ML Engineer",
        "years_experience": 6.5,
        "skills": ["Python", "PyTorch", "Transformers", "MLOps", "Docker", "AWS"],
        "skills_raw": "Python, PyTorch, Transformers, MLOps, Docker, AWS",
        "summary": "Experienced open source contributor.",
        "projects": "Created toolkit with 300+ stars.",
        "linkedin_activity": "Active contributor. 10k followers."
    }
    
    print("Skills Score:", calculate_skills_score(cand["skills"]))
    print("Experience Score:", calculate_experience_score(cand["years_experience"], cand["current_title"]))
    print("Behavioral Score:", calculate_behavioral_score(cand))
