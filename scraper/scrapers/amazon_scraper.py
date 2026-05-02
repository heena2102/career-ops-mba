"""Amazon job scraper using their public JSON API"""
import requests
from typing import List, Dict
from .base_scraper import BaseScraper
from config import JOB_TITLES

class AmazonScraper(BaseScraper):
    """Scrape jobs directly from Amazon's API"""
    
    def __init__(self):
        super().__init__("Amazon")
        self.base_url = "https://www.amazon.jobs/en/search.json"
        
    def scrape(self) -> List[Dict]:
        """Scrape Amazon for configured roles"""
        all_jobs = []
        print(f"  Scraping {self.name}...")
        
        # Amazon uses 'Virtual' for Remote sometimes, but we can search both
        locations = ["Bangalore", "Remote"]
        
        for role in JOB_TITLES[:5]: # testing limit for speed, adjust if needed
            for loc in locations:
                try:
                    params = {
                        "base_query": role,
                        "loc_query": loc,
                        "result_limit": 20,
                        "sort": "recent"
                    }
                    
                    if loc.lower() == "remote":
                        params["loc_query"] = "Virtual"
                        
                    response = requests.get(self.base_url, params=params, timeout=10)
                    if response.status_code != 200:
                        continue
                        
                    data = response.json()
                    for job in data.get('jobs', []):
                        job_data = {
                            "title": job.get('title', ''),
                            "company": "Amazon",
                            "location": "Remote" if loc.lower() == "remote" else job.get('location', ''),
                            "experience": "0-3 years", # difficult to parse from Amazon easily, assume matching
                            "salary": "Not disclosed",
                            "url": f"https://www.amazon.jobs{job.get('job_path', '')}",
                            "job_type": "Full-time",
                            "description": job.get('description_short', '')[:500],
                            "published_at": job.get('posted_date', 'NA')
                        }
                        all_jobs.append(self.standardize_job(job_data))
                except Exception as e:
                    print(f"    Error scraping Amazon for {role} in {loc}: {e}")
                    
        self.jobs = all_jobs
        return all_jobs
