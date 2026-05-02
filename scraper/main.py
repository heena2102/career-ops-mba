#!/usr/bin/env python3
"""
Main job scraper orchestrator
Scrapes multiple job sources and compiles into a single JSON file
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from scrapers.indeed_scraper import IndeedScraper
from scrapers.naukri_scraper import NaukriScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.angellist_scraper import AngelListScraper
from scrapers.internshala_scraper import InternShalaScraper
from scrapers.company_scraper import CompanyScraper
from config import OUTPUT_FILE, FILTERS
from ranker import JobRanker

def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate jobs based on title and company"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    return unique_jobs

def filter_jobs(jobs: List[Dict]) -> List[Dict]:
    """Filter jobs based on criteria"""
    filtered = []
    
    for job in jobs:
        location = job.get("location", "").lower()
        
        # Include if Bangalore OR Remote
        is_bangalore = "bangalore" in location or "bengaluru" in location
        is_remote = "remote" in location
        
        if is_bangalore or is_remote:
            filtered.append(job)
    
    return filtered

def scrape_all_sources() -> List[Dict]:
    """Scrape all job sources"""
    all_jobs = []
    
    scrapers = [
        IndeedScraper(),
        NaukriScraper(),
        LinkedInScraper(),
        # AngelListScraper(),
        InternShalaScraper(),
        CompanyScraper(),
    ]
    
    print("\n🔍 Starting Job Scraping...\n")
    
    for scraper in scrapers:
        try:
            jobs = scraper.scrape()
            print(f"  ✓ Found {len(jobs)} jobs from {scraper.name}")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"  ✗ Error with {scraper.name}: {e}")
    
    return all_jobs

def save_jobs_to_json(jobs: List[Dict], output_path: str) -> None:
    """Save jobs to JSON file"""
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    output_data = {
        "total_jobs": len(jobs),
        "last_updated": datetime.now().isoformat(),
        "jobs": jobs
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved {len(jobs)} jobs to {output_path}\n")

    # Also generate a JS payload so dashboard works even when opened via file://
    js_output_path = output_path.replace(".json", ".js")
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write("window.__JOBS_DATA__ = ")
        json.dump(output_data, f, ensure_ascii=False)
        f.write(";")

    print(f"💾 Saved JS payload to {js_output_path}\n")

import argparse

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='MBA Job Scraper')
    parser.add_argument('--no-rank', action='store_true', help='Skip Gemini ranking (useful if using CLI skill)')
    args = parser.parse_args()

    print("=" * 50)
    print("  🎓 MBA Job Scraper")
    print("=" * 50)
    
    # Scrape all sources
    all_jobs = scrape_all_sources()
    
    print(f"\n📊 Total jobs found: {len(all_jobs)}")
    
    # Filter jobs
    filtered_jobs = filter_jobs(all_jobs)
    print(f"📍 Jobs matching criteria (Bangalore + Remote): {len(filtered_jobs)}")
    
    # Deduplicate
    unique_jobs = deduplicate_jobs(filtered_jobs)
    print(f"🎯 Unique jobs after deduplication: {len(unique_jobs)}")
    
    if args.no_rank:
        print("\n⏩ Skipping built-in ranking as requested.")
        final_jobs = unique_jobs
        for job in final_jobs:
            if 'score' not in job:
                job['score'] = 0
    else:
        # Rank jobs with Gemini intelligence
        print("\n🧠 Ranking jobs with Gemini AI...")
        ranker = JobRanker()
        # Rank only first 50 to save tokens/time during development
        jobs_to_rank = unique_jobs[:50]
        other_jobs = unique_jobs[50:]
        
        ranked_jobs = ranker.rank_jobs(jobs_to_rank)
        
        # Add default score to unranked jobs
        for job in other_jobs:
            job["score"] = 0
            
        final_jobs = ranked_jobs + other_jobs
    
    # Sort by score (descending)
    final_jobs.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    # Save to JSON
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    save_jobs_to_json(final_jobs, output_path)
    
    print("✅ Scraping complete! Open dashboard/index.html in your browser to view jobs.")

if __name__ == "__main__":
    main()
