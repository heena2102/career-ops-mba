# Career-Ops MBA Project Instructions

This file contains the foundational mandates for the Gemini CLI when working in this repository.

## 🚀 The "Scan" Protocol
When the user mentions "scan" or "/career-ops-mba scan", you must perform the following autonomous workflow:

1.  **Scrape:** Run `npm run scrape:no-rank`. This fires the Python scrapers to collect raw job data into `dashboard/data/jobs.json`.
2.  **Read Context:** Read the following files to understand the candidate:
    - `cv.md`: Heena Kauser's resume.
    - `config/profile.yml`: Target roles, compensation, and preferences.
3.  **Analyze & Rank:** 
    - Read the `jobs` array from `dashboard/data/jobs.json`.
    - Evaluate each job against the CV and Profile.
    - Assign a score from 1 (poor fit) to 5 (perfect fit).
    - Focus on Bangalore onsite and Global Remote roles.
4.  **Update Dashboard:**
    - Rewrite `dashboard/data/jobs.json` with the assigned scores.
    - Re-generate `dashboard/data/jobs.js` with the same data (using `window.__JOBS_DATA__ = ...;` format).
    - Sort the jobs by score (highest first) before saving.
5.  **Notify:** Inform the user that the scan is complete and the dashboard is updated with AI rankings.

## 📊 The "Dashboard" Protocol
When asked to show or open the dashboard:
1.  Verify `dashboard/index.html` exists.
2.  Suggest the user open it or use the `open-dashboard.bat` script.

## 🎯 Candidate Focus
- **Name:** Heena Kauser
- **Background:** MBA in Business Analytics, Economics background.
- **Skills:** Power BI, SQL, Python, R, Excel, Stakeholder Management.
- **Target Roles:** Business Analyst, Data Analyst, Project Manager.
