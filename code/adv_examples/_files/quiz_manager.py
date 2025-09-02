class QuizManager(object):
    def __init__(self, course):
        self.course = course

    def create_weekly_assignments(self, weeks=12, points=100):
        """Create weekly assignments for the semester"""
        for week in range(1, weeks + 1):
            due_date = datetime.now() + timedelta(weeks=week)
            
            assignment_data = {
                'name': f"Week {week} Assignment",
                'description': f"<p>Complete Week {week} readings and exercises</p>",
                'due_at': due_date.strftime("%Y-%m-%dT23:59:59Z"),
                'points_possible': points,
                'submission_types': ['online_upload'],
                'allowed_extensions': ['pdf', 'doc', 'docx']
            }
            
            try:
                assignment = self.course.create_assignment(assignment_data)
                print(f"✅ Created: Week {week} Assignment (Due: {due_date.strftime('%Y-%m-%d')})")
            except Exception as e:
                print(f"❌ Error creating Week {week} assignment: {e}")
    
    def upload_syllabus(self, syllabus_file_path):
        """Upload syllabus file and create a page"""
        try:
            # Upload file
            response = self.course.upload(syllabus_file_path)
            
            # Create syllabus page
            syllabus_content = f"""
            <h2>Course Syllabus</h2>
            <p>Please see the attached syllabus file for complete course information.</p>
            <p><a href="{response[1]['url']}">Download Syllabus PDF</a></p>
            """
            
            page_data = {
                'title': 'Syllabus',
                'body': syllabus_content,
                'published': True,
                'front_page': True
            }
            
            page = self.course.create_page(wiki_page=page_data)
            print(f"✅ Uploaded syllabus and created page")
            
        except Exception as e:
            print(f"❌ Error uploading syllabus: {e}")
    
    def create_quiz(self, title, questions_data, time_limit=60):
        """Create a quiz with multiple choice questions"""
        try:
            quiz_data = {
                'title': title,
                'quiz_type': 'assignment',
                'time_limit': time_limit,
                'allowed_attempts': 1,
                'scoring_policy': 'keep_highest'
            }
            
            quiz = self.course.create_quiz(quiz_data)
            
            # Add questions
            for q_data in questions_data:
                question_data = {
                    'question_name': q_data['question'][:50] + "...",
                    'question_text': q_data['question'],
                    'question_type': 'multiple_choice_question',
                    'points_possible': q_data.get('points', 1),
                    'answers': q_data['answers']
                }
                
                quiz.create_question(question=question_data)
            
            print(f"✅ Created quiz: {title} with {len(questions_data)} questions")
            return quiz
            
        except Exception as e:
            print(f"❌ Error creating quiz: {e}")