import pandas as pd
from typing import List, Dict, Any

def get_recommendation(score: float) -> str:
    """
    Determines recommendation tier based on the final score.
    
    Args:
        score (float): Final blended score (0-100).
        
    Returns:
        str: Recommendation category (STRONG HIRE, HIRE, MAYBE, PASS).
    """
    if score >= 85.0:
        return "STRONG HIRE"
    elif score >= 70.0:
        return "HIRE"
    elif score >= 50.0:
        return "MAYBE"
    else:
        return "PASS"

def blend_and_rank_candidates(
    candidates_with_hybrid: List[Dict[str, Any]], 
    llm_results: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Blends the hybrid score and LLM score (60% hybrid / 40% LLM) for candidates
    who have LLM evaluations. For others, uses the hybrid score as final.
    Ranks the entire list of candidates.
    
    Args:
        candidates_with_hybrid (List[Dict[str, Any]]): Candidate list with hybrid scores.
        llm_results (Dict[str, Dict[str, Any]]): Dict mapping candidate_id to LLM scores and reasoning.
        
    Returns:
        List[Dict[str, Any]]: Sorted list of all candidates with final scores and ranks.
    """
    ranked_list: List[Dict[str, Any]] = []
    
    for cand in candidates_with_hybrid:
        cand_id = cand["candidate_id"]
        
        # Check if candidate has LLM scoring results
        if cand_id in llm_results and llm_results[cand_id] is not None:
            res = llm_results[cand_id]
            llm_score = res["llm_score"]
            llm_reasoning = res["llm_reasoning"]
            
            # Blend: 60% Hybrid + 40% LLM
            final_score = round(0.6 * cand["hybrid_score"] + 0.4 * llm_score, 2)
        else:
            # Fallback when LLM is missing, skipped, or failed
            llm_score = ""
            llm_reasoning = "Not assessed (outside top-20 or LLM disabled)" if llm_results else "LLM disabled (fallback active)"
            final_score = cand["hybrid_score"]
            
        cand_copy = cand.copy()
        cand_copy["llm_score"] = llm_score
        cand_copy["llm_reasoning"] = llm_reasoning
        cand_copy["final_score"] = final_score
        cand_copy["recommendation"] = get_recommendation(final_score)
        
        ranked_list.append(cand_copy)
        
    # Sort all candidates by final_score descending
    ranked_list.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Assign ranks
    for idx, cand in enumerate(ranked_list):
        cand["rank"] = idx + 1
        
    return ranked_list

def save_ranked_csv(ranked_candidates: List[Dict[str, Any]], output_path: str) -> None:
    """
    Saves the complete ranked candidate list to a CSV with exact required columns.
    
    Args:
        ranked_candidates (List[Dict[str, Any]]): Complete ranked candidate list.
        output_path (str): Output CSV file path.
    """
    # Columns in the exact requested order:
    # rank, candidate_id, name, current_title, years_experience, top_skills, final_score,
    # semantic_score, skills_score, experience_score, behavior_score, llm_score, llm_reasoning, recommendation
    
    formatted_data = []
    for c in ranked_candidates:
        formatted_data.append({
            "rank": c["rank"],
            "candidate_id": c["candidate_id"],
            "name": c["name"],
            "current_title": c["current_title"],
            "years_experience": c["years_experience"],
            "top_skills": c["skills_raw"],
            "final_score": c["final_score"],
            "semantic_score": c["semantic_score"],
            "skills_score": c["skills_score"],
            "experience_score": c["experience_score"],
            "behavior_score": c["behavior_score"],
            "llm_score": c["llm_score"],
            "llm_reasoning": c["llm_reasoning"],
            "recommendation": c["recommendation"]
        })
        
    df = pd.DataFrame(formatted_data)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Ranked output successfully saved to: {output_path}")

if __name__ == "__main__":
    # Test ranker structure
    cands = [
        {"candidate_id": "CAN-001", "name": "Emily", "hybrid_score": 85.0, "skills_raw": "Python", "semantic_score": 80, "skills_score": 80, "experience_score": 90, "behavior_score": 90, "years_experience": 7.5, "current_title": "Senior ML Engineer"},
        {"candidate_id": "CAN-002", "name": "Bob", "hybrid_score": 40.0, "skills_raw": "Excel", "semantic_score": 40, "skills_score": 20, "experience_score": 50, "behavior_score": 50, "years_experience": 6.0, "current_title": "Civil Engineer"}
    ]
    llm_res = {
        "CAN-001": {"llm_score": 90.0, "llm_reasoning": "Excellent fit."}
    }
    ranked = blend_and_rank_candidates(cands, llm_res)
    print("Ranked:", ranked)
