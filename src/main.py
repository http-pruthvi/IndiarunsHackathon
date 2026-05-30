import os
import argparse
import logging
from tqdm import tqdm
from dotenv import load_dotenv

# Core pipeline modules
from ingest import load_job_description, load_candidates
from embedder import CandidateEmbedder
from scorer import compute_hybrid_scores
from llm_ranker import GeminiRanker
from ranker import blend_and_rank_candidates, save_ranked_csv
from presentation import generate_presentation_deck

# Load configurations
load_dotenv(override=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main_pipeline")

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="AI-Powered Candidate Ranking Pipeline")
    parser.add_argument(
        "--jd", 
        type=str, 
        default="data/job_description.txt", 
        help="Path to the Job Description text/PDF file"
    )
    parser.add_argument(
        "--candidates", 
        type=str, 
        default="data/candidates.csv", 
        help="Path to the Candidates CSV file"
    )
    parser.add_argument(
        "--top", 
        type=int, 
        default=20, 
        help="Number of candidates to screen with LLM"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="output/ranked_candidates.csv", 
        help="Path to save the final ranked candidates CSV"
    )
    parser.add_argument(
        "--deck", 
        type=str, 
        default="output/approach_deck.pdf", 
        help="Path to save the presentation deck PDF"
    )
    return parser.parse_args()

def main() -> None:
    args = parse_arguments()
    logger.info("Starting AI Candidate Ranking Pipeline...")
    
    # 1. Ingestion Phase
    logger.info(f"Ingesting Job Description from: {args.jd}")
    jd_text = load_job_description(args.jd)
    logger.info(f"Ingested Job Description. Size: {len(jd_text)} characters.")
    
    logger.info(f"Ingesting Candidate Profiles from: {args.candidates}")
    candidates = load_candidates(args.candidates)
    logger.info(f"Successfully ingested {len(candidates)} candidate profiles.")
    
    # 2. Semantic Embedding Phase
    embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    logger.info(f"Initializing embedder with model: {embedding_model}")
    embedder = CandidateEmbedder(model_name=embedding_model)
    
    logger.info("Generating sentence embeddings and computing semantic similarities...")
    semantic_scores = embedder.compute_semantic_scores(jd_text, candidates)
    
    # 3. Hybrid Scoring Phase
    logger.info("Computing multi-signal hybrid scores (Semantic, Skills, Experience, Behavioral)...")
    candidates_scored = compute_hybrid_scores(candidates, semantic_scores)
    
    # 4. LLM Assessment Phase
    # Sort by hybrid score first to identify the top candidates for LLM assessment
    candidates_scored.sort(key=lambda x: x["hybrid_score"], reverse=True)
    
    # Initialize the LLM ranker (Google Gemini)
    logger.info("Initializing Google Gemini LLM Ranker...")
    llm_ranker = GeminiRanker()
    
    llm_results = {}
    if llm_ranker.enabled:
        # Determine candidate count for LLM assessment
        limit = min(args.top, len(candidates_scored))
        logger.info(f"LLM enabled. Screening the top {limit} candidates by hybrid score with gemini-1.5-flash...")
        
        for i in tqdm(range(limit), desc="Gemini Assessment"):
            cand = candidates_scored[i]
            cand_id = cand["candidate_id"]
            
            logger.info(f"Analyzing Candidate {i+1}/{limit}: {cand['name']} ({cand_id})")
            eval_res = llm_ranker.rank_candidate(jd_text, cand)
            if eval_res is not None:
                llm_results[cand_id] = eval_res
            else:
                logger.warning(f"Failed to get LLM evaluation for candidate {cand['name']}. Fallback will be used.")
    else:
        logger.warning("LLM Ranker is disabled or missing credentials. Skipping LLM scoring phase (hybrid fallback active).")
        
    # 5. Final Blending & Ranking Phase
    logger.info("Blending hybrid and LLM scores. Generating final ranking...")
    final_ranked_candidates = blend_and_rank_candidates(candidates_scored, llm_results)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # 6. Save Ranked Spreadsheet
    logger.info(f"Saving complete ranked spreadsheet to: {args.output}")
    save_ranked_csv(final_ranked_candidates, args.output)
    
    # 7. Generate Presentation Deck PDF
    logger.info(f"Compiling presentation slide deck to: {args.deck}")
    generate_presentation_deck(final_ranked_candidates, args.deck)
    
    logger.info("Pipeline executed successfully! All submission outputs are ready.")
    
    # Print the top 5 candidates in the console for quick validation
    print("\n" + "="*50)
    print("      TOP 5 RANKED CANDIDATES")
    print("="*50)
    for c in final_ranked_candidates[:5]:
        print(f"Rank {c['rank']}: {c['name']}")
        print(f"  Title: {c['current_title']}")
        print(f"  Experience: {c['years_experience']} yrs")
        print(f"  Final Score: {c['final_score']} (Hybrid: {c['hybrid_score']}, LLM: {c['llm_score'] or 'N/A'})")
        print(f"  Recommendation: {c['recommendation']}")
        print("-"*50)

if __name__ == "__main__":
    main()
