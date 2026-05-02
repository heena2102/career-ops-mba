"""Base scraper class"""
from abc import ABC, abstractmethod
from typing import List, Dict
import re

class BaseScraper(ABC):
    """Base class for all job scrapers"""
    
    def __init__(self, name: str):
        self.name = name
        self.jobs = []
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape jobs from source"""
        pass
    
    def filter_by_location(self, jobs: List[Dict], locations: List[str]) -> List[Dict]:
        """Filter jobs by location"""
        filtered = []
        for job in jobs:
            location = job.get("location", "").lower()
            if any(loc.lower() in location for loc in locations):
                filtered.append(job)
            elif "remote" in location.lower():
                filtered.append(job)
        return filtered
    
    def filter_by_experience(self, jobs: List[Dict]) -> List[Dict]:
        """Filter by MBA-relevant experience level"""
        filtered = []
        experience_keywords = ["0-2", "0-3", "1-3", "2-4", "0-5", "entry", "associate", "graduate", "fresher"]
        
        for job in jobs:
            exp = str(job.get("experience", "")).lower()
            if any(keyword in exp for keyword in experience_keywords) or exp == "":
                filtered.append(job)
        
        return filtered
    
    def standardize_job(self, job: Dict) -> Dict:
        """Standardize job data format"""
        from datetime import datetime
        return {
            "title": job.get("title", "").strip(),
            "company": job.get("company", "").strip(),
            "location": job.get("location", "").strip(),
            "experience": job.get("experience", "").strip(),
            "salary": job.get("salary", "").strip(),
            "url": job.get("url", "").strip(),
            "source": self.name,
            "job_type": job.get("job_type", "").strip(),
            "description": job.get("description", "")[:500].strip(),  # Truncate description
            "published_at": job.get("published_at", datetime.now().strftime("%Y-%m-%d")),
            "discovered_at": datetime.now().strftime("%Y-%m-%d"),
        }
