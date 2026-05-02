# Skill: Career-Ops MBA Scan

Find and rank MBA-relevant jobs in Bangalore and Remote based on your CV and profile.

## Usage
- `/career-ops-mba scan`: Runs the full pipeline: scrapes jobs from Internshala, LinkedIn, etc., ranks them using Gemini, and updates the dashboard.
- `/career-ops-mba dashboard`: Opens the local job dashboard in your browser.

## Instructions
When the user runs `/career-ops-mba scan`:
1. Execute `npm run scrape` to fetch the latest job listings.
2. Read the generated `dashboard/data/jobs.json`.
3. Read the candidate's `cv.md` and `config/profile.yml`.
4. Use your current intelligence to evaluate each job listing against the CV/Profile.
5. Assign a score (1-5) to each job.
6. Update `dashboard/data/jobs.json` and `dashboard/data/jobs.js` with the new scores.
7. Sort the jobs by score (highest first).
8. Notify the user when the dashboard is ready.

## Prompt Context
Always refer to `cv.md` for Heena Kauser's background and `config/profile.yml` for her target roles (Business Analyst, Data Analyst, etc.).
Focus on "Bangalore Onsite" and "Global Remote" opportunities.
High-fit jobs (Score 4-5) should match the MBA graduate criteria and her specific skills like Power BI, SQL, and Economics.
