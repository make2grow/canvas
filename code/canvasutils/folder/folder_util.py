from .. import logger
from .. import getinfo
import os

logname = getinfo.get_logname(__file__)
logger = logger.setup_logger(name=__name__, logfile=logname)

def get_course_folder(course, folder_name):
    """Find and return a folder object by name from a list of folders"""
    folders = course.get_folders()
    for folder in folders:
        if folder.name.lower() == folder_name.lower():
            return folder
    logger.error(f"❌ Folder '{folder_name}' not found.")
    return None

def upload_file_to_folder(course, foldername, filepath):
    """Upload a file to the folder specified by name"""
    folder = get_course_folder(course, foldername)
    if folder:
        logger.info(f"Folder found: {folder.name}")
        logger.info(f"Folder ID: {folder.id}")
        try:
            # Upload the file into the folder
            result = folder.upload(filepath)
            if result[0]:  # Check if upload succeeded
                uploaded_file = result[1]
                if isinstance(uploaded_file, dict):
                    logger.info("uploaded_file is a dictionary")
                    logger.info(f"✅ File uploaded! File ID: {uploaded_file['id']}, Display Name: {uploaded_file['display_name']}")
                else:
                    logger.info("uploaded_file is not a dictionary, likely an object")
                return uploaded_file
            else:
                logger.error(f"❌ File upload failed: {result[0]}")
        except Exception as e:
            logger.exception(f"❌ File upload failed: {e}")
