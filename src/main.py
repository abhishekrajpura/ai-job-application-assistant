#!/usr/bin/env python3
"""
AI Job Application Assistant - Main Entry Point
Enhanced with Local LLM Support
"""

import sys
import argparse
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for the job application bot."""
    parser = argparse.ArgumentParser(description="AI Job Application Assistant")
    parser.add_argument("--platform", default="indeed", help="Job platform to scrape")
    parser.add_argument("--location", help="Job location filter")
    parser.add_argument("--keywords", help="Job keywords filter")
    parser.add_argument("--dry-run", action="store_true", help="Run without applying")
    parser.add_argument("--config", help="Custom config file path")
    parser.add_argument("--max-jobs", type=int, default=50, help="Maximum jobs to process")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    
    # LLM provider options
    parser.add_argument("--llm-provider", choices=["local", "cloud", "auto"], default="auto",
                       help="LLM provider: local (Ollama/LMStudio), cloud (OpenAI/Anthropic), or auto")
    parser.add_argument("--local-model", default="llama2", help="Local LLM model name")
    parser.add_argument("--local-provider", choices=["ollama", "lmstudio", "transformers"], 
                       default="ollama", help="Local LLM provider")
    
    args = parser.parse_args()
    
    # Setup logging
    print("🤖 Starting AI Job Application Assistant...")
    print(f"📋 Platform: {args.platform}")
    print(f"📍 Location: {args.location or 'Default from config'}")
    print(f"🔍 Keywords: {args.keywords or 'Default from config'}")
    print(f"📊 Max jobs: {args.max_jobs}")
    print(f"🧪 Dry run: {args.dry_run}")
    
    # Determine LLM provider
    llm_provider = determine_llm_provider(args.llm_provider)
    print(f"🧠 LLM Provider: {llm_provider}")
    
    if llm_provider == "local":
        print(f"🏠 Local LLM: {args.local_provider} ({args.local_model})")
        test_local_llm_setup(args.local_provider, args.local_model)
    elif llm_provider == "cloud":
        print("☁️ Cloud LLM: Checking API keys...")
        test_cloud_llm_setup()
    
    # Test resume tailoring
    if args.dry_run:
        test_resume_tailoring(llm_provider, args.local_provider, args.local_model)
    
    print("✅ Bot setup complete! Ready for implementation.")
    print()
    print("📝 Next steps:")
    if llm_provider == "local":
        print("1. Make sure your local LLM is running (see docs/LOCAL_LLM_SETUP.md)")
        print(f"2. Verify model '{args.local_model}' is available")
    else:
        print("1. Add your API keys to .env file")
    print("3. Run: python src/main.py --dry-run")
    print("4. Implement scrapers, resume tailoring, and application modules")
    
    return 0

def determine_llm_provider(preference: str) -> str:
    """Determine which LLM provider to use"""
    if preference == "local":
        return "local"
    elif preference == "cloud":
        return "cloud"
    else:  # auto
        # Check environment variables
        local_provider = os.getenv('LOCAL_LLM_PROVIDER', '').lower()
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if local_provider in ['ollama', 'lmstudio', 'transformers']:
            return "local"
        elif openai_key or anthropic_key:
            return "cloud"
        else:
            return "local"  # Default to local for privacy

def test_local_llm_setup(provider: str, model: str):
    """Test local LLM setup"""
    try:
        from resume.local_llm_tailor import LocalLLMResumeTailor
        
        # Test with example resume
        resume_path = "config/master_resume.json"
        if not Path(resume_path).exists():
            resume_path = "config/master_resume.json.example"
        
        tailor = LocalLLMResumeTailor(resume_path, provider, model)
        model_info = tailor.get_model_info()
        
        if model_info['model_loaded']:
            print(f"✅ Local LLM ready: {provider} ({model})")
            print(f"   Privacy: {model_info['privacy']}")
            print(f"   Cost: {model_info['cost']}")
        else:
            print(f"❌ Local LLM setup failed")
            print("💡 See docs/LOCAL_LLM_SETUP.md for setup instructions")
            
    except ImportError as e:
        print(f"⚠️ Local LLM dependencies missing: {e}")
        print("💡 Install with: pip install ollama transformers torch")
    except Exception as e:
        print(f"⚠️ Local LLM test failed: {e}")

def test_cloud_llm_setup():
    """Test cloud LLM setup"""
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key:
        print("✅ OpenAI API key found")
    elif anthropic_key:
        print("✅ Anthropic API key found")
    else:
        print("⚠️ No cloud API keys found")
        print("💡 Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env file")

def test_resume_tailoring(llm_provider: str, local_provider: str = "ollama", local_model: str = "llama2"):
    """Test resume tailoring functionality"""
    print("\n🧪 Testing Resume Tailoring...")
    print("-" * 30)
    
    try:
        # Choose the appropriate tailor
        if llm_provider == "local":
            from resume.local_llm_tailor import LocalLLMResumeTailor
            resume_path = "config/master_resume.json"
            if not Path(resume_path).exists():
                resume_path = "config/master_resume.json.example"
            
            tailor = LocalLLMResumeTailor(resume_path, local_provider, local_model)
        else:
            from resume.resume_tailor import ResumeTailor
            resume_path = "config/master_resume.json"
            if not Path(resume_path).exists():
                resume_path = "config/master_resume.json.example"
            
            tailor = ResumeTailor(resume_path)
        
        # Test with sample job
        sample_job = """
        Data Analyst Position
        
        We are seeking a skilled Data Analyst with experience in:
        - Python and SQL for data analysis
        - Power BI for dashboard creation
        - Excel automation and reporting
        - Cross-functional collaboration
        
        Responsibilities:
        - Build automated reporting systems
        - Analyze business data for insights
        - Create interactive dashboards
        - Support data-driven decisions
        """
        
        print("🎯 Tailoring resume for sample Data Analyst position...")
        result = tailor.tailor_resume(sample_job, "Data Analyst")
        
        if 'error' in result:
            print(f"❌ Tailoring failed: {result['error']}")
        else:
            print("✅ Resume tailoring successful!")
            metadata = result.get('metadata', {})
            provider_info = metadata.get('provider', 'unknown')
            print(f"   Provider: {provider_info}")
            print(f"   Summary: {result['tailored_summary'][:100]}...")
            print(f"   Skills: {len(result['relevant_skills'])} selected")
            print(f"   Experience: {len(result['tailored_experience'])} jobs tailored")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    sys.exit(main())