# Canvas API Course Management
# Example script for professors

import os
from dotenv import load_dotenv
import requests

class CanvasManager:
    def __init__(self):
        self.load_environment()

    def get_canvas_instance(self):
        """Returns the Canvas instance"""
        return self.canvas

    def load_environment(self):
        """Check if .env file exists and has required variables"""
        if not os.path.exists('.env'):
            print("❌ .env file not found!")
            print("   Please copy .env.template to .env and fill in your details")
            return False
        
        load_dotenv()
        
        required_vars = ['API_KEY', 'API_URL']
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
        
        if missing_vars:
            print("❌ Missing or placeholder values in .env file:")
            for var in missing_vars:
                print(f"   - {var}")
            return False

        self.headers = {
            'Authorization': f'Bearer {os.getenv(required_vars[0])}',
            'Content-Type': 'application/json'
        }
        self.url = f'{os.getenv(required_vars[1])}/api/v1'

        print("✅ Environment variables configured")
        return True

    def make_request(self, endpoint, method='GET', data=None, params=None):
        """Make a request to the Canvas API and handle pagination"""
        url = f"{self.url}/{endpoint}"
        results = []

        while url:
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers, params=params)
                elif method == 'POST':
                    response = requests.post(url, headers=self.headers, json=data)
                else:
                    raise ValueError("Invalid HTTP method")

                response.raise_for_status()
                results.extend(response.json())

                # Look for pagination in Link header
                # link: 
                # <https://nku.instructure.com/api/v1/courses?page=2&per_page=10>; rel="next",
                if 'next' in response.links:
                    url = response.links['next']['url'] # python parses the link
                    params = None  # only needed for the first request
                else:
                    url = None
            except Exception as e:
                print(f"❌ Error making request to {url}: {e}")
                break

        return results

    def get_all_courses_json(self):
        """Fetch all courses and return as JSON"""
        courses = self.make_request('courses')
        return courses
    