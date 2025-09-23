import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from canvasapi import Canvas
import inspect
from canvasutils import getinfo # type: ignore
from canvasutils import logger # type: ignore

logname = getinfo.get_logname(__file__)
logger = logger.setup_logger(name='canvasutils', logfile=logname)

def t1_getsource():
    print("🔄 1. Get Source Code of Canvas Methods")
    logger.log(inspect.getsource(Canvas.get_course))
    canvas = getinfo.get_canvas()
    course = canvas.get_course(81929)
    logger.log(inspect.getsource(course.create_quiz))

def t2_python_object_and_json_string():
    print("🔄 2. Python Object and JSON String")
    import json

    # Example Python dictionary
    data = {
        "name": "Alice",
        "age": 25,
        "is_student": True
    }

    # Convert to JSON string
    json_str = json.dumps(data)

    logger(json_str)

    data = json.loads(json_str)
    logger.log(data)

def t3_using_requests():
    print("🔄 3. Using Requests to Fetch Data")
    import requests

    API_URL = "https://nku.instructure.com/api/v1/folders/1432357/files"
    API_KEY = getinfo.get_api_key()

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()

    files_data = response.json()

    for file in files_data:
        logger.info(f"File ID: {file['id']}")
        logger.info(f"Filename: {file['display_name']}")
        logger.info(f"Size: {file['size']} bytes")
#        logger.info(f"Content Type: {file['content_type']}")
        logger.info(f"URL: {file['url']}")


if __name__ == "__main__":
    #t1_getsource()
    #t2_python_object_and_json_string()
    t3_using_requests()
    