import os
import json
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llm_ranker")

def is_api_key_configured() -> bool:
    """
    Checks if the Gemini API Key is configured and not the placeholder.
    
    Returns:
        bool: True if key is set, False otherwise.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key or key.strip() == "" or key.strip() == "your_key_here":
        return False
    return True

class GeminiRanker:
    def __init__(self):
        """
        Initializes the Gemini model using the API key from environment.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = is_api_key_configured()
        
        if self.enabled:
            try:
                genai.configure(api_key=self.api_key)
                # Set up the model
                # Use generation_config to guide output structure to JSON
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config={"response_mime_type": "application/json"}
                )
                logger.info("Gemini AI Ranker initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to configure Gemini API client: {e}. Falling back to hybrid scoring.")
                self.enabled = False
        else:
            logger.info("GEMINI_API_KEY not set or is placeholder. LLM scoring will be skipped (fallback active).")

    def rank_candidate(self, jd_text: str, candidate: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calls Gemini to score a single candidate on role fit, growth trajectory, and behavioral signals.
        
        Args:
            jd_text (str): Job description text.
            candidate (Dict[str, Any]): Normalized candidate dictionary.
            
        Returns:
            Optional[Dict[str, Any]]: A dictionary with keys 'role_fit', 'growth', 'behavior', 'reasoning',
                                      and 'llm_score', or None if disabled/failed.
        """
        if not self.enabled:
            return None
            
        # Formulate candidate summary text for LLM
        cand_str = f"""
Name: {candidate['name']}
Title: {candidate['current_title']}
Experience: {candidate['years_experience']} years
Education: {candidate['education']}
Skills: {candidate['skills_raw']}
Summary: {candidate['summary']}
Projects: {candidate['projects']}
LinkedIn Activity: {candidate['linkedin_activity']}
"""

        prompt = f"""You are an expert technical recruiter. Given this job description and candidate profile, score the candidate from 0-100 on: (1) role fit, (2) growth trajectory, (3) culture/behavioral signals. Return ONLY valid JSON: {{"role_fit": int, "growth": int, "behavior": int, "reasoning": str}}

JOB DESCRIPTION:
{jd_text}

CANDIDATE PROFILE:
{cand_str}
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Basic sanitization of response in case JSON block is returned
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            # Extract scores and validate
            role_fit = int(data.get("role_fit", 0))
            growth = int(data.get("growth", 0))
            behavior = int(data.get("behavior", 0))
            reasoning = str(data.get("reasoning", ""))
            
            # Average scores
            llm_score = round((role_fit + growth + behavior) / 3.0, 2)
            
            return {
                "role_fit": role_fit,
                "growth": growth,
                "behavior": behavior,
                "llm_reasoning": reasoning,
                "llm_score": llm_score
            }
        except Exception as e:
            logger.error(f"Error calling or parsing Gemini for candidate {candidate['name']}: {e}")
            return None

if __name__ == "__main__":
    # Test ranker structure
    ranker = GeminiRanker()
    print("Gemini Enabled:", ranker.enabled)
