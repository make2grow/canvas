from .canvas_manager import CanvasManager

class CourseManager:
    def __init__(self, course_id):
        self.course_id = course_id
        self.canvas_manager = CanvasManager()
        self.course = self.canvas_manager.get_course_object(course_id)

    def get_canvas_instance(self):
        return self.canvas_manager.get_canvas_instance()

    def get_course_info(self):
        """Display basic course information"""
        print(f"Course: {self.course.name}")
        print(f"Course Code: {self.course.course_code}")
        print(f"Course ID: {self.course.id}")
        
        # Count students
        students = list(self.course.get_users(enrollment_type=['student']))
        print(f"Students enrolled: {len(students)}")
        print(students[0])
    
    
    def download_submissions(self, assignment_name, download_folder="submissions"):
        """Download all submissions for an assignment"""
        try:
            # Find assignment by name
            assignments = self.course.get_assignments()
            target_assignment = None
            
            for assignment in assignments:
                if assignment.name == assignment_name:
                    target_assignment = assignment
                    break
            
            if not target_assignment:
                print(f"❌ Assignment '{assignment_name}' not found")
                return
            
            # Create download folder
            os.makedirs(download_folder, exist_ok=True)
            
            # Download submissions
            submissions = target_assignment.get_submissions()
            downloaded_count = 0
            
            for submission in submissions:
                if submission.attachments:
                    student = self.course.get_user(submission.user_id)
                    student_folder = os.path.join(download_folder, f"{student.name}_{student.id}")
                    os.makedirs(student_folder, exist_ok=True)
                    
                    for attachment in submission.attachments:
                        file_url = attachment['url']
                        file_name = attachment['filename']
                        
                        response = requests.get(file_url)
                        file_path = os.path.join(student_folder, file_name)
                        
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        downloaded_count += 1
            
            print(f"✅ Downloaded {downloaded_count} files to {download_folder}")
            
        except Exception as e:
            print(f"❌ Error downloading submissions: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize manager
    manager = CanvasManager()
    
    # Display course info
    manager.get_course_info()
    
    # Example: Create sample quiz
    quiz_questions = [
        {
            'question': 'What is the capital of France?',
            'answers': [
                {'answer_text': 'London', 'answer_weight': 0},
                {'answer_text': 'Paris', 'answer_weight': 100},
                {'answer_text': 'Berlin', 'answer_weight': 0},
                {'answer_text': 'Madrid', 'answer_weight': 0}
            ],
            'points': 2
        },
        {
            'question': 'Which programming language is this course about?',
            'answers': [
                {'answer_text': 'Java', 'answer_weight': 0},
                {'answer_text': 'Python', 'answer_weight': 100},
                {'answer_text': 'C++', 'answer_weight': 0},
                {'answer_text': 'JavaScript', 'answer_weight': 0}
            ],
            'points': 2
        }
    ]
    
    # Uncomment to run operations:
    # manager.create_quiz("Sample Quiz", quiz_questions)
    # manager.create_weekly_assignments(weeks=4)  # Create 4 assignments for testing
