class Student(object):
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def get_info(self):
        return {
            "name": self.name,
            "student_id": self.student_id
        }