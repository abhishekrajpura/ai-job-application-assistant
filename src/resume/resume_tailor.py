"""
Enhanced Resume Tailoring Module with Real LLM Integration
Uses OpenAI or Anthropic APIs to customize resumes for specific job descriptions
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import time

# Try to import LLM libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

class ResumeTailor:
    """AI-powered resume tailoring using LLM APIs"""
    
    def __init__(self, master_resume_path: str, api_key: str = None, provider: str = "auto"):
        self.master_resume_path = master_resume_path
        self.api_key = api_key or self._get_api_key()
        self.provider = self._determine_provider(provider)
        self.master_resume = self._load_master_resume()
        
        # Initialize the LLM client
        self.client = self._initialize_client()
        
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
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables"""
        return (os.getenv('OPENAI_API_KEY') or 
                os.getenv('ANTHROPIC_API_KEY') or 
                os.getenv('CLAUDE_API_KEY'))
    
    def _determine_provider(self, provider: str) -> str:
        """Determine which LLM provider to use"""
        if provider == "auto":
            if os.getenv('OPENAI_API_KEY') and OPENAI_AVAILABLE:
                return "openai"
            elif (os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')) and ANTHROPIC_AVAILABLE:
                return "anthropic"
            else:
                return "mock"  # Fallback to mock for testing
        return provider
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == "openai" and OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
            return openai
        elif self.provider == "anthropic" and ANTHROPIC_AVAILABLE and self.api_key:
            return anthropic.Anthropic(api_key=self.api_key)
        else:
            print(f"⚠️ Using mock LLM client (provider: {self.provider})")
            return None
    
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
    
    def tailor_resume(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """
        Tailor resume for a specific job description using LLM
        
        Args:
            job_description: Full text of the job posting
            job_title: Job title for context (optional)
            
        Returns:
            Dictionary with tailored resume components
        """
        if not self.master_resume:
            return {"error": "Master resume not loaded"}
        
        if not self.api_key and self.provider != "mock":
            return {"error": "No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY"}
        
        print(f"🤖 Tailoring resume using {self.provider} for: {job_title or 'Unknown Position'}")
        
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
            
            # Make LLM API call
            if self.provider == "openai":
                response = self._call_openai(full_prompt)
            elif self.provider == "anthropic":
                response = self._call_anthropic(full_prompt)
            else:
                response = self._mock_tailor_response(job_description, job_title)
            
            # Parse and validate response
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON response from LLM, using mock response")
                    response = self._mock_tailor_response(job_description, job_title)
            
            # Add metadata
            response['metadata'] = {
                'tailored_at': time.time(),
                'job_title': job_title,
                'provider': self.provider,
                'master_resume_path': self.master_resume_path
            }
            
            return response
            
        except Exception as e:
            print(f"❌ Error tailoring resume: {str(e)}")
            return {"error": f"Error tailoring resume: {str(e)}"}
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer who tailors resumes for specific job descriptions. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            raise
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0.3,
                system="You are an expert resume writer who tailors resumes for specific job descriptions. Always respond with valid JSON only.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"❌ Anthropic API error: {e}")
            raise
    
    def _mock_tailor_response(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """Mock response for testing when no API key is available"""
        print("🧪 Using mock response for testing")
        
        # Analyze job description for keywords
        job_lower = job_description.lower()
        
        # Determine focus based on job description
        is_analyst_role = any(word in job_lower for word in ['analyst', 'analytics', 'analysis'])
        is_python_job = 'python' in job_lower
        is_sql_job = 'sql' in job_lower
        is_powerbi_job = any(word in job_lower for word in ['power bi', 'powerbi', 'tableau'])
        
        # Tailor summary based on job requirements
        summary_parts = []
        if is_analyst_role:
            summary_parts.append("Results-driven Data Analyst")
        else:
            summary_parts.append("Detail-oriented Financial & Data Professional")
        
        summary_parts.append("with proven expertise in business intelligence and analytics")
        
        if is_python_job and is_sql_job:
            summary_parts.append("Skilled in Python, SQL, and advanced data processing")
        elif is_sql_job:
            summary_parts.append("Proficient in SQL and database management")
        elif is_python_job:
            summary_parts.append("Experienced in Python programming and automation")
        
        if is_powerbi_job:
            summary_parts.append("Expert in Power BI dashboard development and data visualization")
        
        summary_parts.append("to deliver actionable insights that drive business decisions and operational efficiency")
        
        tailored_summary = " ".join(summary_parts) + "."
        
        # Select relevant skills based on job description
        all_skills = self.master_resume.get('skills', [])
        relevant_skills = []
        
        # Prioritize skills mentioned in job description
        for skill in all_skills:
            skill_lower = skill.lower()
            if any(keyword in job_lower for keyword in skill_lower.split()):
                relevant_skills.append(skill)
        
        # Add core skills if not already included
        core_skills = ["Microsoft Excel", "Data Visualization and Presentations", "Statistical Analysis"]
        for skill in core_skills:
            if skill not in relevant_skills and skill in all_skills:
                relevant_skills.append(skill)
        
        # Limit to top 8 skills
        relevant_skills = relevant_skills[:8]
        
        # Tailor experience bullet points
        experience = self.master_resume.get('experience', [])
        tailored_experience = []
        
        for job in experience:
            tailored_job = {
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'dates': job.get('dates', ''),
                'bullet_points': []
            }
            
            # Enhance bullet points based on job requirements
            for bullet in job.get('bullet_points', []):
                enhanced_bullet = self._enhance_bullet_point(bullet, job_description)
                tailored_job['bullet_points'].append(enhanced_bullet)
            
            tailored_experience.append(tailored_job)
        
        # Generate cover letter points
        cover_letter_points = [
            f"My experience building Power BI dashboards and automating data workflows directly aligns with your need for {'advanced analytics' if is_analyst_role else 'data-driven insights'}.",
            f"I've successfully used {'Python and SQL' if is_python_job and is_sql_job else 'Excel and SQL' if is_sql_job else 'analytical tools'} to {'build data pipelines and perform statistical analysis' if is_python_job else 'analyze business data and generate reports'}, matching your technical requirements.",
            f"My track record of reducing manual processes by 40% through automation demonstrates the operational efficiency improvements you're seeking.",
            f"My proven ability to collaborate with cross-functional teams and deliver actionable insights aligns perfectly with your need for {'business partnership' if 'stakeholder' in job_lower else 'team collaboration'} skills."
        ]
        
        return {
            "tailored_summary": tailored_summary,
            "tailored_experience": tailored_experience,
            "relevant_skills": relevant_skills,
            "cover_letter_points": cover_letter_points
        }
    
    def _enhance_bullet_point(self, bullet: str, job_description: str) -> str:
        """Enhance a bullet point based on job description keywords"""
        job_lower = job_description.lower()
        bullet_lower = bullet.lower()
        
        # Replace generic terms with job-specific language
        enhanced = bullet
        
        if 'dashboard' in bullet_lower and 'visualization' in job_lower:
            enhanced = enhanced.replace('dashboards', 'interactive dashboards and data visualizations')
        
        if 'automat' in bullet_lower and 'efficiency' in job_lower:
            enhanced = enhanced.replace('automate', 'streamline and automate')
        
        if 'data' in bullet_lower and 'insight' in job_lower:
            enhanced = enhanced.replace('data', 'business-critical data')
        
        if 'report' in bullet_lower and 'stakeholder' in job_lower:
            enhanced = enhanced.replace('reports', 'stakeholder reports')
        
        return enhanced
    
    def batch_tailor_resumes(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Tailor resumes for multiple jobs
        
        Args:
            jobs: List of job dictionaries with 'title' and 'description' keys
            
        Returns:
            List of tailored resume responses
        """
        results = []
        
        for i, job in enumerate(jobs):
            print(f"📋 Processing job {i+1}/{len(jobs)}: {job.get('title', 'Unknown')}")
            
            result = self.tailor_resume(
                job_description=job.get('description', ''),
                job_title=job.get('title', '')
            )
            
            result['job_info'] = {
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'url': job.get('url', '')
            }
            
            results.append(result)
            
            # Rate limiting - pause between requests
            if self.provider in ['openai', 'anthropic'] and i < len(jobs) - 1:
                print("⏱️ Pausing to respect API rate limits...")
                time.sleep(2)
        
        return results
    
    def save_tailored_resume(self, tailored_resume: Dict[str, Any], output_path: str):
        """Save tailored resume to file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(tailored_resume, f, indent=2)
            print(f"💾 Tailored resume saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving tailored resume: {e}")

def main():
    """Test the enhanced resume tailor"""
    # Test with different configurations
    tailor = ResumeTailor("config/master_resume.json")
    
    sample_job = """
    Senior Data Analyst Position
    
    We are seeking a skilled Data Analyst to join our team. The ideal candidate will have:
    - Strong experience with Python and SQL for data manipulation
    - Expertise in data visualization tools like Power BI or Tableau  
    - Experience with statistical analysis and predictive modeling
    - Ability to work with cross-functional teams and stakeholders
    - Excel automation and VBA skills preferred
    - Experience with REST APIs and data integration
    
    Responsibilities include:
    - Building interactive dashboards and reports
    - Analyzing business data to identify trends and insights
    - Automating data workflows and processes
    - Collaborating with business stakeholders
    - Supporting data-driven decision making
    """
    
    print("🤖 Testing Enhanced Resume Tailor")
    print("=" * 50)
    
    result = tailor.tailor_resume(sample_job, "Senior Data Analyst")
    
    if 'error' not in result:
        print("✅ Resume tailoring successful!")
        print(f"📝 Summary: {result['tailored_summary'][:100]}...")
        print(f"🎯 Relevant skills: {', '.join(result['relevant_skills'][:5])}")
        print(f"💼 Experience entries: {len(result['tailored_experience'])}")
        print(f"✉️ Cover letter points: {len(result['cover_letter_points'])}")
        
        # Save the result
        output_path = "data/output/test_tailored_resume.json"
        tailor.save_tailored_resume(result, output_path)
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()