"""Workday job scraper using their public JSON API"""
import requests
from typing import List, Dict
from .base_scraper import BaseScraper
from config import JOB_TITLES, WORKDAY_COMPANIES

class WorkdayScraper(BaseScraper):
    """Scrape jobs from large MNC proprietary Workday portals"""
    
    def __init__(self):
        super().__init__("WorkdayPortals")
        
    def scrape(self) -> List[Dict]:
        """Scrape Workday instances for configured roles"""
        all_jobs = []
        print(f"  Scraping {self.name}...")
        
        for company in WORKDAY_COMPANIES:
            company_name = company.get("name")
            tenant = company.get("tenant")
            portal = company.get("portal")
            wd_instance = company.get("wd_instance", "wd1")
            
            base_url = f"https://{tenant}.{wd_instance}.myworkdayjobs.com/wday/cxs/{tenant}/{portal}/jobs"
            
            for role in JOB_TITLES[:5]: # limit for speed
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    
                    payload = {
                        "appliedFacets": {},
                        "limit": 20,
                        "offset": 0,
                        "searchText": role
                    }
                    
                    response = requests.post(base_url, json=payload, headers=headers, timeout=10)
                    
                    if response.status_code != 200:
                        continue
                        
                    data = response.json()
                    
                    for job in data.get('jobPostings', []):
                        location = job.get('locationsText', '')
                        
                        # Apply location filter strictly (Bangalore/Remote)
                        loc_lower = location.lower()
                        # Allow standard Workday locations, India/US Remote, or simply let the central filter handle it.
                        # Actually we will let the central filter handle it or pass if it contains india/us/remote/bang
                        
                        job_data = {
                            "title": job.get('title', ''),
                            "company": company_name,
                            "location": location,
                            "experience": "0-3 years", # Default assumption, workday short JSON doesn't provide
                            "salary": "Not disclosed",
                            "url": f"https://{tenant}.{wd_instance}.myworkdayjobs.com/en-US/{portal}{job.get('externalPath', '')}",
                            "job_type": "Full-time",
                            "description": f"View on Workday: {job.get('title', '')} at {company_name}",
                            "published_at": job.get('postedOn', 'NA'),
                            "source": company_name # Use company name as source to allow filtering
                        }
                        
                        all_jobs.append(self.standardize_job(job_data))
                        
                except Exception as e:
                    print(f"    Error scraping {company_name} for {role}: {e}")
                    
        self.jobs = all_jobs
        return all_jobs
