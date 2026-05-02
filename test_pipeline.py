"""
Test Pipeline for Career-Ops MBA
Verifies scraper output and basic ranking structure
"""
import json
import os
import unittest

class TestCareerOpsPipeline(unittest.TestCase):
    def setUp(self):
        self.data_path = "dashboard/data/jobs.json"
        self.profile_path = "config/profile.yml"
        self.cv_path = "cv.md"

    def test_files_exist(self):
        """Check if essential configuration files exist"""
        self.assertTrue(os.path.exists(self.profile_path), "profile.yml is missing")
        self.assertTrue(os.path.exists(self.cv_path), "cv.md is missing")

    def test_scraper_output(self):
        """Verify that jobs.json exists and has valid structure"""
        if not os.path.exists(self.data_path):
            self.skipTest("jobs.json not found. Run a scan first.")
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.assertIn("jobs", data)
        self.assertGreater(len(data["jobs"]), 0, "No jobs found in jobs.json")
        
        # Check first job structure
        job = data["jobs"][0]
        required_keys = ["title", "company", "location", "url", "source"]
        for key in required_keys:
            self.assertIn(key, job, f"Job missing required key: {key}")

    def test_ranking_integration(self):
        """Check if score field exists (even if 0)"""
        if not os.path.exists(self.data_path):
            self.skipTest("jobs.json not found.")
            
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        job = data["jobs"][0]
        self.assertIn("score", job, "Score field missing from job data. AI ranking might have failed.")

if __name__ == "__main__":
    unittest.main()
