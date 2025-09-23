import json

def store_json_string(json_string, file_name='output.json'):
    """Store a JSON string to a file with pretty formatting"""
    # Ensure the input is a valid JSON string
    try:
        data = json.loads(json_string)  # Parse JSON string to Python object
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON string: {e}")
        return None

    return store_json_object(data, file_name)


def store_json_object(json_object, file_name='output.json'):
    """Store a JSON object to a file with pretty formatting"""
    try:
        # Write to a file with pretty formatting
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_object, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully saved to {file_name}")
    except Exception as e:
        print(f"❌ Error writing to {file_name}: {e}")

    return file_name

def load_json_file(file_name='output.json'):
    """Load a JSON object from a file"""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")
        return None

def count_elements_in_json(file_name='output.json'):
    """Count elements in a JSON file"""
    data = load_json_file(file_name)
    if data:
        return len(data)
    return 0