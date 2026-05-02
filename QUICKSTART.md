# 🚀 Quick Start: Career-Ops MBA

Follow these steps to set up and run your AI-powered job dashboard.

## 1. Initial Setup
Move this project folder to your Desktop (or any preferred directory) and open your terminal there.

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd scraper
pip install -r requirements.txt
cd ..
```

## 2. Using with Gemini CLI (Recommended)
This project is designed to work as a **Gemini CLI Skill**.

1. Open the project folder in Gemini CLI:
   ```bash
   gemini .
   ```
2. Run the specialized scan command:
   ```bash
   /career-ops-mba scan
   ```
   *This will automatically scrape jobs and use the CLI's tokens to rank them based on your `cv.md` and `config/profile.yml`.*

## 3. Manual Operation
If you prefer running it manually:

```bash
# Run full scrape and AI ranking
npm run scrape

# Open the dashboard
start dashboard/index.html
```

## 4. Customizing Your Profile
- Update **`cv.md`** with your latest experience.
- Edit **`config/profile.yml`** to change your target roles, compensation expectations, or keywords.

---
*Built for Heena Kauser | MBA Business Analytics*
