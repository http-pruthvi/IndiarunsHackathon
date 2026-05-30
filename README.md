# AI-Powered Candidate Ranking Pipeline

An intelligent, semantic-first recruitment pipeline built for hiring hackathons. Instead of matching exact keywords like legacy Applicant Tracking Systems (ATS), this system employs dense vector embeddings and Large Language Models (LLMs) to capture the true context, technical expertise, and career trajectory of candidates.

---

## Architecture Diagram (ASCII)

```
                       +-----------------------------+
                       |   Job Description (.txt)    |
                       +--------------+--------------+
                                      |
                                      v
                       +--------------+--------------+
                       |   Candidate Profiles (.csv) |
                       +--------------+--------------+
                                      |
                                      v
                       +--------------+--------------+
                       |     Ingest & Normalize      |
                       +--------------+--------------+
                                      |
                                      v
          +---------------------------+---------------------------+
          |                                                       |
          v                                                       v
+---------+----------+  +--------------------+  +-----------------+---+  +------------------+
|   Semantic Score   |  | Fuzzy Skills Match |  | Experience Score |  | Behavioral Score |
|       (40%)        |  |       (25%)        |  |      (20%)       |  |      (15%)       |
| Sentence Embeddings|  | Set Theory & Fuzz  |  | Target Years &   |  | Open Source &    |
|   (all-MiniLM-L6)  |  |    (RapidFuzz)     |  |   Title Match    |  |  Social Activity |
+---------+----------+  +---------+----------+  +---------+--------+  +--------+---------+
          |                       |                       |                    |
          +-----------------------+-----------+-----------+--------------------+
                                              |
                                              v
                               +--------------+--------------+
                               |     Hybrid Score (100%)     |
                               +--------------+--------------+
                                              |
                                              v
                               +--------------+--------------+
                               |     Filter Top 20           |
                               +--------------+--------------+
                                              |
                                              v
                               +--------------+--------------+
                               |    Google Gemini Review     |
                               |      (gemini-1.5-flash)     |
                               |    Role Fit, Growth, Culture|
                               +--------------+--------------+
                                              |
                                              v
                               +--------------+--------------+
                               |   Blended Scoring Engine    |
                               |  60% Hybrid / 40% LLM Rec   |
                               +--------------+--------------+
                                              |
                                              v
          +-----------------------------------+-----------------------------------+
          |                                                                       |
          v                                                                       v
+---------+------------------+                                         +---------+------------------+
| Ranked Candidates (.csv)   |                                         |  Approach Slide Deck (.pdf)|
|   All 50 Candidates Ranked  |                                         | 10 Clean Premium Slides    |
+----------------------------+                                         +----------------------------+
```

---

## Scoring System & Weights

The pipeline uses a multi-signal **Hybrid Score** (100%) for initial ranking, and then refines the top 20 candidates using a **Blended Score** combining the Hybrid and LLM evaluations.

### 1. Hybrid Score Components (60% of final blend)

| Signal | Weight | Logic & Methodology |
| :--- | :---: | :--- |
| **Semantic Similarity** | **40%** | Converts job descriptions and candidate summaries into dense 384-dimensional vector spaces using `sentence-transformers` (`all-MiniLM-L6-v2`) and computes Cosine Similarity. |
| **Fuzzy Skills Match** | **25%** | Evaluates exact keyword presence and performs fuzzy matching via `rapidfuzz` against a targeted library of 30+ skills (e.g., PyTorch, Docker, LLMs, SQL). |
| **Experience Relevance**| **20%** | Blends quantitative score (relative to a 5-year JD target) and qualitative title fuzzy similarity matching against standard ML titles. |
| **Behavioral Signals** | **15%** | Analyzes simulated community outputs (GitHub open source repositories, package contributions, and LinkedIn network influence). |

### 2. LLM Assessment (40% of final blend)

For the **top 20 candidates** sorted by Hybrid Score, the pipeline calls **Google Gemini (`gemini-1.5-flash`)** to evaluate:
- **Role Fit (0-100)**: Quantitative technical alignment.
- **Growth Trajectory (0-100)**: Seniority path, complexity of projects, and career velocity.
- **Culture/Behavioral (0-100)**: Soft skills, team leadership, and developer community engagement.

$$\text{Final Score} = 0.6 \times \text{Hybrid Score} + 0.4 \times \text{LLM Recruiter Score}$$

> [!NOTE]
> If the `GEMINI_API_KEY` is missing or invalid, the system automatically triggers a **graceful fallback** and uses the Hybrid Score as the final score for all candidates, skipping LLM evaluation without interrupting the execution.

---

## Setup Instructions

### 1. Clone & Initialize Environment
Make sure Python 3.8+ is installed on your system. Navigate to the project root and install the dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and set your Google Gemini API Key:
```bash
cp .env.example .env
```
Inside `.env`, configure your credentials:
```env
GEMINI_API_KEY=your_google_gemini_api_key
TOP_N=20
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## How to Run

Execute the pipeline using the command line:
```bash
python src/main.py --jd data/job_description.txt --candidates data/candidates.csv
```

### Supported Arguments:
- `--jd`: Path to the job description file (default: `data/job_description.txt`).
- `--candidates`: Path to the candidate profile spreadsheet (default: `data/candidates.csv`).
- `--top`: Number of top hybrid-scored candidates to evaluate via LLM (default: `20`).
- `--output`: Path to write the final ranked candidate CSV (default: `output/ranked_candidates.csv`).
- `--deck`: Path to save the presentation PDF (default: `output/approach_deck.pdf`).

---

## Deliverables & Output Formats

You can view the generated submission deliverables here:
* 📊 **Ranked Spreadsheet**: [output/ranked_candidates.csv](output/ranked_candidates.csv)
* 🖥️ **Presentation Slides**: [output/approach_deck.pdf](output/approach_deck.pdf)

### 1. Spreadsheet Output (`output/ranked_candidates.csv`)
A fully-ranked sheet of all 50 candidates containing the following headers:
- `rank`: Final absolute rank (1 to 50).
- `candidate_id`: Standardized identifier (e.g. `CAN-001`).
- `name`: Candidate's name.
- `current_title`: Candidate's professional title.
- `years_experience`: Years of professional experience.
- `top_skills`: List of skills from the candidate's profile.
- `final_score`: The final blended score (or hybrid score under fallback).
- `semantic_score`: Local dense vector embedding similarity score.
- `skills_score`: Fuzzy-logic tech skills match score.
- `experience_score`: Quantified years & title relevance score.
- `behavior_score`: GitHub open-source + LinkedIn social score.
- `llm_score`: Evaluated average score from Gemini (if top-20).
- `llm_reasoning`: Explainable text reasoning returned directly by the AI.
- `recommendation`: Final hiring recommendation:
  - `STRONG HIRE` (Score $\ge 85$)
  - `HIRE` ($70 \le \text{Score} < 85$)
  - `MAYBE` ($50 \le \text{Score} < 70$)
  - `PASS` (Score $< 50$)

### 2. Presentation Deck (`output/approach_deck.pdf`)
A premium 10-slide, 16:9 widescreen PDF presentation describing the problem, our architecture, the scoring signals, and rendering a **live table of the top 5 candidates** from the pipeline's execution.
