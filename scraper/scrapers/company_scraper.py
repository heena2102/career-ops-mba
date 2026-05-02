"""Company portal scraper using Greenhouse and Lever APIs"""
import requests
from typing import List, Dict
from .base_scraper import BaseScraper
from config import TRACKED_COMPANIES, JOB_TITLES

class CompanyScraper(BaseScraper):
    """Scrape jobs from specific company boards (Greenhouse/Lever)"""
    
    def __init__(self):
        super().__init__("CompanyPortals")
        
    def _is_relevant_job(self, title: str) -> bool:
        title_lower = title.lower()
        return any(jt.lower() in title_lower for jt in JOB_TITLES)
        
    def scrape(self) -> List[Dict]:
        """Scrape all configured company portals"""
        all_jobs = []
        
        print(f"  Scraping {self.name}...")
        for company in TRACKED_COMPANIES:
            try:
                if company.get('board_type') == 'greenhouse':
                    jobs = self._scrape_greenhouse(company)
                    all_jobs.extend(jobs)
                elif company.get('board_type') == 'lever':
                    jobs = self._scrape_lever(company)
                    all_jobs.extend(jobs)
            except Exception as e:
                print(f"    Error scraping {company['name']}: {e}")
                
        self.jobs = all_jobs
        return all_jobs
        
    def _scrape_greenhouse(self, company: Dict) -> List[Dict]:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company['board_token']}/jobs"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
            
        data = response.json()
        jobs = []
        for job in data.get('jobs', []):
            title = job.get('title', '')
            if not self._is_relevant_job(title):
                continue
                
            location = job.get('location', {}).get('name', '')
            
            job_data = {
                "title": title,
                "company": company['name'],
                "location": location,
                "experience": "0-3 years", # Defaulting for MBA fresher
                "salary": "Not disclosed",
                "url": job.get('absolute_url', ''),
                "job_type": "Full-time",
                "description": f"View role at {company['name']} portal."
            }
            jobs.append(self.standardize_job(job_data))
            
        return jobs

    def _scrape_lever(self, company: Dict) -> List[Dict]:
        url = f"https://api.lever.co/v0/postings/{company['board_token']}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
            
        data = response.json()
        jobs = []
        for job in data:
            title = job.get('text', '')
            if not self._is_relevant_job(title):
                continue
                
            location = job.get('categories', {}).get('location', '')
            
            job_data = {
                "title": title,
                "company": company['name'],
                "location": location,
                "experience": "0-3 years",
                "salary": "Not disclosed",
                "url": job.get('hostedUrl', ''),
                "job_type": "Full-time",
                "description": f"View role at {company['name']} portal."
            }
            jobs.append(self.standardize_job(job_data))
            
        return jobs
