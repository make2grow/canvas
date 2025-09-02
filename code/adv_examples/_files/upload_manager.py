class UploadManager(object):
    """
    Manages file uploads to Canvas.
    """
    def __init__(self, course):
        self.course = course
        self.canvas = self.course.get_canvas_instance()

