from canvasapi import Canvas

API_URL = "https://YOUR_CANVAS_URL"      # e.g. "https://canvas.instructure.com"
API_KEY = "YOUR_ACCESS_TOKEN"
COURSE_ID = 123456                       # replace with your course ID

# Connect to Canvas
canvas = Canvas(API_URL, API_KEY)

# Get the course
course = canvas.get_course(COURSE_ID)

# --------------------------
# 1. Create a new quiz
# --------------------------
new_quiz = course.create_quiz({
    "title": "My First Quiz",
    "description": "This quiz was created via canvasapi.",
    "quiz_type": "assignment",       # other types: 'practice_quiz', 'graded_survey', 'survey'
    "published": False,              # keep unpublished until ready
    "time_limit": 30,                # in minutes
    "allowed_attempts": 2,           # students can attempt twice
    "shuffle_answers": True,
    "points_possible": 10
})

print(f"Created quiz: {new_quiz.title} (ID: {new_quiz.id})")

# --------------------------
# 2. Add questions
# --------------------------
new_question = new_quiz.create_question({
    "question_name": "Simple Math",
    "question_text": "What is 5 + 7?",
    "question_type": "multiple_choice_question",
    "points_possible": 5,
    "answers": [
        {"answer_text": "10", "weight": 0},
        {"answer_text": "11", "weight": 0},
        {"answer_text": "12", "weight": 100},  # correct
        {"answer_text": "13", "weight": 0}
    ]
})

print(f"Added question: {new_question.question_text}")

# --------------------------
# 3. Retrieve & inspect quiz
# --------------------------
quiz = course.get_quiz(new_quiz.id)
print(f"Quiz title: {quiz.title}")
print(f"Due at: {quiz.due_at}")
print(f"Points possible: {quiz.points_possible}")

# --------------------------
# 4. List all questions
# --------------------------
for q in quiz.get_questions():
    print(f"Q{q.id}: {q.question_text}")