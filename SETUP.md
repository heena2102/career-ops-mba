# 📖 Complete Setup & Installation Guide

## System Requirements

- **Python 3.8+** (for scraper)
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Internet Connection** (for web scraping)
- **~500MB disk space** (for dependencies)

### Check Python Installation

```bash
python --version
# Should output: Python 3.8.x or higher

pip --version
# Should output: pip 20.x or higher
```

If Python is not installed, download from: https://www.python.org/downloads/

---

## Installation Steps

### Step 1: Verify Project Structure

After creating the project, you should have:

```
career-ops-mba/
├── scraper/
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── scrapers/
│       ├── __init__.py
│       ├── base_scraper.py
│       ├── indeed_scraper.py
│       ├── naukri_scraper.py
│       ├── linkedin_scraper.py
│       ├── angellist_scraper.py
│       └── internshala_scraper.py
├── dashboard/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data/
│       └── jobs.json (auto-created)
├── saved-jobs/ (created when you export)
├── package.json
├── README.md
├── QUICKSTART.md
├── open-dashboard.bat (Windows)
├── open-dashboard.sh (Mac/Linux)
└── .gitignore
```

### Step 2: Install Python Dependencies

#### Windows:
```bash
cd scraper
pip install -r requirements.txt
```

#### macOS/Linux:
```bash
cd scraper
pip3 install -r requirements.txt
```

Expected output: All packages installed successfully ✓

### Step 3: Run the Scraper

#### Windows:
```bash
cd scraper
python main.py
```

#### macOS/Linux:
```bash
cd scraper
python3 main.py
```

**Expected output:**
```
==================================================
  🎓 MBA Job Scraper
==================================================

🔍 Starting Job Scraping...
  Scraping Indeed...
  ✓ Found X jobs from Indeed
  Scraping Naukri...
  ✓ Found X jobs from Naukri
  ... more sources ...

📊 Total jobs found: XX
📍 Jobs matching criteria (Bangalore + Remote): XX
🎯 Unique jobs after deduplication: XX
💾 Saved XX jobs to dashboard/data/jobs.json

✅ Scraping complete! Open dashboard/index.html in your browser
```

### Step 4: Open the Dashboard

#### Option A: Double-click on Windows (Easiest)
```bash
# Windows only - double-click this file:
open-dashboard.bat
```

#### Option B: Use Python HTTP Server
```bash
cd dashboard
python -m http.server 8000
# Then open: http://localhost:8000 in browser
```

#### Option C: Open directly in browser
- **Windows**: `start dashboard/index.html`
- **Mac**: `open dashboard/index.html`
- **Linux**: `xdg-open dashboard/index.html`

#### Option D: Drag & drop
- Drag `dashboard/index.html` into your browser window

---

## Dashboard Usage

### First Time Using

1. **Browser opens** to the dashboard
2. **You see**: 35 MBA jobs from multiple sources
3. **Jobs include**: Product Manager, Analyst, Manager, Consultant roles
4. **Locations**: Bangalore onsite OR Remote globally
5. **All jobs**: Entry to mid-level (0-4 years experience)

### Finding Jobs

#### Using Search
- Type in the search box
- Real-time filtering as you type
- Searches job titles, companies, descriptions

#### Using Filters
- **Location**: All | Bangalore | Remote
- **Source**: All | Indeed | Naukri | LinkedIn | AngelList | Internshala
- **Job Type**: All | Full-time | Internship

#### Viewing Job Details
- Click any job card to see full details
- Click "View on [Source]" to apply on original site

### Saving Jobs

1. Click **"💾 Save"** button on any job
2. Job gets saved to your browser's storage
3. Card border turns green
4. Saved count updates at top

### Exporting to CSV

1. Save some jobs (at least 1)
2. Click **"💾 Export Saved Jobs"** button
3. CSV file downloads automatically
4. CSV includes: Title, Company, Location, Salary, Source, URL, Date

---

## Common Tasks

### Refresh Jobs
To get latest job listings:

```bash
cd scraper
python main.py
# or: python3 main.py (Mac/Linux)
```

Then refresh browser (Ctrl+F5 or Cmd+Shift+R)

### Add Custom Job Titles
Edit `scraper/config.py`:

