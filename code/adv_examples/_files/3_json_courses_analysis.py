import json
from typing import Dict, List, Any, Optional

class CourseDataAnalyzer:
    """
    A class to analyze course data stored in JSON format.
    
    This demonstrates:
    - File I/O operations
    - JSON data processing
    - Data filtering and searching
    - Error handling
    """
    
    def __init__(self):
        self.courses_data = {}
    
    def read_json_file(self, file_path: str) -> bool:
        """
        Read course data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            analyzer = CourseDataAnalyzer()
            success = analyzer.read_json_file("courses.json")
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.courses_data = json.load(file)
            print(f"Successfully loaded {len(self.courses_data)} courses from {file_path}")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in '{file_path}': {e}")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def find_courses_by_year_semester(self, year: str, semester: str) -> Dict[str, Any]:
        """
        Find all courses matching the specified year and semester.
        
        Args:
            year (str): The year to search for (e.g., "2024")
            semester (str): The semester to search for (e.g., "Spring", "Fall")
            
        Returns:
            Dict[str, Any]: Dictionary containing matching courses
            
        Example:
            courses = analyzer.find_courses_by_year_semester("2024", "Spring")
        """
        matching_courses = {}
        
        for course_id, course_info in self.courses_data.items():
            if (course_info.get("year") == year and 
                course_info.get("semester") == semester):
                matching_courses[course_id] = course_info
        
        return matching_courses
    
    def find_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a specific course by its ID.
        
        Args:
            course_id (str): The course ID to search for
            
        Returns:
            Optional[Dict[str, Any]]: Course information or None if not found
        """
        return self.courses_data.get(course_id)
    
    def get_all_years(self) -> List[str]:
        """
        Get a list of all unique years in the dataset.
        
        Returns:
            List[str]: Sorted list of years
        """
        years = set()
        for course_info in self.courses_data.values():
            if "year" in course_info:
                years.add(course_info["year"])
        return sorted(list(years))
    
    def get_all_semesters(self) -> List[str]:
        """
        Get a list of all unique semesters in the dataset.
        
        Returns:
            List[str]: List of semesters
        """
        semesters = set()
        for course_info in self.courses_data.values():
            if "semester" in course_info:
                semesters.add(course_info["semester"])
        return sorted(list(semesters))
    
    def print_courses(self, courses: Dict[str, Any]) -> None:
        """
        Print course information in a formatted way.
        
        Args:
            courses (Dict[str, Any]): Dictionary of courses to print
        """
        if not courses:
            print("No courses found.")
            return
        
        print(f"\nFound {len(courses)} course(s):")
        print("-" * 80)
        
        for course_id, course_info in courses.items():
            print(f"Course ID: {course_id}")
            print(f"  Name: {course_info.get('course_name', 'N/A')}")
            print(f"  Code: {course_info.get('course_code', 'N/A')}")
            print(f"  Title: {course_info.get('title', 'N/A')}")
            print(f"  Year: {course_info.get('year', 'N/A')}")
            print(f"  Semester: {course_info.get('semester', 'N/A')}")
            print("-" * 80)
    
    def generate_statistics(self) -> Dict[str, Any]:
        """
        Generate basic statistics about the course data.
        
        Returns:
            Dict[str, Any]: Statistics about the dataset
        """
        stats = {
            "total_courses": len(self.courses_data),
            "years": self.get_all_years(),
            "semesters": self.get_all_semesters(),
            "courses_by_year": {},
            "courses_by_semester": {}
        }
        
        # Count courses by year
        for year in stats["years"]:
            year_courses = self.find_courses_by_year_semester(year, "")
            # Count all courses in this year regardless of semester
            year_count = 0
            for course_info in self.courses_data.values():
                if course_info.get("year") == year:
                    year_count += 1
            stats["courses_by_year"][year] = year_count
        
        # Count courses by semester
        for semester in stats["semesters"]:
            semester_count = 0
            for course_info in self.courses_data.values():
                if course_info.get("semester") == semester:
                    semester_count += 1
            stats["courses_by_semester"][semester] = semester_count
        
        return stats

def main():
    """
    Main function demonstrating the CourseDataAnalyzer usage.
    This serves as a practical example for students.
    """
    print("=== Course Data JSON Analyzer Demo ===\n")
    
    # Create analyzer instance
    analyzer = CourseDataAnalyzer()
    
    analyzer.read_json_file("courses.json")
    print("1. Loading sample course data...")
    
    # Display basic statistics
    print("\n2. Dataset Statistics:")
    stats = analyzer.generate_statistics()
    print(f"   Total courses: {stats['total_courses']}")
    print(f"   Years available: {', '.join(stats['years'])}")
    print(f"   Semesters available: {', '.join(stats['semesters'])}")
    
    # Find courses by year and semester
    print("\n3. Example: Finding 2024 Spring courses")
    spring_2024_courses = analyzer.find_courses_by_year_semester("2025", "Fall")
    analyzer.print_courses(spring_2024_courses)
    
    # Find specific course by ID
    print("\n4. Example: Finding course by ID (81929)")
    specific_course = analyzer.find_course_by_id("81929")
    if specific_course:
        analyzer.print_courses({"81929": specific_course})
    else:
        print("Course not found.")
    
    # Trying to find non-existent data
    print("\n6. Example: Searching for non-existent data (2025 Summer)")
    summer_2025_courses = analyzer.find_courses_by_year_semester("2025", "Summer")
    analyzer.print_courses(summer_2025_courses)


if __name__ == "__main__":
    main()
