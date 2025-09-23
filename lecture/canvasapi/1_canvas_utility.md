---
marp: true
html: true
size: 4:3
paginate: true
style: |
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
    img[alt~="outline"] {
    border: 2px solid #388bee;
  }
---

<!-- _class: lead -->
<!-- _class: frontpage -->
<!-- _paginate: skip -->

# CanvasUtils

---

## Usage of canvasutils package

```txt
.
├── __init__.py
├── canvasutils.py
├── folder
│   └── folder_util.py
└── jsonutil
    ├── json_processor.py
    └── json_util.py
```

---

- The `__init__.py` file makes the directory a Python **package** and re-exports modules, giving a clean interface so users can import without navigating subfolders.
- `jsonutil` is a subdirectory within the package.  
- Its modules are re-exported, so functions can be accessed directly without including the subdirectory name.  

```python
from .jsonutil import json_processor, json_util
from .folder import folder_util
```

---

- Add the `canvasutils` package path to Python’s `sys.path` (if not included).
- Then you can import its exported names directly, without worrying about the internal structure.  

```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from canvasutils import folder_util as folder_utils 
```

Then the functions in the package is accessed using the name.

```python
folder_utils.upload_file_to_folder(...)
canvasutils.folder.upload_file_to_folder(...) # without re-export
```

---

Use `from .. import` to access the file in a parent directory.

```python
from .. import getinfo

def get_course_folder(course, folder_name):
    env = getinfo.get_environment()
```

---

## getinfo.py

get_enviroment() returns API_KEY and API_URL variables from `.env`.  

```python
def get_environment():
  """Check if .env file exists and has required variables"""
  if not os.path.exists('.env'):
      return {}
  
  load_dotenv()
  
  required_vars = ['API_KEY', 'API_URL']
  missing_vars = []
  
  for var in required_vars:
      value = os.getenv(var)
      if not value:
          missing_vars.append(var)
  
  if missing_vars:
      return {}

  return {'API_KEY': os.getenv('API_KEY'), 'API_URL': os.getenv('API_URL')}
```

---

From the get_environment() function, we can get API_KEY and API_URL individually.

```python
def get_api_key():
    """Retrieve the API key from environment variables"""
    env = get_environment()
    if not env:
        return None
    return env["API_KEY"]

def get_api_url():
    """Retrieve the API URL from environment variables"""
    env = get_environment()
    if not env:
        return None
    return env["API_URL"]
```

---

Using get_environment(), we can instantiate the Canvas object.

```python
def get_canvas():
    """Initialize and return a Canvas instance if environment is valid"""
    env = get_environment()
    if not env:
        return None
    return Canvas(env["API_URL"], env["API_KEY"])
```

---

## printinfo.py

print_python_object() function prints out Python object.

```python
def print_python_object(obj):
    """Print a Python object in a readable format"""
    print(type(obj))
    if isinstance(obj, dict):
        for key, value in obj.items():
            print(f"{key}: {value}")
    elif isinstance(obj, list):
        for item in obj:
            print_python_object(item)  # Recursively print each item
    else:
        # For a class object, try to print its __dict__ (attributes)
        if hasattr(obj, '__dict__'):
            for key, value in vars(obj).items():
                print(f"{key}: {value}")
        else:
            print(obj)
```

---

## folder_util.py

get_course_folder() function returns `folder object` from a folder_name string.

```python
def get_course_folder(course, folder_name):
    """Find and return a folder by name from a list of folders"""
    folders = course.get_folders()
    for folder in folders:
        if folder.name.lower() == folder_name.lower():
            return folder
    print(f"❌ Folder '{folder_name}' not found.")
    return None
```

---

