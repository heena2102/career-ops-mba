"""Configuration for job scraper"""

# Job titles to search for (MBA-relevant)
JOB_TITLES = [
    "Product Manager",
    "Business Analyst",
    "Strategy Consultant",
    "Data Analyst",
    "Operations Manager",
    "Marketing Manager",
    "Sales Manager",
    "Project Manager",
    "Associate Consultant",
    "Graduate Engineer",
    "Associate Product Manager",
    "Business Operations",
]

# Keywords for filtering
FILTERS = {
    "locations": ["Bangalore", "Bengaluru", "Remote"],
    "experience_levels": ["0-2 years", "0-3 years", "1-3 years", "2-4 years", "0-5 years", "Entry Level", "Associate", "Graduate"],
}

# Headers for web requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Output
OUTPUT_FILE = "../dashboard/data/jobs.json"
SAVED_JOBS_CSV = "../saved-jobs/saved_jobs.csv"
