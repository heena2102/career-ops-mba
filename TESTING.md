# 🧪 Testing Methodology

Use this guide to verify that your **Career-Ops MBA** setup is working correctly.

## 1. Automated Test
Run the built-in test script to verify file structure and scraper output:
```bash
python test_pipeline.py
```

## 2. Manual Verification Steps

### Step A: The Scraper
Run the scraper without ranking to ensure network connections and parsers are working:
```bash
npm run scrape:no-rank
```
- **Check:** Open `dashboard/data/jobs.json`. It should be populated with jobs from Internshala, LinkedIn, etc.

### Step B: The AI "Scan" Protocol
Inside the Gemini CLI (`gemini .`), run:
```text
scan
```
- **Observe:** The agent should run the scraper, read your `cv.md`, and then output its ranking process.
- **Check:** Look at the terminal output. You should see the agent assigning scores (1-5) to the jobs it found.

### Step C: The Dashboard
Open the dashboard:
```bash
open-dashboard.bat
```
- **Verify:** 
    - High-match jobs (Score 4-5) have **Green Borders**.
    - Low-match jobs have **Red Borders**.
    - Jobs are sorted with the Green ones at the top.

## 3. Troubleshooting
- **No Rankings?** Ensure your `GOOGLE_API_KEY` is in `scraper/.env` OR you are running the `scan` command through the Gemini CLI (which uses the active session).
- **No Jobs?** Check your internet connection. LinkedIn and Indeed scrapers are sensitive to rate limits; if they fail, Internshala usually remains reliable.
