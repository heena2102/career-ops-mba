#!/bin/bash
# MBA Job Dashboard Launcher for macOS/Linux

echo ""
echo "========================================"
echo "  MBA Job Dashboard Launcher"
echo "========================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if jobs.json exists
if [ ! -f "$SCRIPT_DIR/dashboard/data/jobs.json" ]; then
    echo "[!] jobs.json not found. Running scraper first..."
    echo ""
    cd "$SCRIPT_DIR/scraper"
    python3 main.py
    if [ $? -ne 0 ]; then
        echo "[ERROR] Scraper failed. Make sure Python is installed."
        echo "Run: pip install -r requirements.txt"
        exit 1
    fi
fi

echo "[+] Opening dashboard in your browser..."
echo ""

# Open the dashboard
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$SCRIPT_DIR/dashboard/index.html"
else
    xdg-open "$SCRIPT_DIR/dashboard/index.html"
fi

echo "[✓] Dashboard opened! Check your browser."
echo ""
echo "To refresh jobs, run: python3 scraper/main.py"
echo ""
