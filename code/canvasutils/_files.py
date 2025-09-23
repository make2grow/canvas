import json
import re

def to_safe_filename(text, max_length=100):
    """Convert any string to a safe filename"""
    # Remove problematic characters
    safe = re.sub(r'[<>:"/\\|?*]', '', text)
    safe = re.sub(r'[^\w\s\-_.()\[\]]', '_', safe)
    
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe.strip())
    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_.')
    
    # Handle length and empty strings
    if not safe:
        safe = "unnamed_file"
    if len(safe) > max_length:
        safe = safe[:max_length].rsplit('_', 1)[0]
    
    return safe

# Usage with your Canvas course
course_name = "Cross-Platform Development (2025 Fall full term) ASE-456-001-2026-010"
filename = to_safe_filename(course_name) + ".json"
# Result: "Cross_Platform_Development_2025_Fall_full_term_ASE_456_001_2026_010.json"

def make_serializable(obj):
    """
    Convert an object to a JSON-serializable dictionary by filtering out
    non-serializable attributes like Requester objects.
    """
    result = {}
    for key, value in obj.__dict__.items():
        try:
            # Try to serialize the value
            json.dumps(value)
            result[key] = value
        except TypeError:
            # Skip non-serializable objects
            result[key] = f"<Non-serializable: {type(value).__name__}>"
    return result