import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from canvasutils import getinfo as utils # type: ignore

def setup():
  canvas = utils.get_canvas()
  if not canvas:
      print("❌ Failed to initialize Canvas instance.")
      return None
  else:
      print("✅ Canvas instance initialized successfully.")
  return canvas

def t1_exceptions():
    """Handle exceptions during Canvas operations"""
    print("🔄 1. Exception Catch")
    try:
        canvas = setup()
        if not canvas:
            return
        
        c = canvas.get_course(32323231)
        user = c.get_user(1)
        print(f"User ID: {user.id}, Name: {user.name}")
    except Exception as e:
        print(f"❌ An error occurred: {e}") 

def t2_debugging():
    print("🔄 2. Debugging with Logging")
    import logging
    import sys
    
    logger = logging.getLogger("canvasapi")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    try:
        canvas = setup()
        if not canvas:
            return
        
        c = canvas.get_course(81929)
        user = c.get_users()[0]
        logger.debug(f"User ID: {user.id}, Name: {user.name}")
        print(f"User ID: {user.id}, Name: {user.name}")
    except Exception as e:
        print(f"❌ An error occurred: {e}") 
    
def t3_simple_debugging_configuration():
    print("🔄 3. Simple Debugging Configuration")
    import logging
    import sys
    
    logging.basicConfig(
      level=logging.DEBUG,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[logging.FileHandler('logfile.log'), logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger(__name__)

    try:
        canvas = setup()
        if not canvas:
            return
        
        c = canvas.get_course(81929)
        user = c.get_users()[0]
        print(f"User ID: {user.id}, Name: {user.name}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def t4_configure_debugging():
    print("🔄 4. Configure Debugging")
    import logging
    import sys
    
    logging.basicConfig(
        handlers=[logging.FileHandler('logfile.log'), 
                  logging.StreamHandler(sys.stdout)],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    
    # Show DEBUG for your code
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Suppress verbose messages from canvasapi.requester
    logging.getLogger('canvasapi.requester').setLevel(logging.WARNING)

    try:
        canvas = setup()
        if not canvas:
            return
        
        c = canvas.get_course(81929)
        user = c.get_users()[0]
        logger.debug(f"User ID: {user.id}, Name: {user.name}")
        print(f"User ID: {user.id}, Name: {user.name}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def t5_filtering_logging_information():
    print("🔄 5. Filtering Logging Information")
    import logging
    import sys

    class MyFilter(logging.Filter):
        def filter(self, record):
            # Show only messages containing 'User ID'
            return 'User ID' in record.getMessage()

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create stream handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    # Create formatter and set it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)    

    # File handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG) # or set to INFO, WARNING, etc. as needed
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Add the filter to the handler
    handler.addFilter(MyFilter())
    file_handler.addFilter(MyFilter())
    
    # Add handler to logger
    logger.addHandler(handler)
    logger.addHandler(file_handler)

    try:
        canvas = setup()
        if not canvas:
            return
        
        c = canvas.get_course(81929)
        user = c.get_users()[0]
        logger.debug(f"User ID: {user.id}, Name: {user.name}")
            # Example usage
        logger.debug("This is a debug message without User ID")  # Will be filtered out

        print(f"User ID: {user.id}, Name: {user.name}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    #t1_exceptions()
    #t2_debugging()
    #t3_simple_debugging_configuration()
    #t4_configure_debugging()
    t5_filtering_logging_information()
