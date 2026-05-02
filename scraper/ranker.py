"""
Gemini-powered job ranker
Ranks jobs based on CV and Profile configuration
"""
import os
import yaml
import google.generativeai as genai
from typing import List, Dict
import json
from dotenv import load_dotenv

load_dotenv()

class JobRanker:
    def __init__(self):
        # Initialize Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ Warning: GOOGLE_API_KEY not found in environment. Ranking will be skipped.")
            self.model = None
            return

        genai.configure(api_key=api_key)

        # Try to find an available model
        try:
            available_models = [m.name for m in genai.list_models()]
            print(f"    Available models: {available_models}")
            
            if 'models/gemini-1.5-flash' in available_models:
                model_name = 'gemini-1.5-flash'
            elif 'models/gemini-1.5-pro' in available_models:
                model_name = 'gemini-1.5-pro'
            elif 'models/gemini-pro' in available_models:
                model_name = 'gemini-pro'
            else:
                model_name = 'gemini-pro' # Fallback
                
            print(f"    Selected model: {model_name}")
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            print(f"    Error listing models, falling back to gemini-pro: {e}")
            self.model = genai.GenerativeModel('gemini-pro')
        
        # Load profile and CV
        self.profile = self._load_profile()
        self.cv = self._load_cv()

    def _load_profile(self) -> Dict:
        profile_path = os.path.join(os.path.dirname(__file__), "..", "config", "profile.yml")
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return {}

    def _load_cv(self) -> str:
        cv_path = os.path.join(os.path.dirname(__file__), "..", "cv.md")
        try:
            with open(cv_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading CV: {e}")
            return ""

    def rank_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Rank a list of jobs using Gemini"""
        if not self.model or not jobs:
            return [{**job, "score": 3} for job in jobs] # Default score if no model

        ranked_jobs = []
        
        # Process in batches to save tokens and time
        batch_size = 10
        for i in range(0, len(jobs), batch_size):
            batch = jobs[i:i+batch_size]
            print(f"    Ranking batch {i//batch_size + 1}/{(len(jobs)-1)//batch_size + 1}...")
            
            try:
                scores = self._get_batch_scores(batch)
                for job, score in zip(batch, scores):
                    job["score"] = score
                    ranked_jobs.append(job)
            except Exception as e:
                print(f"    Error ranking batch: {e}")
                for job in batch:
                    job["score"] = 3
                    ranked_jobs.append(job)
        
        return ranked_jobs

    def _get_batch_scores(self, batch: List[Dict]) -> List[int]:
        """Get scores for a batch of jobs from Gemini"""
        jobs_text = "\n---\n".join([
            f"ID: {idx}\nTitle: {j['title']}\nCompany: {j['company']}\nLocation: {j['location']}\nDescription: {j.get('description', '')}"
            for idx, j in enumerate(batch)
        ])

        prompt = f"""
        You are a career assistant for Heena Kauser, an MBA graduate in Business Analytics.
        Your task is to rank job listings on a scale of 1 to 5 based on their fit with her profile and CV.

        CANDIDATE PROFILE:
        {yaml.dump(self.profile)}

        CANDIDATE CV:
        {self.cv}

        JOB LISTINGS TO RANK:
        {jobs_text}

        CRITERIA:
        5: Perfect fit - Matches target roles, location (Bangalore/Remote), and candidate's superpowers.
        4: Good fit - Matches target roles and location, but might require slightly more experience or different industry.
        3: Average fit - Relevant but not a top choice.
        2: Poor fit - Major mismatch in role or requirements.
        1: Irrelevant - Not suitable for an MBA graduate.

        RESPONSE FORMAT:
        Return ONLY a JSON array of integers representing the scores for each job in order.
        Example: [5, 3, 4, 2, 1]
        """

        try:
            response = self.model.generate_content(prompt)
            # Clean response text in case it has markdown markers
            text = response.text.strip().replace("```json", "").replace("```", "")
            scores = json.loads(text)
            
            # Ensure we got the right number of scores
            if len(scores) != len(batch):
                return [3] * len(batch)
                
            return [max(1, min(5, int(s))) for s in scores]
        except Exception as e:
            print(f"      Gemini Error: {e}")
            return [3] * len(batch)

if __name__ == "__main__":
    # Test script
    ranker = JobRanker()
    test_jobs = [{"title": "Business Analyst", "company": "Google", "location": "Bangalore"}]
    print(ranker.rank_jobs(test_jobs))
