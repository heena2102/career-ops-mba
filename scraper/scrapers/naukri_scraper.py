"""Naukri job scraper"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import time
from .base_scraper import BaseScraper
from config import JOB_TITLES

class NaukriScraper(BaseScraper):
    """Scrape jobs from Naukri using Selenium"""
    
    def __init__(self):
        super().__init__("Naukri")
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    def scrape(self) -> List[Dict]:
        """Scrape Naukri for jobs"""
        driver = None
        try:
            print(f"  Scraping {self.name}...")
            driver = webdriver.Chrome(options=self.chrome_options)
            
            all_jobs = []
            
            # Naukri search URL format: https://www.naukri.com/product-manager-jobs-in-bangalore
            for term in JOB_TITLES[:5]: # Limit for testing
                try:
                    search_slug = term.lower().replace(" ", "-")
                    # Onsite Bangalore
                    self._scrape_naukri_url(driver, f"https://www.naukri.com/{search_slug}-jobs-in-bangalore", all_jobs)
                    # Remote
                    self._scrape_naukri_url(driver, f"https://www.naukri.com/{search_slug}-jobs?k={term.replace(' ', '%20')}&l=remote", all_jobs)
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

    def _scrape_naukri_url(self, driver, url: str, all_jobs: List[Dict]):
        """Helper to scrape a Naukri search result page"""
        try:
            print(f"    Fetching {url}...")
            driver.get(url)
            
            # Wait for job tuples to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sjw__tuple"))
            )
            
            # Sometimes Naukri uses different classes, try both
            cards = driver.find_elements(By.CLASS_NAME, "sjw__tuple")
            if not cards:
                cards = driver.find_elements(By.CLASS_NAME, "cust-job-tuple")
            
            for card in cards:
                try:
                    title_elem = card.find_element(By.CLASS_NAME, "title")
                    company_elem = card.find_element(By.CLASS_NAME, "comp-name")
                    location_elem = card.find_element(By.CLASS_NAME, "locWp")
                    exp_elem = card.find_element(By.CLASS_NAME, "expWp")
                    
                    job_url = title_elem.get_attribute("href")
                    
                    job_data = {
                        "title": title_elem.text,
                        "company": company_elem.text,
                        "location": location_elem.text,
                        "experience": exp_elem.text,
                        "salary": "Not disclosed",
                        "url": job_url,
                        "job_type": "Full-time",
                        "description": f"View on Naukri: {title_elem.text} at {company_elem.text}"
                    }
                    all_jobs.append(self.standardize_job(job_data))
                except Exception:
                    continue
            
            time.sleep(2)
        except Exception as e:
            # print(f"    Error on page: {e}")
            pass
