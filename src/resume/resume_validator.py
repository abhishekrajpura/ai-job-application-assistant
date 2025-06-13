"""
Resume Validation Functions
Validates master resume JSON structure and content
"""

import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path

class ResumeValidator:
    """Validates resume JSON structure and content"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
        # Required fields for a valid resume
        self.required_sections = [
            'personal_details',
            'professional_summary', 
            'skills',
            'experience',
            'education'
        ]
        
        self.required_personal_fields = [
            'name',
            'email',
            'phone'
        ]
        
        self.required_experience_fields = [
            'title',
            'company',
            'dates',
            'bullet_points'
        ]
        
        self.required_education_fields = [
            'degree',
            'university'
        ]
    
    def validate_resume(self, resume_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a resume JSON file
        
        Args:
            resume_path: Path to the resume JSON file
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        try:
            resume_data = self._load_resume(resume_path)
            if not resume_data:
                return False, self.errors, self.warnings
            
            self._validate_structure(resume_data)
            self._validate_personal_details(resume_data.get('personal_details', {}))
            self._validate_professional_summary(resume_data.get('professional_summary', ''))
            self._validate_skills(resume_data.get('skills', []))
            self._validate_experience(resume_data.get('experience', []))
            self._validate_education(resume_data.get('education', []))
            self._validate_content_quality(resume_data)
            
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _load_resume(self, resume_path: str) -> Dict[str, Any]:
        """Load and parse resume JSON file"""
        try:
            if not Path(resume_path).exists():
                self.errors.append(f"Resume file not found: {resume_path}")
                return {}
            
            with open(resume_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {str(e)}")
            return {}
        except Exception as e:
            self.errors.append(f"Error loading resume file: {str(e)}")
            return {}
    
    def _validate_structure(self, resume_data: Dict[str, Any]):
        """Validate top-level resume structure"""
        for section in self.required_sections:
            if section not in resume_data:
                self.errors.append(f"Missing required section: {section}")
            elif not resume_data[section]:
                self.warnings.append(f"Empty section: {section}")
    
    def _validate_personal_details(self, personal_details: Dict[str, Any]):
        """Validate personal details section"""
        if not personal_details:
            self.errors.append("Personal details section is empty")
            return
        
        for field in self.required_personal_fields:
            if field not in personal_details:
                self.errors.append(f"Missing personal detail: {field}")
            elif not personal_details[field]:
                self.errors.append(f"Empty personal detail: {field}")
        
        # Validate email format
        email = personal_details.get('email', '')
        if email and not self._is_valid_email(email):
            self.errors.append(f"Invalid email format: {email}")
        
        # Validate phone format
        phone = personal_details.get('phone', '')
        if phone and not self._is_valid_phone(phone):
            self.warnings.append(f"Phone format may be invalid: {phone}")
        
        # Check for LinkedIn and portfolio
        if not personal_details.get('linkedin'):
            self.warnings.append("LinkedIn profile not provided")
        if not personal_details.get('portfolio'):
            self.warnings.append("Portfolio/website not provided")
    
    def _validate_professional_summary(self, summary: str):
        """Validate professional summary"""
        if not summary or not summary.strip():
            self.errors.append("Professional summary is empty")
            return
        
        word_count = len(summary.split())
        if word_count < 20:
            self.warnings.append(f"Professional summary is very short ({word_count} words)")
        elif word_count > 150:
            self.warnings.append(f"Professional summary is very long ({word_count} words)")
        
        # Check for key elements
        summary_lower = summary.lower()
        if 'experience' not in summary_lower and 'skilled' not in summary_lower:
            self.warnings.append("Professional summary should mention experience or skills")
    
    def _validate_skills(self, skills: List[str]):
        """Validate skills section"""
        if not skills:
            self.errors.append("Skills section is empty")
            return
        
        if len(skills) < 5:
            self.warnings.append(f"Only {len(skills)} skills listed, consider adding more")
        elif len(skills) > 20:
            self.warnings.append(f"Many skills listed ({len(skills)}), consider grouping")
        
        # Check for empty or very short skills
        for i, skill in enumerate(skills):
            if not skill or not skill.strip():
                self.errors.append(f"Empty skill at position {i+1}")
            elif len(skill.strip()) < 2:
                self.warnings.append(f"Very short skill: '{skill}'")
    
    def _validate_experience(self, experience: List[Dict[str, Any]]):
        """Validate experience section"""
        if not experience:
            self.errors.append("Experience section is empty")
            return
        
        for i, job in enumerate(experience):
            job_prefix = f"Experience entry {i+1}"
            
            # Check required fields
            for field in self.required_experience_fields:
                if field not in job:
                    self.errors.append(f"{job_prefix}: Missing field '{field}'")
                elif not job[field]:
                    self.errors.append(f"{job_prefix}: Empty field '{field}'")
            
            # Validate bullet points
            bullet_points = job.get('bullet_points', [])
            if not bullet_points:
                self.errors.append(f"{job_prefix}: No bullet points provided")
            elif len(bullet_points) < 2:
                self.warnings.append(f"{job_prefix}: Only {len(bullet_points)} bullet point(s)")
            
            # Check bullet point quality
            for j, bullet in enumerate(bullet_points):
                if not bullet or not bullet.strip():
                    self.errors.append(f"{job_prefix}, bullet {j+1}: Empty bullet point")
                elif len(bullet.split()) < 5:
                    self.warnings.append(f"{job_prefix}, bullet {j+1}: Very short bullet point")
                elif not bullet.strip().endswith('.'):
                    self.warnings.append(f"{job_prefix}, bullet {j+1}: Should end with period")
    
    def _validate_education(self, education: List[Dict[str, Any]]):
        """Validate education section"""
        if not education:
            self.warnings.append("Education section is empty")
            return
        
        for i, edu in enumerate(education):
            edu_prefix = f"Education entry {i+1}"
            
            # Check required fields
            for field in self.required_education_fields:
                if field not in edu:
                    self.errors.append(f"{edu_prefix}: Missing field '{field}'")
                elif not edu[field]:
                    self.errors.append(f"{edu_prefix}: Empty field '{field}'")
    
    def _validate_content_quality(self, resume_data: Dict[str, Any]):
        """Validate overall content quality"""
        # Check for common issues
        resume_text = json.dumps(resume_data).lower()
        
        # Check for placeholder text
        placeholders = ['your name', 'your email', 'company name', 'your degree']
        for placeholder in placeholders:
            if placeholder in resume_text:
                self.warnings.append(f"Possible placeholder text found: '{placeholder}'")
        
        # Check for consistent formatting
        experience = resume_data.get('experience', [])
        if experience:
            date_formats = []
            for job in experience:
                dates = job.get('dates', '')
                if dates:
                    date_formats.append(self._extract_date_format(dates))
            
            if len(set(date_formats)) > 1:
                self.warnings.append("Inconsistent date formats in experience section")
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if phone format is reasonable"""
        # Remove common formatting characters
        clean_phone = re.sub(r'[\s\-\(\)\+\.]', '', phone)
        # Check if it's all digits and reasonable length
        return clean_phone.isdigit() and 10 <= len(clean_phone) <= 15
    
    def _extract_date_format(self, date_string: str) -> str:
        """Extract date format pattern from date string"""
        if re.search(r'\d{4}', date_string):
            return 'with_year'
        elif re.search(r'\d{2}', date_string):
            return 'with_short_year'
        else:
            return 'other'
    
    def generate_validation_report(self, resume_path: str) -> str:
        """Generate a detailed validation report"""
        is_valid, errors, warnings = self.validate_resume(resume_path)
        
        report = []
        report.append("📋 Resume Validation Report")
        report.append("=" * 50)
        report.append(f"File: {resume_path}")
        report.append(f"Status: {'✅ VALID' if is_valid else '❌ INVALID'}")
        report.append("")
        
        if errors:
            report.append("🚨 Errors (Must Fix):")
            for error in errors:
                report.append(f"  • {error}")
            report.append("")
        
        if warnings:
            report.append("⚠️ Warnings (Should Consider):")
            for warning in warnings:
                report.append(f"  • {warning}")
            report.append("")
        
        if not errors and not warnings:
            report.append("🎉 No issues found! Resume is well-formatted.")
            report.append("")
        
        report.append("💡 Tips:")
        report.append("  • Use action verbs in bullet points")
        report.append("  • Include quantified achievements")
        report.append("  • Keep professional summary concise (50-100 words)")
        report.append("  • Ensure consistent formatting throughout")
        
        return "\n".join(report)

def validate_resume_file(resume_path: str) -> bool:
    """
    Quick validation function
    
    Args:
        resume_path: Path to resume JSON file
        
    Returns:
        True if valid, False otherwise
    """
    validator = ResumeValidator()
    is_valid, errors, warnings = validator.validate_resume(resume_path)
    
    if errors:
        print("❌ Resume validation failed:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print("⚠️ Resume warnings:")
        for warning in warnings:
            print(f"  • {warning}")
    
    return is_valid

def main():
    """Test the resume validator"""
    # Test with the master resume
    resume_path = "config/master_resume.json"
    
    if not Path(resume_path).exists():
        resume_path = "config/master_resume.json.example"
    
    print("🔍 Testing Resume Validator...")
    print(f"Validating: {resume_path}")
    print()
    
    validator = ResumeValidator()
    report = validator.generate_validation_report(resume_path)
    print(report)

if __name__ == "__main__":
    main()