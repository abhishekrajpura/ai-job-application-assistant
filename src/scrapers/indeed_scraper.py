"""
Indeed Job Scraper
Scrapes job postings from Indeed.com
"""

import time
import random
from typing import List, Dict, Any
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class IndeedScraper:
    """Scrapes job postings from Indeed.com"""
    
    def __init__(self, headless=True, delay_range=(2, 5)):
        self.base_url = "https://ca.indeed.com"
        self.headless = headless
        self.delay_range = delay_range
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            print("💡 Make sure Chrome is installed and chromedriver is in PATH")
            self.driver = None
    
    def search_jobs(self, keywords: str, location: str = "Toronto, ON", max_jobs: int = 50) -> List[Dict[str, Any]]:
        """
        Search for jobs on Indeed
        
        Args:
            keywords: Job search keywords
            location: Job location
            max_jobs: Maximum number of jobs to scrape
            
        Returns:
            List of job dictionaries
        """
        if not self.driver:
            print("❌ Chrome driver not available")
            return []
        
        jobs = []
        start = 0
        
        try:
            while len(jobs) < max_jobs:
                # Construct search URL
                params = {
                    'q': keywords,
                    'l': location,
                    'start': start,
                    'sort': 'date'  # Sort by date for newest jobs
                }
                search_url = f"{self.base_url}/jobs?" + urlencode(params)
                
                print(f"🔍 Searching: {search_url}")
                self.driver.get(search_url)
                
                # Wait for job cards to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-jk]"))
                    )
                except Exception:
                    print("⚠️ No job cards found or page failed to load")
                    break
                
                # Extract job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
                if not job_cards:
                    print("🔚 No more jobs found")
                    break
                
                for card in job_cards:
                    if len(jobs) >= max_jobs:
                        break
                    
                    try:
                        job_data = self.extract_job_data(card)
                        if job_data and self.is_valid_job(job_data):
                            jobs.append(job_data)
                            print(f"✅ Found job {len(jobs)}: {job_data['title']} at {job_data['company']}")
                    except Exception as e:
                        print(f"⚠️ Error extracting job data: {e}")
                        continue
                
                # Random delay to avoid detection
                self.random_delay()
                
                # Move to next page
                start += 10
                
                # Check if there's a next page
                if not self.has_next_page():
                    print("🔚 Reached last page")
                    break
        
        except Exception as e:
            print(f"❌ Error during job search: {e}")
        
        print(f"🎯 Total jobs found: {len(jobs)}")
        return jobs
    
    def extract_job_data(self, job_card) -> Dict[str, Any]:
        """Extract job information from a job card element"""
        try:
            # Job ID
            job_id = job_card.get_attribute("data-jk")
            
            # Job title
            title_element = job_card.find_element(By.CSS_SELECTOR, "h2 a span")
            title = title_element.get_attribute("title") or title_element.text
            
            # Company name
            company_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']")
            company = company_element.text
            
            # Location
            location_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='job-location']")
            location = location_element.text
            
            # Salary (if available)
            salary = ""
            try:
                salary_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='attribute_snippet_testid']")
                salary = salary_element.text
            except:
                pass
            
            # Job snippet/description
            snippet = ""
            try:
                snippet_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='job-snippet']")
                snippet = snippet_element.text
            except:
                pass
            
            # Job URL
            link_element = job_card.find_element(By.CSS_SELECTOR, "h2 a")
            job_url = self.base_url + link_element.get_attribute("href")
            
            # Date posted
            date_posted = ""
            try:
                date_element = job_card.find_element(By.CSS_SELECTOR, "[data-testid='myJobsStateDate']")
                date_posted = date_element.text
            except:
                pass
            
            return {
                'id': job_id,
                'title': title.strip(),
                'company': company.strip(),
                'location': location.strip(),
                'salary': salary.strip(),
                'snippet': snippet.strip(),
                'url': job_url,
                'date_posted': date_posted.strip(),
                'source': 'indeed',
                'scraped_at': time.time()
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting job data: {e}")
            return None
    
    def get_job_description(self, job_url: str) -> str:
        """Get full job description from job URL"""
        try:
            self.driver.get(job_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            
            description_element = self.driver.find_element(By.ID, "jobDescriptionText")
            return description_element.text
            
        except Exception as e:
            print(f"⚠️ Error getting job description: {e}")
            return ""
    
    def is_valid_job(self, job_data: Dict[str, Any]) -> bool:
        """Check if job meets basic criteria"""
        # Skip jobs without essential information
        if not job_data.get('title') or not job_data.get('company'):
            return False
        
        # Skip jobs with certain keywords (can be configured)
        title_lower = job_data.get('title', '').lower()
        skip_keywords = ['senior', 'sr.', 'lead', 'principal', 'director', 'manager']
        
        for keyword in skip_keywords:
            if keyword in title_lower:
                print(f"⏭️ Skipping {job_data['title']} - contains '{keyword}'")
                return False
        
        return True
    
    def has_next_page(self) -> bool:
        """Check if there's a next page of results"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']")
            return next_button.is_enabled()
        except:
            return False
    
    def random_delay(self):
        """Add random delay to avoid detection"""
        delay = random.uniform(*self.delay_range)
        print(f"⏱️ Waiting {delay:.1f}s...")
        time.sleep(delay)
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Test the Indeed scraper"""
    scraper = IndeedScraper(headless=False)  # Set to True for headless mode
    
    try:
        # Test search
        jobs = scraper.search_jobs(
            keywords="data analyst",
            location="Toronto, ON",
            max_jobs=10
        )
        
        print(f"\n📊 Summary:")
        print(f"Total jobs found: {len(jobs)}")
        
        # Show first few jobs
        for i, job in enumerate(jobs[:3]):
            print(f"\nJob {i+1}:")
            print(f"Title: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Salary: {job['salary'] or 'Not specified'}")
            print(f"URL: {job['url']}")
        
        # Test getting full job description for first job
        if jobs:
            print(f"\n📄 Getting full description for: {jobs[0]['title']}")
            description = scraper.get_job_description(jobs[0]['url'])
            print(f"Description length: {len(description)} characters")
            print(f"First 200 chars: {description[:200]}...")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()