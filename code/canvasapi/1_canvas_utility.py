import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from canvasutils import getinfo # type: ignore
from canvasutils import folder_util # type: ignore
from canvasutils import printinfo # type:ignore
from canvasutils import logger # type: ignore

logname = getinfo.get_logname(__file__)
logger = logger.setup_logger(name='canvasutils', logfile=logname)

def t1_get_canvas_and_print():
    canvas = getinfo.get_canvas()
    printinfo.print_python_object(canvas)

def t2_file_ids_in_a_folder():
    print("🔄 1. File IDs in a Folder")
    filename = "Uploaded Media"
    canvas = getinfo.get_canvas()
    if canvas:
        course = canvas.get_course(81929)
        if course:
            folder = folder_util.get_course_folder(course, filename)
            if folder:
                logger.info(f"Folder found: {folder.name}")
                logger.info(f"Folder ID: {folder.id}")
                # utils.print_python_object(folder)
            else:
                logger.error("❌ Folder not found.")

            files = folder.get_files()
            for file in files:
                logger.info(f"File Name: {file.display_name}, File ID: {file.id}")
        else: 
            logger.error("❌ Course not found.")

def t3_upload_file_to_folder():
    print("🔄 2. Upload File to Folder")
    foldername = "Uploaded Media"
    canvas = getinfo.get_canvas()
    if canvas:
        course = canvas.get_course(81929)
        local_file_path = "img/img1.png"  # Update this to the file you want to upload
        file_dict = folder_util.upload_file_to_folder(course, foldername, local_file_path)
        if file_dict:
            logger.info(f"File uploaded successfully:")
            logger.info(f" - File Name: {file_dict['display_name']}")
            logger.info(f" - File ID: {file_dict['id']}")

def main():
    t1_get_canvas_and_print()
    t2_file_ids_in_a_folder()
    t3_upload_file_to_folder()

if __name__ == "__main__":
    main()