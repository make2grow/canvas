#!/usr/bin/env python3
"""
Canvas API Quick Reference - Essential Operations
A condensed script showing the most common Canvas API operations
"""

from turtle import title
from canvasapi import Canvas
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import markdown

def get_env_variables():
  load_dotenv()
  api_key = os.getenv('API_KEY')
  api_url = os.getenv('API_URL')
  return api_url, api_key

# 1. GET COURSE INFO
def get_course_info(course):
  name = course.name;
  students = list(course.get_users(enrollment_type=['student']))
  assignments = list(course.get_assignments())
  print(f"Students: {len(students)}")
  print(f"Assignments: {len(assignments)}")
  print(f"Course Name: {name}")

def t1_get_course_info_demo(course):
  print("\n1. 📊 COURSE INFORMATION")
  get_course_info(course)

# 2. CREATE ASSIGNMENT
def get_assignment_groups(course):
  print("\n2-1. 📑 ASSIGNMENT GROUPS")
  assignment_groups = course.get_assignment_groups()  # or through API endpoint /courses/:course_id/assignment_groups
  for group in assignment_groups:
    print(group.id, group.name)

def create_assignment(course, name, description, due_days_from_now=7, points=100):
  due_date = (datetime.now() + timedelta(days=due_days_from_now)).strftime("%Y-%m-%dT23:59:59Z")
  
  assignment_data = {
    'name': name,
    'description': description,
    'due_at': due_date,
    'points_possible': points,
    'submission_types': ['online_upload'],
    'allowed_extensions': ['pdf', 'doc', 'docx','zip'],
    'assignment_group_id': 237086, # exam
  }
  
  assignment = course.create_assignment(assignment_data)
  print(f"✅ Created: {name} (Due: {due_date[:10]})")
  return assignment
def t2_create_assignment_demo(course, name):
  print("\n2. 📝 CREATE ASSIGNMENT (Demo)")
  # get_assignment_groups(course)
  create_assignment(course, name, "Description of the assignment")

# 3. CREATE QUIZ

def create_simple_quiz(course, title, questions_list, time_limit=30):
  # Create quiz
  quiz_data = {
    'title': title,
    'quiz_type': 'assignment',
    'time_limit': time_limit,
    'allowed_attempts': 1
  }
  quiz = course.create_quiz(quiz_data)
  
  # Add questions
  for q in questions_list:
    question_data = {
      'question_name': q['question'][:50],
      'question_text': q['question'],
      'question_type': 'multiple_choice_question',
      'points_possible': 1,
      'answers': q['answers']
    }
    quiz.create_question(question=question_data)
  
  print(f"✅ Created quiz: {title} with {len(questions_list)} questions")
  return quiz

def t3_create_quiz_demo(course, title):
  print("\n3. ❓ CREATE QUIZ (Demo)")
  # Example quiz data
  sample_questions = [
    {
      'question': 'What is 2 + 2?',
      'answers': [
        {'answer_text': '3', 'answer_weight': 0},
        {'answer_text': '4', 'answer_weight': 100},  # Correct answer
        {'answer_text': '5', 'answer_weight': 0}
      ]
    }
  ]
  create_simple_quiz(course, title, sample_questions)

# 4. CREATE PAGE
def markdown_to_html(markdown_content):
  return markdown.markdown(markdown_content, \
       extensions=['extra', 'codehilite', 'toc'])

def create_course_page(course, title, content, is_front_page=False, published=False):
  page_data = {
    'title': title,
    'body': content,
    'published': published,
    'front_page': is_front_page
  }
  page = course.create_page(wiki_page=page_data)
  print(f"✅ Created page: {title}")
  return page

def t4_create_page_demo(course, title, content):
  print("\n4. 📄 CREATE PAGE (Demo)")
  html_content = markdown_to_html(content)
  create_course_page(course, title, html_content)

# 5. UPLOAD FILE
def display_folders(course):
  folders = course.get_folders()
  for folder in folders:
    print(f"Name: {folder.name}, ID: {folder.id}, Parent ID: {folder.parent_folder_id}, Hidden: {folder.hidden}")


def upload_file_to_default_course(course, file_path):
  try:
    response = course.upload(file_path)

    print(f"✅ Uploaded: {file_path}")
    return response[1]['url']  # Return file URL
  except Exception as e:
    print(f"❌ Upload failed: {e}")
    return None

def upload_file_to_course(course, file_path,
    folder_name="Lectures"):
  try:
    folders = course.get_folders()
    target_folder = None
    for folder in folders:
      if folder.name == folder_name: 
        target_folder = folder
        break
    
    if not target_folder:
      target_folder = course.create_folder(folder_name)
    
    # Upload file
    response = target_folder.upload(file_path)
    print(f"✅ Uploaded: {file_path}")
    return response
  except Exception as e:
    print(f"❌ Error: {e}")

