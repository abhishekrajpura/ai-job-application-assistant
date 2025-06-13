"""
Resume Tailoring Module
Uses LLM to customize resumes for specific job descriptions
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path

class ResumeTailor:
    """AI-powered resume tailoring using LLM"""
    
    def __init__(self, master_resume_path: str, api_key: str = None):
        self.master_resume_path = master_resume_path
        self.api_key = api_key or os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        self.master_resume = self._load_master_resume()
        
        # Your proven prompt system
        self.tailoring_prompt = """
INSTRUCTIONS
Analyze: Read the entire job description carefully. Identify the top 5-7 most important keywords, skills, and qualifications the employer is looking for.
Match: Compare these required qualifications with the information in my master resume.
Rewrite: Rewrite the professional_summary and the bullet_points within the experience section. Do not change titles, companies, or dates.
Tailor Bullet Points: For each job in my experience, rephrase the bullet points to use action verbs and directly reflect the language and priorities found in the job description. Quantify achievements with metrics (like percentages or numbers) where possible, using the data from my master resume.
Select Skills: From my master list of skills, create a new, targeted list of the most relevant skills for this specific job.
Generate Cover Letter Points: Create a short list of 3-4 bullet points I can use to build a compelling cover letter. Each point should connect one of my key experiences or skills directly to a stated need in the job description.

CONSTRAINTS
DO NOT invent or exaggerate any skills, experiences, or metrics. You must only use information present in my master resume.
DO NOT change my personal details, job titles, company names, or employment dates.
The tone must be professional and confident. Avoid clichés and buzzwords.
Your final output MUST BE a single, valid JSON object and nothing else. Do not include any explanatory text before or after the JSON block.

OUTPUT FORMAT
Your entire response must be a single JSON object with the following structure:

{
  "tailored_summary": "...",
  "tailored_experience": [
    {
      "title": "Data Analyst",
      "company": "First Service Residential",
      "dates": "May 2023 Current",
      "bullet_points": [
        "...",
        "..."
      ]
    }
  ],
  "relevant_skills": [
    "...",
    "..."
  ],
  "cover_letter_points": [
    "...",
    "..."
  ]
}
        """
    
    def _load_master_resume(self) -> Dict[str, Any]:
        """Load the master resume JSON"""
        try:
            with open(self.master_resume_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Master resume not found at {self.master_resume_path}")
            print("💡 Copy config/master_resume.json.example to config/master_resume.json")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing master resume JSON: {e}")
            return {}
    
    def tailor_resume(self, job_description: str) -> Dict[str, Any]:
        """
        Tailor resume for a specific job description using LLM
        
        Args:
            job_description: Full text of the job posting
            
        Returns:
            Dictionary with tailored resume components
        """
        if not self.master_resume:
            return {"error": "Master resume not loaded"}
        
        if not self.api_key:
            return {"error": "No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY"}
        
        try:
            # Construct the full prompt
            full_prompt = f"""
{self.tailoring_prompt}

**My Master Resume:**
{json.dumps(self.master_resume, indent=2)}

**Job Description:**
{job_description}

Please provide the tailored resume JSON:
            """
            
            # TODO: Implement actual LLM API call
            # For now, return a mock response
            return self._mock_tailor_response(job_description)
            
        except Exception as e:
            return {"error": f"Error tailoring resume: {str(e)}"}
    
    def _mock_tailor_response(self, job_description: str) -> Dict[str, Any]:
        """Mock response for testing - replace with actual LLM call"""
        return {
            "tailored_summary": "Results-driven Data Analyst with proven expertise in business intelligence and analytics. Skilled in Python, SQL, Power BI, and Excel to deliver actionable insights that drive business decisions. Experience in data visualization, process automation, and cross-functional collaboration in dynamic environments.",
            "tailored_experience": [
                {
                    "title": "Data Analyst",
                    "company": "First Service Residential", 
                    "dates": "May 2023 Current",
                    "bullet_points": [
                        "Designed Power Apps solutions automating data workflows, reducing manual entry by 40% and improving data accuracy.",
                        "Built comprehensive Power BI dashboards providing daily insights to leadership across sales, operations, and marketing teams.",
                        "Developed Excel VBA automation scripts for monthly reconciliations, saving 12 hours weekly and eliminating manual errors.",
                        "Created dynamic Power BI reports for property performance metrics, collaborating with finance teams to meet analytical requirements.",
                        "Integrated Microsoft 365 components with CRM systems using REST APIs, enhancing data connectivity and workflow efficiency."
                    ]
                },
                {
                    "title": "Lead Development Representative",
                    "company": "First Service Residential",
                    "dates": "June 2023-Feb 2025", 
                    "bullet_points": [
                        "Developed data analytics projects delivering actionable marketing insights and supporting strategic decision-making.",
                        "Built data pipelines for ingestion and preprocessing using Python and SQL, ensuring data quality and accessibility.",
                        "Created interactive BI dashboards for sales performance tracking and customer segmentation analysis using Power BI.",
                        "Applied machine learning techniques for predictive analytics and collaborated on A/B testing to optimize marketing campaigns."
                    ]
                }
            ],
            "relevant_skills": [
                "Python & SQL",
                "Power BI/Tableau", 
                "Data Visualization and Presentations",
                "Statistical Analysis",
                "Microsoft Excel",
                "Excel VBA automation",
                "Power Automate",
                "API-based integrations"
            ],
            "cover_letter_points": [
                "My experience building Power BI dashboards and automating data workflows at First Service Residential directly aligns with your need for advanced analytics and process improvement.",
                "I've successfully used Python and SQL to build data pipelines and perform statistical analysis, which matches your requirements for technical data analysis skills.",
                "My track record of collaborating with cross-functional teams and delivering actionable insights demonstrates the communication and business partnership skills you're seeking.",
                "My proven ability to reduce manual processes by 40% through automation aligns perfectly with your focus on operational efficiency and innovation."
            ]
        }
    
    def validate_tailored_resume(self, tailored_resume: Dict[str, Any]) -> List[str]:
        """Validate the tailored resume for completeness and accuracy"""
        errors = []
        
        required_fields = ["tailored_summary", "tailored_experience", "relevant_skills", "cover_letter_points"]
        for field in required_fields:
            if field not in tailored_resume:
                errors.append(f"Missing required field: {field}")
        
        # Validate experience entries
        if "tailored_experience" in tailored_resume:
            for i, exp in enumerate(tailored_resume["tailored_experience"]):
                required_exp_fields = ["title", "company", "dates", "bullet_points"]
                for field in required_exp_fields:
                    if field not in exp:
                        errors.append(f"Experience entry {i} missing field: {field}")
        
        return errors

def main():
    """Test the resume tailor"""
    tailor = ResumeTailor("config/master_resume.json")
    
    sample_job = """
    Data Analyst Position
    
    We are seeking a skilled Data Analyst to join our team. The ideal candidate will have:
    - Strong experience with Python and SQL
    - Expertise in data visualization tools like Power BI or Tableau  
    - Experience with statistical analysis and reporting
    - Ability to work with cross-functional teams
    - Excel automation and VBA skills preferred
    
    Responsibilities include building dashboards, analyzing business data, and providing actionable insights.
    """
    
    result = tailor.tailor_resume(sample_job)
    print("🤖 Tailored Resume:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()