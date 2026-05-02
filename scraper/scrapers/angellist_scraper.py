"""AngelList job scraper"""
import requests
from typing import List, Dict
from .base_scraper import BaseScraper
from config import HEADERS

class AngelListScraper(BaseScraper):
    """Scrape jobs from AngelList (startup jobs)"""
    
    def __init__(self):
        super().__init__("AngelList")
        self.base_url = "https://www.angel.co"
    
    def scrape(self) -> List[Dict]:
        """Scrape AngelList for startup jobs"""
        try:
            print(f"  Scraping {self.name}...")
            
            jobs = []
            roles = ["Product Manager", "Business Developer", "Operations Manager", "Data Analyst"]
            
            for role in roles:
                # Mock startup jobs
                job_data = {
                    "title": role,
                    "company": "Startup Inc.",
                    "location": "Bangalore",
                    "experience": "0-3 years",
                    "salary": "₹8-18 LPA",
                    "url": f"{self.base_url}/jobs?keywords={role.replace(' ', '+')}&locations=Bangalore",
                    "job_type": "Full-time",
                    "description": f"Help our startup grow. Looking for passionate {role}."
                }
                jobs.append(self.standardize_job(job_data))
            
            # Remote startup jobs
            for role in roles:
                job_data = {
                    "title": role,
                    "company": "Remote Startup",
                    "location": "Remote",
                    "experience": "0-3 years",
                    "salary": "₹10-20 LPA",
                    "url": f"{self.base_url}/jobs?keywords={role.replace(' ', '+')}&locations=Remote",
                    "job_type": "Full-time",
                    "description": f"100% Remote {role} opportunity"
                }
                jobs.append(self.standardize_job(job_data))
            
            self.jobs = jobs
            return jobs
        
        except Exception as e:
            print(f"  Error scraping {self.name}: {e}")
            return []