def t5_upload_file_demo(course, file_path):
  print("\n5. 📁 UPLOAD FILE")
  #display_folders(course)
  path = upload_file_to_course(course, file_path)

  print(f"File uploaded to: {path}" if path else "File upload failed")

# 6. CREATE HOMEWORK

def assignment_exists(course, title):
    assignments = course.get_assignments()  # This fetches all assignments in the course
    for assignment in assignments:
        if assignment.name == title:
            return assignment.id
    return -1

def create_homework(course, title, description, due_date, points=100):
    assignment_data = {
        'name': title,
        'description': description,
        'due_at': due_date,  # Format: "2024-12-31T23:59:59Z"
        'points_possible': points,
        'submission_types': ['online_upload'],
        'allowed_extensions': ['pdf', 'doc', 'docx']
    }
    
    assignment = course.create_assignment(assignment_data)
    print(f"✅ Created assignment: {title}")
    return assignment

def t6_create_homework_demo(course, title):
    print("\n6. 📚 CREATE HOMEWORK (Demo)")
    id = assignment_exists(course, title)
    if id > 0:
        print(f"❌ Assignment '{title}' already exists")
        hw = course.get_assignment(id)
    hw = create_homework(course, title, "Homework description", "2024-12-31T23:59:59Z")
    print(hw)

# 7. DOWNLOAD SUBMISSIONS
def get_assignment_submission(course, assignment_name):
  # Find assignment
  target_assignment = None
  for assignment in course.get_assignments():
    if assignment.name == assignment_name:
      target_assignment = assignment
      break

  if not target_assignment:
    print(f"❌ Assignment '{assignment_name}' not found")
    return []

  # Get submissions
  submission = list(target_assignment.get_submissions())[0]
  return submission.__dict__

def download_assignment_submissions(course, assignment_name, download_folder="downloads"):
  # Find assignment
  target_assignment = None
  for assignment in course.get_assignments():
    if assignment.name == assignment_name:
      target_assignment = assignment
      break
  
  if not target_assignment:
    print(f"❌ Assignment '{assignment_name}' not found")
    return
  
  # Download submissions
  os.makedirs(download_folder, exist_ok=True)
  submissions = target_assignment.get_submissions()
  count = 0
  
  for submission in submissions:
    if submission.attachments:
      for attachment in submission.attachments:
        filename = attachment.filename if hasattr(attachment, 'filename') else f"file_{count}"
        student_name = getattr(submission, 'user_id', 'unknown_student')
        student_folder = os.path.join(download_folder, '') # f"student_{student_name}")
      
        print(f"  📄 Downloading: {student_name}:{filename}")
        file_path = os.path.join(student_folder, filename)
        attachment.download(file_path)
        count += 1
  
  print(f"✅ Would download {count} submissions to {download_folder}")

def t7_download_assignment_submissions_demo(course, assignment_name, download_folder="downloads"):
    print("\n6. 📥 DOWNLOAD SUBMISSIONS")
    res = get_assignment_submission(course, "HW1")
    #print(res)
    download_assignment_submissions(course, assignment_name, download_folder)

# 8. STUDENT ANALYTICS
def show_course_analytics(course):
  students = list(course.get_users(enrollment_type=['student']))
  assignments = list(course.get_assignments())
  
  print(f"📊 Course Analytics:")
  print(f"   Total students: {len(students)}")
  print(f"   Total assignments: {len(assignments)}")
  
  # Show submission rates for recent assignments
  assignments = sorted(course.get_assignments(), key=lambda a: (a.due_at or ""), reverse=True)
  recent_assignments = assignments[:3] if len(assignments) >= 3 else assignments
  for assignment in recent_assignments:
    submissions = list(assignment.get_submissions())
    submitted_count = sum(1 for s in submissions if s.submitted_at)
    percentage = (submitted_count / len(students)) * 100 if students else 0
    print(f"   {assignment.name}: {submitted_count}/{len(students)} ({percentage:.1f}%)")

def t8_show_course_analytics_demo(course):
  print("\n8. 📈 STUDENT ANALYTICS")
  show_course_analytics(course)

def main():
  # Setup
  url, key = get_env_variables()
  canvas = Canvas(url, key)
  course_id = 81929 # "Cross-Platform Development (2025 Fall full term) ASE-456-001-2026-010",
  course = canvas.get_course(course_id)

  print(f"Working with course: {course.name}")
  print("=" * 50)

  #t1_get_course_info_demo(course)
  #t2_create_assignment_demo(course, "Example Assignment")
  #t3_create_quiz_demo(course, "Example Quiz")
  #t4_create_page_demo(course, "Example Course Information Markdown", "## Course Syllabus\nWelcome to the course!") 
  #t5_upload_file_demo(course, "./img/code.png")
  #t6_create_homework_demo(course, "Example Homework")
  #t7_download_assignment_submissions_demo(course, "HW1", download_folder="downloads")
  t8_show_course_analytics_demo(course)

if __name__ == "__main__":
  main()
