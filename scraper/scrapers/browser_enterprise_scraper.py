"""Browser-based enterprise scraper using Selenium for protected ATS portals"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import time
from .base_scraper import BaseScraper
from config import JOB_TITLES

class BrowserEnterpriseScraper(BaseScraper):
    """Scrapes protected ATS portals (like Eightfold) using Selenium"""
    
    def __init__(self):
        super().__init__("EnterprisePortals")
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    def scrape(self) -> List[Dict]:
        all_jobs = []
        driver = None
        
        # Eightfold AI portals
        eightfold_companies = [
            ("American Express", "aexp.eightfold.ai"),
            ("BNY Mellon", "bnymellon.eightfold.ai")
        ]
        
        try:
            print(f"  Scraping {self.name} (Browser Automation)...")
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.set_page_load_timeout(20)
            
            locations = ["Bengaluru", "Remote"]
            
            for company_name, domain in eightfold_companies:
                for location in locations:
                    for role in JOB_TITLES[:3]: # Testing limit
                        try:
                            # Standard Eightfold search URL
                            url = f"https://{domain}/careers?query={role.replace(' ', '%20')}&location={location}"
                            print(f"    Searching {company_name} for {role} in {location}...")
                            driver.get(url)
                            
                            # Wait for potential job cards to load (Eightfold uses React)
                            time.sleep(4) 
                            
                            # Generic extraction since specific classes vary by tenant
                            # Look for typical Eightfold card links
                            cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/careers?domain=']")
                            if not cards:
                                cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/careers/job']")
                            
                            for card in cards[:5]: # Limit per search
                                try:
                                    title = card.text.split('\n')[0] if card.text else role
                                    job_url = card.get_attribute("href")
                                    
                                    job_data = {
                                        "title": title,
                                        "company": company_name,
                                        "location": location,
                                        "experience": "0-3 years",
                                        "salary": "Not disclosed",
                                        "url": job_url,
                                        "job_type": "Full-time",
                                        "description": f"View on Eightfold: {title} at {company_name}",
                                        "source": company_name,
                                        "published_at": "NA"
                                    }
                                    all_jobs.append(self.standardize_job(job_data))
                                except:
                                    continue
                                    
                        except Exception as e:
                            print(f"    Error scraping {company_name}: {e}")
                            
        except Exception as e:
            print(f"  Error initializing browser scraper: {e}")
        finally:
            if driver:
                driver.quit()
                
        self.jobs = all_jobs
        return all_jobs
