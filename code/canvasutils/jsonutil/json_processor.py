# Handle both relative and absolute imports for testing
try:
    from . import json_util
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    import json_util

import re
from typing import List, Dict, Any

class JsonProcessor(object):
    
    # 🔧 CONSOLIDATED REGEX PATTERN - Single source of truth!
    # \( - literal opening parenthesis
    # (\d{4}) - capture group 1: exactly 4 digits (year)
    # \s+ - one or more whitespace characters
    # (\w+) - capture group 2: one or more word characters (semester)
    # (?:\s+[^)]*)? - optional non-capturing group for additional text
    # \) - literal closing parenthesis
    SEMESTER_PATTERN = re.compile(r'\((\d{4})\s+(\w+)(?:\s+[^)]*)?\)', re.IGNORECASE)

    def __init__(self, file_name):
        self.file_name = file_name
        self.courses: List[Dict[Any, Any]] = json_util.load_json_file(file_name) 
        self.semester_courses: Dict[str, List[Dict[Any, Any]]] = self.analyze_available_semesters()

    def get_courses(self) -> List[Dict[Any, Any]]:
        return self.courses
    
    def get_semester_courses(self) -> Dict[str, List[Dict[Any, Any]]]:
        return self.semester_courses

    def filter_courses_regex(self, year: str, semester: str) -> List[Dict[Any, Any]]:
        """
        Filter courses using the consolidated class regex pattern.
        Now uses SEMESTER_PATTERN and checks captured groups for exact matching.
        
        Args:
            year: Target year (e.g., "2025")
            semester: Target semester (e.g., "Fall", "Spring")
        
        Returns:
            List of filtered courses
        """
        filtered_courses = []
        
        for course in self.courses:
            course_name = course.get('name', '')
            match = self.SEMESTER_PATTERN.search(course_name)
            if match:
                # Extract year and semester from capture groups
                course_year = match.group(1)
                course_semester = match.group(2)
                
                # Case-insensitive comparison for semester
                if (course_year == year and 
                    course_semester.lower() == semester.lower()):
                    filtered_courses.append(course)
        
        return filtered_courses

    def analyze_available_semesters(self) -> Dict[str, List[Dict[Any, Any]]]:
        """
        Analyze what year/semester combinations are available in the dataset.
        Now uses the consolidated SEMESTER_PATTERN instead of creating a duplicate.

        Returns:
            Dictionary with "year semester" as key and list of courses as value
            Example: {"2025 Fall": [course1, course2], "2024 Spring": [course3]}
        """
        semester_courses = {}
    
        for course in self.courses:
            course_name = course.get('name', '')
            match = self.SEMESTER_PATTERN.search(course_name)
            if match:
                year = match.group(1)      # First capture group: year (e.g., "2025")
                semester = match.group(2)  # Second capture group: semester (e.g., "Fall")
                year_semester = f"{year} {semester}"  # Combine: "2025 Fall"
                
                # Initialize list if key doesn't exist, then append
                if year_semester not in semester_courses:
                    semester_courses[year_semester] = []
                semester_courses[year_semester].append(course)
        
        return semester_courses

    def extract_semester_info(self, course_name: str) -> tuple[str, str] | None:
        """
        Helper method to extract year and semester from a course name.
        Uses the consolidated SEMESTER_PATTERN.
        
        Args:
            course_name: The course name string
            
        Returns:
            Tuple of (year, semester) if found, None otherwise
        """
        match = self.SEMESTER_PATTERN.search(course_name)
        if match:
            return (match.group(1), match.group(2))
        return None

    def get_courses_by_semester(self, year: str, semester: str) -> List[Dict[Any, Any]]:
        """
        Get courses by year and semester from the pre-computed semester map.
        This is more efficient than regex filtering for repeated queries.
        
        Args:
            year: Target year (e.g., "2025")
            semester: Target semester (e.g., "Fall", "Spring")
            
        Returns:
            List of courses for the specified semester
        """
        year_semester = f"{year} {semester}"
        return self.semester_courses.get(year_semester, [])

    def print_course_summary(self, title: str, count=10):
        """
        Print a summary of courses.
        
        Args:
            title: Title for the summary
            count: Number of courses to show in detail
        """
        print(f"\n=== {title} ===")
        print(f"Total courses: {len(self.courses)}")
        
        if self.courses:
            print("\nSample courses:")
            for i, course in enumerate(self.courses[:count]):
                print(f"  {i+1}. {course.get('name', 'No name')}")
                print(f"     ID: {course.get('id')}")
                print(f"     Code: {course.get('course_code', 'N/A')}")
            
            if len(self.courses) > count:
                print(f"  ... and {len(self.courses) - count} more courses")

    def print_semester_summary(self, max_semesters=10):
        """
        Print a summary of available semesters.
        
        Args:
            max_semesters: Maximum number of semesters to display
        """
        print(f"\n=== Available Semesters ===")
        print(f"Total semesters found: {len(self.semester_courses)}")
        
        sorted_semesters = sorted(self.semester_courses.items())
        for i, (year_semester, courses_list) in enumerate(sorted_semesters[:max_semesters]):
            print(f"  {year_semester}: {len(courses_list)} courses")
        
        if len(sorted_semesters) > max_semesters:
            print(f"  ... and {len(sorted_semesters) - max_semesters} more semesters")

# Test section - only runs when file is executed directly
if __name__ == "__main__":
    print("Testing JsonProcessor directly...")
    print("🔧 This version uses CONSOLIDATED regex patterns - no duplication!")
    
    # Test with the courses.json file
    try:
        # Change to the correct directory
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(os.path.dirname(script_dir))
        courses_file = os.path.join(parent_dir, 'courses.json')
        
        if os.path.exists(courses_file):
            print(f"Found courses file: {courses_file}")
            processor = JsonProcessor(courses_file)
            
            # Test the consolidated pattern
            processor.print_semester_summary()
            
            # Test both filtering methods
            print(f"\n=== Testing Both Filtering Methods ===")
            
            # Method 1: Direct from semester map (fastest)
            fall_2025_map = processor.get_courses_by_semester("2025", "Fall")
            print(f"From semester map: {len(fall_2025_map)} courses for 2025 Fall")
            
            # Method 2: Regex filtering (uses consolidated pattern)
            fall_2025_regex = processor.filter_courses_regex("2025", "Fall")
            print(f"From regex filter: {len(fall_2025_regex)} courses for 2025 Fall")
            
            # They should be the same!
            if len(fall_2025_map) == len(fall_2025_regex):
                print("✅ Both methods return the same count - consolidation successful!")
            else:
                print("❌ Methods return different counts - check implementation")
            
            # Test helper method
            if processor.courses:
                sample_course = processor.courses[0]
                semester_info = processor.extract_semester_info(sample_course.get('name', ''))
                if semester_info:
                    year, semester = semester_info
                    print(f"\nSample extraction: '{sample_course.get('name', '')}' -> {year} {semester}")
            
        else:
            print(f"Courses file not found at: {courses_file}")
            print("Available files in parent directory:")
            for file in os.listdir(parent_dir):
                if file.endswith('.json'):
                    print(f"  {file}")
                    
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
