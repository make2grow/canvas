#!/usr/bin/env python3
"""
Canvas API with Markdown Support
Enhanced example showing how to use Markdown for content creation
"""

from canvasapi import Canvas
import os
from dotenv import load_dotenv
import markdown
from datetime import datetime, timedelta

class CanvasCourseManager:
    def __init__(self):
        load_dotenv()
        self.canvas = Canvas(
            os.getenv("CANVAS_API_URL"), 
            os.getenv("CANVAS_API_TOKEN")
        )
        self.course = self.canvas.get_course(int(os.getenv("COURSE_ID")))
    
    def markdown_to_html(self, markdown_content):
        """Convert Markdown to HTML for Canvas"""
        return markdown.markdown(
            markdown_content, 
            extensions=['extra', 'codehilite', 'toc']
        )
    
    def create_page_from_markdown(self, title, markdown_content, front_page=False):
        """Create a Canvas page using Markdown content"""
        try:
            # Convert Markdown to HTML
            html_content = self.markdown_to_html(markdown_content)
            
            page_data = {
                'title': title,
                'body': html_content,
                'editing_roles': 'teachers',
                'published': True,
                'front_page': front_page
            }
            
            page = self.course.create_page(wiki_page=page_data)
            print(f"✅ Created page: {title}")
            return page
            
        except Exception as e:
            print(f"❌ Error creating page: {e}")
    
    def create_assignment_from_markdown(self, title, markdown_description, due_date, points=100):
        """Create assignment with Markdown description"""
        try:
            # Convert Markdown description to HTML
            html_description = self.markdown_to_html(markdown_description)
            
            assignment_data = {
                'name': title,
                'description': html_description,
                'due_at': due_date,
                'points_possible': points,
                'submission_types': ['online_upload'],
                'allowed_extensions': ['pdf', 'doc', 'docx', 'txt', 'md']
            }
            
            assignment = self.course.create_assignment(assignment_data)
            print(f"✅ Created assignment: {title}")
            return assignment
            
        except Exception as e:
            print(f"❌ Error creating assignment: {e}")
    
    def load_markdown_file(self, file_path):
        """Load Markdown content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading markdown file: {e}")
            return None

# Example usage with Markdown
if __name__ == "__main__":
    manager = CanvasCourseManager()
    
    # Example 1: Syllabus using Markdown
    syllabus_markdown = """
# Course Syllabus

## Course Description
This course covers fundamental concepts in computer science, including:
- Programming fundamentals
- Data structures and algorithms
- Software engineering principles

## Learning Objectives
By the end of this course, students will be able to:

1. **Understand** basic programming concepts
2. **Apply** theoretical knowledge to practical problems
3. **Analyze** complex algorithms and data structures
4. **Design** efficient software solutions

## Course Schedule

| Week | Topic | Assignment |
|------|-------|------------|
| 1 | Introduction to Programming | Homework 1 |
| 2 | Data Structures | Homework 2 |
| 3 | Algorithms | Project 1 |

## Grading Policy

- **Homework**: 40%
- **Projects**: 35%
- **Midterm**: 12.5%
- **Final**: 12.5%

## Important Notes

> **Note**: All assignments must be submitted through Canvas before the due date.

### Code Submission Format
```python
# Example: Hello World program
def hello_world():
    print("Hello, World!")
    return "Success"
```

## Contact Information
- **Email**: professor@university.edu
- **Office Hours**: MWF 2:00-3:00 PM
- **Office**: Science Building Room 123
"""
    
    # Create syllabus page
    # manager.create_page_from_markdown("Course Syllabus", syllabus_markdown, front_page=True)
    
    # Example 2: Assignment with Markdown description
    assignment_markdown = """
# Programming Assignment 1: Hello World

## Objective
Create your first Python program that demonstrates basic programming concepts.

## Requirements

### Part 1: Basic Output
1. Create a Python file named `hello.py`
2. Write a function that prints "Hello, World!"
3. Include proper documentation

### Part 2: User Input
1. Modify your program to ask for the user's name
2. Greet the user personally
3. Handle edge cases (empty input, etc.)

### Example Code Structure
```python
def greet_user():
    name = input("What's your name? ")
    if name.strip():
        print(f"Hello, {name}!")
    else:
        print("Hello, Anonymous!")

if __name__ == "__main__":
    greet_user()
```

## Submission Guidelines

- **Format**: Submit as a `.py` file
- **Naming**: Use `lastname_firstname_hw1.py`
- **Comments**: Include your name and date at the top

## Grading Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| Functionality | 40 | Program runs without errors |
| Code Quality | 30 | Clean, readable code |
| Documentation | 20 | Proper comments and docstrings |
| Creativity | 10 | Going beyond requirements |

**Total**: 100 points

## Due Date
**Friday, March 15, 2024 at 11:59 PM**

## Questions?
Post questions in the Canvas discussion forum or visit office hours.
"""
    
    # Create assignment with Markdown
    due_date = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%dT23:59:59Z")
    # manager.create_assignment_from_markdown(
    #     "Programming Assignment 1", 
    #     assignment_markdown, 
    #     due_date, 
    #     points=100
    # )
    
    # Example 3: Load Markdown from external file
    print("Example Markdown content created!")
    print("Uncomment the function calls above to create actual Canvas content.")
    
    # Show the HTML conversion
    print("\n" + "="*50)
    print("MARKDOWN CONVERSION PREVIEW:")
    print("="*50)
    html_output = manager.markdown_to_html(assignment_markdown)
    print("Markdown converted to HTML successfully!")
    print(f"HTML length: {len(html_output)} characters")
