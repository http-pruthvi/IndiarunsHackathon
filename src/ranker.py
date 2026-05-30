import os
import pandas as pd
from fpdf import FPDF
from typing import List, Dict, Any

class RankedPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(10, 15, 10)
        self.set_auto_page_break(True, margin=20)

    def header(self):
        # Draw a beautiful dark navy header banner
        self.set_fill_color(13, 27, 42) # #0D1B2A (Dark Navy)
        self.rect(0, 0, 210, 32, "F")
        
        # Title text
        self.set_xy(10, 8)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(0, 180, 216) # #00B4D8 (Teal)
        self.cell(190, 8, "AI-Powered Recruiter: Candidate Rankings", ln=True)
        
        self.set_font("Helvetica", "", 10)
        self.set_text_color(255, 255, 255)
        self.set_x(10)
        self.cell(190, 5, "Hiring Hackathon Submission - Senior Machine Learning Engineer Shortlist", ln=True)
        
        # Border accent line
        self.set_draw_color(0, 180, 216)
        self.set_line_width(1.0)
        self.line(0, 32, 210, 32)
        
        # Reset colors and position for content
        self.set_text_color(0, 0, 0)
        # We start page content at y=38 to leave room below the header
        self.set_y(38)

    def footer(self):
        # Page numbering and brand watermark
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(95, 10, "Hackathon Recruitment Pipeline - Confidential", align="L")
        self.set_x(105)
        self.cell(95, 10, f"Page {self.page_no()} of {{nb}}", align="R")

def get_recommendation(score: float) -> str:
    """
    Determines recommendation tier based on the final score.
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
    """
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
    print(f"Ranked output successfully saved to CSV: {output_path}")

def save_ranked_pdf(ranked_candidates: List[Dict[str, Any]], output_path: str) -> None:
    """
    Generates a professionally-formatted multipage PDF of all 50 ranked candidates.
    """
    pdf = RankedPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- EXECUTIVE SUMMARY SUMMARY CARD ---
    pdf.set_fill_color(245, 247, 250) # Light slate grey card background
    pdf.set_draw_color(220, 224, 230)
    pdf.set_line_width(0.3)
    pdf.rect(10, 38, 190, 25, "DF")
    
    # Count recommendation categories
    strong_hires = sum(1 for c in ranked_candidates if c["recommendation"] == "STRONG HIRE")
    hires = sum(1 for c in ranked_candidates if c["recommendation"] == "HIRE")
    maybes = sum(1 for c in ranked_candidates if c["recommendation"] == "MAYBE")
    passes = sum(1 for c in ranked_candidates if c["recommendation"] == "PASS")
    
    pdf.set_xy(15, 41)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(13, 27, 42)
    pdf.cell(180, 5, "Executive Talent Search Summary:", ln=True)
    pdf.set_xy(15, 48)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(180, 5, f"Total Candidates: {len(ranked_candidates)}   |   Strong Hires: {strong_hires}   |   Hires: {hires}   |   Maybes: {maybes}   |   Passes: {passes}", ln=True)
    pdf.set_xy(15, 54)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(180, 5, "*Scores are derived via weighted semantic vectors (40%), fuzzy skills matching (25%), experience targets (20%), and community footprint (15%).", ln=True)
    
    # --- TABLE OF CANDIDATES ---
    table_headers = ["Rank", "Candidate Name", "Professional Title", "Exp", "Score", "Recommendation"]
    col_widths = [15, 45, 60, 15, 20, 35] # Total width = 190mm
    
    y_start = 70
    pdf.set_xy(10, y_start)
    
    # Header Row
    pdf.set_fill_color(13, 27, 42) # Dark navy header background
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    for idx, h in enumerate(table_headers):
        align = "C" if idx in [0, 3, 4, 5] else "L"
        pdf.cell(col_widths[idx], 10, h, border=0, align=align, fill=True)
    pdf.ln()
    
    # Data Rows
    pdf.set_font("Helvetica", "", 9)
    for idx, c in enumerate(ranked_candidates):
        # Perform automatic page-break checking
        if pdf.get_y() > 270:
            pdf.add_page()
            # Re-draw headers on new page
            pdf.set_fill_color(13, 27, 42)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 10)
            for h_idx, h in enumerate(table_headers):
                align = "C" if h_idx in [0, 3, 4, 5] else "L"
                pdf.cell(col_widths[h_idx], 10, h, border=0, align=align, fill=True)
            pdf.ln()
            pdf.set_font("Helvetica", "", 9)
            
        pdf.set_x(10)
        
        # Zebra striping
        if idx % 2 == 0:
            pdf.set_fill_color(248, 249, 250)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        # Draw cells
        # Set text color based on recommendation
        rec = c["recommendation"]
        if rec == "STRONG HIRE":
            pdf.set_text_color(0, 140, 180) # Strong teal
        elif rec == "HIRE":
            pdf.set_text_color(0, 110, 80) # Green
        elif rec == "MAYBE":
            pdf.set_text_color(180, 110, 0) # Orange
        else:
            pdf.set_text_color(150, 150, 150) # Grey
            
        # Write values
        pdf.cell(col_widths[0], 8, str(c["rank"]), border=0, align="C", fill=True)
        
        # Reset text color for name and title
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_widths[1], 8, c["name"][:20], border=0, align="L", fill=True)
        pdf.cell(col_widths[2], 8, c["current_title"][:30], border=0, align="L", fill=True)
        pdf.cell(col_widths[3], 8, f"{c['years_experience']}y", border=0, align="C", fill=True)
        
        # Re-highlight final score and recommendation
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_widths[4], 8, f"{c['final_score']:.2f}", border=0, align="C", fill=True)
        
        if rec == "STRONG HIRE":
            pdf.set_text_color(0, 150, 200)
        elif rec == "HIRE":
            pdf.set_text_color(0, 130, 90)
        elif rec == "MAYBE":
            pdf.set_text_color(200, 120, 0)
        else:
            pdf.set_text_color(130, 130, 130)
            
        pdf.cell(col_widths[5], 8, rec, border=0, align="C", fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.ln()
        
    # Make sure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"Ranked output successfully saved to PDF: {output_path}")

if __name__ == "__main__":
    pass
