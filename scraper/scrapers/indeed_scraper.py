"""Indeed job scraper"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import time
from .base_scraper import BaseScraper
from config import JOB_TITLES

class IndeedScraper(BaseScraper):
    """Scrape jobs from Indeed using Selenium"""
    
    def __init__(self):
        super().__init__("Indeed")
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    def scrape(self) -> List[Dict]:
        """Scrape Indeed for jobs"""
        driver = None
        try:
            print(f"  Scraping {self.name}...")
            driver = webdriver.Chrome(options=self.chrome_options)
            
            all_jobs = []
            
            # For MBA graduates, we search in India (Bangalore) and Global (Remote)
            search_configs = [
                {"base_url": "https://in.indeed.com", "location": "Bangalore"},
                {"base_url": "https://www.indeed.com", "location": "Remote"}
            ]
            
            for config in search_configs:
                for term in JOB_TITLES[:5]:  # Limit to first 5 for speed during testing
                    try:
                        url = f"{config['base_url']}/jobs?q={term.replace(' ', '+')}&l={config['location']}"
                        print(f"    Searching {term} in {config['location']}...")
                        driver.get(url)
                        
                        # Wait for job cards to load
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                        )
                        
                        cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
                        
                        for card in cards:
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span[title]")
                                company_elem = card.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
                                location_elem = card.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']")
                                
                                # URL is in the anchor tag within the h2
                                link_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                                job_url = link_elem.get_attribute("href")
                                
                                job_data = {
                                    "title": title_elem.get_attribute("title"),
                                    "company": company_elem.text,
                                    "location": location_elem.text,
                                    "experience": "0-3 years",  # Target level
                                    "salary": "Not disclosed",
                                    "url": job_url,
                                    "job_type": "Full-time",
                                    "description": f"View on Indeed: {title_elem.get_attribute('title')} at {company_elem.text}"
                                }
                                all_jobs.append(self.standardize_job(job_data))
                            except Exception as e:
                                continue
                                
                        time.sleep(2)  # Polite delay
                    except Exception as e:
                        print(f"    Error searching {term}: {e}")
            
            self.jobs = all_jobs
            return all_jobs
            
        except Exception as e:
            print(f"  Error scraping {self.name}: {e}")
            return []
        finally:
            if driver:
                driver.quit()
