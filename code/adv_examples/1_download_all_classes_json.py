import os

from canvas.canvas_manager import CanvasManager
import canvas.utils.json_util as json_util

def generate_json_file(file_name):
    canvas_manager = CanvasManager()
    res = canvas_manager.get_all_courses_json()
    print(len(res))
    print(json_util.store_json_object(res, file_name))

def main():
    file_name = 'courses.json'
    if not os.path.exists(file_name):
        print(f"{file_name} not found. Generating...")
        generate_json_file(file_name)
    else:
        print(f"{file_name} already exists.")

    count = json_util.count_elements_in_json(file_name)
    print(f"Number of courses found: {count}")

if __name__ == "__main__":
    main()

