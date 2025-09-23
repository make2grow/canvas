import re

def get_courses(canvas, year, semester):
    SEMESTER_PATTERN = re.compile(r'\((\d{4})\s+(\w+)(?:\s+[^)]*)?\)', re.IGNORECASE)        
    filtered_courses = []

    for course in canvas.get_courses():
        course_name = getattr(course, 'name', '')
        match = SEMESTER_PATTERN.search(course_name)
        if match:
            # Extract year and semester from capture groups
            course_year = match.group(1)
            course_semester = match.group(2)
            # Case-insensitive comparison for semester
            if (course_year == year and 
                course_semester.lower() == semester.lower()):
                filtered_courses.append(course)
    return filtered_courses