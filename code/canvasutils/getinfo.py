from dotenv import load_dotenv # type: ignore
from canvasapi import Canvas # type: ignore
import os

from . import logger

def get_logname(pathname, delete=True):
    filename = os.path.basename(pathname)
    module_name = os.path.splitext(filename)[0]
    #folder = os.path.dirname(pathname)
    #logname = os.path.join(folder, f'__{module_name}.log')
    logname = f'__{module_name}.log'

    if delete and os.path.exists(logname):
        print(f"INFO: {logname} deleted")
        os.remove(logname)

    return logname        

logname = get_logname(__file__)
logger = logger.setup_logger(name=__name__, logfile=logname)

def get_environment():
  """Check if .env file exists and has required variables"""
  if not os.path.exists('.env'):
      print("❌ .env file not found!")
      print("   Please copy .env.template to .env and fill in your details")
      return {}
  
  load_dotenv()
  
  required_vars = ['API_KEY', 'API_URL']
  missing_vars = []
  
  for var in required_vars:
      value = os.getenv(var)
      if not value:
          missing_vars.append(var)
  
  if missing_vars:
      print("❌ Missing or placeholder values in .env file:")
      for var in missing_vars:
          print(f"   - {var}")
      return {}

  return {'API_KEY': os.getenv('API_KEY'), 'API_URL': os.getenv('API_URL')}

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

def get_canvas():
    """Initialize and return a Canvas instance if environment is valid"""
    env = get_environment()
    if not env:
        return None
    return Canvas(env["API_URL"], env["API_KEY"])
