import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class CandidateEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the sentence transformer model.
        
        Args:
            model_name (str): Sentence-transformer model name.
        """
        self.model = SentenceTransformer(model_name)
        
    def build_profile_text(self, candidate: Dict[str, Any]) -> str:
        """
        Concatenates candidate profile fields into a single structured text representation
        for dense vector embedding.
        
        Args:
            candidate (Dict[str, Any]): Normalized candidate dictionary.
            
        Returns:
            str: Cohesive, structured profile text.
        """
        parts = [
            f"Candidate Name: {candidate.get('name', '')}",
            f"Current Professional Title: {candidate.get('current_title', '')}",
            f"Years of Relevant Experience: {candidate.get('years_experience', 0.0)} years",
            f"Educational Background: {candidate.get('education', '')}",
            f"Technical Skills and Expertises: {candidate.get('skills_raw', '')}",
            f"Professional Summary: {candidate.get('summary', '')}",
            f"Key Projects and Contributions: {candidate.get('projects', '')}"
        ]
        return "\n".join(parts)

    def compute_semantic_scores(self, jd_text: str, candidates: List[Dict[str, Any]]) -> List[float]:
        """
        Computes cosine similarity between the JD and all candidates' profiles.
        
        Args:
            jd_text (str): Loaded job description text.
            candidates (List[Dict[str, Any]]): List of normalized candidates.
            
        Returns:
            List[float]: A list of semantic similarity scores (0-100) corresponding to candidates.
        """
        if not candidates:
            return []
            
        # Generate texts
        candidate_texts = [self.build_profile_text(c) for c in candidates]
        
        # Encode JD and candidates
        jd_embedding = self.model.encode(jd_text, convert_to_numpy=True)
        cand_embeddings = self.model.encode(candidate_texts, convert_to_numpy=True)
        
        # Calculate Cosine Similarity
        # Normalize embeddings to unit vectors for easy cosine similarity via dot product
        jd_norm = jd_embedding / np.linalg.norm(jd_embedding)
        cand_norms = cand_embeddings / np.linalg.norm(cand_embeddings, axis=1, keepdims=True)
        
        similarities = np.dot(cand_norms, jd_norm)
        
        # Scale to 0-100
        # Cosine similarity ranges from -1 to 1. For sentence embeddings, it's typically >= 0.
        # We will bound it between 0 and 1, then scale to 0-100.
        scores = [float(np.clip(sim, 0.0, 1.0) * 100.0) for sim in similarities]
        return scores

if __name__ == "__main__":
    # Quick test
    from ingest import load_job_description, load_candidates
    try:
        jd = load_job_description("data/job_description.txt")
        cands = load_candidates("data/candidates.csv")[:2]
        
        embedder = CandidateEmbedder()
        scores = embedder.compute_semantic_scores(jd, cands)
        print("Semantic scores for first two candidates:", scores)
    except Exception as e:
        print("Embedder test failed:", e)
