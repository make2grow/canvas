from canvas import JsonProcessor
import canvas.utils.json_util as json_util

def main():
    file_name = 'courses.json'

    # Load and process courses using the JsonProcessor class
    print("Loading courses data...")
    processor = JsonProcessor(file_name)
    
    courses = processor.get_courses()
    semester_courses = processor.get_semester_courses()
    
    print(f"Total courses: {len(courses)}")
    
    # Method 1: Get 2025 Fall courses from the semester map
    fall_2025_courses = semester_courses.get("2025 Fall", [])
    
    print(f"\nFound {len(fall_2025_courses)} courses for 2025 Fall")
    
    # Show some examples
    if fall_2025_courses:
        print("\n2025 Fall Courses:")
        for course in fall_2025_courses:
            print(f"  - {course['name']}")
            print(f"    ID: {course['id']}")
    else:
        print("No 2025 Fall courses found in the dataset")
        
        # Let's see what semesters are available for demonstration
        print("\nAvailable semesters:")
        for year_semester, courses_list in sorted(semester_courses.items()):
            print(f"  {year_semester}: {len(courses_list)} courses")
    
    # Method 2: Use the regex filter method
    fall_2025_regex = processor.filter_courses_regex("2025", "Fall")
    print(f"\nUsing regex filter - 2025 Fall courses: {len(fall_2025_regex)}")
    
    # Demonstrate with existing data
    fall_2020_courses = semester_courses.get("2020 Fall", [])
    print(f"\nFor comparison - 2020 Fall courses: {len(fall_2020_courses)}")
    if fall_2020_courses:
        for course in fall_2020_courses[:4]:  # Show first 4
            print(f"  - {course['name']}")
            print(f"    ID: {course['id']}")
            print(f"    Code: {course.get('course_code', 'N/A')}")

    json_util.store_json_object(fall_2025_courses, 'fall_2025_courses.json')    
if __name__ == "__main__":
    main()
