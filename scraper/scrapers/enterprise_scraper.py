"""Enterprise job scraper for companies with proprietary ATS"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from .base_scraper import BaseScraper
from config import HEADERS, JOB_TITLES, ENTERPRISE_COMPANIES

class EnterpriseScraper(BaseScraper):
    """Scrapes LinkedIn specifically for target Enterprise companies"""
    
    def __init__(self):
        super().__init__("EnterprisePortals")
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def scrape(self) -> List[Dict]:
        """Scrape LinkedIn for specific enterprise companies"""
        try:
            print(f"  Scraping {self.name}...")
            
            all_jobs = []
            search_locations = ["Bangalore", "Remote"]
            
            # To avoid LinkedIn rate limits, we search primarily by Company name
            # and then filter results locally by JOB_TITLES
            
            for company in ENTERPRISE_COMPANIES:
                for location in search_locations:
                    try:
                        params = {
                            "keywords": company,
                            "location": location,
                            "start": 0
                        }
                        
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
                                date_elem = card.select_one(".job-search-card__listdate") or card.select_one(".job-search-card__listdate--new")
                                
                                if not title_elem or not company_elem or not link_elem:
                                    continue
                                    
                                title_text = title_elem.get_text(strip=True)
                                company_text = company_elem.get_text(strip=True)
                                
                                # Verify it's actually the target company (rough match)
                                if company.lower() not in company_text.lower():
                                    continue
                                    
                                # Verify it matches one of our target roles
                                is_relevant = any(role.lower() in title_text.lower() for role in JOB_TITLES)
                                if not is_relevant:
                                    continue
                                    
                                published_at = "NA"
                                if date_elem and date_elem.has_attr('datetime'):
                                    published_at = date_elem['datetime']
                                elif date_elem:
                                    published_at = date_elem.get_text(strip=True)
                                    
                                job_data = {
                                    "title": title_text,
                                    "company": company_text,
                                    "location": location_elem.get_text(strip=True) if location_elem else location,
                                    "experience": "0-3 years",
                                    "salary": "Not disclosed",
                                    "url": link_elem['href'].split('?')[0],
                                    "job_type": "Full-time",
                                    "description": f"View on LinkedIn: {title_text} at {company_text}",
                                    "published_at": published_at
                                }
                                all_jobs.append(self.standardize_job(job_data))
                            except Exception:
                                continue
                        
                        time.sleep(1) # Polite delay
                    except Exception as e:
                        print(f"    Error searching {company}: {e}")
            
            self.jobs = all_jobs
            return all_jobs
        
        except Exception as e:
            print(f"  Error scraping {self.name}: {e}")
            return []
