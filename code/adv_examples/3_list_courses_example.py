"""
Canvas API Course Mapper

This script demonstrates how to:
1. Connect to Canvas API using authentication
2. Retrieve course data from the API
3. Process JSON responses
4. Create a mapping of course numbers to course names
5. Handle errors gracefully

Educational concepts covered:
- REST API interactions
- HTTP authentication
- JSON data parsing
- Dictionary data structures
- Error handling and logging
- Environment variables for security
"""

from dotenv import load_dotenv
import requests
import json
import os
from typing import Dict, List, Optional
import logging
import re

# Configure logging for educational purposes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
filename='canvas_mapper.log'  # Add this line if you want to log to a file
logger = logging.getLogger(__name__)


class CanvasCourseMapper:
    """
    A class to interact with Canvas API and create course mappings.
    
    This demonstrates object-oriented programming concepts and encapsulation.
    """
    
    def __init__(self, canvas_url: str, api_token: str):
        """
        Initialize the Canvas API client.
        
        Args:
            canvas_url (str): Your Canvas instance URL (e.g., 'https://youruniversity.instructure.com')
            api_token (str): Your Canvas API token
        """
        self.canvas_url = canvas_url.rstrip('/')  # Remove trailing slash if present
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Canvas API client initialized")
    
    def get_all_courses(self, per_page: int = 100) -> List[Dict]:
        """
        Retrieve all courses from Canvas API.
        
        Args:
            per_page (int): Number of courses to retrieve per API call
            
        Returns:
            List[Dict]: List of course dictionaries
        """
        courses = []
        page = 1
        
        while True:
            # Construct API endpoint URL
            url = f"{self.canvas_url}/api/v1/courses"
            
            # Parameters for the API request
            params = {
                'per_page': per_page,
                'page': page,
                'include[]': ['course_code', 'name', 'term'],  # Include additional course info
                'state[]': ['available', 'completed', 'unpublished']  # Include different course states
            }
            
            try:
                logger.info(f"Fetching page {page} of courses...")
                response = requests.get(url, headers=self.headers, params=params)
                
                # Check if request was successful
                response.raise_for_status()
                
                # Parse JSON response
                page_courses = response.json()
                
                # If no courses returned, we've reached the end
                if not page_courses:
                    break
                
                courses.extend(page_courses)
                page += 1
                
                logger.info(f"Retrieved {len(page_courses)} courses from page {page-1}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching courses: {e}")
                break
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON response: {e}")
                break
        
        logger.info(f"Total courses retrieved: {len(courses)}")
        return courses
    
    def create_course_mapping(self, courses) -> Dict[str, Dict[str, str]]:
        """
        Create a mapping with course_id as key and course details as dictionary.
        Extract year and semester from course_name.
        """
        def _parse_year_semester_from_name(course_name):
            """
            Parse course title, year and semester from course name.
            
            Examples: 
            - "Advanced Programming Workshop (2018 Fall)" -> ("Advanced Programming Workshop", "2018", "Fall")
            - "Data Structures Spring 2019" -> ("Data Structures", "2019", "Spring")
            - "Calculus II (Fall 2020)" -> ("Calculus II", "2020", "Fall")
            - "Machine Learning 2021 Summer Session" -> ("Machine Learning", "2021", "Summer")
            
            Args:
                course_name (str): The full course name string
                
            Returns:
                tuple: (course_title, year, semester)
            """
            if not course_name:
                return "Unknown", "Unknown", "Unknown"
            
            # Initialize defaults
            title = "Unknown"
            year = "Unknown"
            semester = "Unknown"
            
            # Extract year (4-digit number starting with 20)
            year_match = re.search(r'\b(20\d{2})\b', course_name)
            if year_match:
                year = year_match.group(1)
            
            # Extract semester (case insensitive)
            course_name_lower = course_name.lower()
            semester_match = None
            
            if re.search(r'\bfall\b', course_name_lower):
                semester = "Fall"
                semester_match = re.search(r'\bfall\b', course_name_lower)
            elif re.search(r'\bspring\b', course_name_lower):
                semester = "Spring"
                semester_match = re.search(r'\bspring\b', course_name_lower)
            elif re.search(r'\bsummer\b', course_name_lower):
                semester = "Summer"
                semester_match = re.search(r'\bsummer\b', course_name_lower)
            
            # Extract title by finding where year/semester information starts
            title_end_pos = len(course_name)  # Default to full string
            
            # Find the earliest position of year or semester
            if year_match:
                title_end_pos = min(title_end_pos, year_match.start())
            
            if semester_match:
                title_end_pos = min(title_end_pos, semester_match.start())
            
            # Extract title and clean it up
            if title_end_pos < len(course_name):
                title = course_name[:title_end_pos].strip()
                
                # Remove trailing punctuation like parentheses, commas, etc.
                title = re.sub(r'[\(\[\{,\-\s]+$', '', title).strip()
                
                # If title is empty after cleaning, use original course name
                if not title:
                    title = course_name.strip()
            else:
                title = course_name.strip()
            
            return title, year, semester

        course_map = {}
        
        for course in courses:
            # Extract basic course information
            course_id = str(course.get('id', 'Unknown'))
            course_name = course.get('name', 'Unnamed Course')
            course_code = course.get('course_code', 'N/A')
            
            # Extract year and semester from course_name
            title, year, semester = _parse_year_semester_from_name(course_name)
            
            # Create course dictionary
            course_details = {
                "course_name": course_name,
                "course_code": course_code,
                "title": title,
                "year": year,
                "semester": semester
            }
            
            course_map[course_id] = course_details
        
        return course_map

    
    def save_mapping_to_file(self, course_map: Dict[str, str], filename: str = 'course_mapping.json'):
        """
        Save the course mapping to a JSON file.
        
        Args:
            course_map (Dict[str, str]): Course mapping dictionary
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(course_map, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Course mapping saved to {filename}")
            
        except IOError as e:
            logger.error(f"Error saving to file: {e}")
    
    def print_course_mapping(self, course_map: Dict[str, str], limit: Optional[int] = None):
        """
        Print the course mapping in a readable format.
        
        Args:
            course_map (Dict[str, str]): Course mapping dictionary
            limit (Optional[int]): Limit number of courses to display
        """
        print("\n" + "="*80)
        print("CANVAS COURSE MAPPING")
        print("="*80)
        print(f"{'Course Code':<20} | {'Course Name'}")
        print("-"*80)
        
        items = list(course_map.items())
        if limit:
            items = items[:limit]
        
        for course_code, course_name in items:
            # Truncate long course names for better display
            display_name = course_name[:50] + "..." if len(course_name) > 50 else course_name
            print(f"{course_code:<20} | {display_name}")
        
        if limit and len(course_map) > limit:
            print(f"\n... and {len(course_map) - limit} more courses")
        
        print(f"\nTotal courses: {len(course_map)}")


def load_config_from_environment() -> tuple:
    """
    Load Canvas configuration from environment variables.
    This demonstrates secure credential handling.
    
    Returns:
        tuple: (canvas_url, api_token)
    """
    load_dotenv()
    canvas_url = os.getenv('API_URL')
    api_token = os.getenv('API_KEY')
    
    if not canvas_url:
        raise ValueError("API_URL environment variable is required")
    
    if not api_token:
        raise ValueError("API_KEY environment variable is required")
    
    return canvas_url, api_token


def main():
    """
    Main function to demonstrate the Canvas course mapping workflow.
    """
    try:
        print("Canvas Course Mapper - Educational Example")
        print("==========================================")
        
        # Method 1: Load from environment variables (recommended for security)
        try:
            canvas_url, api_token = load_config_from_environment()
            logger.info("Loaded configuration from environment variables")
        except ValueError as e:
            logger.error(f"Environment variable not found: {e}")
            raise ValueError("Both Canvas URL and API token are required")
        
        # Initialize the Canvas mapper
        mapper = CanvasCourseMapper(canvas_url, api_token)
        
        # Retrieve courses from Canvas
        print("\nFetching courses from Canvas...")
        courses = mapper.get_all_courses()
        
        if not courses:
            print("No courses found or error occurred during retrieval.")
            return
        
        # Create course mapping
        print("Creating course mapping...")
        course_map = mapper.create_course_mapping(courses)
        
        # Display results
        mapper.print_course_mapping(course_map, limit=20)  # Show first 20 courses
        
        # Save to file
        save_option = input("\nSave mapping to JSON file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter filename (press Enter for 'courses.json'): ").strip()
            if not filename:
                filename = 'courses.json'
            
            mapper.save_mapping_to_file(course_map, filename)
        
        print("\nScript completed successfully!")
        return courses
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"\nError: {e}")
        print("Please check your Canvas URL and API token.")


if __name__ == "__main__":
    courses = main()

