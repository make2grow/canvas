from canvasapi import Canvas
from dotenv import load_dotenv
import os
import json
from utils.files import to_safe_filename, make_serializable
from utils.courses import get_courses

def main():
    load_dotenv()
    canvas = Canvas(os.getenv("API_URL"), os.getenv("API_KEY"))

    year = "2025"
    semester = "Fall"
    filtered_courses = get_courses(canvas, year, semester)
    serializable_courses = []
    for course in filtered_courses:
        print(f"Course Name: {course.name}")
        print("=== Course Data (filtered) ===")
        serializable_course = make_serializable(course)
        serializable_courses.append(serializable_course)

    filename = to_safe_filename(f"{year}_{semester}_courses") + ".json"
    with open(filename, "w") as f:
        json.dump(serializable_courses, f, indent=2)

if __name__ == "__main__":
    main()
