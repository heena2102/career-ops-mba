"""LinkedIn job scraper"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from .base_scraper import BaseScraper
from config import HEADERS, JOB_TITLES

class LinkedInScraper(BaseScraper):
    """Scrape jobs from LinkedIn (Public Pages)"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def scrape(self) -> List[Dict]:
        """Scrape LinkedIn for jobs"""
        try:
            print(f"  Scraping {self.name}...")
            
            all_jobs = []
            
            search_locations = ["Bangalore", "Remote"]
            
            for location in search_locations:
                for term in JOB_TITLES[:5]: # Limit for testing
                    try:
                        params = {
                            "keywords": term,
                            "location": location,
                            "start": 0
                        }
                        
                        print(f"    Searching {term} in {location}...")
                        response = requests.get(self.base_url, params=params, headers=HEADERS, timeout=10)
                        
                        if response.status_code != 200:
                            continue
                            
                        soup = BeautifulSoup(response.content, 'lxml')
                        job_cards = soup.select("li")
                        
                        for card in job_cards:
                            try:
                                title_elem = card.select_one(".base-search-card__title")
                                company_elem = card.select_one(".base-search-card__subtitle")
                                location_elem = card.select_one(".base-search-card__metadata .job-search-card__location")
                                link_elem = card.select_one("a.base-card__full-link")
                                
                                if not title_elem or not company_elem or not link_elem:
                                    continue
                                    
                                job_data = {
                                    "title": title_elem.get_text(strip=True),
                                    "company": company_elem.get_text(strip=True),
                                    "location": location_elem.get_text(strip=True) if location_elem else location,
                                    "experience": "0-3 years",
                                    "salary": "Not disclosed",
                                    "url": link_elem['href'].split('?')[0],
                                    "job_type": "Full-time",
                                    "description": f"View on LinkedIn: {title_elem.get_text(strip=True)} at {company_elem.get_text(strip=True)}"
                                }
                                all_jobs.append(self.standardize_job(job_data))
                            except Exception:
                                continue
                        
                        time.sleep(1) # Polite delay
                    except Exception as e:
                        print(f"    Error searching {term}: {e}")
            
            self.jobs = all_jobs
            return all_jobs
        
        except Exception as e:
            print(f"  Error scraping {self.name}: {e}")
            return []
