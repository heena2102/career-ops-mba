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

# Company Portals (Greenhouse & Lever)
# Indian companies for Bangalore onsite, Global companies for Remote
TRACKED_COMPANIES = [
    {"name": "Razorpay", "board_type": "lever", "board_token": "razorpay"},
    {"name": "Meesho", "board_type": "lever", "board_token": "meesho"},
    {"name": "ClearTax", "board_type": "greenhouse", "board_token": "cleartax"},
    {"name": "Pine Labs", "board_type": "greenhouse", "board_token": "pinelabs"},
    {"name": "Postman", "board_type": "greenhouse", "board_token": "postman"},
    {"name": "Stripe", "board_type": "greenhouse", "board_token": "stripe"},
    {"name": "GitLab", "board_type": "greenhouse", "board_token": "gitlab"},
    {"name": "GitHub", "board_type": "greenhouse", "board_token": "github"},
    {"name": "Atlassian", "board_type": "lever", "board_token": "atlassian"},
    {"name": "Shopify", "board_type": "greenhouse", "board_token": "shopify"},
    {"name": "Notion", "board_type": "greenhouse", "board_token": "notion"},
    {"name": "Airtable", "board_type": "greenhouse", "board_token": "airtable"},
    {"name": "Plaid", "board_type": "greenhouse", "board_token": "plaid"},
    {"name": "Coinbase", "board_type": "greenhouse", "board_token": "coinbase"},
    {"name": "Vercel", "board_type": "greenhouse", "board_token": "vercel"},
    {"name": "Deliveroo", "board_type": "greenhouse", "board_token": "deliveroo"}
]
