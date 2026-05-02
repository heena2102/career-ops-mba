# 🎓 Career-Ops MBA - Job Scraper + Dashboard

An intelligent job scraper designed specifically for MBA graduates looking for opportunities in **Bangalore (onsite)** and **Remote roles globally**. Features a beautiful interactive dashboard to browse, filter, and save jobs.

Built with inspiration from [career-ops](https://github.com/santifer/career-ops) and [career-ops-india](https://github.com/Justinsharon/career-ops-india).

---

## ✨ Features

- **🔍 Multi-Source Scraping**: Scrapes from Indeed, Naukri, LinkedIn, AngelList, and Internshala
- **📍 Smart Filtering**: Automatically filters for Bangalore onsite OR Remote opportunities
- **🎯 MBA-Focused**: Targets entry-level to mid-level roles (0-4 years experience)
- **🌐 Beautiful Dashboard**: Modern, responsive HTML dashboard with real-time search and filters
- **💾 Save & Export**: Save interesting jobs and export them to CSV
- **⚡ Fast & Lightweight**: No heavy frameworks - vanilla JS, CSS, and Python

---

## 🏗️ Project Structure

```
career-ops-mba/
├── scraper/                    # Python scraper backend
│   ├── scrapers/               # Individual scraper modules
│   │   ├── base_scraper.py     # Base class for all scrapers
│   │   ├── indeed_scraper.py
│   │   ├── naukri_scraper.py
│   │   ├── linkedin_scraper.py
│   │   ├── angellist_scraper.py
│   │   └── internshala_scraper.py
│   ├── config.py               # Configuration & filters
│   ├── main.py                 # Main entry point
│   └── requirements.txt         # Python dependencies
├── dashboard/                  # Frontend (HTML/CSS/JS)
│   ├── index.html              # Main dashboard page
│   ├── styles.css              # Dashboard styling
│   ├── app.js                  # Dashboard logic
│   └── data/
│       └── jobs.json           # Generated job data (created by scraper)
├── saved-jobs/                 # Saved jobs CSV location
├── package.json                # NPM project metadata
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for running a simple HTTP server)

### Step 1: Clone/Setup
```bash
cd career-ops-mba
```

### Step 2: Run the Scraper
```bash
# Install Python dependencies
cd scraper
pip install -r requirements.txt

# Run the scraper
python main.py
```

This will generate `dashboard/data/jobs.json` with all scraped jobs.

### Step 3: Open the Dashboard
Open `dashboard/index.html` in your web browser:
```bash
# Option 1: Direct file (simplest)
# On Windows: 
start dashboard/index.html

# On Mac:
open dashboard/index.html

# On Linux:
xdg-open dashboard/index.html
```

Or use a simple HTTP server:
```bash
# Using Python 3
cd dashboard
python -m http.server 8000
# Then open http://localhost:8000 in your browser
```

---

## 📊 Dashboard Features

### Search & Filters
- **🔍 Text Search**: Search by job title, company, location, or keywords
- **📍 Location Filter**: All | Bangalore | Remote
- **🏢 Source Filter**: All job boards or specific sources
- **💼 Job Type Filter**: Full-time, Internship, etc.

### Job Cards
Each job displays:
- Job title and company
- Location (with emoji)
- Job type and source
- Salary (if available)
- Brief description
- Links to apply on source platform

### Save & Export
- **💾 Save Job**: Click "Save" to mark jobs for later
- **📥 Export to CSV**: Export all saved jobs as CSV file with:
  - Title, Company, Location
  - Job Type, Salary, Experience
  - Source, URL, Saved Date

---

## 🛠️ How It Works

### Scraper Architecture

1. **Configuration** (`config.py`):
   - Defines job titles to search (Product Manager, Analyst, etc.)
   - Sets filter criteria and output paths

2. **Base Scraper** (`base_scraper.py`):
   - Common methods for all scrapers
   - Location and experience filtering
   - Job data standardization

3. **Individual Scrapers**:
   - Each platform has its own scraper module
   - Handles platform-specific HTML/API structures
   - Returns standardized job objects

4. **Main Orchestrator** (`main.py`):
   - Runs all scrapers in parallel
   - Filters results by location criteria
   - Deduplicates jobs
   - Exports to JSON for dashboard

### Dashboard Architecture

1. **HTML Structure** (`index.html`):
   - Header with statistics
   - Filter controls
   - Jobs grid container
   - Modal for job details

2. **Styling** (`styles.css`):
   - Responsive grid layout
   - Modern card-based design
   - Smooth animations and transitions
   - Mobile-friendly

3. **Application Logic** (`app.js`):
   - Loads jobs from JSON
   - Real-time filtering and search
   - Save/unsave functionality with localStorage
   - CSV export
   - Modal job details viewer

---

## 📋 Job Filtering Criteria

### Location
- ✅ **Bangalore/Bengaluru** - Onsite positions
- ✅ **Remote** - Work from anywhere

### Experience Level
- Entry Level (0-2 years)
- Associate (0-3 years)  
- Graduate Programs
- Junior roles (1-3 years)
- Mid-level (2-4 years)

### Job Roles (MBA-Relevant)
- Product Manager
- Business Analyst
- Data Analyst
- Strategy Consultant
- Operations Manager
- Marketing Manager
- Sales Manager
- Project Manager
- Business Development
- Management Consultant

---

## 🔧 Customization

### Add More Job Titles
Edit `scraper/config.py`:
```python
JOB_TITLES = [
    "Product Manager",
    "Your Role Here",  # Add custom roles
    "Another Role",
]
```

### Add More Scrapers
1. Create `scraper/scrapers/new_scraper.py`
2. Inherit from `BaseScraper`
3. Implement `scrape()` method
4. Import and add to `main.py`

### Modify Dashboard Styling
Edit `dashboard/styles.css` for colors, fonts, layout, etc.

---

## 📝 Saved Jobs CSV Format

When you export saved jobs, you get a CSV file with:

| Title | Company | Location | Job Type | Salary | Experience | Source | URL | Saved Date |
|-------|---------|----------|----------|--------|------------|--------|-----|-----------|
| Product Manager | Company A | Bangalore | Full-time | ₹20-30L | 1-3 yrs | Naukri | https://... | 2026-05-01 |

---

## 🚨 Troubleshooting

### "No jobs found" error
- ✅ Make sure scraper ran successfully: `cd scraper && python main.py`
- ✅ Check that `dashboard/data/jobs.json` exists
- ✅ Clear browser cache and refresh

### Dashboard won't load jobs
- ✅ Run the scraper first to generate `jobs.json`
- ✅ Check browser console for errors (F12)
- ✅ Use HTTP server instead of file:// protocol

### Python scraper fails
- ✅ Install dependencies: `pip install -r scraper/requirements.txt`
- ✅ Check Python version: `python --version` (need 3.8+)
- ✅ Check internet connection

---

## 📦 Dependencies

### Python
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `selenium` - Browser automation (optional)
- `python-dotenv` - Environment variables
- `lxml` - XML/HTML processing

### Frontend
- Vanilla JavaScript (no dependencies)
- CSS3 (no preprocessor)
- HTML5

---

## 🎯 Future Enhancements

- [ ] Email notifications for new jobs matching criteria
- [ ] AI-powered job recommendations
- [ ] LinkedIn integration for easy apply
- [ ] Advanced filtering (salary range, company type)
- [ ] Job comparison tool
- [ ] Application tracking system
- [ ] Browser extension
- [ ] Mobile app

---

## 📄 License

MIT License - feel free to use, modify, and distribute

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

---

## 📞 Support

Found a bug or have a suggestion? Open an issue on GitHub!

---

## 🙏 Acknowledgments

Inspired by:
- [santifer/career-ops](https://github.com/santifer/career-ops) - European job market
- [Justinsharon/career-ops-india](https://github.com/Justinsharon/career-ops-india) - Indian job market

---

## ⚠️ Disclaimer

This tool is for educational purposes. Please respect the terms of service of each job board. Always check robots.txt and terms of service before scraping.

---

Built with ❤️ for MBA graduates | Last Updated: May 2026
