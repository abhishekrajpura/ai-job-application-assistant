"""
Local LLM Integration for Resume Tailoring
Supports local models via Ollama, LM Studio, or direct model loading
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
import time

# Try to import local LLM libraries
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ollama = None

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class LocalLLMResumeTailor:
    """AI-powered resume tailoring using local LLMs"""
    
    def __init__(self, master_resume_path: str, model_provider: str = "ollama", model_name: str = "llama2"):
        self.master_resume_path = master_resume_path
        self.model_provider = model_provider.lower()
        self.model_name = model_name
        self.master_resume = self._load_master_resume()
        
        # Initialize the local LLM
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._initialize_local_llm()
        
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
    
    def _initialize_local_llm(self):
        """Initialize the local LLM based on provider"""
        print(f"🤖 Initializing local LLM: {self.model_provider} ({self.model_name})")
        
        if self.model_provider == "ollama":
            self._initialize_ollama()
        elif self.model_provider == "lmstudio":
            self._initialize_lmstudio()
        elif self.model_provider == "transformers":
            self._initialize_transformers()
        else:
            print(f"❌ Unsupported provider: {self.model_provider}")
            print("💡 Supported providers: ollama, lmstudio, transformers")
    
    def _initialize_ollama(self):
        """Initialize Ollama client"""
        if not OLLAMA_AVAILABLE:
            print("❌ Ollama library not available. Install with: pip install ollama")
            return
        
        try:
            # Test if Ollama is running
            response = ollama.list()
            available_models = [model['name'] for model in response.get('models', [])]
            
            if self.model_name not in available_models:
                print(f"⚠️ Model '{self.model_name}' not found in Ollama")
                print(f"📋 Available models: {', '.join(available_models) if available_models else 'None'}")
                print(f"💡 Pull model with: ollama pull {self.model_name}")
                
                # Try to pull the model automatically
                print(f"🔄 Attempting to pull {self.model_name}...")
                try:
                    ollama.pull(self.model_name)
                    print(f"✅ Successfully pulled {self.model_name}")
                except Exception as e:
                    print(f"❌ Failed to pull model: {e}")
                    return
            
            # Test the model
            test_response = ollama.generate(
                model=self.model_name,
                prompt="Hello",
                options={"num_predict": 10}
            )
            
            print(f"✅ Ollama model '{self.model_name}' ready")
            self.model = "ollama_ready"
            
        except Exception as e:
            print(f"❌ Ollama initialization failed: {e}")
            print("💡 Make sure Ollama is installed and running:")
            print("   • Install: https://ollama.ai/")
            print("   • Start: ollama serve")
            print(f"   • Pull model: ollama pull {self.model_name}")
    
    def _initialize_lmstudio(self):
        """Initialize LM Studio client (OpenAI-compatible API)"""
        try:
            # Test LM Studio API (usually runs on localhost:1234)
            base_url = "http://localhost:1234/v1"
            response = requests.get(f"{base_url}/models", timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('data', [])
                if models:
                    print(f"✅ LM Studio API ready with {len(models)} model(s)")
                    self.model = base_url
                else:
                    print("⚠️ LM Studio API running but no models loaded")
            else:
                print("❌ LM Studio API not responding")
                
        except requests.exceptions.RequestException:
            print("❌ LM Studio not running on localhost:1234")
            print("💡 Start LM Studio and load a model, then enable the API server")
    
    def _initialize_transformers(self):
        """Initialize Transformers model directly"""
        if not TRANSFORMERS_AVAILABLE:
            print("❌ Transformers library not available. Install with:")
            print("   pip install transformers torch")
            return
        
        try:
            print(f"🔄 Loading model {self.model_name}...")
            print("⚠️ This may take several minutes for the first run...")
            
            # Use a smaller model if specific one not provided
            if self.model_name == "llama2":
                self.model_name = "microsoft/DialoGPT-medium"  # Smaller alternative
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Create text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            print(f"✅ Transformers model '{self.model_name}' loaded")
            
        except Exception as e:
            print(f"❌ Transformers initialization failed: {e}")
            print("💡 Try a smaller model like 'gpt2' or 'microsoft/DialoGPT-medium'")
    
    def _load_master_resume(self) -> Dict[str, Any]:
        """Load the master resume JSON"""
        try:
            with open(self.master_resume_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Master resume not found at {self.master_resume_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing master resume JSON: {e}")
            return {}
    
    def tailor_resume(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """
        Tailor resume for a specific job description using local LLM
        
        Args:
            job_description: Full text of the job posting
            job_title: Job title for context (optional)
            
        Returns:
            Dictionary with tailored resume components
        """
        if not self.master_resume:
            return {"error": "Master resume not loaded"}
        
        if not self.model:
            return {"error": "Local LLM not initialized"}
        
        print(f"🤖 Tailoring resume using local {self.model_provider} for: {job_title or 'Unknown Position'}")
        
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
            
            # Generate response based on provider
            if self.model_provider == "ollama":
                response_text = self._call_ollama(full_prompt)
            elif self.model_provider == "lmstudio":
                response_text = self._call_lmstudio(full_prompt)
            elif self.model_provider == "transformers":
                response_text = self._call_transformers(full_prompt)
            else:
                return {"error": f"Unsupported provider: {self.model_provider}"}
            
            # Parse and validate response
            if response_text:
                try:
                    # Try to extract JSON from response
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    
                    if json_start != -1 and json_end > json_start:
                        json_text = response_text[json_start:json_end]
                        response = json.loads(json_text)
                    else:
                        raise json.JSONDecodeError("No JSON found", response_text, 0)
                        
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON response from local LLM, using smart fallback")
                    response = self._smart_fallback_response(job_description, job_title)
            else:
                print("⚠️ Empty response from local LLM, using smart fallback")
                response = self._smart_fallback_response(job_description, job_title)
            
            # Add metadata
            response['metadata'] = {
                'tailored_at': time.time(),
                'job_title': job_title,
                'provider': f"local_{self.model_provider}",
                'model_name': self.model_name,
                'master_resume_path': self.master_resume_path
            }
            
            return response
            
        except Exception as e:
            print(f"❌ Error tailoring resume: {str(e)}")
            return {"error": f"Error tailoring resume: {str(e)}"}
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama local LLM"""
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "num_predict": 2000,
                    "top_p": 0.9,
                    "stop": ["Human:", "Assistant:"]
                }
            )
            return response.get('response', '')
        except Exception as e:
            print(f"❌ Ollama API error: {e}")
            return ""
    
    def _call_lmstudio(self, prompt: str) -> str:
        """Call LM Studio local API"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are an expert resume writer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{self.model}/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ LM Studio API error: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"❌ LM Studio API error: {e}")
            return ""
    
    def _call_transformers(self, prompt: str) -> str:
        """Call Transformers model directly"""
        try:
            # Truncate prompt if too long
            max_length = 1000  # Adjust based on model capacity
            if len(prompt) > max_length:
                prompt = prompt[:max_length] + "...\n\nPlease provide the tailored resume JSON:"
            
            response = self.pipeline(
                prompt,
                max_length=len(prompt) + 500,
                num_return_sequences=1,
                temperature=0.3,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = response[0]['generated_text']
            # Remove the original prompt from response
            return generated_text[len(prompt):].strip()
            
        except Exception as e:
            print(f"❌ Transformers error: {e}")
            return ""
    
    def _smart_fallback_response(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """Smart fallback when LLM response is invalid"""
        print("🧠 Using smart fallback response with local analysis")
        
        # Analyze job description for keywords
        job_lower = job_description.lower()
        
        # Determine focus based on job description
        is_analyst_role = any(word in job_lower for word in ['analyst', 'analytics', 'analysis'])
        is_python_job = 'python' in job_lower
        is_sql_job = 'sql' in job_lower
        is_powerbi_job = any(word in job_lower for word in ['power bi', 'powerbi', 'tableau'])
        
        # Extract key skills mentioned in job description
        job_skills = []
        for skill in self.master_resume.get('skills', []):
            if any(word in job_lower for word in skill.lower().split()):
                job_skills.append(skill)
        
        # Tailor summary
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
        
        summary_parts.append("Experience in real estate and property analytics with a focus on operational efficiency and data-driven decision making")
        
        tailored_summary = " ".join(summary_parts) + "."
        
        # Select relevant skills
        relevant_skills = job_skills[:8] if job_skills else self.master_resume.get('skills', [])[:8]
        
        # Tailor experience
        experience = self.master_resume.get('experience', [])
        tailored_experience = []
        
        for job in experience:
            tailored_job = {
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'dates': job.get('dates', ''),
                'bullet_points': []
            }
            
            # Enhance bullet points
            for bullet in job.get('bullet_points', []):
                enhanced_bullet = self._enhance_bullet_for_job(bullet, job_description)
                tailored_job['bullet_points'].append(enhanced_bullet)
            
            tailored_experience.append(tailored_job)
        
        # Generate cover letter points
        cover_letter_points = [
            f"My experience building automated data workflows and Power BI dashboards at First Service Residential directly aligns with your need for data-driven insights and process improvement.",
            f"I've successfully leveraged {'Python and SQL' if is_python_job and is_sql_job else 'Excel and analytical tools'} to reduce manual processes by 40% and deliver actionable business intelligence.",
            f"My background in real estate analytics provides valuable domain expertise that can contribute to your team's success in data analysis and reporting.",
            f"My proven track record of collaborating with cross-functional teams and stakeholders ensures effective communication of complex data insights to drive business decisions."
        ]
        
        return {
            "tailored_summary": tailored_summary,
            "tailored_experience": tailored_experience,
            "relevant_skills": relevant_skills,
            "cover_letter_points": cover_letter_points
        }
    
    def _enhance_bullet_for_job(self, bullet: str, job_description: str) -> str:
        """Enhance bullet point based on job description"""
        job_lower = job_description.lower()
        enhanced = bullet
        
        # Enhance based on job keywords
        if 'automation' in job_lower and 'automat' in bullet.lower():
            enhanced = enhanced.replace('automated', 'streamlined and automated')
        
        if 'dashboard' in job_lower and 'dashboard' in bullet.lower():
            enhanced = enhanced.replace('dashboards', 'interactive business intelligence dashboards')
        
        if 'stakeholder' in job_lower and ('report' in bullet.lower() or 'insight' in bullet.lower()):
            enhanced = enhanced.replace('insights', 'stakeholder-focused insights')
        
        return enhanced

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model setup"""
        return {
            "provider": self.model_provider,
            "model_name": self.model_name,
            "model_loaded": self.model is not None,
            "supports_local": True,
            "privacy": "Complete - all processing local",
            "cost": "Free after initial setup"
        }

def main():
    """Test the local LLM resume tailor"""
    print("🏠 Testing Local LLM Resume Tailor")
    print("=" * 50)
    
    # Test different providers
    providers = [
        ("ollama", "llama2"),
        ("lmstudio", "local-model"),
        ("transformers", "microsoft/DialoGPT-medium")
    ]
    
    for provider, model in providers:
        print(f"\n🔄 Testing {provider} with {model}")
        print("-" * 30)
        
        tailor = LocalLLMResumeTailor(
            "config/master_resume.json.example",
            model_provider=provider,
            model_name=model
        )
        
        model_info = tailor.get_model_info()
        print(f"Model loaded: {'✅' if model_info['model_loaded'] else '❌'}")
        
        if model_info['model_loaded']:
            sample_job = """
            Data Analyst Position
            
            We need someone with Python, SQL, and Power BI experience.
            Responsibilities include building dashboards and automating reports.
            """
            
            result = tailor.tailor_resume(sample_job, "Data Analyst")
            
            if 'error' not in result:
                print("✅ Tailoring successful!")
                print(f"Provider: {result['metadata']['provider']}")
            else:
                print(f"❌ Error: {result['error']}")
        
        print()

if __name__ == "__main__":
    main()