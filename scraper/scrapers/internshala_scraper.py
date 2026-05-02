"""Internshala job scraper"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base_scraper import BaseScraper
from config import HEADERS, JOB_TITLES

class InternShalaScraper(BaseScraper):
    """Scrape jobs from Internshala"""
    
    def __init__(self):
        super().__init__("Internshala")
        self.base_url = "https://internshala.com"
    
    def scrape(self) -> List[Dict]:
        """Scrape Internshala for jobs"""
        try:
            print(f"  Scraping {self.name}...")
            
            all_jobs = []
            
            for role in JOB_TITLES:
                # Bangalore jobs
                bangalore_jobs = self._scrape_url(f"{self.base_url}/jobs/keywords-{role.replace(' ', '%20')}/location-Bangalore")
                all_jobs.extend(bangalore_jobs)
                
                # Remote jobs
                remote_jobs = self._scrape_url(f"{self.base_url}/jobs/keywords-{role.replace(' ', '%20')}/location-Remote")
                all_jobs.extend(remote_jobs)
                
                print(f"    - Found {len(bangalore_jobs) + len(remote_jobs)} jobs for {role}")
            
            self.jobs = all_jobs
            return all_jobs
        
        except Exception as e:
            print(f"  Error scraping {self.name}: {e}")
            return []

    def _scrape_url(self, url: str) -> List[Dict]:
        """Helper to scrape a specific Internshala URL"""
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'lxml')
            job_cards = soup.select(".individual_internship")
            
            results = []
            for card in job_cards:
                try:
                    title_elem = card.select_one(".job-internship-name")
                    company_elem = card.select_one(".company-name")
                    location_elem = card.select_one(".location_link")
                    salary_elem = card.select_one(".salary_container .desktop")
                    date_elem = card.select_one(".status-inactive") or card.select_one(".status-success") or card.select_one(".status")
                    
                    if not title_elem or not company_elem:
                        continue
                        
                    published_at = date_elem.get_text(strip=True) if date_elem else "NA"
                        
                    job_data = {
                        "title": title_elem.get_text(strip=True),
                        "company": company_elem.get_text(strip=True),
                        "location": location_elem.get_text(strip=True) if location_elem else "Remote",
                        "experience": "0-2 years",  # Internshala is mostly for freshers/early career
                        "salary": salary_elem.get_text(strip=True) if salary_elem else "Not disclosed",
                        "url": self.base_url + title_elem.find_parent('a')['href'] if title_elem.find_parent('a') else url,
                        "job_type": "Full-time",
                        "description": f"View details on Internshala: {title_elem.get_text(strip=True)} at {company_elem.get_text(strip=True)}",
                        "published_at": published_at
                    }
                    results.append(self.standardize_job(job_data))
                except Exception as e:
                    continue
            
            return results
        except Exception as e:
            print(f"    Error fetching {url}: {e}")
            return []
