#!/usr/bin/env python3
"""
Test Script for Task 2: Master Resume System
Tests resume validation and LLM integration
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from resume.resume_validator import ResumeValidator, validate_resume_file
from resume.resume_tailor import ResumeTailor

def test_resume_validation():
    """Test the resume validation functionality"""
    print("🔍 Testing Resume Validation...")
    print("=" * 50)
    
    # Test with master resume
    resume_path = "config/master_resume.json"
    if not Path(resume_path).exists():
        resume_path = "config/master_resume.json.example"
    
    validator = ResumeValidator()
    report = validator.generate_validation_report(resume_path)
    print(report)
    
    # Quick validation test
    print("\n🚀 Quick Validation Test:")
    is_valid = validate_resume_file(resume_path)
    print(f"Resume is {'✅ VALID' if is_valid else '❌ INVALID'}")
    
    return is_valid

def test_resume_tailoring():
    """Test the resume tailoring functionality"""
    print("\n🤖 Testing Resume Tailoring...")
    print("=" * 50)
    
    # Test with master resume
    resume_path = "config/master_resume.json"
    if not Path(resume_path).exists():
        resume_path = "config/master_resume.json.example"
    
    tailor = ResumeTailor(resume_path)
    
    # Test job description
    sample_job = """
    Data Analyst - Business Intelligence
    
    We are seeking a talented Data Analyst to join our growing team. The successful candidate will:
    
    Requirements:
    - Bachelor's degree in relevant field
    - 2+ years experience in data analysis
    - Strong proficiency in SQL and Python
    - Experience with Power BI or similar BI tools
    - Excel expertise including VBA automation
    - Experience with statistical analysis
    - Strong communication skills
    
    Responsibilities:
    - Develop and maintain Power BI dashboards
    - Analyze business data to identify trends and insights
    - Automate reporting processes
    - Collaborate with stakeholders across departments
    - Support data-driven decision making
    - Create documentation and training materials
    
    Preferred:
    - Experience with real estate or property management
    - Knowledge of REST APIs and data integration
    - Familiarity with SharePoint and Microsoft 365
    """
    
    print("🎯 Job Title: Data Analyst - Business Intelligence")
    print("📋 Tailoring resume...")
    
    try:
        result = tailor.tailor_resume(sample_job, "Data Analyst - Business Intelligence")
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print("✅ Resume tailoring successful!")
        print(f"🔧 Provider: {result.get('metadata', {}).get('provider', 'Unknown')}")
        print()
        
        # Display results
        print("📝 Tailored Professional Summary:")
        print(f"   {result['tailored_summary']}")
        print()
        
        print("🎯 Relevant Skills:")
        for skill in result['relevant_skills']:
            print(f"   • {skill}")
        print()
        
        print("💼 Experience Highlights:")
        for i, exp in enumerate(result['tailored_experience'][:2]):  # Show first 2 jobs
            print(f"   {exp['title']} at {exp['company']}")
            for bullet in exp['bullet_points'][:2]:  # Show first 2 bullets
                print(f"     • {bullet}")
            if i < len(result['tailored_experience']) - 1:
                print()
        
        print("✉️ Cover Letter Points:")
        for point in result['cover_letter_points']:
            print(f"   • {point}")
        
        # Save test result
        output_path = "data/output/test_tailored_resume.json"
        tailor.save_tailored_resume(result, output_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during tailoring: {e}")
        return False

def test_api_integration():
    """Test API integration status"""
    print("\n🔗 Testing API Integration...")
    print("=" * 50)
    
    # Check for API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
    
    print(f"OpenAI API Key: {'✅ Found' if openai_key else '❌ Not found'}")
    print(f"Anthropic API Key: {'✅ Found' if anthropic_key else '❌ Not found'}")
    
    if not openai_key and not anthropic_key:
        print("⚠️ No API keys found. Using mock responses for testing.")
        print("💡 Set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file for real LLM integration.")
        return False
    
    # Test API availability
    try:
        import openai
        print("✅ OpenAI library available")
        openai_available = True
    except ImportError:
        print("❌ OpenAI library not available")
        openai_available = False
    
    try:
        import anthropic
        print("✅ Anthropic library available")
        anthropic_available = True
    except ImportError:
        print("❌ Anthropic library not available")
        anthropic_available = False
    
    return (openai_key and openai_available) or (anthropic_key and anthropic_available)

def main():
    """Run all tests for Task 2"""
    print("🎯 Task 2: Master Resume System - Test Suite")
    print("=" * 60)
    
    # Test 1: Resume Validation
    validation_passed = test_resume_validation()
    
    # Test 2: Resume Tailoring
    tailoring_passed = test_resume_tailoring()
    
    # Test 3: API Integration
    api_ready = test_api_integration()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"Resume Validation: {'✅ PASSED' if validation_passed else '❌ FAILED'}")
    print(f"Resume Tailoring: {'✅ PASSED' if tailoring_passed else '❌ FAILED'}")
    print(f"API Integration: {'✅ READY' if api_ready else '⚠️ MOCK MODE'}")
    
    if validation_passed and tailoring_passed:
        print("\n🎉 Task 2: Master Resume System - COMPLETED!")
        print("✅ Your resume is validated and ready")
        print("✅ LLM integration is working")
        print("✅ Resume tailoring is functional")
        
        if api_ready:
            print("✅ Real API integration is configured")
        else:
            print("⚠️ Using mock responses (add API keys for real integration)")
        
        print("\n🚀 Ready to proceed with Task 3!")
        return True
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)