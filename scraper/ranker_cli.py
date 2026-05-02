import json
import os
from datetime import datetime

def rank_jobs():
    jobs_path = '../dashboard/data/jobs.json'
    js_path = '../dashboard/data/jobs.js'
    
    if not os.path.exists(jobs_path):
        print(f"Error: {jobs_path} not found.")
        return

    with open(jobs_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    jobs = data.get('jobs', [])
    
    primary_roles = ["business analyst", "data analyst", "project manager"]
    secondary_roles = ["program manager", "hr analytics", "product manager", "strategy consultant", "operations manager"]
    
    for job in jobs:
        title = job.get('title', '').lower()
        location = job.get('location', '').lower()
        experience = job.get('experience', '').lower()
        
        score = 1
        
        # Check for Primary Roles
        is_primary = any(role in title for role in primary_roles)
        is_secondary = any(role in title for role in secondary_roles)
        
        # Location check (Bangalore or Remote)
        is_bangalore = "bangalore" in location or "bengaluru" in location
        is_remote = "remote" in location
        
        # Experience check (Entry level or 0-3 years)
        is_entry = any(exp in experience for exp in ["0-3", "0-2", "0-1", "fresher", "entry", "associate"]) or experience == ""
        
        if is_primary:
            if is_bangalore or is_remote:
                if is_entry:
                    score = 5
                else:
                    score = 4
            else:
                score = 3
        elif is_secondary:
            if is_bangalore or is_remote:
                if is_entry:
                    score = 4
                else:
                    score = 3
            else:
                score = 2
        else:
            if is_bangalore or is_remote:
                score = 2
            else:
                score = 1
                
        # Bonus for specific companies from CV/Preferences if applicable (not specified in protocol but good)
        
        job['score'] = score

    # Sort jobs by score (highest first)
    jobs.sort(key=lambda x: x['score'], reverse=True)
    
    # Update metadata
    data['jobs'] = jobs
    data['last_updated'] = datetime.now().isoformat()
    data['total_ranked'] = len(jobs)

    # Save JSON
    with open(jobs_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    # Save JS
    js_content = f"window.__JOBS_DATA__ = {json.dumps(data, indent=2)};"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"✅ Ranked {len(jobs)} jobs. Updated JSON and JS files.")

if __name__ == "__main__":
    rank_jobs()