```python
JOB_TITLES = [
    "Product Manager",
    "Business Analyst",
    "Data Scientist",        # Add your roles
    "Your Custom Role",      # Add your roles
]
```

Then re-run scraper.

### Export Saved Jobs
1. Save jobs in dashboard
2. Click "💾 Export Saved Jobs"
3. File downloads as `saved-jobs-YYYY-MM-DD.csv`
4. Open in Excel or Google Sheets

### Change Dashboard Theme
Edit `dashboard/styles.css`:

```css
:root {
    --primary-color: #2563eb;        /* Change blue */
    --accent-color: #f59e0b;         /* Change orange */
    /* ... etc ... */
}
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'bs4'"

**Cause**: Python dependencies not installed

**Fix**:
```bash
cd scraper
pip install -r requirements.txt
```

### Issue: "No jobs showing in dashboard"

**Cause**: jobs.json not created

**Fix**:
1. Run scraper: `cd scraper && python main.py`
2. Check file exists: `dashboard/data/jobs.json`
3. Refresh browser (Ctrl+F5)

### Issue: "Python not found"

**Cause**: Python not installed or not in PATH

**Fix**:
1. Install Python from https://python.org
2. Add to PATH during installation
3. Restart terminal
4. Verify: `python --version`

### Issue: "Scraper has errors"

**Cause**: Missing dependencies or network issue

**Fix**:
```bash
cd scraper
pip install -r requirements.txt --upgrade
python main.py
```

### Issue: "Dashboard won't load jobs"

**Cause**: Browser security restrictions with file:// protocol

**Fix**:
```bash
cd dashboard
python -m http.server 8000
# Open http://localhost:8000
```

### Issue: "CSV export not working"

**Cause**: No saved jobs or browser issue

**Fix**:
1. Save at least 1 job first
2. Try a different browser
3. Check browser console (F12)

---

## Performance Tips

### For Large Number of Jobs

If you scrape 1000+ jobs:

1. **Use HTTP Server** instead of file:// protocol
2. **Clear filters** often to reduce rendering
3. **Don't export huge CSVs** at once
4. **Use search** instead of scrolling

### For Faster Scraping

1. **Reduce job titles** in config.py
2. **Reduce locations** if not needed
3. **Increase timeout** if getting errors
4. **Check internet speed**

---

## Next Steps

### Immediate
- [ ] Run scraper (`python scraper/main.py`)
- [ ] Open dashboard in browser
- [ ] Browse 35 MBA jobs
- [ ] Save 5-10 interesting jobs
- [ ] Export to CSV

### Short Term
- [ ] Customize job titles for your search
- [ ] Run scraper every week
- [ ] Track applications in exported CSV

### Long Term
- [ ] Add more job boards
- [ ] Setup automated daily scrapes
- [ ] Deploy dashboard online
- [ ] Add email notifications
- [ ] Build application tracker

---

## Need Help?

### Resources
- **Full Documentation**: See `README.md`
- **Quick Start**: See `QUICKSTART.md`
- **Scraper Code**: Check `scraper/main.py`
- **Dashboard Code**: Check `dashboard/app.js`

### Python Issues
- Official Docs: https://docs.python.org
- Pip Docs: https://pip.pypa.io

### Browser Issues
- Clear cache: Ctrl+Shift+Del (Windows) or Cmd+Shift+Del (Mac)
- Check console: F12 → Console tab
- Try different browser

---

## Security Notes

⚠️ **Important**: This tool respects robots.txt and terms of service of job boards. For production use:

- Add delays between requests
- Rotate user agents
- Cache results locally
- Don't distribute scraped data
- Check each site's ToS

---

## Version Information

- **Project**: Career-Ops MBA v1.0.0
- **Created**: May 2026
- **Python**: 3.8+
- **License**: MIT

---

## Summary

You now have a complete, working job scraper for MBA graduates! 

**To get started:**
```bash
# 1. Run scraper
cd scraper && python main.py

# 2. Open dashboard
start dashboard/index.html  # Windows
# or
open dashboard/index.html   # Mac
# or
xdg-open dashboard/index.html  # Linux
```

That's it! Happy job hunting! 🚀

---

*Built with ❤️ for MBA graduates seeking opportunities in Bangalore and globally*
